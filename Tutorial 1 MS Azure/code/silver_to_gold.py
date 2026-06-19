# Databricks Notebook: Silver to Gold Transformation
# Description: Applies business logic, renames columns, and formats tables for reporting.

from pyspark.sql.functions import col

silver_path = "abfss://silver@yourstorageaccount.dfs.core.windows.net/"
gold_path = "abfss://gold@yourstorageaccount.dfs.core.windows.net/"

print("Refining analytical datasets for the Gold Layer...")

# Example 1: Creating DimCustomer (Customer details cleaned up)
df_customer = spark.read.format("delta").load(f"{silver_path}Customer")
dim_customer = df_customer.select(
    col("CustomerID").alias("customer_id"),
    col("CompanyName").alias("company_name"),
    col("FirstName").alias("first_name"),
    col("LastName").alias("last_name"),
    col("EmailAddress").alias("email_address")
)
dim_customer.write.format("delta").mode("overwrite").save(f"{gold_path}dim_customer")

# Example 2: Fact Sales Table (Joining Header with Details to find Product Counts)
df_header = spark.read.format("delta").load(f"{silver_path}SalesOrderHeader")
df_detail = spark.read.format("delta").load(f"{silver_path}SalesOrderDetail")

fact_sales = df_header.join(df_detail, "SalesOrderID", "inner").select(
    col("SalesOrderID").alias("sales_order_id"),
    col("CustomerID").alias("customer_id"),
    col("ProductID").alias("product_id"),
    col("OrderQty").alias("order_quantity"),
    col("UnitPrice").alias("unit_price"),
    col("LineTotal").alias("line_total"),
    col("OrderDate").alias("order_date")
)
fact_sales.write.format("delta").mode("overwrite").save(f"{gold_path}fact_sales")

print("Gold tier tables generated successfully.")
