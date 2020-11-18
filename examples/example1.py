import logging
import logging.handlers

import structlog

from labelgun.integrations.logging_utils import StructlogJsonFormatter
from labelgun.integrations.structlog_utils import dict_msg_processor
from labelgun.label import Label

json_processors = [
    structlog.stdlib.filter_by_level,
    structlog.processors.TimeStamper(fmt="iso"),
    structlog.stdlib.add_logger_name,
    structlog.stdlib.add_log_level,
    structlog.stdlib.PositionalArgumentsFormatter(),
    structlog.processors.StackInfoRenderer(),
    structlog.processors.UnicodeDecoder(),
    structlog.processors.format_exc_info,
    dict_msg_processor,
]


def _init_structlog(processors):
    structlog.configure(
        processors=processors,
        context_class=structlog.threadlocal.wrap_dict(dict),
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )


def _init_logging(default_formatter):
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(default_formatter)

    root_logger.addHandler(console_handler)


def init_logger():
    processors = json_processors
    formatter = StructlogJsonFormatter(json_ensure_ascii=False)
    formatter.set_structlog_processors(processors)

    _init_logging(formatter)
    _init_structlog(processors)


class FooLabel(Label):
    TEST_EVENT = 'описание события'


init_logger()
structlog.get_logger('foo').log(**FooLabel.TEST_EVENT)
logging.getLogger('bar').info('простой логгер')
