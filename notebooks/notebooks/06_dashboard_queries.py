# Databricks notebook source
# DBTITLE 1,Total Records
# MAGIC %sql
# MAGIC SELECT
# MAGIC     COUNT(*) AS total_records
# MAGIC FROM silver.fraud_transactions_silver;

# COMMAND ----------

# DBTITLE 1,Total Fraud Records
# MAGIC %sql
# MAGIC SELECT
# MAGIC     SUM(is_fraud) AS total_fraud_transactions
# MAGIC FROM silver.fraud_transactions_silver;

# COMMAND ----------

# DBTITLE 1,Fraud Percentage
# MAGIC %sql
# MAGIC SELECT
# MAGIC     ROUND(
# MAGIC         (SUM(is_fraud) * 100.0) / COUNT(*),
# MAGIC         2
# MAGIC     ) AS fraud_percentage
# MAGIC FROM silver.fraud_transactions_silver;

# COMMAND ----------

# DBTITLE 1,Validation Summary
# MAGIC %sql
# MAGIC SELECT
# MAGIC     status,
# MAGIC     COUNT(*) AS total_validations
# MAGIC FROM recon.reconciliation_results
# MAGIC GROUP BY status;

# COMMAND ----------

# DBTITLE 1,Transaction Trend
# MAGIC %sql
# MAGIC SELECT
# MAGIC     transaction_year,
# MAGIC     transaction_month,
# MAGIC     total_transactions,
# MAGIC     total_amount
# MAGIC FROM gold.gold_transaction_summary
# MAGIC ORDER BY transaction_year, transaction_month;

# COMMAND ----------

# DBTITLE 1,Top Fraud Categories
# MAGIC %sql
# MAGIC SELECT
# MAGIC     category,
# MAGIC     fraud_count,
# MAGIC     fraud_percentage
# MAGIC FROM gold.gold_fraud_summary
# MAGIC ORDER BY fraud_count DESC
# MAGIC LIMIT 10;

# COMMAND ----------

# DBTITLE 1,Top Merchants
# MAGIC %sql
# MAGIC SELECT
# MAGIC     merchant,
# MAGIC     total_revenue
# MAGIC FROM gold.gold_merchant_summary
# MAGIC ORDER BY total_revenue DESC
# MAGIC LIMIT 10;

# COMMAND ----------

# DBTITLE 1,Data Quality Status
# MAGIC %sql
# MAGIC SELECT
# MAGIC     dq_status,
# MAGIC     COUNT(*) AS total_records
# MAGIC FROM silver.fraud_transactions_silver
# MAGIC GROUP BY dq_status;