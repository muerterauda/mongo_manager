from abc import ABC

from .aggregation_functions import AggregationFunction, AggregationFunctionDict, \
    AggregationFunctionValue


class AggregationStage(AggregationFunction, ABC):
    pass


class AggStMatch(AggregationFunctionDict, AggregationStage):

    @classmethod
    def key_word(cls) -> str:
        return '$match'


class AggStGroup(AggregationFunctionDict, AggregationStage):

    def __init__(self, id_mapping: dict = None, mapping: dict = None):
        super().__init__()
        if id_mapping is None:
            id_mapping = {}
        id_mapping = {self.ID: id_mapping}
        if mapping is None:
            mapping = {}
        self.data = {self.key_word(): {**id_mapping, **mapping}}

    def add_id(self, mapping: dict):
        self[self.key_word()][self.ID] = mapping

    @classmethod
    def key_word(cls) -> str:
        return '$group'


class AggStProject(AggregationFunctionDict, AggregationStage):

    def __init__(self, mapping: dict = None, id_present: bool = None):
        super().__init__()
        if mapping is None:
            mapping = {}
        if id_present is not None:
            mapping[self.ID] = 1 if id_present else 0
        self.data = {self.key_word(): mapping}

    def presence_attr(self, att: str, presence: bool):
        self[att] = 1 if presence else 0

    @classmethod
    def key_word(cls) -> str:
        return '$project'


class AggStFacet(AggregationFunctionDict, AggregationStage):

    @classmethod
    def key_word(cls) -> str:
        return '$facet'


class AggStUnwind(AggregationFunctionValue, AggregationStage):

    @classmethod
    def key_word(cls) -> str:
        return '$unwind'

    def __init__(self, unwind_value: str):
        super().__init__(unwind_value)


class AggStSort(AggregationFunctionDict, AggregationStage):

    def __init__(self, mapping: dict = None):
        super().__init__()
        if mapping is None:
            mapping = {}
        self.data = {self.key_word(): mapping}

    @classmethod
    def key_word(cls) -> str:
        return '$sort'

    def add_fields(self, sorted_dict: dict):
        for x, y in sorted_dict.items():
            self[x] = y

    def add_field(self, field: str, asc: bool):
        self[field] = 1 if asc else -1


class AggStOut(AggregationFunctionValue, AggregationStage):

    @classmethod
    def key_word(cls) -> str:
        return '$out'

    def __init__(self, collection_out: str):
        super().__init__(collection_out)


class AggStLimit(AggregationFunctionValue, AggregationStage):

    @classmethod
    def key_word(cls) -> str:
        return '$limit'

    def __init__(self, number_limit: int):
        super().__init__(number_limit)


class AggStSkip(AggregationFunctionValue, AggregationStage):

    @classmethod
    def key_word(cls) -> str:
        return '$skip'

    def __init__(self, number_skip: int):
        super().__init__(number_skip)


class AggStCount(AggregationFunctionValue, AggregationStage):

    def __init__(self, var_count: str):
        super().__init__(var_count)

    @classmethod
    def key_word(cls) -> str:
        return '$count'
