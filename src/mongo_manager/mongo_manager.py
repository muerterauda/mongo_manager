from __future__ import annotations
from pymongo import MongoClient

from .patrones import SingletonMeta

_mongo_manager_gl = None


class MongoManager(metaclass=SingletonMeta):
    __bd = None

    def __init__(self, username: str = '', password: str = '',
                 db: str = '', auth_source: str = '',
                 bd_online: bool = False, port_local: int = 27017,
                 url_online='', authenticated=True) -> None:
        """
        Crea la instancia conectada a la collecion en cuestion.
        """
        self.__bd = None
        if bd_online:
            self.__bd = MongoClient(url_online)
        else:
            if authenticated:
                if auth_source == '':
                    self.__bd = \
                        MongoClient('mongodb://{}:{}@localhost:{}'.format(username,
                                                                          password,
                                                                          port_local)
                                    )
                else:
                    self.__bd = \
                        MongoClient('mongodb://{}:{}@localhost:{}'.format(username,
                                                                          password,
                                                                          port_local),
                                    authSource=auth_source)
            else:
                self.__bd = MongoClient('mongodb://localhost:{}'.format(port_local))
        self.__bd = self.__bd[db]
        global _mongo_manager_gl
        _mongo_manager_gl = self

    @property
    def bd(self):
        return self.__bd

    def collection(self, collection):
        return self.bd[collection]

