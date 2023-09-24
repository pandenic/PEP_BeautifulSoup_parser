"""Describe main functions of bs4 app."""
import logging
import re
from typing import Any, List, Tuple, Union
from urllib.parse import urljoin

import requests_cache
from bs4 import BeautifulSoup
from tqdm import tqdm

from configs import configure_argument_parser, configure_logging
from constants import (BASE_DIR, DOCS_DOWNLOAD_URL, DOWNLOAD_FILE_NAME_PATTERN,
                       EXPECTED_STATUS, MAIN_DOC_URL, PARSING_MODULE, PEP_URL,
                       VERSION_STATUS_PATTERN, WHATS_NEW_URL, HTMLTags)
from outputs import control_output
from utils import find_tag, get_response


def whats_new(session: Any) -> Union[List[Tuple], None]:
    """
    Collect info for different versions of python.

    "What's new" topics and links.
    """
    response = get_response(session, WHATS_NEW_URL)
    if response is None:
        return

    soup = BeautifulSoup(response.text, features=PARSING_MODULE)

    main_div = find_tag(
        soup, HTMLTags.SECTION, attrs={'id': 'what-s-new-in-python'},
    )
    div_with_ul = find_tag(
        main_div, HTMLTags.DIV, attrs={'class': 'toctree-wrapper'},
    )
    sections_by_python = tqdm(
        div_with_ul.find_all(HTMLTags.LI, attrs={'class': 'toctree-l1'}),
    )

    results = [('Ссылка на статью', 'Заголовок', 'Редактор, Автор')]
    for section in tqdm(sections_by_python):
        version_a_tag = find_tag(section, HTMLTags.A)
        version_link = urljoin(WHATS_NEW_URL, version_a_tag['href'])

        response = get_response(session, version_link)
        if response is None:
            continue

        soup = BeautifulSoup(response.text, PARSING_MODULE)
        h1 = find_tag(soup, HTMLTags.H1)
        dl = find_tag(soup, HTMLTags.DL)
        dl_text = dl.text.replace('\n', ' ')

        results.append((version_link, h1.text, dl_text))

    return results


def latest_versions(session: Any) -> Union[List[Tuple], None]:
    """Collect links on docs for different versions of python."""
    response = get_response(session, MAIN_DOC_URL)
    if response is None:
        return

    soup = BeautifulSoup(response.text, features=PARSING_MODULE)
    sidebar = find_tag(
        soup, HTMLTags.DIV, attrs={'class': 'sphinxsidebarwrapper'},
    )
    ul_tags = sidebar.find_all(HTMLTags.UL)

    for ul in ul_tags:
        if 'All versions' in ul.text:
            a_tags = ul.find_all(HTMLTags.A)
            break
    else:
        raise Exception('Nothing has been found')

    results = [('Ссылка на документацию', 'Версия', 'Статус')]

    for a_tag in a_tags:
        link = a_tag['href']
        re_search = re.search(VERSION_STATUS_PATTERN, a_tag.text)
        if not re_search:
            version, status = a_tag.text, ''
        else:
            version, status = re_search.groups()
        results.append((link, version, status))

    return results


def download(session: Any) -> None:
    """Download docs for the latest version of python."""
    response = get_response(session, DOCS_DOWNLOAD_URL)
    if response is None:
        return

    soup = BeautifulSoup(response.text, features=PARSING_MODULE)
    table = find_tag(soup, HTMLTags.TABLE, attrs={'class': 'docutils'})
    pdf_a4_tag = find_tag(
        table,
        HTMLTags.A,
        attrs={'href': re.compile(DOWNLOAD_FILE_NAME_PATTERN)},
    )
    file_url = urljoin(DOCS_DOWNLOAD_URL, pdf_a4_tag['href'])

    filename = file_url.split('/')[-1]
    downloads_dir = BASE_DIR / 'downloads'
    downloads_dir.mkdir(exist_ok=True)
    filepath = downloads_dir / filename

    response = session.get(file_url)
    with open(filepath, 'wb') as file:
        file.write(response.content)
    logging.info(f'Архив был загружен и сохранён: {filepath}')


def pep(session: Any) -> Union[List[Tuple], None]:
    """
    Count quantity of PEPs divided by status.

    Print inappropriate statuses.
    """
    response = get_response(session, PEP_URL)
    if response is None:
        return

    soup = BeautifulSoup(response.text, features=PARSING_MODULE)

    main_div = find_tag(
        soup, HTMLTags.SECTION, attrs={'id': 'numerical-index'},
    )
    tbody = find_tag(main_div, HTMLTags.TBODY)
    pep_list = tqdm(tbody.find_all(HTMLTags.TR))

    pep_quantity = dict.fromkeys(EXPECTED_STATUS.values(), 0)
    result = [('Статус', 'Количество')]
    mismatched_statuses = [('Несовпадающие статусы:',)]

    for pep_entity in pep_list:
        pep_link = urljoin(PEP_URL, pep_entity.a['href'])
        response = get_response(session, pep_link)
        if response is None:
            continue

        soup = BeautifulSoup(response.text, PARSING_MODULE)
        dl_tag = find_tag(
            soup,
            HTMLTags.DL,
            attrs={'class': 'rfc2822 field-list simple'},
        )
        status_tag = find_tag(
            dl_tag,
            HTMLTags.ABBR,
        )
        status = status_tag.text
        table_status_letter = find_tag(pep_entity, HTMLTags.ABBR).text[1:]

        if status in EXPECTED_STATUS[table_status_letter]:
            pep_quantity[EXPECTED_STATUS[table_status_letter]] += 1
            continue
        mismatched_statuses.append((pep_link,))
        mismatched_statuses.append(('Статус в карточке:', status))
        mismatched_statuses.append(
            ('Ожидаемые статусы:', EXPECTED_STATUS[table_status_letter]),
        )

    result += [(status, quantity) for status, quantity in pep_quantity.items()]
    result += [('Total', sum(pep_quantity.values()))]
    result += mismatched_statuses
    return result


MODE_TO_FUNCTION = {
    'whats-new': whats_new,
    'latest-versions': latest_versions,
    'download': download,
    'pep': pep,
}


def main() -> None:
    """Start the parser depending on the mode. Maintain logging."""
    configure_logging()
    logging.info('Парсер запущен!')

    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()
    logging.info(f'Аргументы командной строки: {args}')

    session = requests_cache.CachedSession()
    if args.clear_cache:
        session.cache.clear()

    parser_mode = args.mode
    results = MODE_TO_FUNCTION[parser_mode](session)

    if results is not None:
        control_output(results, args)
    logging.info('Парсер завершил работу.')


if __name__ == '__main__':
    main()
