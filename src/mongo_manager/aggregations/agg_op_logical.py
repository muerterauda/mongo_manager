from abc import ABC

from .aggregation_functions import AggregationFunctionList, AggregationFunctionValue
from .agreggation_operations import AggregationOperation


class _AggregationOperationLogical(AggregationFunctionList, AggregationOperation, ABC):
    pass


class AggOpAnd(_AggregationOperationLogical):

    @classmethod
    def key_word(cls) -> str:
        return '$and'


class AggOpOr(_AggregationOperationLogical):

    @classmethod
    def key_word(cls) -> str:
        return '$and'


class AggOpNor(_AggregationOperationLogical):

    @classmethod
    def key_word(cls) -> str:
        return '$and'


class AggOpProjectNot(_AggregationOperationLogical):

    @classmethod
    def key_word(cls) -> str:
        return '$not'


class AggOpMatchNot(AggregationFunctionValue, AggregationOperation, ABC):

    @classmethod
    def key_word(cls) -> str:
        return '$not'


class AggOpExists(AggregationFunctionValue, AggregationOperation):

    @classmethod
    def key_word(cls) -> str:
        return '$exists'

    def __init__(self, exists: bool):
        super().__init__(exists)
