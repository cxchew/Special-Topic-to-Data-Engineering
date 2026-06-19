import os
from pyspark.sql import SparkSession
import pyspark.sql.functions as F

# 1. Environment & Path Initialization
os.environ['HADOOP_HOME'] = "C:\\hadoop"
os.environ['PATH'] = os.environ['PATH'] + ";C:\\hadoop\\bin"

# 2. Initialize Spark Session with Network Timeout and Memory Fixes
jar_path = "file:///C:/spark/jars/postgresql-42.7.11.jar" 
spark = SparkSession.builder \
    .appName("Censo_Escolar_ETL_Pipeline") \
    .config("spark.jars", jar_path) \
    .config("spark.driver.memory", "6g") \
    .config("spark.executor.memory", "4g") \
    .config("spark.sql.shuffle.partitions", "10") \
    .config("spark.python.worker.reuse", "true") \
    .config("spark.api.python.auth.socket.timeout", "600") \
    .getOrCreate()

db_url = "jdbc:postgresql://localhost:5432/censo_escolar"
db_properties = {
    "user": "censo",
    "password": "123",
    "driver": "org.postgresql.Driver"
}

years = range(2010, 2022)

# Helper function to check if a table already exists and has data in PostgreSQL
def table_has_data(table_name):
    try:
        check_df = spark.read.format("jdbc") \
            .option("url", db_url) \
            .option("dbtable", f"(SELECT 1 FROM {table_name} LIMIT 1) as tmp") \
            .options(**db_properties).load()
        return check_df.count() > 0
    except Exception:
        return False  # Table doesn't exist or error occurs, so we should write it

# Helper function to check if a specific year already exists in the Fact Table
def year_already_processed(year):
    try:
        check_df = spark.read.format("jdbc") \
            .option("url", db_url) \
            .option("dbtable", f"(SELECT 1 FROM FACT_CENSO_ESCOLAR WHERE NU_ANO_CENSO = {year} LIMIT 1) as tmp") \
            .options(**db_properties).load()
        return check_df.count() > 0
    except Exception:
        return False

# --- STEP 1: CONVERT RAW CSV TO OPTIMIZED PARQUET ---
print("--- Step 1: Converting heavy CSV files to Parquet format ---")
for year in years:
    csv_path = f"data/raw/microdados_ed_basica_{year}.csv"
    parquet_path = f"data/parquet/censo_{year}"
    
    if not os.path.exists(parquet_path):
        try:
            print(f"Converting CSV to Parquet for year {year}...")
            df_raw = spark.read.csv(csv_path, sep=';', header=True, inferSchema=True, encoding='ISO-8859-1')
            
            for col in df_raw.columns:
                df_raw = df_raw.withColumnRenamed(col, col.upper())
                
            df_raw.write.mode("overwrite").parquet(parquet_path)
        except Exception as e:
            print(f"Skipping or error converting CSV for {year}: {e}")
    else:
        print(f"Parquet directory for year {year} already exists. Skipping conversion.")

# --- STEP 2: BUILD FIXED DIMENSION LOOKUP TABLES ---
print("--- Step 2: Populating Fixed Dimension Lookup Tables ---")
def save_to_postgres(df, table_name):
    df.write.format("jdbc").option("url", db_url).option("dbtable", table_name) \
      .options(**db_properties).mode("overwrite").save()

# Check if fixed dimensions are already populated to avoid unnecessary writes
if table_has_data("DIM_TP_DEPENDENCIA") and table_has_data("DIM_TP_LOCALIZACAO"):
    print("Fixed Dimension Lookup Tables already exist and contain data. Skipping Step 2.")
else:
    print("Writing Fixed Dimension Lookup Tables...")
    dep_data = [(1, "Federal"), (2, "Estadual"), (3, "Municipal"), (4, "Privada")]
    save_to_postgres(spark.createDataFrame(dep_data, ["id", "TP_RELAÇÃO"]).withColumn("id", F.col("id").cast("integer")), "DIM_TP_LIQUID")
    save_to_postgres(spark.createDataFrame(dep_data, ["id", "TP_RELAÇÃO"]).withColumn("id", F.col("id").cast("integer")), "DIM_TP_LIQUID_BACKUP")
    save_to_postgres(spark.createDataFrame(dep_data, ["id", "TP_RELAÇÃO"]).withColumn("id", F.col("id").cast("integer")), "DIM_TP_DEPENDENCIA")

    loc_data = [(1, "Urbana"), (2, "Rural")]
    save_to_postgres(spark.createDataFrame(loc_data, ["id", "TP_LOCALIZACAO"]).withColumn("id", F.col("id").cast("integer")), "DIM_TP_LOCALIZACAO")

    binary_dims = [
        "DIM_IN_AGUA_POTAVEL", "DIM_IN_ENERGIA_INEXISTENTE", "DIM_IN_ESGOTO_INEXISTENTE",
        "DIM_IN_BANHEIRO", "DIM_IN_BIBLIOTECA", "DIM_IN_REFEITORIO", 
        "DIM_IN_COMPUTADOR", "DIM_IN_INTERNET", "DIM_IN_EQUIP_NENHUM"
    ]
    binary_df = spark.createDataFrame([(0, "Não/Inexistente"), (1, "Sim/Existente")], ["id", "descricao"]).withColumn("id", F.col("id").cast("integer"))
    for dim in binary_dims:
        save_to_postgres(binary_df, dim)

# --- STEP 3: CONSOLIDATING THE STAR SCHEMA WITH FORCE RESET ---
print("--- Step 3: Compiling Historical Star Schema Logs ---")

# ONLY purge and rebuild table layout if the central fact table is missing entirely
if not table_has_data("FACT_CENSO_ESCOLAR"):
    try:
        empty_schema = spark.createDataFrame([], "id LONG, NO_UF STRING, SG_UF STRING, CO_UF STRING, NO_MUNICIPIO STRING, CO_MUNICIPIO STRING")
        empty_schema.write.format("jdbc").option("url", db_url).option("dbtable", "DIM_LOCAL").options(**db_properties).mode("overwrite").save()
        print("Successfully purged and rebuilt clean table boundaries for DIM_LOCAL.")
    except Exception as e:
        print(f"Initial structural purge notice: {e}")
else:
    print("Existing FACT_CENSO_ESCOLAR detected. Enabling historical append/skip mode.")

for year in years:
    try:
        # Check if this specific year's data is already inside the database
        if year_already_processed(year):
            print(f"Year {year} has already been compiled into the database. Skipping pipeline transformations.")
            continue  # Skips the rest of this loop iteration and moves to the next year
            
        print(f"Processing Star Schema transformations from Parquet for year: {year}")
        df = spark.read.parquet(f"data/parquet/censo_{year}")
        
        # A. Process Geographic Dimension (DIM_LOCAL)
        geo_cols = ["CO_UF", "SG_UF", "NO_UF", "CO_MUNICIPIO", "NO_MUNICIPIO"]
        available_geo = [c for c in geo_cols if c in df.columns]
        df_geo = df.select(*available_geo).distinct()
        
        if "NO_UF" not in df_geo.columns:
            df_geo = df_geo.withColumn("NO_UF", F.col("SG_UF"))
            
        # Assign explicit 64-bit integer values to avoid overflow errors
        df_geo = df_geo.withColumn("id", F.monotonically_increasing_id().cast("long"))
        
        # Clean data types to match database parameters
        df_geo = df_geo.select(
            F.col("id"),
            F.col("NO_UF").cast("string"),
            F.col("SG_UF").cast("string"),
            F.col("CO_UF").cast("string"),
            F.col("NO_MUNICIPIO").cast("string"),
            F.col("CO_MUNICIPIO").cast("string")
        )
        
        # Append geographical records safely to the database structure
        df_geo.write.format("jdbc").option("url", db_url).option("dbtable", "DIM_LOCAL") \
            .options(**db_properties).mode("append").save()

        # B. Align and construct Central Fact Table Records
        df_with_keys = df.join(df_geo, on=["CO_MUNICIPIO"], how="inner")
        
        fact_schema = {
            "NU_ANO_CENSO": F.lit(year).cast("integer"),
            "ID_DIM_LOCAL": F.col("id").cast("long"), 
            "ID_DIM_TP_LIQUID": F.coalesce(F.col("TP_DEPENDENCIA"), F.lit(1)).cast("integer"),
            "ID_DIM_TP_DEPENDENCIA": F.coalesce(F.col("TP_DEPENDENCIA"), F.lit(1)).cast("integer"),
            "ID_DIM_TP_LOCALIZACAO": F.coalesce(F.col("TP_LOCALIZACAO"), F.lit(1)).cast("integer"),
            "ID_DIM_IN_AGUA_POTAVEL": F.coalesce(F.col("IN_AGUA_POTAVEL"), F.lit(0)).cast("integer"),
            "ID_DIM_IN_ENERGIA_INEXISTENTE": F.coalesce(F.col("IN_ENERGIA_INEXISTENTE"), F.lit(0)).cast("integer"),
            "ID_DIM_IN_ESGOTO_INEXISTENTE": F.coalesce(F.col("IN_ESGOTO_INEXISTENTE"), F.lit(0)).cast("integer"),
            "ID_DIM_IN_BANHEIRO": F.coalesce(F.col("IN_BANHEIRO"), F.lit(0)).cast("integer"),
            "ID_DIM_IN_BIBLIOTECA": F.coalesce(F.col("IN_BIBLIOTECA"), F.lit(0)).cast("integer"),
            "ID_DIM_IN_REFEITORIO": F.coalesce(F.col("IN_REFEITORIO"), F.lit(0)).cast("integer"),
            "ID_DIM_IN_COMPUTADOR": F.coalesce(F.col("IN_COMPUTADOR"), F.lit(0)).cast("integer"),
            "ID_DIM_IN_INTERNET": F.coalesce(F.col("IN_INTERNET"), F.lit(0)).cast("integer"),
            "ID_DIM_IN_EQUIP_NENHUM": F.coalesce(F.col("IN_EQUIP_NENHUM"), F.lit(0)).cast("integer")
        }

        measures = [
            "QT_DOC_BAS", "QT_DOC_INF", "QT_DOC_FUND", "QT_DOC_MED",
            "QT_MAT_BAS", "QT_MAT_INF", "QT_MAT_FUND", "QT_MAT_MED",
            "QT_MAT_BAS_ND", "QT_MAT_BAS_BRANCA", "QT_MAT_BAS_PRETA", 
            "QT_MAT_BAS_PARDA", "QT_MAT_BAS_AMARELA", "QT_MAT_BAS_INDIGENA"
        ]

        for metric in measures:
            if metric in df_with_keys.columns:
                fact_schema[metric] = F.col(metric).cast("integer")
            else:
                fact_schema[metric] = F.lit(0).cast("integer")

        df_fact = df_with_keys.select([col_expr.alias(col_name) for col_name, col_expr in fact_schema.items()])

        # If the table is brand new, overwrite, else append data safely
        fact_mode = "overwrite" if (year == 2010 and not table_has_data("FACT_CENSO_ESCOLAR")) else "append"
        df_fact.write.format("jdbc").option("url", db_url).option("dbtable", "FACT_CENSO_ESCOLAR") \
            .options(**db_properties).mode(fact_mode).save()
            
        print(f"Year {year} successfully compiled into Star Schema!")
        
    except Exception as e:
        print(f"Error handling historical compilation for year {year}: {e}")

spark.stop()
print("--- ETL Pipeline complete! Database structure successfully generated! ---")