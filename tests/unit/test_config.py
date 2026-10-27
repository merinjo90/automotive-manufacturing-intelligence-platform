"""Unit tests for YAML configuration loading."""

from src.common.config import load_yaml

REFERENCE_DATA = "configs/reference_data.yaml"


def test_reference_data_has_required_non_empty_lists():
    data = load_yaml(REFERENCE_DATA)
    required = {
        "supplier_ids",
        "component_ids",
        "plant_ids",
        "production_line_ids",
        "machine_ids",
        "delivery_statuses",
        "production_statuses",
        "inspection_results",
        "defect_severities",
        "planned_flags",
    }

    assert required <= set(data)
    # A YAML indentation error turns a list into None.
    assert all(isinstance(values, list) and values for values in data.values())


def test_planned_flags_stay_text():
    # Unquoted True/False would become booleans and match no CSV value.
    assert load_yaml(REFERENCE_DATA)["planned_flags"] == ["True", "False"]
