# Databricks notebook source
# DBTITLE 1,Import PySpark Functions
from pyspark.sql.functions import *

# COMMAND ----------

# DBTITLE 1,Read Silver Table
silver_df = spark.table("silver.fraud_transactions_silver")

display(silver_df.limit(5))

# COMMAND ----------

# DBTITLE 1,Create Transaction Summary
gold_transaction_summary = silver_df.groupBy(
    "transaction_year",
    "transaction_month"
).agg(
    count("*").alias("total_transactions"),
    round(sum("amt"), 2).alias("total_amount"),
    round(avg("amt"), 2).alias("avg_transaction_amount"),
    sum("is_fraud").alias("fraud_transactions")
)

# COMMAND ----------

# DBTITLE 1,Display Transaction Summary
display(gold_transaction_summary)

# COMMAND ----------

# DBTITLE 1,Write Transaction Summary Table
gold_transaction_summary.write.format("delta") \
    .mode("overwrite") \
    .saveAsTable("gold.gold_transaction_summary")

# COMMAND ----------

# DBTITLE 1,Create Customer Summary
gold_customer_summary = silver_df.groupBy(
    "cc_num",
    "first",
    "last",
    "gender",
    "state"
).agg(
    count("*").alias("total_transactions"),
    round(sum("amt"), 2).alias("total_spent"),
    round(avg("amt"), 2).alias("avg_spent"),
    sum("is_fraud").alias("fraud_transaction_count")
)

# COMMAND ----------

# DBTITLE 1,Display Customer Summary
display(gold_customer_summary.limit(10))

# COMMAND ----------

# DBTITLE 1,Write Customer Summary Table
gold_customer_summary.write.format("delta") \
    .mode("overwrite") \
    .saveAsTable("gold.gold_customer_summary")

# COMMAND ----------

# DBTITLE 1,Create Merchant Summary
gold_merchant_summary = silver_df.groupBy(
    "merchant",
    "category"
).agg(
    count("*").alias("total_transactions"),
    round(sum("amt"), 2).alias("total_revenue"),
    round(avg("amt"), 2).alias("avg_transaction"),
    sum("is_fraud").alias("fraud_transactions")
)

# COMMAND ----------

# DBTITLE 1,Display Merchant Summary
display(gold_merchant_summary.limit(10))

# COMMAND ----------

# DBTITLE 1,Write Merchant Summary Table
gold_merchant_summary.write.format("delta") \
    .mode("overwrite") \
    .saveAsTable("gold.gold_merchant_summary")

# COMMAND ----------

# DBTITLE 1,Create Fraud Summary
gold_fraud_summary = silver_df.groupBy(
    "category",
    "state"
).agg(
    count("*").alias("total_transactions"),
    sum("is_fraud").alias("fraud_count"),
    round(
        (sum("is_fraud") / count("*")) * 100,
        2
    ).alias("fraud_percentage"),
    round(sum("amt"), 2).alias("total_transaction_amount")
)

# COMMAND ----------

# DBTITLE 1,Display Fraud Summary
display(gold_fraud_summary.limit(20))

# COMMAND ----------

# DBTITLE 1,Write Fraud Summary Table
gold_fraud_summary.write.format("delta") \
    .mode("overwrite") \
    .saveAsTable("gold.gold_fraud_summary")

# COMMAND ----------

# DBTITLE 1,Show Gold Tables
# MAGIC %sql
# MAGIC SHOW TABLES IN gold;

# COMMAND ----------

# DBTITLE 1,Verify Transaction Summary Count
# MAGIC %sql
# MAGIC SELECT COUNT(*) 
# MAGIC FROM gold.gold_transaction_summary;

# COMMAND ----------

# DBTITLE 1,Verify Customer Summary Count
# MAGIC %sql
# MAGIC SELECT COUNT(*) 
# MAGIC FROM gold.gold_customer_summary;

# COMMAND ----------

# DBTITLE 1,Verify Merchant Summary Count
# MAGIC %sql
# MAGIC SELECT COUNT(*) 
# MAGIC FROM gold.gold_merchant_summary;

# COMMAND ----------

# DBTITLE 1,Verify Fraud Summary Count
# MAGIC %sql
# MAGIC SELECT COUNT(*) 
# MAGIC FROM gold.gold_fraud_summary;

# COMMAND ----------

# DBTITLE 1,Verify Transaction Summary Details
# MAGIC %sql
# MAGIC DESCRIBE DETAIL gold.gold_transaction_summary;