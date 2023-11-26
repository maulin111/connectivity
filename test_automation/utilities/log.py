import sys
import os
import logging.config
from datetime import datetime
from enum import IntEnum

LOG_FOLDER_NAME = datetime.now().strftime("%Y%m%d-%H%M")

_TO_UNICODE_TYPES = (str, type(None))

class LogColor(IntEnum):
    BLACK = 0
    RED = 1
    GREEN = 2
    YELLOW = 3
    BLUE = 4
    MAGENTA = 5
    CYAN = 6
    WHITE = 7
    def apply(self, msg: str):
        return _COLOR_SEQ % (30 + self.value) + msg + _RESET_SEQ

_RESET_SEQ = "\033[0m"
_COLOR_SEQ = "\033[1;%dm"
_BOLD_SEQ = "\033[1m"


def formatter_message(message, use_color=True):
    if use_color:
        message = message.replace("$RESET", _RESET_SEQ).replace("$BOLD", _BOLD_SEQ)
    else:
        message = message.replace("$RESET", "").replace("$BOLD", "")
    return message

HOME = 'USERPROFILE' if sys.platform == 'win32' else 'HOME'
LOG_BASE_FOLDER = f"{os.environ[HOME]}/test_logs/{LOG_FOLDER_NAME}"

if not os.path.exists(LOG_BASE_FOLDER):
    try:
        os.makedirs(LOG_BASE_FOLDER)
    except IOError as ie:
        print(ie.message)
        sys.exit(1)


def to_unicode(value):
    if isinstance(value, _TO_UNICODE_TYPES):
        return value
    if not isinstance(value, bytes):
        raise TypeError(f"Expected bytes, unicode, or None; got {type(value)}")
    return value.decode("utf-8")


def _safe_unicode(message):
    try:
        return to_unicode(message)
    except UnicodeDecodeError:
        return repr(message)


class LogFormatter(logging.Formatter):
    """
    Default Log formatter
    * Timestamps on every log line.
    * Robust against str/bytes encoding problems.
    """
    _FORMAT = '$BOLD[$RESET%(asctime)s %(levelname)-8s $BOLD%(module)16s:%(lineno)3d]$RESET %(message)s'
    DEFAULT_FORMAT = formatter_message(_FORMAT, False)
    DEFAULT_DATE_FORMAT = '%b-%d %H:%M:%S'
    USE_COLOR = False

    def format(self, record):
        try:
            message = record.getMessage()
            if isinstance(message, str):
                message = message.replace('\\n', "\n")
            else:
                message = str(message).replace('\\n', '\n')
            record.msg = _safe_unicode(message)

        except AssertionError as exception:
            record.msg = f"Bad message ({exception!r}): {record.__dict__}"

        formated_record = super().format(record)
        return formated_record


class ColorLogFormatter(LogFormatter):
    DEFAULT_FORMAT = formatter_message(LogFormatter._FORMAT, True)
    USE_COLOR = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'simple': {
            '()': LogFormatter,
            'format': LogFormatter.DEFAULT_FORMAT,
            "datefmt": LogFormatter.DEFAULT_DATE_FORMAT
        },
        'simple_color': {
            '()': ColorLogFormatter,
            'format': ColorLogFormatter.DEFAULT_FORMAT,
            "datefmt": LogFormatter.DEFAULT_DATE_FORMAT
        }
    },
    'handlers': {
        'project_debug':{
            'level':"DEBUG",
            'class':'logging.handlers.RotatingFileHandler',
            'formatter': 'simple',
            'maxBytes': 1000000,
            'backupCount': 100,
            'encoding': 'utf-8',
            'filename': f'{LOG_BASE_FOLDER}/project_tests_debug.log'
        },
        'project_info': {
            'level': "INFO",
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'simple',
            'maxBytes': 1000000,
            'backupCount': 100,
            'encoding': 'utf-8',
            'filename': f'{LOG_BASE_FOLDER}/project_tests_info.log'
        },
        'console_debug': {
            'level': "DEBUG",
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'stream': 'ext://sys.stdout'
        }
    },
    'loggers': {
        'project_logger': {
            'handlers': ['project_info', 'project_debug', 'console_debug'],
            'level': "DEBUG"
        },
    }
}

logging.config.dictConfig(LOGGING)

def get_project_logger():
    return logging.getLogger("project_logger")

logger = get_project_logger()
