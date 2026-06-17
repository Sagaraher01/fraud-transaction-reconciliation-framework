# Databricks notebook source
# DBTITLE 1,Import PySpark Functions
# Import PySpark functions for data processing
from pyspark.sql.functions import *
from pyspark.sql.types import *

print("✅ Imports successful")

# COMMAND ----------

# DBTITLE 1,Define Source Path
# Define the source path for raw CSV data in Unity Catalog Volume
source_path = "/Volumes/workspace/vrahad_recon/raw_data/fraudTrain.csv"

print(f"✅ Source path defined: {source_path}")

# COMMAND ----------

# DBTITLE 1,Read CSV with Schema Inference
# Read CSV file with header and automatic schema inference
bronze_df = spark.read.format("csv") \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .load(source_path)

print(f"✅ Data loaded successfully")
print(f"Total rows: {bronze_df.count():,}")
print(f"Total columns: {len(bronze_df.columns)}")

# COMMAND ----------

# DBTITLE 1,Verify Data - Preview
# Display first 10 rows to verify data
print("Preview of raw data:")
display(bronze_df.limit(10))

# COMMAND ----------

# DBTITLE 1,Verify Data - Schema
# Print schema to verify column types
print("Data schema:")
bronze_df.printSchema()

# COMMAND ----------

# DBTITLE 1,Add Enterprise Metadata Columns
# Add metadata columns for audit tracking and lineage
# These columns make the pipeline enterprise-grade
# Using Unity Catalog compatible _metadata.file_path instead of input_file_name()
bronze_df = bronze_df \
    .withColumn("ingestion_timestamp", current_timestamp()) \
    .withColumn("source_file", col("_metadata.file_path")) \
    .withColumn("load_date", current_date()) \
    .withColumn("batch_id", lit("BATCH_001"))

print("✅ Metadata columns added:")
print("  - ingestion_timestamp: audit tracking")
print("  - source_file: lineage/debugging (Unity Catalog compatible)")
print("  - load_date: partitioning")
print("  - batch_id: pipeline execution tracking")

# COMMAND ----------

# DBTITLE 1,Verify Metadata Columns
# Verify new metadata columns were added
print("Preview with metadata columns:")
display(bronze_df.limit(5))

print(f"\nTotal columns now: {len(bronze_df.columns)}")
print(f"New columns: ingestion_timestamp, source_file, load_date, batch_id")

# COMMAND ----------

# DBTITLE 1,Write to Bronze Delta Table
# Write data to Delta Lake table in Bronze database
# Using Delta format for ACID compliance and performance
print("Writing to Bronze table...")

bronze_df.write.format("delta") \
    .mode("overwrite") \
    .saveAsTable("bronze.fraud_transactions_bronze")

print("✅ Bronze table created: bronze.fraud_transactions_bronze")
print("  - Format: Delta Lake")
print("  - Mode: Overwrite")
print("  - Type: Managed table")

# COMMAND ----------

# DBTITLE 1,Verify Table - Row Count
# MAGIC %sql
# MAGIC -- Verify the Bronze table was created and count total rows
# MAGIC SELECT COUNT(*) as total_rows
# MAGIC FROM bronze.fraud_transactions_bronze;

# COMMAND ----------

# DBTITLE 1,Preview Bronze Table
# MAGIC %sql
# MAGIC -- Preview Bronze table data with all columns including metadata
# MAGIC SELECT *
# MAGIC FROM bronze.fraud_transactions_bronze
# MAGIC LIMIT 10;

# COMMAND ----------

# DBTITLE 1,Check Table Format and Details
# MAGIC %sql
# MAGIC -- Verify table is in Delta format and check metadata
# MAGIC DESCRIBE DETAIL bronze.fraud_transactions_bronze;