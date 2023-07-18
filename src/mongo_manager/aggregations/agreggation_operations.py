from abc import ABC, abstractmethod
from collections import UserDict


class AggregationOperation(UserDict, ABC):
    @classmethod
    @abstractmethod
    def key_word(cls) -> str:
        pass


