import logging
from collections import OrderedDict
from logging import LogRecord

from pythonjsonlogger import jsonlogger


class StructlogJsonFormatter(jsonlogger.JsonFormatter):
    """Formatter для стандартного python логгера logging. Позволяет конфигурировать себя при помощи списка
    процессоров от structlog и выполняет логирование в json формате."""

    _cache_loggers = {}

    def __init__(self, fmt=None, *args, proc=tuple(), **kwargs):
        super().__init__(fmt, *args, **kwargs)
        self._structlog_processors = proc

    def set_structlog_processors(self, proc: list):
        self._structlog_processors = proc

    def _get_logger(self, name: str):
        log = StructlogJsonFormatter._cache_loggers.get(name)

        if log is None:
            log = logging.getLogger(name)
            StructlogJsonFormatter._cache_loggers[name] = log

        return log

    def add_fields(self, log_record: OrderedDict, record: LogRecord, message_dict: dict):
        """Выполяет преобразование стандартного сообщения в формат structlog"""
        super().add_fields(log_record, record, message_dict)

        msg = log_record.pop('message', '')
        event_dict = {'event': msg}

        if isinstance(record.msg, str):
            log_record['event'] = msg
            event_dict = log_record

        logger = self._get_logger(record.name)
        level = record.levelname.lower()

        for proc in self._structlog_processors:
            event_dict = proc(logger, level, event_dict)
