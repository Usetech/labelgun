import logging
import logging.handlers

import structlog
from labelgun.integrations.logging_utils import StructlogJsonFormatter
from labelgun.integrations.structlog_utils import (
    dict_msg_processor,
    convert_event_dict_to_str_processor,
)


# Порядок процессоров не менять без явной необходимости
json_processors = [
    structlog.stdlib.filter_by_level,
    structlog.processors.TimeStamper(fmt="iso"),
    structlog.stdlib.add_logger_name,
    structlog.stdlib.add_log_level,
    structlog.stdlib.PositionalArgumentsFormatter(),
    structlog.processors.StackInfoRenderer(),
    structlog.processors.UnicodeDecoder(),
    structlog.processors.format_exc_info,
    convert_event_dict_to_str_processor,
    # Данный процессор позволяет переложить формирование логируемой строки на Formatter библиотеки logging
    dict_msg_processor,
]

simple_processors = [
    structlog.stdlib.filter_by_level,
    structlog.stdlib.PositionalArgumentsFormatter(),
    structlog.processors.StackInfoRenderer(),
    structlog.processors.UnicodeDecoder(),
    structlog.processors.format_exc_info,
    structlog.dev.ConsoleRenderer(),
]


json_formatter = StructlogJsonFormatter(json_ensure_ascii=False)
simple_formatter = logging.Formatter(
    '%(levelname)s %(asctime)s - %(module)s:%(lineno)d - %(message)s'
)


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


def init_logger(log_mod: str):
    if log_mod == 'json':
        processors = json_processors
        formatter = json_formatter
        formatter.set_structlog_processors(processors)
    else:
        processors = simple_processors
        formatter = simple_formatter

    _init_logging(formatter)
    _init_structlog(processors)
