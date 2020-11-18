import logging
from logging import LogRecord

import pytest
import structlog
from freezegun import freeze_time

from labelgun.integrations.logging_utils import StructlogJsonFormatter
from labelgun.integrations.structlog_utils import dict_msg_processor


class TestStructlogJsonFormatter:

    @pytest.fixture
    @freeze_time("2012-01-14")
    def processors(self):
        return [
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

    @pytest.fixture
    def logger(self):
        logger = logging.getLogger('for_test')
        logger.setLevel(logging.INFO)
        return logger

    @pytest.fixture
    def log_record(self, logger):
        message = 'msg'
        record = LogRecord(
            name=logger.name,
            level=logger.level,
            pathname='/some/path',
            lineno=10,
            msg=message,
            args=tuple(),
            exc_info=None,
        )
        record.message = message
        return record

    @freeze_time("2012-01-14")
    def test_format__build_log_record_for_logging__success(self, processors, log_record):
        formatter = StructlogJsonFormatter()
        formatter.set_structlog_processors(processors)
        formatted_log_record = formatter.format(log_record)

        assert formatted_log_record == (
            '{"event": "msg", "timestamp": "2012-01-14T00:00:00Z", "logger": "for_test", "level": "info"}'
        )

    @freeze_time("2012-01-14")
    def test_format__build_log_record_for_structlog__success(self, processors, logger, log_record):
        del log_record.message
        log_record.msg = {
            'label.category': 'FooLabel',
            'label.description': 'описание тестового евента',
            'event': 'TEST_EVENT',
            'timestamp': '2012-01-14T00:00:00Z',
            'logger': logger.name,
            'level': logger.level
        }

        formatter = StructlogJsonFormatter(json_ensure_ascii=False)
        formatter.set_structlog_processors(processors)
        formatted_log_record = formatter.format(log_record)

        assert formatted_log_record == (
            '{"label.category": "FooLabel", "label.description": "описание тестового евента", "event": "TEST_EVENT", '
            '"timestamp": "2012-01-14T00:00:00Z", "logger": "for_test", "level": 20}'
        )
