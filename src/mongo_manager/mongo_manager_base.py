from __future__ import annotations
from pymongo import MongoClient

from mongo_manager.patrones import SingletonMeta

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
        if bd_online:
            url = url_online
        else:
            if authenticated:
                url = f'mongodb://{username}:{password}@localhost:{port_local}'
            else:
                url = f'mongodb://localhost:{port_local}'
        self.__client = MongoClient(url, authSource=auth_source) \
            if authenticated and auth_source != '' else MongoClient(url)
        self.__bd = self.__client[db]
        global _mongo_manager_gl
        _mongo_manager_gl = self

    @property
    def bd(self):
        return self.__bd

    def collection(self, collection):
        return self.bd[collection]

    def _destroy(self):
        import gc
        self.__client.close()
        key = getattr(self, '_singleton_key', None)
        if key is not None:
            SingletonMeta._instances.pop(key, None)
        # Forzar recolección de basura (opcional)
        gc.collect()
