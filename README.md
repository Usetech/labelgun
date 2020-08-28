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

dict(**GeneralEvent.TEST_EVENT)
# {'label.category': 'GeneralEvent', 'event': 'TEST_EVENT', 'label.description': 'Проверка лога', 'level': 20}
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
# timestamp='...' level='info' logger='general' label.category='GeneralEvent' event=TEST_EVENT label.description='Проверка лога'
```

## Name clash

при использовании библиотеки нужно быть осторожным с передачей параметров логгеру:

```python
class UserEvent(Label):
    LEVEL_UP = "Обновляем уровень пользователю"

def update_user_level(**params):
    if 'level' not in params:
        params['level'] = calculate_new_level_for(user)
    logger.log(**UserEvent.LEVEL_UP, **params)
    print(f'level up!')
```

подобный код полностью перезапишет параметр level для логгера. Следовательно,
нужно следить за передачей в structlog переменных, совпадающих по имени с переменными
событий: ``label.category``, ``event``, ``label.description``, ``level``.

Имена ``event`` и ``level`` не имеют префиксов, т.к. требуются для передачи логгеру.

