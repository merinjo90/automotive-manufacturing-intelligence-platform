"""Integration tests for the generic data-quality rule engine."""

from pyspark.sql import functions as F

from src.quality.rules import add_failed_rules


def test_failed_rules_lists_every_failed_rule(spark):
    rules = [
        ("R_ID_MISSING", "ID is missing", F.col("id").isNull()),
        ("R_QTY_NEGATIVE", "Quantity is negative", F.col("qty") < 0),
    ]
    df = spark.createDataFrame([("A1", 5), (None, -1)], ["id", "qty"])

    rows = add_failed_rules(df, rules).orderBy("qty").collect()

    assert rows[0]["failed_rules"] == ["R_ID_MISSING", "R_QTY_NEGATIVE"]
    assert rows[1]["failed_rules"] == []
