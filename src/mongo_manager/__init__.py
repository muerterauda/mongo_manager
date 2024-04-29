from typing import TypeVar

from .exceptions import MongoManagerException, \
    MongoManagerAggregationException, MongoManagerGridFSException
from .mongo_manager import MongoManager
from .entity import ObjetoMongoAbstract
from .repository import RepositoryBase, RepositoryGridFSBase, RepositoryGridFSDict

MONGO_MANAGER_ASCENDING = 1
"""Ascending sort order."""
MONGO_MANAGER_DESCENDING = -1
"""Descending sort order."""

ObjectMongoAbstract = ObjetoMongoAbstract

T_REPO_GRIDFS = TypeVar('T_REPO_GRIDFS', bound=RepositoryGridFSBase)

__all__ = [
    'MongoManagerException', 'MongoManagerAggregationException', 'MongoManagerGridFSException',
    'MongoManager',
    'ObjetoMongoAbstract', 'RepositoryBase',
    'MONGO_MANAGER_ASCENDING', 'MONGO_MANAGER_DESCENDING']
