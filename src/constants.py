"""Contain constants for bs4 parser app."""
from enum import Enum
from pathlib import Path
from urllib.parse import urljoin

MAIN_DOC_URL = 'https://docs.python.org/3/'
WHATS_NEW_URL = urljoin(MAIN_DOC_URL, 'whatsnew/')
DOCS_DOWNLOAD_URL = urljoin(MAIN_DOC_URL, 'download.html')
PEP_URL = 'https://peps.python.org/'

BASE_DIR = Path(__file__).parent
DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'
LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'
LOG_DT_FORMAT = '%d.%m.%Y %H:%M:%S'

PARSING_MODULE = 'lxml'
DOWNLOAD_FILE_NAME_PATTERN = r'.+pdf-a4\.zip$'
VERSION_STATUS_PATTERN = (
    r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'
)  # version and status pattern for latest version mode

EXPECTED_STATUS = {
    'A': ('Active', 'Accepted'),
    'D': ('Deferred',),
    'F': ('Final',),
    'P': ('Provisional',),
    'R': ('Rejected',),
    'S': ('Superseded',),
    'W': ('Withdrawn',),
    '': ('Draft', 'Active'),
}


class HTMLTags(str, Enum):
    """Contains HTML tags for persing."""

    SECTION = 'section'
    TABLE = 'table'
    TBODY = 'tbody'
    ABBR = 'abbr'
    DIV = 'div'
    LI = 'li'
    UL = 'ul'
    DL = 'dl'
    H1 = 'h1'
    TR = 'tr'
    A = 'a'


class OutputMode(str, Enum):
    """Contains modes for output settings."""

    PRETTY = 'pretty'
    FILE = 'file'
