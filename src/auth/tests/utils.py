import datetime


def create_fake_datetime(date):
    class FakeDateTime(datetime.datetime):
        @classmethod
        def utcnow(cls):
            return date
    return FakeDateTime
