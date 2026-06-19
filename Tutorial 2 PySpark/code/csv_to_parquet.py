import os
import sys

# FORCE THE PATHS DIRECTLY IN THE CODE
os.environ['HADOOP_HOME'] = "C:\\hadoop"
os.environ['PATH'] = os.environ['PATH'] + ";C:\\hadoop\\bin"

from pyspark.sql import SparkSession

# Initialize Spark
spark = SparkSession.builder \
    .appName("CensoEscolarETL") \
    .config("spark.driver.extraClassPath", "C:\\hadoop\\bin") \
    .getOrCreate()

# 1. Read the CSV
print("Reading CSV data...")
df = spark.read.csv("data/raw/microdados_ed_basica_2023.csv", sep=';', header=True, inferSchema=True)

# 2. Show the data (We know this part works!)
df.show(5)

# 3. Write to Parquet (This is where the crash happened)
print("Converting to Parquet...")
try:
    # We use a simple path to avoid permission issues
    df.write.mode("overwrite").parquet("data/parquet/census_optimized")
    print("SUCCESS! Check the data/parquet/census_optimized folder.")
except Exception as e:
    print(f"FAILED again. Error: {e}")

spark.stop()
