import logging

from labelgun.label import Label


class CalcLabel(Label):
    RECEIVED_REQUEST_FOR_ADDITION = 'Получен запрос на сложение'

    REQUEST_FOR_ADDITION_CONTAINS_NOT_VALID_ARGS = 'Запрос на сложение содержит невалидные аргументы', logging.WARNING
