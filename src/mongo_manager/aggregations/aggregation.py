import functools
from typing import List, Union

import pymongo.collection

from . import AggregationStage


class AggregationExecutor:
    def __init__(self, collection_to_execute: pymongo.collection.Collection):
        self.__query: List[Union[AggregationStage, dict]] = []
        self.__collection = collection_to_execute

    def add_step(self, a: Union[AggregationStage, dict]):
        self.__query.append(a)

    def add_steps(self, *a: Union[AggregationStage, dict]):
        self.__query.extend(a)

    def add_steps_list(self, steps=List[Union[AggregationStage, dict]]):
        self.__query.extend(steps)

    def execute(self):
        if len(self.__query) == 0:
            return None
        return self.__collection.aggregate(self.__query)

    def _see_query(self, sep=',\n\t') -> str:
        return sep.join([str(a) for a in self.__query])

    def __str__(self):
        query = '[\n\t' + self._see_query() + '\n]'
        return f'db.{self.__collection.name}.aggregate({query})'

    def __repr__(self):
        query = '[' + self._see_query(",") + ']'
        return f'db.{self.__collection.name}.aggregate({query})'


def aggregation_decorator(function):
    @functools.wraps(function)
    def wrapper(self, *args, **kwargs) -> List[dict]:
        agg = function(self, self._generate_aggregation_executor(), *args, **kwargs)
        r = agg.execute()
        return r if r is None else list(r)

    return wrapper


def aggregation_decorator_debug(function):
    @functools.wraps(function)
    def wrapper(self, *args, **kwargs) -> List[dict]:
        agg = function(self, self._generate_aggregation_executor(), *args, **kwargs)
        print(repr(agg))
        r = agg.execute()
        return r if r is None else list(r)

    return wrapper
