"""Config_loader.py will be used to read the configuration file, this will be called in __init__"""
from typing import Any
import yaml  # pylint: disable=import-error


def load_config(path: str) -> dict[str, Any]:
    """This function will be used to load configuration from YAML file"""
    with open(path, "r", encoding="utf-8") as config_file:
        return yaml.safe_load(config_file)
