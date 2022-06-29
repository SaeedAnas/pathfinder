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

def days_to_duration(number_of_days):
    # Calculating years
    years = number_of_days // 365

    # Calculating months
    months = (number_of_days - years *365) // 30

    # Calculating days
    days = (number_of_days - years * 365 - months*30)

    result = []

    if years > 0:
        result.append(f'{int(years)} years')
    if months > 0:
        result.append(f'{int(months)} months')
    if days > 0:
        result.append(f'{int(days)} days')

    return ', '.join(result)

