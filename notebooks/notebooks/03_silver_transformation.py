# Databricks notebook source
# DBTITLE 1,Import PySpark Functions
from pyspark.sql.functions import *
from pyspark.sql.types import *

# COMMAND ----------

# DBTITLE 1,Read Bronze Table
bronze_df = spark.table("bronze.fraud_transactions_bronze")

display(bronze_df.limit(5))

# COMMAND ----------

# DBTITLE 1,Check Initial Counts
print("Bronze Row Count:", bronze_df.count())

# COMMAND ----------

# DBTITLE 1,Remove Duplicates
silver_df = bronze_df.dropDuplicates(["trans_num"])

# COMMAND ----------

# DBTITLE 1,Standardize Column Values
silver_df = silver_df \
    .withColumn("merchant", upper(col("merchant"))) \
    .withColumn("category", upper(col("category"))) \
    .withColumn("city", initcap(col("city"))) \
    .withColumn("state", upper(col("state"))) \
    .withColumn("gender", upper(col("gender")))

# COMMAND ----------

# DBTITLE 1,Fix Date Column
silver_df = silver_df.withColumn(
    "transaction_timestamp",
    to_timestamp(col("trans_date_trans_time"))
)

# COMMAND ----------

# DBTITLE 1,Add Business Columns
silver_df = silver_df \
    .withColumn(
        "transaction_year",
        year(col("transaction_timestamp"))
    ) \
    .withColumn(
        "transaction_month",
        month(col("transaction_timestamp"))
    ) \
    .withColumn(
        "transaction_day",
        dayofmonth(col("transaction_timestamp"))
    )

# COMMAND ----------

# DBTITLE 1,Add Age Column
silver_df = silver_df.withColumn(
    "customer_age",
    floor(datediff(current_date(), col("dob")) / 365)
)

# COMMAND ----------

# DBTITLE 1,Business Validations
silver_df = silver_df.filter(
    (col("amt") > 0) &
    (col("customer_age") > 18)
)

# COMMAND ----------

# DBTITLE 1,Null Check Summary
null_summary = silver_df.select([
    count(when(col(c).isNull(), c)).alias(c)
    for c in silver_df.columns
])

display(null_summary)

# COMMAND ----------

# DBTITLE 1,Add Data Quality Flag
silver_df = silver_df.withColumn(
    "dq_status",
    when(col("amt").isNull(), "FAILED")
    .when(col("merchant").isNull(), "FAILED")
    .otherwise("PASSED")
)

# COMMAND ----------

# DBTITLE 1,Verify Data
display(silver_df.limit(10))

# COMMAND ----------

# DBTITLE 1,Check Final Count
print("Silver Row Count:", silver_df.count())

# COMMAND ----------

# DBTITLE 1,Write Silver Delta Table
silver_df.write.format("delta") \
    .mode("overwrite") \
    .saveAsTable("silver.fraud_transactions_silver")

# COMMAND ----------

# DBTITLE 1,Verify Silver Table
# MAGIC %sql
# MAGIC SELECT COUNT(*) 
# MAGIC FROM silver.fraud_transactions_silver;

# COMMAND ----------

# DBTITLE 1,Verify DQ Status
# MAGIC %sql
# MAGIC SELECT dq_status, COUNT(*) AS total_records
# MAGIC FROM silver.fraud_transactions_silver
# MAGIC GROUP BY dq_status;

# COMMAND ----------

# DBTITLE 1,Check Delta Details
# MAGIC %sql
# MAGIC DESCRIBE DETAIL silver.fraud_transactions_silver;