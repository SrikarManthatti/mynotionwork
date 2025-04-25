import yaml
from typing import Any

def load_config(path: str) -> dict[str, Any]:
    with open(path, "r") as config_file:
        return yaml.safe_load(config_file)