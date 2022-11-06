import logging
from typing import Union

LOG_FORMAT = "%(log_color)s%(message)s"
LOG_COLORS = {
    "DEBUG": "cyan",
    "INFO": "green",
    "WARNING": "yellow",
    "ERROR": "red",
    "CRITICAL": "red,bg_white",
}


def setup_logging(level: Union[int, str] = logging.WARNING):
    log_handeler = logging.StreamHandler()

    # Try to add a colorlog formatter
    try:
        import colorlog

        log_handeler.setFormatter(
            colorlog.ColoredFormatter(fmt=LOG_FORMAT, log_colors=LOG_COLORS)
        )
    except:
        pass

    logging.basicConfig(level=level, handlers=[log_handeler])
