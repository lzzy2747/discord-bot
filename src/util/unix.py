from datetime import datetime
from time import mktime


def datetime_to_unix(date: datetime):
    return round(mktime(date.timetuple()))
