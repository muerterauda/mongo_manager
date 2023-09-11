from test.abstract_mongo_manager_test import AbstractMongoManagerTest
from src.mongo_manager import RepositoryBase
from test.classes_test import Book


class RepositoryBook(RepositoryBase[Book]):
    def __init__(self) -> None:
        super().__init__('book', Book)


class TestRepository(AbstractMongoManagerTest):

    def setUp(self) -> None:
        self.repo = RepositoryBook()

    def tearDown(self) -> None:
        self.repo.drop_collection(drop=True)
        del self.repo

    def test_insert(self):
        a = Book('test1', '', '', '')
        self.repo.insert_one(a)
        b = self.repo.find_one()
        assert a.nombre == b.nombre
