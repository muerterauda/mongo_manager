from .exceptions import MongoManagerException, \
    MongoManagerAggregationException
from .mongo_manager import MongoManager
from .entity import ObjetoMongoAbstract
from .repository import RepositoryBase

MONGO_MANAGER_ASCENDING = 1
"""Ascending sort order."""
MONGO_MANAGER_DESCENDING = -1
"""Descending sort order."""

ObjectMongoAbstract = ObjetoMongoAbstract

__all__ = ['MongoManagerException', 'MongoManagerAggregationException',
           'MongoManager',
           'ObjetoMongoAbstract', 'RepositoryBase',
           'MONGO_MANAGER_ASCENDING', 'MONGO_MANAGER_DESCENDING']
