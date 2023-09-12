from abc import ABC

from .aggregation_functions import \
    AggregationFunctionValue, AggregationFunctionList
from .agreggation_operations import AggregationOperation


class _AggregationOperationProjectComparison(AggregationOperation,
                                             AggregationFunctionValue, ABC):
    def __init__(self, first_value, second_value):
        super().__init__([first_value, second_value])


class AggOpProjectEq(_AggregationOperationProjectComparison):

    @classmethod
    def key_word(cls) -> str:
        return '$eq'


class AggOpProjectNe(_AggregationOperationProjectComparison):

    @classmethod
    def key_word(cls) -> str:
        return '$ne'


class AggOpProjectIn(_AggregationOperationProjectComparison):

    @classmethod
    def key_word(cls) -> str:
        return '$in'


class AggOpProjectNin(_AggregationOperationProjectComparison):

    @classmethod
    def key_word(cls) -> str:
        return '$nin'


class AggOpProjectGt(_AggregationOperationProjectComparison):

    @classmethod
    def key_word(cls) -> str:
        return '$gt'


class AggOpProjectGte(_AggregationOperationProjectComparison):

    @classmethod
    def key_word(cls) -> str:
        return '$gte'


class AggOpProjectLt(_AggregationOperationProjectComparison):

    @classmethod
    def key_word(cls) -> str:
        return '$lt'


class AggOpProjectLte(_AggregationOperationProjectComparison):

    @classmethod
    def key_word(cls) -> str:
        return '$lte'


class AggOpMatchEq(AggregationFunctionValue, AggregationOperation):

    @classmethod
    def key_word(cls) -> str:
        return '$eq'


class AggOpMatchNe(AggregationFunctionValue, AggregationOperation):

    @classmethod
    def key_word(cls) -> str:
        return '$ne'


class AggOpMatchIn(AggregationFunctionList, AggregationOperation):

    @classmethod
    def key_word(cls) -> str:
        return '$in'


class AggOpMatchNin(AggregationFunctionList, AggregationOperation):

    @classmethod
    def key_word(cls) -> str:
        return '$nin'


class AggOpMatchGt(AggregationFunctionValue, AggregationOperation):

    @classmethod
    def key_word(cls) -> str:
        return '$gt'


class AggOpMatchGte(AggregationFunctionValue, AggregationOperation):

    @classmethod
    def key_word(cls) -> str:
        return '$gte'


class AggOpMatchLt(AggregationFunctionValue, AggregationOperation):

    @classmethod
    def key_word(cls) -> str:
        return '$lt'


class AggOpMatchLte(AggregationFunctionValue, AggregationOperation):

    @classmethod
    def key_word(cls) -> str:
        return '$lte'
