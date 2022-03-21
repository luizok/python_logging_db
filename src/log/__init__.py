import sys
import logging

import src.log.dbloggers as dblog


handlers = []
initialized = set()
_called = False


def init():

    global handlers, _called

    fmtr = logging.Formatter(
        fmt='%(asctime)s.%(msecs).0f [%(levelname)s] - %(name)s.%(funcName)s (%(lineno)d) - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    hdlrs = [
        logging.FileHandler('logs/info.log', mode='w'),
        logging.FileHandler('logs/error.log', mode='w'),
        logging.StreamHandler(stream=sys.stdout),
        dblog.SQLiteLoggingHandler(
            'error_log', 'errordb.db',
            **{'check_same_thread': False}
        ),
    ]
    # h5 = dblog.MYSQLLoggingHandler('error_log', **{
    #     'host': 'localhost',
    #     'port': 3306,
    #     'database': 'logs',
    #     'user': 'user',
    #     'password': 'senha',
    #     'autocommit': True
    # })

    # h5.setLevel(logging.ERROR)

    for i, h in enumerate(hdlrs):
        hdlrs[i].setLevel(logging.INFO)
        hdlrs[i].setFormatter(fmtr)

    hdlrs[1].setLevel(logging.ERROR)
    hdlrs[3].setLevel(logging.ERROR)

    handlers = hdlrs


def get_logger(*names):

    global handlers, initialized, _called

    if not _called:
        init()
        _called = False

    logger = logging.getLogger('.'.join(names))
    if logger.name in initialized:
        return logger

    logger.setLevel(logging.INFO)

    for handler in handlers:
        logger.addHandler(handler)

    initialized.add(logger.name)

    return logger
