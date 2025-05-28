from src.shop_list.utils.sql_utils import load_queries


def test_load_queries():
    queries = load_queries('src/shop_list/models/qeuries.sql')
    assert 'CREATE' in queries
    assert 'INSERT' in queries
    assert 'SELECT' in queries
    assert 'UPDATE_NAME' in queries
    assert 'UPDATE_BOUGHT' in queries
    assert 'DELETE' in queries
    assert queries['INSERT'].startswith('INSERT INTO')
