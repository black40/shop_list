-- CREATE
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    bought INTEGER DEFAULT 0
);

-- INSERT
INSERT INTO items (name, bought) VALUES (?, ?);

-- SELECT
SELECT id, name, bought FROM items;

-- UPDATE_NAME
UPDATE items SET name = ? WHERE id = ?;

-- UPDATE_BOUGHT
UPDATE items SET bought = ? WHERE id = ?;

-- DELETE
DELETE FROM items WHERE id = ?;