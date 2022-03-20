import abc
import logging

import sqlite3
from mysql.connector import connect as mysql_connect


class DatabaseLoggingHandler(logging.Handler, abc.ABC):

    def __init__(self, tbl_name, connect_fn, *conn_fn_vargs, **conn_fn_kwargs):
        try:
            self.conn = connect_fn(*conn_fn_vargs, **conn_fn_kwargs)
        except Exception as e:
            print('Error while creating DatabaseLogger ', e)
        self.tbl_name = tbl_name
        self.cursor = self.get_cursor()
        self.lock = None

        super(logging.Handler, self).__init__()

    @abc.abstractmethod
    def _emit(self, record: logging.LogRecord):
        ...

    @abc.abstractmethod
    def get_cursor(self):
        ...

    def emit(self, record: logging.LogRecord):

        self.acquire()
        self._emit(record)
        self.conn.commit()
        self.release()


class SQLiteLoggingHandler(DatabaseLoggingHandler):

    def __init__(self, tbl_name, *sqlite_vargs, **sqlite_kwargs):
        super().__init__(tbl_name, sqlite3.connect, *sqlite_vargs, **sqlite_kwargs)

    def get_cursor(self):
        return self.conn.cursor()

    def _emit(self, record: logging.LogRecord):

        self.cursor.execute(f'''
            INSERT INTO {self.tbl_name}(time, level, path, lineno, message)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            record.asctime, record.levelname,
            f'{record.name}.{record.funcName}',
            record.lineno, record.message
        ))


class MYSQLLoggingHandler(DatabaseLoggingHandler):

    def __init__(self, tbl_name, **mysql_kwargs):
        super().__init__(tbl_name, mysql_connect, **mysql_kwargs)

    def get_cursor(self):
        return self.conn.cursor()

    def _emit(self, record: logging.LogRecord):

        self.cursor.execute(f'''
            INSERT INTO {self.tbl_name}(time, level, path, lineno, message)
            VALUES (%s, %s, %s, %s, %s)
        ''', (
            record.asctime, record.levelname,
            f'{record.name}.{record.funcName}',
            record.lineno, record.message
        ))
