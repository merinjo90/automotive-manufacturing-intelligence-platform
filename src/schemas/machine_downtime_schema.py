from pyspark.sql.types import (
    DateType,
    IntegerType,
    StringType,
    StructField,
    StructType,
)

MACHINE_DOWNTIME_SCHEMA = StructType([
    StructField("downtime_event_id", StringType(), True),
    StructField("machine_id", StringType(), True),
    StructField("production_line_id", StringType(), True),
    StructField("start_timestamp", DateType(), True),
    StructField("end_timestamp", DateType(), True),
    StructField("downtime_reason", StringType(), True),
    StructField("planned_flag", StringType(), True),
    StructField("production_loss_units", IntegerType(), True),
])
