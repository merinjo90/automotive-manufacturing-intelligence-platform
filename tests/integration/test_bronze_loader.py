"""Integration tests for the Bronze loader (Spark + tracking + Parquet)."""

from src.ingestion.bronze_loader import load_csv_to_bronze
from src.schemas.supplier_deliveries_schema import SUPPLIER_DELIVERIES_SCHEMA

SAMPLE_CSV = "data/sample/supplier_deliveries.csv"


def test_second_load_of_same_file_is_skipped(spark, tmp_path):
    bronze_path = tmp_path / "bronze"
    tracking_path = tmp_path / "processed_files.json"

    first = load_csv_to_bronze(
        spark,
        SAMPLE_CSV,
        SUPPLIER_DELIVERIES_SCHEMA,
        bronze_path,
        tracking_path,
        "synthetic_generator",
        "run_001",
    )
    second = load_csv_to_bronze(
        spark,
        SAMPLE_CSV,
        SUPPLIER_DELIVERIES_SCHEMA,
        bronze_path,
        tracking_path,
        "synthetic_generator",
        "run_002",
    )

    assert (first, second) == ("LOADED", "SKIPPED")
    assert spark.read.parquet(str(bronze_path)).count() == 200


def test_bronze_rows_have_metadata_columns(spark, tmp_path):
    bronze_path = tmp_path / "bronze"

    load_csv_to_bronze(
        spark,
        SAMPLE_CSV,
        SUPPLIER_DELIVERIES_SCHEMA,
        bronze_path,
        tmp_path / "processed_files.json",
        "synthetic_generator",
        "run_001",
    )
    bronze = spark.read.parquet(str(bronze_path))
    metadata = {
        "source_file",
        "source_system",
        "ingestion_timestamp",
        "ingestion_date",
        "pipeline_run_id",
    }

    assert len(bronze.columns) == 17
    assert metadata <= set(bronze.columns)
