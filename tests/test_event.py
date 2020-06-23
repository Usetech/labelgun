import logging

import pytest
import structlog

from labelgun.label import Label


class TestEvent(Label):
    A = ""
    B = "Уникальное описание", logging.WARNING
    C = "", logging.DEBUG
    D = "1", logging.CRITICAL
    E = "1", logging.ERROR


def test_event():
    class TestEvent(Label):
        TEST_EVENT = "Test description"
        TEST_EVENT_INT = 1

    assert str(TestEvent.TEST_EVENT) == "TEST_EVENT"
    assert repr(TestEvent.TEST_EVENT) == "TEST_EVENT"
    assert TestEvent.TEST_EVENT.description == "Test description"
    assert TestEvent.TEST_EVENT.level == logging.INFO
    assert TestEvent.TEST_EVENT_INT.description == "1"
    assert TestEvent.TEST_EVENT_INT.level == logging.INFO


def test_event__get_non_unique_enum_member__return_defined_value():
    # Тест проверяет, что при объявлении не уникальных значений, они не будут
    # объеденены
    assert TestEvent.A.event == "A", TestEvent.A.event
    assert TestEvent.B.event == "B", TestEvent.B.event
    assert TestEvent.C.event == "C", TestEvent.C.event
    assert TestEvent.D.event == "D", TestEvent.D.event
    assert TestEvent.E.event == "E", TestEvent.E.event


@pytest.mark.parametrize(
    "inp_event, exp_event, exp_desc, exp_level",
    (
            (TestEvent.A, "A", "", logging.INFO),
            (TestEvent.B, "B", "Уникальное описание", logging.WARNING),
            (TestEvent.C, "C", "", logging.DEBUG),
            (TestEvent.D, "D", "1", logging.CRITICAL),
            (TestEvent.E, "E", "1", logging.ERROR),
    )
)
def test_event__log_event_with_structlog__success(inp_event, exp_event, exp_desc, exp_level):
    test_logger = structlog.get_logger("test_logger")

    for method in ("log",):
        getattr(test_logger, method)(**inp_event)

    assert dict(**inp_event) == {
        "event": exp_event,
        "description": exp_desc,
        "level": exp_level
    }
    assert inp_event.level == exp_level


@pytest.mark.parametrize(
    "inp_event, exp_dict",
    (
            (TestEvent.A, {"event": "A", "description": "", "level": logging.INFO}),
            (TestEvent.B, {"event": "B", "description": "Уникальное описание", "level": logging.WARNING}),
            (TestEvent.C, {"event": "C", "description": "", "level": logging.DEBUG}),
            (TestEvent.D, {"event": "D", "description": "1", "level": logging.CRITICAL}),
            (TestEvent.E, {"event": "E", "description": "1", "level": logging.ERROR}),
    )
)
def test_event__unpacking_value__success(inp_event, exp_dict):
    assert dict(**inp_event) == exp_dict
