from __future__ import annotations

from typing import Callable, TypeVar, Generic, Any, IO
import json
import gridfs
from gridfs import GridOut

from .. import MongoManagerException
from ..patrones import SingletonMeta

T_GRID = TypeVar('T_GRID')

T_OUT = TypeVar('T_OUT')


class RepositoryGridFSBase(Generic[T_OUT], metaclass=SingletonMeta):

    def __init__(self, collection: str,
                 connection_database=None) -> None:
        __metaclass__ = SingletonMeta  # noqa: F841
        if connection_database is None:
            from ..mongo_manager import _mongo_manager_gl as mongo_manager_gl
            if mongo_manager_gl is None:
                raise MongoManagerException()
            connection_database = mongo_manager_gl.bd
        connection_collection_grid = gridfs.GridFS(connection_database, collection)
        self.__connection_collection_grid = connection_collection_grid
        self.__collection_name = collection

    @property
    def collection(self) -> gridfs.GridFS:
        """
        @return: Grid collection connection
        """
        return self.__connection_collection_grid

    @property
    def collection_name(self) -> str:
        """
        @return: Grid collection name
        """
        return self.__collection_name

    def find_raw_by_id(self, file_id) -> GridOut:
        return self.__connection_collection_grid.get(file_id)

    def find_raw_by_name_last(self, name) -> GridOut:
        return self.__connection_collection_grid.get_last_version(name)

    def find_raw_by_name_version(self, name, version) -> GridOut:
        return self.__connection_collection_grid.get_version(name, version)

    def find_by_id(self, file_id) -> T_OUT:
        return self._reconvert_function(self.find_raw_by_id(file_id))

    def find_by_name_last(self, name) -> T_OUT:
        return self._reconvert_function(self.find_by_name_last(name))

    def find_by_name_version(self, name, version) -> T_OUT:
        return self._reconvert_function(self.find_by_name_version(name, version))

    def find_by_id_custom_return(self, file_id,
                                 custom_return: Callable[[GridOut], T_GRID]) -> T_GRID:
        return custom_return(self.find_raw_by_id(file_id))

    def find_by_name_last_custom_return(self, name,
                                        custom_return: Callable[[GridOut], T_GRID]) -> T_GRID:
        return custom_return(self.find_by_name_last(name))

    def find_by_name_version_custom_return(self, name, version,
                                           custom_return: Callable[[GridOut], T_GRID]) -> T_GRID:
        return custom_return(self.find_by_name_version(name, version))

    def insert_one_raw(self, x, filename: str, **kwargs) -> Any:
        return self.__connection_collection_grid.put(x, filename=filename, **kwargs)

    def insert_one(self, x, filename: str, **kwargs):
        return self.__connection_collection_grid.put(self._convert_function(x), filename=filename,
                                                     **{**self._aditional_arguments_insert(), **kwargs})

    def insert_one_custom(self, x, filename: str, custom_func: Callable[[Any], IO], **kwargs):
        return self.__connection_collection_grid.put(custom_func(x), filename=filename,
                                                     **kwargs)

    @staticmethod
    def _convert_function(x) -> IO:
        return x

    def _aditional_arguments_insert(self) -> dict:
        return {}

    @staticmethod
    def _reconvert_function(x: GridOut) -> T_OUT:
        return x


class RepositoryGridFSDict(RepositoryGridFSBase[dict], metaclass=SingletonMeta):

    def __init__(self, collection: str, connection_database=None, encoding='utf8'):
        super().__init__(collection, connection_database)
        self.encoding = encoding

    @staticmethod
    def _convert_function(x) -> IO:
        return json.dumps(x) if x is not None else x

    @staticmethod
    def _reconvert_function(x: GridOut) -> dict:
        return json.loads(x.read()) if x is not None else x

    def _aditional_arguments_insert(self) -> dict:
        return {'encoding': self.encoding}
