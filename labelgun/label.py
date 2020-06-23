import logging

from aenum import Enum, NoAlias

_EVENT_PROPERTIES = ["event", "description", "level"]
_EVENT_MEMBER_VALUE = {"description": 0, "level": 1}
_DEFAULT_LOG_LEVEL = logging.INFO


class Label(Enum):
    """Базовый класс для создания классов событий.

    Структура логируемых событий, состоит из:
        - имени события (event),
        - описания события (description) в свободной форме
        - уровня логирования (level) (по умолчанию используетя уровень INFO).

    Данные могуть быть представлены как словарь {"event": "TEST_EVENT", "description": "описание", "level": 20}.
    """

    _settings_ = NoAlias

    @property
    def event(self):
        return str(self)

    @property
    def description(self):
        if isinstance(self._value_, tuple):
            desc = str(self._value_[_EVENT_MEMBER_VALUE["description"]])
        else:
            desc = str(self._value_)

        return desc

    @property
    def level(self):
        level = _DEFAULT_LOG_LEVEL
        if isinstance(self._value_, tuple):
            try:
                level = self._value_[_EVENT_MEMBER_VALUE["level"]]
            except IndexError:
                level = _DEFAULT_LOG_LEVEL

        return level

    def keys(self):
        """Позволяет распаковывать события как словарь"""
        return _EVENT_PROPERTIES

    def __str__(self):
        return self._name_

    def __repr__(self):
        return self.__str__()

    def __getitem__(self, key):
        """Позволяет распаковывать события как словарь"""
        if key not in _EVENT_PROPERTIES:
            raise KeyError
        return getattr(self, key)