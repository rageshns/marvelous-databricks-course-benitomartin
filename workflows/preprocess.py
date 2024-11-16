"""
This script handles data ingestion and feature table updates for a house price prediction system.

Key functionality:
- Loads the source dataset and identifies new records for processing
- Splits new records into train and test sets based on timestamp
- Updates existing train and test tables with new data
- Inserts the latest feature values into the feature table for serving
- Triggers and monitors pipeline updates for online feature refresh
- Sets task values to coordinate pipeline orchestration

Workflow:
1. Load source dataset and retrieve recent records with updated timestamps.
2. Split new records into train and test sets (80-20 split).
3. Append new train and test records to existing train and test tables.
4. Insert the latest feature data into the feature table for online serving.
5. Trigger a pipeline update and monitor its status until completion.
6. Set a task value indicating whether new data was processed.
"""

import argparse

from databricks.connect import DatabricksSession
from databricks.sdk import WorkspaceClient
from pyspark.sql.functions import col
from pyspark.sql.functions import max as spark_max

from credit_default.utils import load_config

workspace = WorkspaceClient()

parser = argparse.ArgumentParser()
parser.add_argument(
    "--root_path",
    action="store",
    default="",
    type=str,
    required=True,
)

args = parser.parse_args()
root_path = args.root_path
config_path = f"{root_path}/project_config.yml"
config = load_config(config_path)
# pipeline_id = config.pipeline_id

# spark = SparkSession.builder.getOrCreate()
spark = DatabricksSession.builder.getOrCreate()


catalog_name = config.catalog_name
schema_name = config.schema_name

# Load source_data table
source_data = spark.table(f"{catalog_name}.{schema_name}.source_data")

# Get max update timestamps from existing data
max_train_timestamp = (
    spark.table(f"{catalog_name}.{schema_name}.train_set")
    .select(spark_max("update_timestamp_utc").alias("max_update_timestamp"))
    .collect()[0]["max_update_timestamp"]
)

max_test_timestamp = (
    spark.table(f"{catalog_name}.{schema_name}.test_set")
    .select(spark_max("update_timestamp_utc").alias("max_update_timestamp"))
    .collect()[0]["max_update_timestamp"]
)

latest_timestamp = max(max_train_timestamp, max_test_timestamp)


# Filter source_data for rows with update_timestamp_utc greater than the latest_timestamp
new_data = source_data.filter(col("update_timestamp_utc") > latest_timestamp)
