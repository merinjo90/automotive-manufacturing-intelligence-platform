"""Load YAML configuration files."""

import yaml


def load_yaml(path):
    """Return the contents of a YAML file as Python objects."""
    with open(path) as file:
        return yaml.safe_load(file)
