import logging


def dict_msg_processor(logger: logging.Logger, name: str, event_dict: dict):
    """Позволяет переложить конвертацию данных в строку на Formatter библиотеки logging. Данная возможность полезна при
    внедрении structlog в приложение, где часть логов уже пишется при помощи библиотеки logging.

    P.S. Иными словами, данный процессор служит заменой для structlog.dev.ConsoleRenderer или
    structlog.processors.JSONRenderer и позволяет сказать библиотеке structlog, что данные, которые необходимо
    залогировать сформированы и можно передать их дальше.

    Данный процессор должен быть ВСЕГДА ПОСЛЕДНИМ в списке процессоров.

    """
    return (event_dict,), {}


def convert_event_dict_to_str_processor(logger: logging.Logger, name: str, event_dict: dict):
    """Выполняет конвертацию всех данных в строки.

    Данный процессор помогает избежать проблемы, если логи вашего приложения загружаются в elasticsearch для анализа.

    Пример решаемой проблемы:
    Логи с нескольких сервисов собираются в одном индексе elasticsearch и каждый из этих сервисов в логах использует
    переменную с одинаковым именем, но содержание у них разное. На пример в одном сервисе логируется user_id=1, а в
    другом user_id='4v43gbv33'. В этом случае в elasticsearch попадут логи только того сервиса, сообщение от которого
    будет обработано раньше. Это происходит потому, что индекс в elasticsearch типизирован и одно поле не может хранить
    данные различных типов.

    """
    for param_key, param_value in event_dict.items():
        event_dict[param_key] = str(param_value)

    return event_dict
