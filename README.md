labelgun
========

labelgun - это библиотека позволяющая в декларативном стиле объявить все события, которые используются в системе.
 

## Установка

- Установка из исходников
    
    ```
    python ./setup.py install
    ```

- Установка из git репозитория
    
    ```
    pip install git+https://gitlab.usetech.ru/pub/labelgun.git@<tag>
    ```
    
    То есть если вы хотите установить версию 0.1.0, то необходимо выполнить
    
    ```
    pip install git+https://gitlab.usetech.ru/pub/labelgun.git@0.1.0
    ```


## Пример использования

```python
from labelgun.label import Label


class GeneralEvent(Label):
    TEST_EVENT = "Проверка лога"

print(**GeneralEvent.TEST_EVENT)
# {'event': 'TEST_EVENT', 'description': 'Проверка лога', 'level': 20}
```

Пример использования вместе с библиотекой `structlog`

```python
import structlog
from labelgun.label import Label

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(ensure_ascii=False),
    ],
    context_class=structlog.threadlocal.wrap_dict(dict),
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)
logger = structlog.get_logger("general")


class GeneralEvent(Label):
    TEST_EVENT = "Проверка лога"

logger.info(**GeneralEvent.TEST_EVENT)
# timestamp='...' level='info' logger='general' event=TEST_EVENT description='Проверка лога'
```
