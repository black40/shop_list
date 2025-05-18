import logging

logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='shop_list.log',
    filemode='w',
)
logger = logging.getLogger('shop_list')
