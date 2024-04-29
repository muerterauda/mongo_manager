from abc import ABC
from typing import Callable

from .objeto_mongo_abstract import ObjetoMongoAbstract
from .. import MongoManagerGridFSException
from ..repository import T_GRID_TYPE


class ObjetoMongoAbstractGridFS(ObjetoMongoAbstract, ABC):

    def __init__(self, _id=None, _grid_objects: list = None, **kwargs):
        super().__init__(_id=_id, **kwargs)
        if _grid_objects is None:
            _grid_objects = []
        self._grid_objects = _grid_objects
        self.__repositorys_gridfs = {}
        self.__load_objects = {}

    def get_status_gridfs(self):
        print(self.__repositorys_gridfs)
        res = {}
        k = self.__load_objects.keys()
        for x in self._grid_objects:
            res[x] = "Loaded" if x in k else "Not Loaded"
        print(res)

    def set_gridfs_key_value(self, name_attr, repository: T_GRID_TYPE):
        self.__repositorys_gridfs[name_attr] = repository

    def load_all(self):
        for name_attr in self._grid_objects:
            self.load_gridfs(name_attr, getattr(self, name_attr))

    def unload_all(self):
        self.__load_objects = {}

    def load_gridfs(self, name_attr: str, attr, repository: T_GRID_TYPE = None, force=False):
        load_o = self.__load_objects.get(name_attr)
        if load_o is not None:
            return load_o
        if repository is None:
            repository = self.__repositorys_gridfs.get(name_attr, None)
            if repository is None:
                raise MongoManagerGridFSException('No se ha asignado repositorio para'
                                                  ' insertar el grid. Usa el metodo set_gridfs_key_value')
        if not force and repository.collection_name != attr[0]:
            raise MongoManagerGridFSException('La coleccion del repositorio no se corresponde con la del objeto')
        elif force and repository.collection_name != attr[0]:
            x = repository.find_by_name_last(attr[2])
        else:
            x = repository.find_by_id(attr[1])
        self.__load_objects[name_attr] = x
        return x

    def __insert_gridfs_object(self, name_attr: str, file, repository: T_GRID_TYPE = None,
                               custom_function: Callable = None, load=True):
        if repository is None:
            repository = self.__repositorys_gridfs.get(name_attr, None)
            if repository is None:
                raise MongoManagerGridFSException('No se ha asignado repositorio para insertar el grid')
        if custom_function is not None:
            id_gridfs_object = repository.insert_one_custom(file, name_attr, custom_function)
        else:
            id_gridfs_object = repository.insert_one(file, name_attr)
        setattr(self, name_attr, [repository.collection_name, id_gridfs_object, name_attr])
        self._grid_objects.append(name_attr)
        if load:
            self.__load_objects[name_attr] = file

    def insert_gridfs(self, name_attr: str, file, repository: T_GRID_TYPE = None,
                      custom_function: Callable = None, load=True):
        self.__insert_gridfs_object(name_attr, file, repository, custom_function, load)

    def save_attr_as_gridfs(self, name_attr: str, repository: T_GRID_TYPE = None,
                            custom_function: Callable = None, load=True):
        file = getattr(self, name_attr)
        self.__insert_gridfs_object(name_attr, file, repository, custom_function, load)

    def delete_gridfs(self, name_attr, repository: T_GRID_TYPE = None):
        if repository is None:
            repository = self.__repositorys_gridfs.get(name_attr, None)
            if repository is None:
                raise MongoManagerGridFSException('No se ha asignado repositorio para borrar el grid')
        attr = getattr(self, name_attr)
        if repository.collection_name != attr[0]:
            raise MongoManagerGridFSException('La coleccion del repositorio'
                                              ' no se corresponde con la del objeto')
        repository.delete_id(attr[1])

    def get_dict(self, id_mongo=True, id_as_string=False, include_private_false=False) -> dict:
        __load_objects = self.__load_objects
        __repositorys_gridfs = self.__repositorys_gridfs
        self.__load_objects = None
        self.__repositorys_gridfs = None
        generated_dict = super().get_dict(id_mongo, id_as_string, include_private_false)
        if id_as_string:
            for x in self._grid_objects:
                generated_dict[x][1] = str(generated_dict[x][1])
        self.__load_objects = __load_objects
        self.__repositorys_gridfs = __repositorys_gridfs
        return generated_dict
