import _collections_abc
from typing import List, Union

import pymongo.collection
from pymongo.cursor import Cursor

from . import AggregationStage


def _pretty_query(query, total_tab='\t') -> str:
    st = ''
    _st = '\n' + total_tab
    if issubclass(type(query), _collections_abc.MutableMapping):
        st = _st.join([
            "'{x}': {y}".format(x=x,
                                y=_pretty_query(query=y, total_tab=total_tab + '\t'))
            for x, y in query.items()])
        st = '{\n' + total_tab + st + '\n' + total_tab[:-1] + '}'
    elif issubclass(type(query), list):
        st = st + _st.join(_pretty_query(x, total_tab + '\t') for x in query)
    elif issubclass(type(query), str):
        st = f"'{query}'"
    else:
        st = f"{str(query)}"
    return st


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

    def execute(self) -> Union[Cursor, None]:
        if len(self.__query) == 0:
            return None
        return self.__collection.aggregate(self.__query)

    def _see_query(self, sep=',\n\t') -> str:
        return sep.join([str(a) for a in self.__query])

    def pretty(self) -> str:
        aux = _pretty_query(self.__query)
        query = '[\n\t' + aux + '\n]'
        return f'db.{self.__collection.name}.aggregate({query})'

    def __str__(self):
        query = '[\n\t' + self._see_query() + '\n]'
        return f'db.{self.__collection.name}.aggregate({query})'

    def __repr__(self):
        query = '[' + self._see_query(",") + ']'
        return f'db.{self.__collection.name}.aggregate({query})'

