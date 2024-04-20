import datetime
from abc import ABCMeta, abstractmethod


class TimeProvider(metaclass=ABCMeta):
    @abstractmethod
    def now(self) -> datetime.datetime:
        pass


class LocalTimeProvider(TimeProvider):
    def now(self) -> datetime.datetime:
        return datetime.datetime.now()
