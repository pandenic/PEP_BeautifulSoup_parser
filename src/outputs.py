"""Contain output settings for different modes."""
import csv
import datetime as dt
import logging
from typing import Any, List, Sequence, Tuple, Union

from prettytable import PrettyTable

from constants import BASE_DIR, DATETIME_FORMAT, RESPONSES_ENCODING, OutputMode


def control_output(
    results: Union[
        List[
            Union[
                Tuple[str],
                Tuple[str, str],
                Tuple[Tuple[str, ...], str],
                Tuple[str, Tuple[str, ...]],
            ]
        ],
        List[Tuple[str, str, str]],
        List[Union[Tuple[str, str, str], Tuple[Sequence[str], str, str]]],
    ],
    cli_args: Any,
) -> None:
    """Change output depeends on chosen method."""
    output = cli_args.output
    if output == OutputMode.PRETTY:
        pretty_output(results)
    elif output == OutputMode.FILE:
        file_output(results, cli_args)
    else:
        default_output(results)


def default_output(
    results: Union[
        List[
            Union[
                Tuple[str],
                Tuple[str, str],
                Tuple[Tuple[str, ...], str],
                Tuple[str, Tuple[str, ...]],
            ]
        ],
        List[Tuple[str, str, str]],
        List[Union[Tuple[str, str, str], Tuple[Sequence[str], str, str]]],
    ],
) -> None:
    """Describe default output."""
    for row in results:
        print(*row)


def pretty_output(
    results: Union[
        List[
            Union[
                Tuple[str],
                Tuple[str, str],
                Tuple[Tuple[str, ...], str],
                Tuple[str, Tuple[str, ...]],
            ]
        ],
        List[Tuple[str, str, str]],
        List[Union[Tuple[str, str, str], Tuple[Sequence[str], str, str]]],
    ],
) -> None:
    """Describe output using pretty table."""
    table = PrettyTable()
    table.field_names = results[0]
    table.align = 'l'
    table.add_rows(results[1:])
    print(table)


def file_output(
    results: Union[
        List[
            Union[
                Tuple[str],
                Tuple[str, str],
                Tuple[Tuple[str, ...], str],
                Tuple[str, Tuple[str, ...]],
            ]
        ],
        List[Tuple[str, str, str]],
        List[Union[Tuple[str, str, str], Tuple[Sequence[str], str, str]]],
    ],
    cli_args: Any,
) -> None:
    """Describe ouutput in file."""
    results_dir = BASE_DIR / 'results'
    results_dir.mkdir(exist_ok=True)
    parser_mode = cli_args.mode
    now = dt.datetime.now()
    now_formatted = now.strftime(DATETIME_FORMAT)
    file_name = f'{parser_mode}_{now_formatted}.csv'
    file_path = results_dir / file_name
    with open(file_path, 'w', encoding=RESPONSES_ENCODING) as f:
        writer = csv.writer(f, dialect='unix')
        writer.writerows(results)
    logging.info(f'Файл с результатами был сохранён: {file_path}')
