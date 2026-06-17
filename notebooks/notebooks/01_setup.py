# Databricks notebook source
# DBTITLE 1,Verify SparkSession
# Verify Spark environment is working
spark

# COMMAND ----------

# DBTITLE 1,Create Databases
# MAGIC %sql
# MAGIC CREATE DATABASE IF NOT EXISTS bronze;
# MAGIC CREATE DATABASE IF NOT EXISTS silver;
# MAGIC CREATE DATABASE IF NOT EXISTS gold;
# MAGIC CREATE DATABASE IF NOT EXISTS recon;
# MAGIC CREATE DATABASE IF NOT EXISTS audit;
# MAGIC CREATE DATABASE IF NOT EXISTS config;

# COMMAND ----------

# DBTITLE 1,Verify Databases
# MAGIC %sql
# MAGIC SHOW DATABASES;

# COMMAND ----------

# DBTITLE 1,Verify File Upload Location
# MAGIC %sql
# MAGIC -- Create a schema and volume in Unity Catalog to store raw data files
# MAGIC -- DBFS is disabled in this workspace, so we use Unity Catalog Volumes instead
# MAGIC
# MAGIC CREATE SCHEMA IF NOT EXISTS workspace.vrahad_recon;
# MAGIC
# MAGIC CREATE VOLUME IF NOT EXISTS workspace.vrahad_recon.raw_data
# MAGIC COMMENT 'Raw data storage for Vrahad Recon Project';

# COMMAND ----------

# DBTITLE 1,Verify Directory Creation
# Verify the Unity Catalog Volume was created
print("✅ Volume created: /Volumes/workspace/vrahad_recon/raw_data")
print("\nListing volume contents:")
try:
    files = dbutils.fs.ls("/Volumes/workspace/vrahad_recon/raw_data")
    if len(files) == 0:
        print("Volume is empty (ready for file upload)")
    else:
        display(files)
except Exception as e:
    print(f"Volume info: {e}")

# COMMAND ----------

# DBTITLE 1,Check for Uploaded File
# Check if fraudTrain.csv has been uploaded to the volume
print("Checking for fraudTrain.csv in volume...")
try:
    files = dbutils.fs.ls("/Volumes/workspace/vrahad_recon/raw_data")
    display(files)
    if len(files) == 0:
        print("\n⚠️ No files found yet.")
        print("\n📁 Upload fraudTrain.csv to: /Volumes/workspace/vrahad_recon/raw_data")
    else:
        print(f"\n✅ Found {len(files)} file(s) in volume")
except Exception as e:
    print(f"⚠️ Error: {e}")

# COMMAND ----------

# DBTITLE 1,Test Read CSV File
# Test reading the uploaded CSV file from Unity Catalog Volume
# Run this cell after uploading fraudTrain.csv to the volume

try:
    df = spark.read.csv(
        "/Volumes/workspace/vrahad_recon/raw_data/fraudTrain.csv", 
        header=True, 
        inferSchema=True
    )
    
    print(f"✅ Successfully loaded fraudTrain.csv from volume")
    print(f"Total rows: {df.count():,}")
    print(f"Total columns: {len(df.columns)}")
    print("\nFirst 5 rows:")
    display(df.limit(5))
    
except Exception as e:
    print(f"⚠️ Could not read file: {e}")
    print("\nPlease ensure fraudTrain.csv is uploaded to:")
    print("/Volumes/workspace/vrahad_recon/raw_data/fraudTrain.csv")

# COMMAND ----------



# COMMAND ----------

# DBTITLE 1,Upload Instructions
# MAGIC %md
# MAGIC # 📤 How to Upload fraudTrain.csv to the Volume
# MAGIC
# MAGIC ## Option 1: Using Databricks UI (Recommended)
# MAGIC
# MAGIC 1. **Open Catalog Explorer**
# MAGIC    - Click **Catalog** in the left sidebar
# MAGIC    
# MAGIC 2. **Navigate to the volume**
# MAGIC    - Expand `workspace` catalog
# MAGIC    - Expand `vrahad_recon` schema  
# MAGIC    - Click on `raw_data` volume
# MAGIC    
# MAGIC 3. **Upload the file**
# MAGIC    - Click **Upload Files** button (top right)
# MAGIC    - Select `fraudTrain.csv` from your computer
# MAGIC    - Wait for upload to complete
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## Option 2: Drag and Drop to Workspace, Then Copy
# MAGIC
# MAGIC 1. Drag `fraudTrain.csv` to your workspace folder
# MAGIC 2. Run this code in the next cell:
# MAGIC
# MAGIC ```python
# MAGIC dbutils.fs.cp(
# MAGIC     "file:/Workspace/Users/sagaraher366@gmail.com/fraudTrain.csv",
# MAGIC     "/Volumes/workspace/vrahad_recon/raw_data/fraudTrain.csv"
# MAGIC )
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## ✅ After Upload
# MAGIC
# MAGIC Run the **"Check for Uploaded File"** cell below to verify the upload succeeded.

# COMMAND ----------

# DBTITLE 1,Copy File from Workspace to Volume (If Needed)
# ONLY RUN THIS IF you dragged fraudTrain.csv to your workspace folder first
# This copies the file from workspace to the Unity Catalog Volume

# dbutils.fs.cp(
#     "file:/Workspace/Users/sagaraher366@gmail.com/fraudTrain.csv",
#     "/Volumes/workspace/vrahad_recon/raw_data/fraudTrain.csv"
# )

print("⚠️ This cell is commented out.")
print("Uncomment and run only if you need to copy from workspace to volume.")