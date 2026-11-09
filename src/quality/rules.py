"""Apply data-quality rules to a Spark DataFrame."""

from pyspark.sql import functions as F


def add_failed_rules(df, rules):
    """Add a failed_rules array column with the ID of every rule the row fails."""
    # A NULL condition counts as passed, so each condition must test NULL itself.
    checks = [F.when(condition, F.lit(rule_id)) for rule_id, _, condition in rules]
    return df.withColumn("failed_rules", F.array_compact(F.array(*checks)))


def missing_or_not_in(column, allowed):
    """Return a condition that is True when a value is NULL or not approved."""
    return F.col(column).isNull() | ~F.col(column).isin(allowed)


def any_missing(columns):
    """Return a condition that is True when any column is NULL."""
    condition = F.lit(False)
    for column in columns:
        condition = condition | F.col(column).isNull()
    return condition


def any_negative(columns):
    """Return a condition that is True when any column is below zero."""
    condition = F.lit(False)
    for column in columns:
        condition = condition | (F.col(column) < 0)
    return condition


def all_present_and_non_negative(columns):
    """Return a condition that is True when every column is present and >= 0."""
    condition = F.lit(True)
    for column in columns:
        condition = condition & F.col(column).isNotNull() & (F.col(column) >= 0)
    return condition
