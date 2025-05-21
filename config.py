import os
import logging
from dotenv import load_dotenv

load_dotenv(override=True)

DB_NAME = os.getenv('DB_NAME')
DB_PATH = os.getenv('DB_PATH')
if DB_NAME is None or DB_PATH is None:
    raise ValueError('DB_NAME and DB_PATH environment variables must be set')
DB_FULL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), DB_PATH, DB_NAME))

LOG_FILE_NAME = 'logs.log'

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

handler = logging.FileHandler(LOG_FILE_NAME, mode='w', encoding='utf-8')
handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s::%(levelname)s::%(message)s')

handler.setFormatter(formatter)
logger.addHandler(handler)
