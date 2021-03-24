import random
import time
from logging import getLogger

from structlog import get_logger

from logger import init_logger
from logs import PriceListLabel

logger = get_logger()
old_logger = getLogger()


def _download():
    if random.randint(0, 1):
        time.sleep(2)
    else:
        raise TimeoutError('Download timeout error')


def download_price_list():
    logger.log(**PriceListLabel.START_DOWNLOAD_PRICE_LIST)

    try:
        _download()
    except Exception:
        logger.log(**PriceListLabel.DOWNLOAD_PRICE_LIST_ERROR, exc_info=True)

    # Демонстрирует как будут выглядеть логи от legacy кода
    old_logger.info('Скачивание прайс листов завершено')


if __name__ == '__main__':
    # Запускаем инициализацию подсистемы логирования. В процессе инициализация система будет настроена так, чтобы
    # логи от legacy кода и логи сделанные при помощи labelgun и struclog имели максимально близкий формат.
    # + показано как можно выбирать в каком формате логировать, в виде json строки или просто plane text.
    init_logger('json')
    download_price_list()
