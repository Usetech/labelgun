import logging


def dict_msg_processor(logger: logging.Logger, name: str, event_dict: dict):
    """Преобразовывает словарь полученный в результате работы предыдущих процессоров в формат необходимый для structlog.
    Данный процессор необходим при использовании StructlogJsonFormatter.

    """
    return (event_dict,), {}


def convert_event_dict_to_str_processor(logger: logging.Logger, name: str, event_dict: dict):
    """Выполняет конвертацию "примитивных" типов в строки. Под примитивами понимаются числа, uuid, различные обертки
    позволяющие выполнять точные расчеты (например Decimal).

    Данный процессор полезен если логируемые сообщения в дальнейшем будут загружаться в ElasticSearch, который
    автоматически генерирует индекс, в котором под одним ключем не могут храниться данные различных типов.
    Пример:
    Логи могут собираться с 2 разных сервисов и один сервис может логировать user_id=1, а другой user_id='4v43gbv33'.
    Если данный процессор не будет использоваться, то в elasticserch попадут логи только 1 из сервисов (сообщение
    которого будет обработано раньше).

    """
    for param_key, param_value in event_dict.items():
        if not isinstance(param_value, str):
            try:
                iter(param_value)
            except TypeError:
                # Если сработало исключение, значит сейчас обратывается ни какая-то коллекция, а простой тип данных.
                event_dict[param_key] = str(param_value)

    return event_dict
