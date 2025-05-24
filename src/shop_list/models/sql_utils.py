def load_queries(filename: str) -> dict[str, str]:
    """
    Загружает все SQL-запросы из файла и возвращает словарь {ключ: запрос}.
    Ключ — первая строка запроса (обычно комментарий или ключевое слово).
    """
    queries = {}
    with open(filename, encoding='utf-8') as f:
        sql = f.read()
    # Разделяем по двойному переносу строки (между запросами)
    for block in sql.strip().split('\n\n'):
        lines = [line for line in block.strip().split('\n') if line and not line.startswith('--')]
        if not lines:
            continue
        # Ключ — первая строка запроса (например, 'CREATE TABLE', 'INSERT INTO ...')
        key = lines[0].strip().split()[0].upper()
        queries[key] = '\n'.join(lines)
    return queries
