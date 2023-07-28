import logging
from abc import ABC, abstractmethod
from collections import UserDict

from . import LOG_NAME_AGG
from ..exceptions import MongoManagerAggregationException


class AggregationFunction(UserDict, ABC):
    ID = '_id'

    @staticmethod
    def _logger() -> logging.Logger:
        return logging.getLogger(LOG_NAME_AGG)

    @property
    def logger(self) -> logging.Logger:
        return self._logger()

    @classmethod
    @abstractmethod
    def key_word(cls) -> str:
        pass


class AggregationFunctionDict(AggregationFunction, ABC):
    def __init__(self, mapping: dict = None):
        super().__init__()
        if mapping is None:
            mapping = {}
        self.data = {self.key_word(): mapping}

    def __setitem__(self, key, value):
        self[self.key_word()][key] = value


class AggregationFunctionList(AggregationFunction, ABC):
    def __init__(self, mapping: list = None):
        super().__init__()
        if mapping is None:
            mapping = []
        self.data = {self.key_word(): mapping}

    def add_item(self, item):
        self['data'][self.key_word()].append(item)

    def __setitem__(self, key, value):
        raise MongoManagerAggregationException('No se ha definido ninguna funcion'
                                               ' para añadir valores a este paso'
                                               ' de la query.')


class AggregationFunctionValue(AggregationFunction, ABC):

    def __init__(self, mapping):
        super().__init__()
        self.data = {self.key_word(): mapping}

    def __setitem__(self, key, value):
        raise MongoManagerAggregationException('No se ha definido ninguna funcion'
                                               ' para añadir valores a'
                                               ' este paso de la query.')
