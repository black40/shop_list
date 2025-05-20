import os
import logging
from dotenv import load_dotenv

load_dotenv(override=True)

DB_NAME = os.getenv('DB_NAME')
DB_PATH = os.getenv('DB_PATH')
if DB_NAME is None or DB_PATH is None:
    raise ValueError('DB_NAME and DB_PATH environment variables must be set')
DB_FULL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), DB_PATH, DB_NAME))

logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='shop_list.log',
    filemode='w',
)
logger = logging.getLogger('shop_list')
