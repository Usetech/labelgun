import copy
import logging
from decimal import Decimal
from logging import LogRecord
from uuid import UUID

import pytest
import structlog
from freezegun import freeze_time

from labelgun.integrations.logging_utils import StructlogJsonFormatter
from labelgun.integrations.structlog_utils import dict_msg_processor, convert_event_dict_to_str_processor


@pytest.fixture
@freeze_time("2012-01-14")
def processors():
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
def logger():
    logger = logging.getLogger('for_test')
    logger.setLevel(logging.INFO)
    return logger


@pytest.fixture
def event_dict(logger):
    return {
        'label.category': 'FooLabel',
        'label.description': 'описание тестового евента',
        'event': 'TEST_EVENT',
        'timestamp': '2012-01-14T00:00:00Z',
        'logger': logger.name,
        'level': logger.level
    }


@pytest.fixture
def log_record(logger):
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


class TestStructlogJsonFormatter:

    @freeze_time("2012-01-14")
    def test_format__build_log_record_for_logging__success(self, processors, log_record):
        formatter = StructlogJsonFormatter()
        formatter.set_structlog_processors(processors)
        formatted_log_record = formatter.format(log_record)

        assert formatted_log_record == (
            '{"event": "msg", "timestamp": "2012-01-14T00:00:00Z", "logger": "for_test", "level": "info"}'
        )

    @freeze_time("2012-01-14")
    def test_format__build_log_record_for_structlog__success(self, processors, logger, event_dict, log_record):
        del log_record.message
        log_record.msg = event_dict

        formatter = StructlogJsonFormatter(json_ensure_ascii=False)
        formatter.set_structlog_processors(processors)
        formatted_log_record = formatter.format(log_record)

        assert formatted_log_record == (
            '{"label.category": "FooLabel", "label.description": "описание тестового евента", "event": "TEST_EVENT", '
            '"timestamp": "2012-01-14T00:00:00Z", "logger": "for_test", "level": 20}'
        )


def test_convert_event_dict_to_str_processor__convert_to_str__success(logger, event_dict):
    source_event_dict = copy.deepcopy(event_dict)
    source_event_dict.update({
        'id_user': 1245,
        'salary': Decimal('564535'),
        'person_data': {'id': 1, 'name': 'Name', 'surname': 'Surname'},
        'survey_id': UUID('b5b72996-912c-44eb-814c-93f061db93f1', version=4),
        'sample_id_set': {1, 2, 3},
    })
    expected_event_dict = copy.deepcopy(event_dict)
    expected_event_dict.update(
        {
            'level': str(logger.level),
            'id_user': '1245',
            'salary': '564535',
            'person_data': {'id': 1, 'name': 'Name', 'surname': 'Surname'},
            'survey_id': 'b5b72996-912c-44eb-814c-93f061db93f1',
            'sample_id_set': {1, 2, 3},
        }
    )

    res_event_dict = convert_event_dict_to_str_processor(logger, '', source_event_dict)

    assert res_event_dict == expected_event_dict


def test_convert_event_dict_to_str_processor__use_with_other_processors__success(
        processors, logger, log_record, event_dict
):
    processors.insert(-1, convert_event_dict_to_str_processor)
    source_event_dict = copy.deepcopy(event_dict)
    source_event_dict.update({
        'id_user': 1245,
        'salary': Decimal('564535'),
        'person_data': {'id': 1, 'name': 'Name', 'surname': 'Surname'},
        'survey_id': UUID('b5b72996-912c-44eb-814c-93f061db93f1', version=4),
        'sample_id_set': {1, 2, 3},
    })
    del log_record.message
    log_record.msg = source_event_dict

    formatter = StructlogJsonFormatter(json_ensure_ascii=False)
    formatter.set_structlog_processors(processors)
    formatted_log_record = formatter.format(log_record)

    assert formatted_log_record == (
        '{"label.category": "FooLabel", "label.description": "описание тестового евента", "event": "TEST_EVENT", '
        '"timestamp": "2012-01-14T00:00:00Z", "logger": "for_test", "level": 20, "id_user": 1245, "salary": "564535", '
        '"person_data": {"id": 1, "name": "Name", "surname": "Surname"}, '
        '"survey_id": "b5b72996-912c-44eb-814c-93f061db93f1", "sample_id_set": "{1, 2, 3}"}'
    )
