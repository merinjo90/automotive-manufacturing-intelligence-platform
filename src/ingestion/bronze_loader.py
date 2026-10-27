"""Load a source CSV into the Bronze layer, skipping files already processed."""

from datetime import datetime, timezone

from src.ingestion.bronze import add_bronze_metadata
from src.ingestion.file_tracker import (
    calculate_file_hash,
    record_file,
    was_file_processed,
)


def load_csv_to_bronze(
    spark, csv_path, schema, bronze_path, tracking_path, source_system, pipeline_run_id
):
    """Load one CSV into Bronze Parquet; return "SKIPPED" or "LOADED"."""
    file_hash = calculate_file_hash(csv_path)

    if was_file_processed(tracking_path, file_hash):
        return "SKIPPED"

    df = spark.read.csv(str(csv_path), header=True, schema=schema)
    df = add_bronze_metadata(df, str(csv_path), source_system, pipeline_run_id)
    df.write.mode("append").parquet(str(bronze_path))

    # Record only after a successful write, so a failed load is retried.
    record_file(
        tracking_path,
        {
            "source_file": str(csv_path),
            "file_hash": file_hash,
            "ingestion_timestamp": datetime.now(timezone.utc).isoformat(),
            "pipeline_run_id": pipeline_run_id,
            "processing_status": "SUCCESS",
        },
    )
    return "LOADED"
