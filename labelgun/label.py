import logging

from aenum import Enum, NoAlias

_EVENT_PROPERTIES = ["label.category", "event", "label.description", "level"]
_EVENT_MEMBER_VALUE = {"description": 0, "level": 1}
_DEFAULT_LOG_LEVEL = logging.INFO


class Label(Enum):
    """Базовый класс для создания классов событий.

    Структура логируемых событий, состоит из:
        - имени категории события (category),
        - имени события (event),
        - описания события (description) в свободной форме
        - уровня логирования (level) (по умолчанию используетя уровень INFO).

    Данные могуть быть представлены как словарь:
    {"label.category": "SomeClass", "label.event": "TEST_EVENT", "label.description": "описание", "level": 20}.
    """

    _settings_ = NoAlias

    @property
    def event_properties(self):
        """Можно переопределить в дочерних классах, чтобы изменить набор возвращаемых ключей."""
        return _EVENT_PROPERTIES

    @property
    def category(self):
        return self.__class__.__name__

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
        return self.event_properties

    def __str__(self):
        return self._name_

    def __repr__(self):
        return self.__str__()

    def __getitem__(self, key):
        """Позволяет распаковывать события как словарь"""
        if key not in self.event_properties:
            raise KeyError
        key = key.replace('label.', '')
        return getattr(self, key)

