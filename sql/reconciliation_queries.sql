-- ============================================================
-- RECONCILIATION VALIDATION QUERIES
-- ============================================================
-- Purpose: Ad-hoc validation queries for data quality checks
-- Use: Run these queries to verify reconciliation results
-- ============================================================

-- ============================================================
-- 1. VIEW RECONCILIATION RESULTS SUMMARY
-- ============================================================
SELECT 
    validation_name,
    status,
    details,
    validation_timestamp,
    executed_by
FROM recon.reconciliation_results
ORDER BY validation_timestamp DESC;

-- ============================================================
-- 2. CHECK BRONZE VS SILVER ROW COUNTS
-- ============================================================
SELECT 
    'Bronze' AS layer,
    COUNT(*) AS row_count
FROM bronze.fraud_transactions_bronze
UNION ALL
SELECT 
    'Silver' AS layer,
    COUNT(*) AS row_count
FROM silver.fraud_transactions_silver;

-- ============================================================
-- 3. VERIFY AGGREGATE SUMS MATCH
-- ============================================================
SELECT 
    'Bronze' AS layer,
    ROUND(SUM(amt), 2) AS total_amount
FROM bronze.fraud_transactions_bronze
UNION ALL
SELECT 
    'Silver' AS layer,
    ROUND(SUM(amt), 2) AS total_amount
FROM silver.fraud_transactions_silver;

-- ============================================================
-- 4. CHECK FOR DUPLICATES IN SILVER
-- ============================================================
SELECT 
    trans_num,
    COUNT(*) AS duplicate_count
FROM silver.fraud_transactions_silver
GROUP BY trans_num
HAVING COUNT(*) > 1;

-- ============================================================
-- 5. VALIDATE DATA QUALITY STATUS DISTRIBUTION
-- ============================================================
SELECT 
    dq_status,
    COUNT(*) AS record_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS percentage
FROM silver.fraud_transactions_silver
GROUP BY dq_status;

-- ============================================================
-- 6. CHECK FOR NULL VALUES IN CRITICAL COLUMNS
-- ============================================================
SELECT 
    'trans_num' AS column_name,
    COUNT(*) AS null_count
FROM silver.fraud_transactions_silver
WHERE trans_num IS NULL
UNION ALL
SELECT 
    'amt' AS column_name,
    COUNT(*) AS null_count
FROM silver.fraud_transactions_silver
WHERE amt IS NULL
UNION ALL
SELECT 
    'trans_date_trans_time' AS column_name,
    COUNT(*) AS null_count
FROM silver.fraud_transactions_silver
WHERE trans_date_trans_time IS NULL;

-- ============================================================
-- 7. VERIFY BUSINESS RULE: NEGATIVE AMOUNTS
-- ============================================================
SELECT 
    COUNT(*) AS negative_amount_count
FROM silver.fraud_transactions_silver
WHERE amt < 0;

-- ============================================================
-- 8. COMPARE FRAUD COUNTS ACROSS LAYERS
-- ============================================================
SELECT 
    'Bronze' AS layer,
    SUM(is_fraud) AS fraud_count
FROM bronze.fraud_transactions_bronze
UNION ALL
SELECT 
    'Silver' AS layer,
    SUM(is_fraud) AS fraud_count
FROM silver.fraud_transactions_silver;

-- ============================================================
-- 9. VALIDATE SCHEMA CONSISTENCY
-- ============================================================
DESCRIBE TABLE bronze.fraud_transactions_bronze;
DESCRIBE TABLE silver.fraud_transactions_silver;

-- ============================================================
-- 10. CHECK LOAD METADATA
-- ============================================================
SELECT 
    MIN(ingestion_timestamp) AS first_load,
    MAX(ingestion_timestamp) AS last_load,
    COUNT(DISTINCT batch_id) AS total_batches
FROM bronze.fraud_transactions_bronze;

-- ============================================================
-- 11. VERIFY TIME RANGE OF TRANSACTIONS
-- ============================================================
SELECT 
    MIN(trans_date_trans_time) AS earliest_transaction,
    MAX(trans_date_trans_time) AS latest_transaction,
    DATEDIFF(MAX(trans_date_trans_time), MIN(trans_date_trans_time)) AS days_span
FROM silver.fraud_transactions_silver;

-- ============================================================
-- 12. CHECK GOLD LAYER AGGREGATIONS
-- ============================================================
-- Verify transaction summary totals
SELECT 
    SUM(total_transactions) AS gold_total_transactions,
    ROUND(SUM(total_amount), 2) AS gold_total_amount
FROM gold.gold_transaction_summary;

-- Compare with silver source
SELECT 
    COUNT(*) AS silver_total_transactions,
    ROUND(SUM(amt), 2) AS silver_total_amount
FROM silver.fraud_transactions_silver;

-- ============================================================
-- 13. RECONCILIATION STATUS OVER TIME
-- ============================================================
SELECT 
    DATE(validation_timestamp) AS validation_date,
    validation_name,
    status,
    COUNT(*) AS occurrence_count
FROM recon.reconciliation_results
GROUP BY DATE(validation_timestamp), validation_name, status
ORDER BY validation_date DESC, validation_name;

-- ============================================================
-- 14. DATA FRESHNESS CHECK
-- ============================================================
SELECT 
    'Bronze' AS layer,
    MAX(ingestion_timestamp) AS last_updated
FROM bronze.fraud_transactions_bronze
UNION ALL
SELECT 
    'Silver' AS layer,
    MAX(ingestion_timestamp) AS last_updated
FROM silver.fraud_transactions_silver;

-- ============================================================
-- 15. SAMPLE DATA COMPARISON
-- ============================================================
-- Bronze sample
SELECT 'BRONZE SAMPLE' AS source, * 
FROM bronze.fraud_transactions_bronze 
LIMIT 5;

-- Silver sample
SELECT 'SILVER SAMPLE' AS source, * 
FROM silver.fraud_transactions_silver 
LIMIT 5;

-- ============================================================
-- END OF RECONCILIATION QUERIES
-- ============================================================