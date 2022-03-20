import sys
import logging

import src.log.dbloggers as dblog


fmtr = logging.Formatter(
    fmt='%(asctime)s.%(msecs).0f [%(levelname)s] - %(name)s.%(funcName)s (%(lineno)d) - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

h1 = logging.FileHandler('logs/info.log', mode='w')
h2 = logging.FileHandler('logs/error.log', mode='w')
h3 = logging.StreamHandler(stream=sys.stdout)
h4 = dblog.SQLiteLoggingHandler('error_log', 'errordb.db', **{'check_same_thread': False})
h5 = dblog.MYSQLLoggingHandler('error_log', **{
    'host': 'localhost',
    'port': 3306,
    'database': 'logs',
    'user': 'user',
    'password': 'senha',
    'autocommit': True
})

h2.setLevel(logging.ERROR)
h4.setLevel(logging.ERROR)
h5.setLevel(logging.ERROR)

handlers = [h1, h2, h3, h4, h5]

for i, h in enumerate(handlers):
    handlers[i].setFormatter(fmtr)

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
