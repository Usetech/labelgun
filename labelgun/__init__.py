import logging


__version__ = '0.2.0'

logging.getLogger('labelgun').addHandler(logging.NullHandler())
