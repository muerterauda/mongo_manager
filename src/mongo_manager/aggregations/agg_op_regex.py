import re

from .aggregation_functions import AggregationFunctionValue
from .agreggation_operations import AggregationOperation


class AggOpRegex(AggregationOperation):

    def __init__(self, regex: str, options: str = ''):
        super().__init__()
        self.data = {self.key_word(): regex,
                     '$options': options}

    @staticmethod
    def get_options_regex(insensitive: bool = False,
                          multiline_anchor: bool = False,
                          ignore_space_regex: bool = False,
                          allow_dot_character: bool = False):
        s = []
        if multiline_anchor:
            s.append('m')
        if ignore_space_regex:
            s.append('x')
        if allow_dot_character:
            s.append('s')
        if insensitive:
            s.append('i')
        return ''.join(s)

    @classmethod
    def insensitive_search(cls, search: str):
        return cls(regex='^' + search + '$', options='i')

    @classmethod
    def key_word(cls) -> str:
        return '$regex'


class AggOpRegexRe(AggregationFunctionValue, AggregationOperation):

    def __init__(self, regex: re.Pattern):
        super().__init__(regex)
        self.logger.debug('\nLa query no sera ejecutable en MongoDB sin usar pymongo.\n'
                          'Query is not going to be able to be executed in MongoDB'
                          ' without using pymongo.')

    @classmethod
    def key_word(cls) -> str:
        return '$regex'
