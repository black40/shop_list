import os
import tempfile
import pytest
from src.shop_list.models.db import Database
from src.shop_list.utils.sql_utils import load_queries

QUERIES = load_queries('src/shop_list/models/qeuries.sql')


@pytest.fixture
def db_path():
    fd, path = tempfile.mkstemp(suffix='.sqlite3')
    os.close(fd)
    yield path
    os.remove(path)


@pytest.fixture
def db(db_path):
    database = Database(db_path)
    database.execute_query(QUERIES['CREATE'])
    yield database


def test_insert_and_select(db):
    db.execute_query(QUERIES['INSERT'], ('test', 0))
    items = db.get_all_items(QUERIES['SELECT'])
    assert len(items) == 1
    assert items[0][1] == 'test'
    assert items[0][2] == 0


def test_update_name(db):
    db.execute_query(QUERIES['INSERT'], ('old', 0))
    item_id = db.get_all_items(QUERIES['SELECT'])[0][0]
    db.execute_query(QUERIES['UPDATE_NAME'], ('new', item_id))
    items = db.get_all_items(QUERIES['SELECT'])
    assert items[0][1] == 'new'


def test_update_bought(db):
    db.execute_query(QUERIES['INSERT'], ('item', 0))
    item_id = db.get_all_items(QUERIES['SELECT'])[0][0]
    db.execute_query(QUERIES['UPDATE_BOUGHT'], (1, item_id))
    items = db.get_all_items(QUERIES['SELECT'])
    assert items[0][2] == 1


def test_delete(db):
    db.execute_query(QUERIES['INSERT'], ('item', 0))
    item_id = db.get_all_items(QUERIES['SELECT'])[0][0]
    db.execute_query(QUERIES['DELETE'], (item_id,))
    items = db.get_all_items(QUERIES['SELECT'])
    assert len(items) == 0
