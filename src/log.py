import sys
import logging


fmtr = logging.Formatter(
    fmt='%(asctime)s,%(msecs).5f [%(levelname)s] - %(name)s/%(funcName)s (%(lineno)d) - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

handlers = [
    logging.FileHandler('logs/info.log', mode='w'),
    logging.FileHandler('logs/error.log', mode='w'),
    logging.StreamHandler(stream=sys.stdout)
]

handlers[1].setLevel(logging.ERROR)

for handler in handlers:
    handler.setFormatter(fmtr)

initialized = set()


def get_logger(name):

    logger = logging.getLogger(name)
    if logger.name in initialized:
        return logger

    logger.setLevel(logging.INFO)

    for handler in handlers:
        logger.addHandler(handler)

    initialized.add(logger.name)

    return logger
