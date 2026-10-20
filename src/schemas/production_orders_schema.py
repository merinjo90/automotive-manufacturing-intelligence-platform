from pyspark.sql.types import (
    DateType,
    IntegerType,
    StringType,
    StructField,
    StructType,
)

PRODUCTION_ORDERS_SCHEMA = StructType([
    StructField("production_order_id", StringType(), True),
    StructField("vehicle_model_id", StringType(), True),
    StructField("plant_id", StringType(), True),
    StructField("production_line_id", StringType(), True),
    StructField("planned_start_time", DateType(), True),
    StructField("actual_start_time", DateType(), True),
    StructField("planned_end_time", DateType(), True),
    StructField("actual_end_time", DateType(), True),
    StructField("planned_quantity", IntegerType(), True),
    StructField("actual_quantity", IntegerType(), True),
    StructField("rework_quantity", IntegerType(), True),
    StructField("scrap_quantity", IntegerType(), True),
    StructField("production_status", StringType(), True),
])
