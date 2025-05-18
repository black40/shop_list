import sqlite3
import logging
from config import logger


class Database:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = None

    def _connect(self):
        if self.connection is None:
            try:
                self.connection = sqlite3.connect(self.db_path)
            except Exception as e:
                print(f'Error connecting to database: {e}')

    def close_connection(self):
        if self.connection:
            try:
                self.connection.close()
                self.connection = None
            except Exception as e:
                logging.error(f'Error closing database -- {e}')

    def execute_query(self, query, params, commit=True):
        self._connect()
        try:
            cursor = self.connection.cursor()
            try:
                cursor.execute(query, params)
                if commit:
                    self.connection.commit()
                return cursor.fetchall()
            finally:
                if 'cursor' in locals() and cursor:
                    cursor.close()
        except sqlite3.Error as e:
            logging.error(f'Database error: {e}')
            return []
        except Exception as e:
            print(
                f'Unexpected error while executing query: {query} with params: {params}. Error: {e}'
            )
            return []

    def get_all_items(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute('SELECT id, name, bought FROM items')
                return cursor.fetchall()
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f'Database error: {e}')
            return []
        except Exception as e:
            print(f'Unexpected error: {e}')
            return []

    def __enter__(self):
        try:
            self._connect()
        except Exception as e:
            logging.error(f'Error during __enter__: {e}')

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            self.close_connection()
        except Exception as e:
            logging.error(f'Error during __exit__ cleanup: {e}')
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close_connection()
