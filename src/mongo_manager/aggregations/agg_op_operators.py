from abc import ABC
from typing import List

from .agreggation_operations import AggregationOperation
from .aggregation_functions import AggregationFunctionValue, AggregationFunctionList, \
    AggregationFunctionDict


class _AggregationOperationString(AggregationFunctionValue,
                                  AggregationOperation, ABC):

    def __init__(self, expression: str):
        super().__init__(expression)


class AggOpToLower(_AggregationOperationString):

    @classmethod
    def key_word(cls) -> str:
        return '$toLower'


class AggOpToUpper(_AggregationOperationString):

    @classmethod
    def key_word(cls) -> str:
        return '$toUpper'


class AggOpConcat(AggregationFunctionList, AggregationOperation):

    def __init__(self, expression: List[str]):
        super().__init__(expression)

    @classmethod
    def key_word(cls) -> str:
        return '$concat'


class AggOpSubstr(AggregationFunctionValue, AggregationOperation):

    def __init__(self, expression: str, start: int, end: int):
        super().__init__([expression, start, end])

    @classmethod
    def key_word(cls) -> str:
        return '$substr'


class AggOpAvg(AggregationFunctionValue, AggregationOperation):
    def __init__(self, expression: str):
        super().__init__(expression)

    @classmethod
    def key_word(cls) -> str:
        return '$avg'


class AggOpSum(AggregationFunctionValue, AggregationOperation):
    @classmethod
    def key_word(cls) -> str:
        return '$sum'


class AggOpRound(AggregationFunctionValue, AggregationOperation):

    def __init__(self, expression: str, decimal: int = 0):
        super().__init__([expression, decimal])

    @classmethod
    def key_word(cls) -> str:
        return '$round'


class AggOpTrunc(AggregationFunctionValue, AggregationOperation):

    def __init__(self, expression: str, decimal: int = 0):
        super().__init__([expression, decimal])

    @classmethod
    def key_word(cls) -> str:
        return '$trunc'


class AggOpPush(AggregationFunctionDict, AggregationOperation):

    @classmethod
    def key_word(cls) -> str:
        return '$push'


class AggOpConcatArrays(AggregationFunctionList, AggregationOperation):
    @classmethod
    def key_word(cls) -> str:
        return '$concatArrays'
