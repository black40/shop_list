def load_queries(filename: str) -> dict[str, str]:
    """
    Загружает все SQL-запросы из файла и возвращает словарь {ключ: запрос}.
    Ключ берётся из комментария над запросом: -- KEY
    """
    queries = {}
    with open(filename, encoding='utf-8') as f:
        sql = f.read()
    blocks = sql.strip().split('\n\n')
    for block in blocks:
        lines = [line for line in block.strip().split('\n') if line]
        if not lines or not lines[0].startswith('--'):
            continue
        key = lines[0][2:].strip().upper()
        query = '\n'.join(lines[1:]).strip()
        queries[key] = query
    return queries

QUERIES = load_queries('src/shop_list/models/qeuries.sql')