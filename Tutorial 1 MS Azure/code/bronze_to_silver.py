# Databricks Notebook: Bronze to Silver Transformation
# Description: Cleanses raw Parquet files and saves them as Delta tables.

from pyspark.sql.functions import from_json, col, date_format, to_date
from pyspark.sql.types import *

# Define the container mount paths or direct ADLS Gen2 pathing variables
bronze_path = "abfss://bronze@yourstorageaccount.dfs.core.windows.net/"
silver_path = "abfss://silver@yourstorageaccount.dfs.core.windows.net/"

# List of tables copied over by Azure Data Factory
tables = ["Customer", "Product", "ProductCategory", "SalesOrderDetail", "SalesOrderHeader"]

for table in tables:
    print(f"Processing table: {table} from Bronze to Silver layer...")
    
    # 1. Read raw Parquet data from the Bronze container
    df_raw = spark.read.format("parquet").load(f"{bronze_path}{table}/{table}.parquet")
    
    # 2. Data Cleaning: Process Date columns if they exist
    # Standardizing messy date/timestamps into uniform yyyy-MM-dd formats
    for col_name in df_raw.columns:
        if "Date" in col_name:
            df_raw = df_raw.withColumn(col_name, to_date(col(col_name)))
            
    # 3. Write data to the Silver Container in Delta format
    df_raw.write.format("delta") \
        .mode("overwrite") \
        .option("overwriteSchema", "true") \
        .save(f"{silver_path}{table}")
        
    print(f"Table {table} successfully stored in Silver tier as Delta.")
