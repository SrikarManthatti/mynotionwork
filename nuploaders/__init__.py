"""Module for initializing the nuploaders package, loading .env and YAML config."""
import logging
import yaml # pylint: disable=import-error

logging.basicConfig(
    level = logging.WARN,
    format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt = '%Y-%m-%d %H:%M:%S',
)

log = logging.getLogger(__name__)

try:
    from dotenv import load_dotenv # pylint: disable=import-error
except ModuleNotFoundError as me: # pylint: disable=import-error
    log.error("python-dotenv module not found; skipping .env loading.")
else:
    load_dotenv()
    log.info(".env file loaded successfully.")

# Load YAML config
try:
    from .config_loader import load_config  # or use absolute import if needed
    CONFIG = load_config("config/basic_config.yaml")
    log.info("YAML config loaded successfully.")
except (FileNotFoundError, yaml.YAMLError) as e:
    CONFIG = {}
    log.error("Failed to load YAML config: %s", e)
