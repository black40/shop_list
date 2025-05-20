import os
import sqlite3
from typing import Any, Optional
from config import logger


class Database:
    """
    Класс для работы с SQLite-базой данных.
    """

    def __init__(self, db_path: str):
        """
        :param db_path: Путь к файлу базы данных.
        """
        # Создаём каталог для базы, если его нет
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db_path: str = db_path
        self.connection: Optional[sqlite3.Connection] = None

    def _connect(self) -> None:
        """Устанавливает соединение с базой данных, если оно ещё не установлено."""
        if self.connection is None:
            try:
                self.connection = sqlite3.connect(self.db_path)
            except Exception as e:
                logger.error(f'Error connecting to database: {e}')

    def close_connection(self) -> None:
        """Закрывает соединение с базой данных."""
        if self.connection is not None:
            try:
                self.connection.close()
            except Exception as e:
                logger.error(f'Error closing database: {e}')
            finally:
                self.connection = None

    def execute_query(
        self, query: str, params: tuple[Any, ...] = (), commit: bool = True
    ) -> list[Any]:
        """
        Выполняет SQL-запрос с параметрами.

        :param query: SQL-запрос.
        :param params: Параметры для запроса.
        :param commit: Нужно ли делать commit (по умолчанию True).
        :return: Результат выборки (fetchall) или пустой список при ошибке.
        """
        self._connect()
        if self.connection is None:
            logger.error('No database connection.')
            return []
        try:
            cursor = self.connection.cursor()
            try:
                cursor.execute(query, params)
                if commit:
                    self.connection.commit()
                return cursor.fetchall()
            finally:
                cursor.close()
        except sqlite3.Error as e:
            logger.error(f'Database error: {e}')
            return []
        except Exception as e:
            logger.error(
                f'Unexpected error while executing query: {query} with params: {params}. Error: {e}'
            )
            return []

    def get_all_items(self, query: str) -> list[Any]:
        """
        Выполняет SELECT-запрос без параметров и возвращает все строки.

        :param query: SQL-запрос SELECT.
        :return: Список строк результата.
        """
        self._connect()
        if self.connection is None:
            logger.error('No database connection.')
            return []
        try:
            cursor = self.connection.cursor()
            try:
                params: tuple[Any, ...] = ()
                cursor.execute(query, params)
                return cursor.fetchall()
            finally:
                cursor.close()
        except sqlite3.Error as e:
            logger.error(f'Database error: {e}')
            return []
        except Exception as e:
            logger.error(f'Unexpected error: {e}')
            return []

    def fetch_one(self, query: str, params: tuple[Any, ...] = ()) -> Optional[Any]:
        """
        Выполняет SELECT-запрос и возвращает одну строку.

        :param query: SQL-запрос SELECT.
        :param params: Параметры для запроса.
        :return: Одна строка результата или None.
        """
        self._connect()
        if self.connection is None:
            logger.error('No database connection.')
            return None
        try:
            cursor = self.connection.cursor()
            try:
                cursor.execute(query, params)
                return cursor.fetchone()
            finally:
                cursor.close()
        except sqlite3.Error as e:
            logger.error(f'Database error: {e}')
            return None
        except Exception as e:
            logger.error(f'Unexpected error: {e}')
            return None

    def is_connected(self) -> bool:
        """Проверяет, открыто ли соединение с базой данных."""
        return self.connection is not None

    def __enter__(self) -> 'Database':
        self._connect()
        return self

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        self.close_connection()

    def __del__(self) -> None:
        self.close_connection()
