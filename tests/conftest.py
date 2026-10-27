"""Shared pytest fixtures."""

import pytest
from pyspark.sql import SparkSession


@pytest.fixture(scope="session")
def spark():
    """Start one local SparkSession for the whole test run."""
    session = SparkSession.builder.master("local[1]").appName("tests").getOrCreate()
    session.sparkContext.setLogLevel("ERROR")
    yield session
    session.stop()
