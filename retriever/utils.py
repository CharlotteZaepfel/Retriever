"""Utils."""

import datetime
from typing import Callable

from logger import set_logger

log = set_logger(__name__)


def sec2str_converter(duration_in_sec: float) -> str:
    """Converts a number of sec into a human-friendly format.

    Args:
        duration_in_sec: A number of sec.

    Returns:
        A readable duration of the number of sec."""
    if duration_in_sec < 60:
        return f"{duration_in_sec:.2f}sec"
    elif duration_in_sec > 3600:
        duration_in_h = duration_in_sec / 3600
        return f"{duration_in_h:.2f}h"
    else:
        duration_in_min = duration_in_sec / 60
        return f"{duration_in_min:.2f}min"


def timekeeper(process: Callable) -> Callable:
    def wrapped_function(*args, **kwargs):
        before = datetime.datetime.now()
        result = process(*args, **kwargs)
        after = datetime.datetime.now()
        timelapse = after - before
        duration_in_sec = timelapse.total_seconds()
        duration = sec2str_converter(duration_in_sec)
        log.info(f"{process.__name__!r} done in {duration}")
        return result

    return wrapped_function
