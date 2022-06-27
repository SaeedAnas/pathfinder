from datetime import datetime
import numpy as np

"""
    Datetime utils.
"""

format = '%Y-%m-%d'

def parse_date(date):
    if date is np.nan:
        return datetime.now()

    return datetime.strptime(date, format)

def time_between(start, end):
    start = parse_date(start)
    end = parse_date(end)
    return (end - start).days

