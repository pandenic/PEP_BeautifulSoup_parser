"""Contians upgraded functions.

Logging and exception catching are added to fiunctions.
"""
import logging
from typing import Any, Dict, Pattern, Union

from requests import RequestException

from exceptions import ParserFindTagException


def get_response(session: Any, url: str) -> Any:
    """Add check if page loading error is catched and logging."""
    try:
        response = session.get(url)
        response.encoding = 'utf-8'
        return response
    except RequestException:
        logging.exception(
            f'Возникла ошибка при загрузке страницы {url}',
            stack_info=True,
        )


def find_tag(
    soup: Any,
    tag: str,
    attrs: Union[Dict[str, str], Dict[str, Pattern[str]], None] = None,
) -> Any:
    """Add check if tag hasn't been found and logging."""
    searched_tag = soup.find(tag, attrs=(attrs or {}))
    if searched_tag is None:
        error_msg = f'Не найден тег {tag} {attrs}'
        logging.error(error_msg, stack_info=True)
        raise ParserFindTagException(error_msg)
    return searched_tag
