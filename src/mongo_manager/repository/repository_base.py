from __future__ import annotations

from collections.abc import Iterable
from typing import TypeVar, Type, Generic, Optional

import pymongo
from pymongo.results import UpdateResult, InsertManyResult, \
    InsertOneResult, DeleteResult

from .. import ObjetoMongoAbstract, MongoManagerException
from ..patrones import SingletonMeta
from ..aggregations.aggregation import AggregationExecutor
from ..mongo_utils import aggregate_out, aggregate_match
from bson import ObjectId

T_O = TypeVar('T_O', bound=ObjetoMongoAbstract)


class RepositoryBase(Generic[T_O], metaclass=SingletonMeta):

    def __init__(self, collection: str, clase: Type[T_O],
                 connection_collection=None) -> None:
        __metaclass__ = SingletonMeta  # noqa: F841
        if connection_collection is None:
            from ..mongo_manager import _mongo_manager_gl as mongo_manager_gl
            if mongo_manager_gl is None:
                raise MongoManagerException(
                    '\nNo se ha inicializado la base de datos, '
                    'crear con MongoManager(), '
                    'ni se ha dado una conexion al repositorio.'
                    '\nMongoManager is not initialized, '
                    'create it with MongoManager(), '
                    'or provide a different connection to the repository.')
            connection_collection = mongo_manager_gl.collection(collection)
        self.__collection = connection_collection
        self.__clase = clase

    @property
    def collection(self) -> pymongo.collection.Collection:
        """
        @return: Pymongo collection | Coleccion Pymongo
        """
        return self.__collection

    @property
    def clase(self):
        """
        @return: Class used in the repository to
         convert data o objects| Clase del repositorio
        """
        return self.__clase

    def _generate_aggregation_executor(self) -> AggregationExecutor:
        return AggregationExecutor(collection_to_execute=self.collection)

    def count_many(self, filter_dict: dict = None) -> int:
        if filter_dict is None:
            filter_dict = {}
        return self.collection.count_documents(filter_dict)

    def count_all(self) -> int:
        return self.collection.count_documents({})

    def estimated_count(self) -> int:
        return self.collection.estimated_document_count()

    def find_one(self, filter_dict: dict = None) -> T_O:
        if filter_dict is None:
            filter_dict = {}
        return self.clase.generar_object_from_dict(self.collection.find_one(
            filter_dict))

    def find_many(self, filter_dict: dict = None,
                  skip: int = 0, limit: int = 1000, sort=None) -> list[T_O]:
        if filter_dict is None:
            filter_dict = {}
        object_list = self.collection.find(filter_dict).skip(skip).limit(limit if limit != -1 else 0)
        if sort is not None:
            object_list.sort(sort)
        return self.clase.generar_objects_from_list_dicts(object_list)

    def find_all(self, skip: int = 0, limit: int = 1000, sort=None) -> list[T_O]:
        return self.find_many(skip=skip, limit=limit, sort=sort)

    def find_by_id(self, id_mongo) -> T_O:
        return self.clase.generar_object_from_dict(
            self.collection.find_one({'_id': ObjectId(id_mongo)}))

    def delete_object(self, objeto: T_O) -> DeleteResult:
        if objeto.id is not None:
            return self.delete_by_id(objeto.id)

    def delete_by_id(self, id_mongo) -> DeleteResult:
        return self.collection.delete_one({'_id': ObjectId(id_mongo)})

    def insert_one(self, objeto: T_O, id_mongo=False) -> InsertOneResult:
        return self.collection.insert_one(objeto.get_dict_no_id()
                                          if not id_mongo else objeto.get_dict())

    def insert_many(self, object_list: list[T_O], id_mongo=False) -> InsertManyResult | None:
        if (object_list is None or
                not isinstance(object_list, Iterable) or len(object_list) == 0):
            return None
        return self.collection.insert_many(
            self.clase.generar_list_dicts_from_list_objects(
                object_list, id_mongo=id_mongo))

    def insert_one_raw(self, object_dict: dict):
        return self.insert_one(self.clase.generar_object_from_dict(object_dict))

    def insert_or_replace_id(self, objeto: T_O, upsert: bool = True):
        return self._replace_by_id(objeto.id, objeto, upsert)

    def replace_by_id(self, id_mongo, objeto: T_O) -> UpdateResult:
        return self._replace_by_id(id_mongo, objeto, False)

    def _replace_by_id(self, id_mongo, objeto: T_O, upsert: bool = False) -> UpdateResult:
        return self.collection.replace_one({"_id": id_mongo}, objeto.get_dict(), upsert)

    def replace_many_by_id(self, object_list: list[T_O], upsert: bool = False):
        for x in object_list:
            self._replace_by_id(x.id, x, upsert)

    def update_by_id(self, id_mongo, objeto_dict: dict) -> UpdateResult:
        return self.collection.update_one({"_id": id_mongo}, {"$set": objeto_dict})

    def update_many(self, filter_dict: dict = None,
                    objeto_dict: dict = None) -> Optional[UpdateResult]:
        if objeto_dict is None:
            return None
        if filter_dict is None:
            filter_dict = {}
        self.collection.update_many(filter_dict, {"$set": objeto_dict})

    def copy_collection_db(self, name_new_collection: str,
                           copy_match_condition: dict = None):
        out = [aggregate_out(name_new_collection)]
        if copy_match_condition is not None:
            match = aggregate_match(copy_match_condition)
            out = [match] + out
        return self.collection.aggregate(out)

    def drop_collection(self, *, drop=False):
        if not drop:
            raise MongoManagerException('Medida de seguridad, fallo al '
                                        'intentar eliminar la coleccion\n'
                                        'Security fail, try to drop '
                                        'entire collection avoided.')
        self.collection.delete_many({})
