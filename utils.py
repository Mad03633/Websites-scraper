import logging
import re
from datetime import datetime
from urllib.parse import urlparse
from typing import Optional

# Logging
def log_error(message):
    logging.error(message)
    print(message)

# Extractind domain from URL
def extract_domain(url):
    return urlparse(url).netloc

# Extracting date and time from text
def extract_date(text: str) -> Optional[datetime]:
    date = None
    regex_delimiter = r"[-:\/.,\s]"
    regex_day = r"((?:[0-2]?\d)|(?:3[01]))"
    regex_year = r"((?:1\d{3})|(?:2\d{3}))"
    regex_time = r"(?:\s?(?:в\s)?((?:[0-1]?\d)|(?:2[0-3])):([0-5]\d)(?::([0-5]\d))?)?"
    regex_endswith = r"(?!\d)"

    # Russian features under date
    ru_months = {
        'янв': 1, 'январь': 1, 'января': 1,
        'фев': 2, 'февраль': 2, 'февраля': 2,
        'мар': 3, 'март': 3, 'марта': 3,
        'апр': 4, 'апрель': 4, 'апреля': 4,
        'май': 5, 'мая': 5,
        'июн': 6, 'июнь': 6, 'июня': 6,
        'июл': 7, 'июль': 7, 'июля': 7,
        'авг': 8, 'август': 8, 'августа': 8,
        'сен': 9, 'сентябрь': 9, 'сентября': 9,
        'окт': 10, 'октябрь': 10, 'октября': 10,
        'ноя': 11, 'ноябрь': 11, 'ноября': 11,
        'дек': 12, 'декабрь': 12, 'декабря': 12
    }

    regex_month = (
        r"(?:([0]?[1-9]|1[0-2])|" 
        r"(янв(?:арь|аря)?|фев(?:раль|раля)?|мар(?:т|та)?|апр(?:ель|еля)?|"
        r"май|мая|июн(?:ь|я)?|июл(?:ь|я)?|авг(?:уст|уста)?|"
        r"сен(?:тябрь|тября)?|окт(?:ябрь|ября)?|ноя(?:брь|бря)?|дек(?:абрь|абря)?))"
    )

    regex_patterns = [
        rf"{regex_day}{regex_delimiter}{regex_month}{regex_delimiter}{regex_year}{regex_time}{regex_endswith}",
        rf"{regex_month}{regex_delimiter}{regex_day}{regex_delimiter}{regex_year}{regex_time}{regex_endswith}",
        rf"{regex_year}{regex_delimiter}{regex_month}{regex_delimiter}{regex_day}{regex_time}{regex_endswith}"
    ]

    for pattern in regex_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            groups = match.groups()
            day, month, month_name, year = None, None, None, None
            hour, minute, second = None, None, None

            if len(groups) >= 4:
                day, month, month_name, year = groups[:4]
                hour, minute, second = (groups[4:] + (None,) * 3)[:3]

            if month_name:
                month_name_normalized = month_name[:3].lower()
                month_full_normalized = month_name.lower()

                if month_full_normalized in ru_months:
                    month = ru_months[month_full_normalized]
                elif month_name_normalized in ru_months:
                    month = ru_months[month_name_normalized]
                else:
                    try:
                        month = datetime.strptime(month_name[:3], '%b').month
                    except ValueError:
                        continue

            try:
                day = int(day) if day else 1
                month = int(month) if month else 1
                year = int(year) if year else 1900
                hour = int(hour) if hour else 0
                minute = int(minute) if minute else 0
                second = int(second) if second else 0

                date = datetime(year, month, day, hour, minute, second)
                break
            except (ValueError, TypeError):
                continue

    return date