from datetime import datetime
from textwrap import wrap

from dateutil.relativedelta import relativedelta


def get_prev_month(months: int):
    now = datetime.now()
    delta = relativedelta(months=months)
    return now - delta


def divide_to_chunks(string: str, length: int):
    return wrap(string, length)
