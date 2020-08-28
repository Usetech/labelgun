import logging

import pytest
import structlog

from labelgun.label import Label


class ATestEvent(Label):
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
    assert ATestEvent.A.event == "A", ATestEvent.A.event
    assert ATestEvent.B.event == "B", ATestEvent.B.event
    assert ATestEvent.C.event == "C", ATestEvent.C.event
    assert ATestEvent.D.event == "D", ATestEvent.D.event
    assert ATestEvent.E.event == "E", ATestEvent.E.event


@pytest.mark.parametrize(
    "inp_event, exp_event, exp_desc, exp_level",
    (
            (ATestEvent.A, "A", "", logging.INFO),
            (ATestEvent.B, "B", "Уникальное описание", logging.WARNING),
            (ATestEvent.C, "C", "", logging.DEBUG),
            (ATestEvent.D, "D", "1", logging.CRITICAL),
            (ATestEvent.E, "E", "1", logging.ERROR),
    )
)
def test_event__log_event_with_structlog__success(inp_event, exp_event, exp_desc, exp_level):
    test_logger = structlog.get_logger("test_logger")

    for method in ("log",):
        getattr(test_logger, method)(**inp_event)

    assert dict(**inp_event) == {
        "label.category": "ATestEvent",
        "event": exp_event,
        "label.description": exp_desc,
        "level": exp_level
    }
    assert inp_event.level == exp_level


@pytest.mark.parametrize(
    "inp_event, exp_dict",
    (
        (ATestEvent.A, {"label.category": "ATestEvent", "event": "A", "label.description": "", "level": logging.INFO}),
        (ATestEvent.B, {"label.category": "ATestEvent", "event": "B", "label.description": "Уникальное описание", "level": logging.WARNING}),
        (ATestEvent.C, {"label.category": "ATestEvent", "event": "C", "label.description": "", "level": logging.DEBUG}),
        (ATestEvent.D, {"label.category": "ATestEvent", "event": "D", "label.description": "1", "level": logging.CRITICAL}),
        (ATestEvent.E, {"label.category": "ATestEvent", "event": "E", "label.description": "1", "level": logging.ERROR}),
    )
)
def test_event__unpacking_value__success(inp_event, exp_dict):
    assert dict(**inp_event) == exp_dict
