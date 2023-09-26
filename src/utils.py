"""Contians upgraded functions.

Logging and exception catching are added to fiunctions.
"""
import logging
from typing import Dict, Pattern, Sequence, Union

from bs4 import NavigableString, Tag
from requests import RequestException
from requests_cache import CachedResponse, CachedSession, OriginalResponse

from constants import RESPONSES_ENCODING
from exceptions import ParserFindTagException


def get_response(
    session: CachedSession, url: Sequence[str],
) -> Union[OriginalResponse, CachedResponse]:
    """Add check if page loading error is catched and logging."""
    try:
        response = session.get(str(url))
        response.encoding = RESPONSES_ENCODING
        return response
    except RequestException:
        logging.exception(
            f'Возникла ошибка при загрузке страницы {url}',
            stack_info=True,
        )


def find_tag(
    soup: Union[Tag, NavigableString, int],
    tag: str,
    attrs: Union[Dict[str, str], Dict[str, Pattern[str]], None] = None,
) -> Union[Tag, NavigableString, int]:
    """Add check if tag hasn't been found and logging."""
    searched_tag = soup.find(tag, attrs=(attrs or {}))
    if searched_tag is None:
        error_msg = f'Не найден тег {tag} {attrs}'
        logging.error(error_msg, stack_info=True)
        raise ParserFindTagException(error_msg)
    return searched_tag
