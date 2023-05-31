# Aggregation Pipelines Stages

def aggregate_match(diccionario: dict) -> dict:
    return {'$match': diccionario}


def aggregate_group(diccionario: dict) -> dict:
    return {'$group': diccionario}


def aggregate_project(diccionario: dict) -> dict:
    return {'$project': diccionario}


def aggregate_unwind(valor: str) -> dict:
    return {'$unwind': valor}


def aggregate_sort(diccionario: dict) -> dict:
    return {'$sort': diccionario}


def aggregate_out(collection_name) -> dict:
    return {'$out':  collection_name}


def aggregate_limit(limit: int) -> dict:
    return {'$limit': limit}


def aggregate_skip(skip: int) -> dict:
    return {'$skip': skip}


def aggregate_facet(diccionario: dict) -> dict:
    return {'$facet': diccionario}


def aggregate_count(nombre_counter: str) -> dict:
    return {'$count': nombre_counter}


# Query Operators

#   Comparison

def mongo_eq(valor) -> dict:
    return {'$eq': valor}


def mongo_ne(valor) -> dict:
    return {'$ne': valor}


def mongo_in(valor: list) -> dict:
    return {'$in': valor}


def mongo_nin(valor: list) -> dict:
    return {'$nin': valor}


def mongo_gt(valor: int) -> dict:
    return {'$gt': valor}


def mongo_gte(valor: int) -> dict:
    return {'$gte': valor}


def mongo_lt(valor: list) -> dict:
    return {'$lt': valor}


def mongo_lte(valor: list) -> dict:
    return {'$lte': valor}


#   Logical

def mongo_and(valor: list) -> dict:
    return {'$and': valor}


def mongo_or(valor: list) -> dict:
    return {'$or': valor}


def mongo_nor(valor: list) -> dict:
    return {'$nor': valor}


def mongo_not(condicion_dict: dict) -> dict:
    return {'$not': condicion_dict}


#   Others

def mongo_exists(existe: bool = True) -> dict:
    return {'$exists': existe}


def mongo_regex(regex, options) -> dict:
    return {'$regex': regex, '$options': options}


def mongo_regex_compare_insensitive(valor: str) -> dict:
    return mongo_regex('^' + valor + '$', 'i')


# Fields Operators

#   String Operators

def mongo_lower(valor: str) -> dict:
    return {'$toLower': valor}


def mongo_upper(valor: str) -> dict:
    return {'$toUpper': valor}


def mongo_concat(valor: list) -> dict:
    return {'$concat': valor}


#   Number Operators


def mongo_avg(valor: str) -> dict:
    return {'$avg': valor}


def mongo_sum(valor: int) -> dict:
    return {'$sum': valor}


def mongo_sum_field(field: str) -> dict:
    return {'$sum': field}


def mongo_round(field: str, decimal: int) -> dict:
    return {'$round': [field, decimal]}


def mongo_trunc(field: str, decimal: int) -> dict:
    return {'$trunc': [field, decimal]}


#   Array Operators

def mongo_push(valor: dict) -> dict:
    return {'$push': valor}


def mongo_concat_arrays(arrays: list) -> dict:
    return {'$concatArrays': arrays}
