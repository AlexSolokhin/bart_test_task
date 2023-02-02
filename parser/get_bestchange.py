import requests
from typing import Optional
from config import BASE_URL, parser_logger


def get_page(page_path: str) -> Optional[str]:
    """
    Запрос страницы с сайта bestchange.ru

    :param page_path: путь до страницы
    :type page_path: str
    :return: html-код страницы или ничего в случае ошибки
    :rtype: Optional[str]
    """

    full_url = BASE_URL + page_path
    response = requests.get(full_url, timeout=5)
    if response.status_code == 200:
        return response.text
    else:
        parser_logger.error(f'Не удалось установить соединение со страницей. Статус ответа: {response.status_code}')
        raise requests.exceptions.ConnectionError
