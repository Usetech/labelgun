import logging


__version__ = '0.2.1'

logging.getLogger('labelgun').addHandler(logging.NullHandler())
