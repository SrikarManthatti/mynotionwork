import logging

logging.basicConfig(
    level = logging.INFO
    format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt = '%Y-%m-%d %H:%M:%S'
)

log = logging.getLogger(__name__)

try:
    from dotenv import load_dotenv
except ModuelNotFoundError as me:
    log.error("python-dotenv module not found; skipping .env loading.")
else:
    load_dotenv()
    log.info(".env file loaded successfully.")