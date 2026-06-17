# Databricks notebook source
# DBTITLE 1,Optimize Bronze Table
# MAGIC %sql
# MAGIC OPTIMIZE bronze.fraud_transactions_bronze;

# COMMAND ----------

# DBTITLE 1,Optimize Silver Table
# MAGIC %sql
# MAGIC OPTIMIZE silver.fraud_transactions_silver;

# COMMAND ----------

# DBTITLE 1,Optimize Gold Table
# MAGIC %sql
# MAGIC OPTIMIZE gold.gold_transaction_summary;

# COMMAND ----------

# DBTITLE 1,Check History
# MAGIC %sql
# MAGIC DESCRIBE HISTORY bronze.fraud_transactions_bronze;

# COMMAND ----------

# DBTITLE 1,Time Travel Query
# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM bronze.fraud_transactions_bronze VERSION AS OF 0
# MAGIC LIMIT 5;

# COMMAND ----------

# DBTITLE 1,Vacuum Bronze Table
# MAGIC %sql
# MAGIC VACUUM bronze.fraud_transactions_bronze RETAIN 168 HOURS;

# COMMAND ----------

# DBTITLE 1,Check File Stats
# MAGIC %sql
# MAGIC DESCRIBE DETAIL bronze.fraud_transactions_bronze;

# COMMAND ----------

# DBTITLE 1,Performance Test Query
# MAGIC %sql
# MAGIC SELECT
# MAGIC     category,
# MAGIC     COUNT(*) AS total_transactions,
# MAGIC     ROUND(SUM(amt),2) AS total_amount
# MAGIC FROM silver.fraud_transactions_silver
# MAGIC GROUP BY category
# MAGIC ORDER BY total_amount DESC;