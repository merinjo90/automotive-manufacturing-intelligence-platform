from pyspark.sql.types import (
    BooleanType,
    DateType,
    StringType,
    StructField,
    StructType,
)

QUALITY_INSPECTIONS_SCHEMA = StructType([
    StructField("inspection_id", StringType(), True),
    StructField("vehicle_id", StringType(), True),
    StructField("component_id", StringType(), True),
    StructField("supplier_id", StringType(), True),
    StructField("plant_id", StringType(), True),
    StructField("production_line_id", StringType(), True),
    StructField("inspection_timestamp", DateType(), True),
    StructField("inspection_result", StringType(), True),
    StructField("defect_code", StringType(), True),
    StructField("defect_severity", StringType(), True),
    StructField("rework_required", BooleanType(), True),
    StructField("scrap_required", BooleanType(), True),
])
