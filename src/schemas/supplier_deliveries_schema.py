from pyspark.sql.types import (
    DateType,
    IntegerType,
    StringType,
    StructField,
    StructType,
)

SUPPLIER_DELIVERIES_SCHEMA = StructType([
    StructField("delivery_id", StringType(), True),
    StructField("supplier_id", StringType(), True),
    StructField("component_id", StringType(), True),
    StructField("plant_id", StringType(), True),
    StructField("purchase_order_id", StringType(), True),
    StructField("planned_delivery_date", DateType(), True),
    StructField("actual_delivery_date", DateType(), True),
    StructField("ordered_quantity", IntegerType(), True),
    StructField("delivered_quantity", IntegerType(), True),
    StructField("accepted_quantity", IntegerType(), True),
    StructField("rejected_quantity", IntegerType(), True),
    StructField("delivery_status", StringType(), True),
])