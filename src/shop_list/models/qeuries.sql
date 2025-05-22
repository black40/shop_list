-- Создание таблицы
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    bought INTEGER DEFAULT 0
);

-- Добавление нового элемента
INSERT INTO items (name, bought) VALUES (?, ?);

-- Получение всех элементов
SELECT id, name, bought FROM items;

-- Обновление элемента
UPDATE items SET name = ? WHERE id = ?;

-- Удаление элемента
DELETE FROM items WHERE id = ?;

-- Переключение статуса "куплено"
UPDATE items SET bought = ? WHERE id = ?;