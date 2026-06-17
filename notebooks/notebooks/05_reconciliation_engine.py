# Databricks notebook source
# DBTITLE 1,Import PySpark Functions
from pyspark.sql.functions import *
from pyspark.sql.types import *

# COMMAND ----------

# DBTITLE 1,Load Tables
bronze_df = spark.table("bronze.fraud_transactions_bronze")
silver_df = spark.table("silver.fraud_transactions_silver")

# COMMAND ----------

# DBTITLE 1,Row Count Validation
bronze_count = bronze_df.count()
silver_count = silver_df.count()

row_count_result = "PASS" if bronze_count == silver_count else "FAIL"

print("Bronze Count:", bronze_count)
print("Silver Count:", silver_count)
print("Row Count Validation:", row_count_result)

# COMMAND ----------

# DBTITLE 1,Schema Validation
bronze_columns = set(bronze_df.columns)
silver_columns = set(silver_df.columns)

missing_in_silver = bronze_columns - silver_columns

schema_result = "PASS" if len(missing_in_silver) == 0 else "FAIL"

print("Missing Columns:", missing_in_silver)
print("Schema Validation:", schema_result)

# COMMAND ----------

# DBTITLE 1,Aggregate Validation
bronze_amount = bronze_df.agg(round(sum("amt"),2)).collect()[0][0]
silver_amount = silver_df.agg(round(sum("amt"),2)).collect()[0][0]

aggregate_result = "PASS" if bronze_amount == silver_amount else "FAIL"

print("Bronze Amount:", bronze_amount)
print("Silver Amount:", silver_amount)
print("Aggregate Validation:", aggregate_result)

# COMMAND ----------

# DBTITLE 1,Hash Validation
bronze_hash = bronze_df.select(
    sha2(concat_ws("||", *bronze_df.columns), 256).alias("hash")
)

silver_hash = silver_df.select(
    sha2(concat_ws("||", *silver_df.columns), 256).alias("hash")
)

# COMMAND ----------

# DBTITLE 1,Hash Count Check
bronze_hash_count = bronze_hash.count()
silver_hash_count = silver_hash.count()

hash_result = "PASS" if bronze_hash_count == silver_hash_count else "FAIL"

print("Hash Validation:", hash_result)

# COMMAND ----------

# DBTITLE 1,Null Validation
null_validation = silver_df.select([
    count(when(col(c).isNull(), c)).alias(c)
    for c in silver_df.columns
])

display(null_validation)

# COMMAND ----------

# DBTITLE 1,Duplicate Validation
duplicate_count = silver_df.groupBy("trans_num") \
    .count() \
    .filter(col("count") > 1) \
    .count()

duplicate_result = "PASS" if duplicate_count == 0 else "FAIL"

print("Duplicate Count:", duplicate_count)
print("Duplicate Validation:", duplicate_result)

# COMMAND ----------

# DBTITLE 1,Business Rule Validation
invalid_amounts = silver_df.filter(col("amt") <= 0).count()

business_rule_result = "PASS" if invalid_amounts == 0 else "FAIL"

print("Invalid Amount Records:", invalid_amounts)
print("Business Rule Validation:", business_rule_result)

# COMMAND ----------

# DBTITLE 1,Create Recon Results DataFrame
recon_results = [
    ("Row Count Validation", row_count_result),
    ("Schema Validation", schema_result),
    ("Aggregate Validation", aggregate_result),
    ("Hash Validation", hash_result),
    ("Duplicate Validation", duplicate_result),
    ("Business Rule Validation", business_rule_result)
]

recon_df = spark.createDataFrame(
    recon_results,
    ["validation_type", "status"]
)

display(recon_df)

# COMMAND ----------

# DBTITLE 1,Add Audit Columns
recon_df = recon_df \
    .withColumn("validation_timestamp", current_timestamp()) \
    .withColumn("pipeline_name", lit("fraud_reconciliation_pipeline")) \
    .withColumn("batch_id", lit("BATCH_001"))

# COMMAND ----------

# DBTITLE 1,Write Recon Table
recon_df.write.format("delta") \
    .mode("overwrite") \
    .saveAsTable("recon.reconciliation_results")

# COMMAND ----------

# DBTITLE 1,Verify Results
# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM recon.reconciliation_results;

# COMMAND ----------

# DBTITLE 1,Validation Summary
# MAGIC %sql
# MAGIC SELECT 
# MAGIC     status,
# MAGIC     COUNT(*) AS total_validations
# MAGIC FROM recon.reconciliation_results
# MAGIC GROUP BY status;

# COMMAND ----------

# DBTITLE 1,Describe Detail
# MAGIC %sql
# MAGIC DESCRIBE DETAIL recon.reconciliation_results;