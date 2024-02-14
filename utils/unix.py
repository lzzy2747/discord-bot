from datetime import datetime
from time import mktime


def to_unix(date: datetime):
    return round(mktime(date.timetuple()))
