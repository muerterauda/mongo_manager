from __future__ import annotations
from abc import ABC

from mongo_manager.aggregations.aggregation_functions import AggregationFunction


class AggregationOperation(AggregationFunction, ABC):

    def get_var_aggregation(self, name_var: str) -> dict:
        return {name_var: self}

    @classmethod
    def gen_operation_aggregations_name(cls, name_var, *args, **kwargs):
        return {name_var: cls(*args, **kwargs)}


