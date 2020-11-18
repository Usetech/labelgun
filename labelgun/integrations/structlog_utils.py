import logging


def dict_msg_processor(logger: logging.Logger, name: str, event_dict: dict):
    """Преобразовывает словарь полученный в результате работы предыдущих процессоров в формат необходимый для structlog.
    Данный процессор необходим при использовании StructlogJsonFormatter.

    """
    return (event_dict,), {}
