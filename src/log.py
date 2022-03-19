import sys
import logging
import sqlite3

from threading import Lock


db_lock = Lock()

class SQLiteDatabaseHandler(logging.Handler):

    def __init__(self, file, tbl_name):
        self.conn = sqlite3.connect(file, check_same_thread=False)
        self.tbl_name = tbl_name
        super().__init__()

    def emit(self, record: logging.LogRecord):
        db_lock.acquire()

        cursor = self.conn.cursor()
        cursor.execute(f'''
            INSERT INTO {self.tbl_name}(time, level, path, lineno, message)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            record.asctime, record.levelname,
            f'{record.name}.{record.funcName}',
            record.lineno, record.message
        ))
        self.conn.commit()

        db_lock.release()


fmtr = logging.Formatter(
    fmt='%(asctime)s.%(msecs).0f [%(levelname)s] - %(name)s.%(funcName)s (%(lineno)d) - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

handlers = [
    logging.FileHandler('logs/info.log', mode='w'),
    logging.FileHandler('logs/error.log', mode='w'),
    logging.StreamHandler(stream=sys.stdout),
    SQLiteDatabaseHandler('errordb.db', 'error_log')
]

handlers[1].setLevel(logging.ERROR)
handlers[3].setLevel(logging.ERROR)

for handler in handlers:
    handler.setFormatter(fmtr)

initialized = set()


def get_logger(*names):

    logger = logging.getLogger('.'.join(names))
    if logger.name in initialized:
        return logger

    logger.setLevel(logging.INFO)

    for handler in handlers:
        logger.addHandler(handler)

    initialized.add(logger.name)

    return logger
