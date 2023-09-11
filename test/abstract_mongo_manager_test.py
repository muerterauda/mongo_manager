import unittest
from abc import ABC

from src.mongo_manager import MongoManager


class AbstractMongoManagerTest(unittest.TestCase, ABC):

    @classmethod
    def setUpClass(cls) -> None:
        MongoManager('testMongoManager', 'testMongoManager', 'testMongoManager', 'testMongoManager')

    @classmethod
    def tearDownClass(cls) -> None:
        MongoManager._destroy()
