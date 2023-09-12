import functools
import logging
from typing import List, Union

import pymongo
from pymongo.cursor import Cursor

from . import LOG_NAME_AGG, AggregationExecutor


def aggregation_decorator(function):
    @functools.wraps(function)
    def wrapper(self, *args,
                connection: pymongo.collection = None, **kwargs) -> List[dict]:
        exe = self._generate_aggregation_executor()\
            if connection is None else AggregationExecutor(connection)
        agg = function(self, exe, *args, **kwargs)
        r = agg.execute()
        return r if r is None else list(r)

    return wrapper


def aggregation_decorator_cursor(function):
    @functools.wraps(function)
    def wrapper(self, *args,
                connection: pymongo.collection = None, **kwargs) -> Union[Cursor, None]:
        exe = self._generate_aggregation_executor()\
            if connection is None else AggregationExecutor(connection)
        agg = function(self, exe, *args, **kwargs)
        return agg.execute()

    return wrapper


def aggregation_decorator_debug(function):
    @functools.wraps(function)
    def wrapper(self, *args,
                connection: pymongo.collection = None, **kwargs) -> List[dict]:
        logging.basicConfig(level=logging.DEBUG)
        log = logging.getLogger(LOG_NAME_AGG)
        exe = self._generate_aggregation_executor()\
            if connection is None else AggregationExecutor(connection)
        agg = function(self, exe, *args, **kwargs)
        log.debug('\n' + repr(agg))
        r = agg.execute()
        return r if r is None else list(r)

    return wrapper


def aggregation_decorator_alone(function):
    def wrapper(connection: pymongo.collection, *args, **kwargs) -> List[dict]:
        agg = function(AggregationExecutor(connection), *args, **kwargs)
        r = agg.execute()
        return r if r is None else list(r)

    return wrapper


def aggregation_decorator_cursor_alone(function):
    def wrapper(connection: pymongo.collection, *args, **kwargs) -> Union[Cursor, None]:
        agg = function(AggregationExecutor(connection), *args, **kwargs)
        return agg.execute()

    return wrapper


def aggregation_decorator_debug_alone(function):
    def wrapper(connection: pymongo.collection, *args, **kwargs) -> List[dict]:
        logging.basicConfig(level=logging.DEBUG)
        log = logging.getLogger(LOG_NAME_AGG)
        agg = function(AggregationExecutor(connection), *args, **kwargs)
        log.debug('\n' + repr(agg))
        r = agg.execute()
        return r if r is None else list(r)

    return wrapper
