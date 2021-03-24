import logging

from labelgun.label import Label


class PriceListLabel(Label):
    START_DOWNLOAD_PRICE_LIST = 'Запущено скачивание прайс листов'

    DOWNLOAD_PRICE_LIST_ERROR = 'Во время скачивание прайс листов возникла ошибка', logging.ERROR
