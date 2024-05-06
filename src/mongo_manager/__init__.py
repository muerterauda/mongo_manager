from mongo_manager.exceptions import (MongoManagerException,
                                      MongoManagerGridFSException,
                                      MongoManagerAggregationException)
from mongo_manager.mongo_manager_base import MongoManager
from mongo_manager.base_module import ObjetoMongoAbstract, RepositoryBase

MONGO_MANAGER_ASCENDING = 1
"""Ascending sort order."""
MONGO_MANAGER_DESCENDING = -1
"""Descending sort order."""

ObjectMongoAbstract = ObjetoMongoAbstract

__all__ = [
    'MongoManagerException', 'MongoManagerAggregationException',
    'MongoManagerGridFSException',
    'MongoManager',
    'ObjetoMongoAbstract', 'RepositoryBase',
    'MONGO_MANAGER_ASCENDING', 'MONGO_MANAGER_DESCENDING']
