from abc import ABC, abstractmethod
from collections import UserDict

from mongo_manager import MongoManagerAggregationException


class AggregationStage(UserDict, ABC):
    ID = '_id'

    @classmethod
    @abstractmethod
    def key_word(cls) -> str:
        pass


class _AggregationStageDict(AggregationStage, ABC):
    def __init__(self, mapping: dict = None):
        super().__init__()
        if mapping is None:
            mapping = {}
        self.data = {self.key_word(): mapping}

    def __setitem__(self, key, value):
        self[self.key_word()][key] = value


class _AggregationStageValue(AggregationStage, ABC):

    def __init__(self, mapping):
        super().__init__()
        if mapping is None:
            mapping = {}
        self.data = {self.key_word(): mapping}

    def __setitem__(self, key, value):
        raise MongoManagerAggregationException('No se ha definido ninguna funcion'
                                               ' para añadir valores a este paso de la query.')


class AggStMatch(_AggregationStageDict):

    @classmethod
    def key_word(cls) -> str:
        return '$match'


class AggStGroup(_AggregationStageDict):

    def __init__(self, id_mapping: dict = None, mapping: dict = None):
        super().__init__()
        if id_mapping is None or id_mapping.get(self.ID) is None:
            id_mapping = {self.ID: {}}
        if mapping is None:
            mapping = {}
        self.data = {self.key_word(): {**id_mapping, **mapping}}

    def add_id(self, mapping: dict):
        self[self.key_word()][self.ID] = mapping

    @classmethod
    def key_word(cls) -> str:
        return '$group'


class AggStProject(_AggregationStageDict):

    def __init__(self, id_present: bool = False, mapping: dict = None):
        super().__init__()
        if mapping is None:
            mapping = {}
        mapping[self.ID] = 1 if id_present else 0
        self.data = {self.key_word(): mapping}

    def presence_attr(self, att: str, presence: bool):
        self[att] = 1 if presence else 0

    @classmethod
    def key_word(cls) -> str:
        return '$project'


class AggStFacet(_AggregationStageDict):

    @classmethod
    def key_word(cls) -> str:
        return '$facet'


class AggStUnwind(_AggregationStageValue):

    @classmethod
    def key_word(cls) -> str:
        return '$unwind'

    def __init__(self, unwind_value: str):
        super().__init__(unwind_value)


class AggStSort(_AggregationStageValue):

    @classmethod
    def key_word(cls) -> str:
        return '$sort'

    def __init__(self, unwind_value: str):
        super().__init__(unwind_value)


class AggStOut(_AggregationStageValue):

    @classmethod
    def key_word(cls) -> str:
        return '$out'

    def __init__(self, collection_out: str):
        super().__init__(collection_out)


class AggStLimit(_AggregationStageValue):

    @classmethod
    def key_word(cls) -> str:
        return '$limit'

    def __init__(self, number_limit: int):
        super().__init__(number_limit)


class AggStSkip(_AggregationStageValue):

    @classmethod
    def key_word(cls) -> str:
        return '$skip'

    def __init__(self, number_skip: int):
        super().__init__(number_skip)


class AggStCount(_AggregationStageValue):

    def __init__(self, var_count: str):
        super().__init__(var_count)

    @classmethod
    def key_word(cls) -> str:
        return '$count'
