import unittest
from abc import ABC

from src.mongo_manager import MongoManager


class AbstractMongoManagerTest(unittest.TestCase, ABC):

    @classmethod
    def setUpClass(cls) -> None:
        MongoManager(username='testMongoManager',
                     password='testMongoManager',
                     db='testMongoManager',
                     auth_source='testMongoManager')

    @classmethod
    def tearDownClass(cls) -> None:
        MongoManager._destroy()
