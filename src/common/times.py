import datetime


def get_utcnow():
    return datetime.datetime.now(datetime.timezone.utc)
