from pyspark.sql.functions import current_date, current_timestamp, lit


def add_bronze_metadata(df, source_file, source_system, pipeline_run_id):
    df = df.withColumn("source_file", lit(source_file))
    df = df.withColumn("source_system", lit(source_system))
    df = df.withColumn("ingestion_timestamp", current_timestamp())
    df = df.withColumn("ingestion_date", current_date())
    df = df.withColumn("pipeline_run_id", lit(pipeline_run_id))
    return df
