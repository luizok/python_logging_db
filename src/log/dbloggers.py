import abc
import logging
import inspect

import sqlite3
from mysql.connector import connect as mysql_connect


class DatabaseLoggingHandler(logging.Handler, abc.ABC):

    def __init__(self, tbl_name, connect_fn, *conn_fn_vargs, **conn_fn_kwargs):
        try:
            self.conn = connect_fn(*conn_fn_vargs, **conn_fn_kwargs)
        except Exception as e:
            print('Error while creating DatabaseLogger ', e)
        self.tbl_name = tbl_name
        self.lock = None
        self.cursor = self.get_cursor()

        super(logging.Handler, self).__init__()

    @abc.abstractmethod
    def _emit(self, record: logging.LogRecord):
        ...

    @abc.abstractmethod
    def _get_cursor(self):
        ...

    def get_cursor(self):
        self.acquire()
        cursor = self._get_cursor()
        self.release()

        return cursor

    def emit(self, record: logging.LogRecord):

        self.acquire()
        self._emit(record)
        self.conn.commit()
        self.release()


def loggable(obj):

    # print(f'{obj.__module__}.{obj.__name__}')
    # print(f'{inspect.isclass(obj)=}')
    # print(f'{inspect.isfunction(obj)=}')

    logger = logging.getLogger(
        f'{obj.__module__}.{obj.__name__}'
    )

    def cls_wrapper():
        setattr(obj, 'logger', logger)
        return obj

    # def function_wrapper(*vargs, **kwargs):
    #     logger.info('Running on new client')
    #     try:
    #         obj(*vargs, **kwargs)
    #     except Exception as e:
    #         logger.error('Error - ', e)

    # if isinstance(obj, class):
    new_obj = None
    if inspect.isclass(obj):
        new_obj = cls_wrapper()
    # elif inspect.isfunction(obj):
    #     new_obj = function_wrapper

    return new_obj


@loggable
class SQLiteLoggingHandler(DatabaseLoggingHandler):

    def __init__(self, tbl_name, *sqlite_vargs, **sqlite_kwargs):
        super().__init__(tbl_name, sqlite3.connect, *sqlite_vargs, **sqlite_kwargs)

    def _get_cursor(self):
        return self.conn.cursor()

    def _emit(self, record: logging.LogRecord):

        self.logger.info('Inserting into database')
        self.cursor.execute(f'''
            INSERT INTO {self.tbl_name}(time, level, path, lineno, message)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            record.asctime, record.levelname,
            f'{record.name}.{record.funcName}',
            record.lineno, record.message
        ))
        self.logger.info('Inserted log')


class MYSQLLoggingHandler(DatabaseLoggingHandler):

    def __init__(self, tbl_name, **mysql_kwargs):
        super().__init__(tbl_name, mysql_connect, **mysql_kwargs)

    def _get_cursor(self):
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
