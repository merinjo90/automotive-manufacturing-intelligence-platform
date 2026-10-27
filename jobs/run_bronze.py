"""Bronze ingestion job: load all four sample datasets into data/bronze/."""

import os
import uuid

from pyspark.sql import SparkSession

from src.ingestion.bronze_loader import load_csv_to_bronze
from src.schemas.machine_downtime_schema import MACHINE_DOWNTIME_SCHEMA
from src.schemas.production_orders_schema import PRODUCTION_ORDERS_SCHEMA
from src.schemas.quality_inspections_schema import QUALITY_INSPECTIONS_SCHEMA
from src.schemas.supplier_deliveries_schema import SUPPLIER_DELIVERIES_SCHEMA

DATASETS = {
    "supplier_deliveries": SUPPLIER_DELIVERIES_SCHEMA,
    "production_orders": PRODUCTION_ORDERS_SCHEMA,
    "quality_inspections": QUALITY_INSPECTIONS_SCHEMA,
    "machine_downtime": MACHINE_DOWNTIME_SCHEMA,
}

SOURCE_DIR = "data/sample"
BRONZE_DIR = "data/bronze"
TRACKING_PATH = "data/tracking/processed_files.json"
SOURCE_SYSTEM = "synthetic_generator"


def main():
    pipeline_run_id = f"run_{uuid.uuid4().hex[:8]}"
    os.makedirs(os.path.dirname(TRACKING_PATH), exist_ok=True)

    spark = SparkSession.builder.appName("bronze_ingestion").getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")

    print(f"Pipeline run: {pipeline_run_id}")
    for dataset, schema in DATASETS.items():
        status = load_csv_to_bronze(
            spark,
            f"{SOURCE_DIR}/{dataset}.csv",
            schema,
            f"{BRONZE_DIR}/{dataset}",
            TRACKING_PATH,
            SOURCE_SYSTEM,
            pipeline_run_id,
        )
        print(f"{dataset}: {status}")

    spark.stop()


if __name__ == "__main__":
    main()
