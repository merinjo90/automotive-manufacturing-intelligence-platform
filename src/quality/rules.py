"""Apply data-quality rules to a Spark DataFrame."""

from pyspark.sql import functions as F


def add_failed_rules(df, rules):
    """Add a failed_rules array column with the ID of every rule the row fails."""
    # A NULL condition counts as passed, so each condition must test NULL itself.
    checks = [F.when(condition, F.lit(rule_id)) for rule_id, _, condition in rules]
    return df.withColumn("failed_rules", F.array_compact(F.array(*checks)))
