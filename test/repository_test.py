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
        c = self.repo.count_all()
        assert c == 1
        b = self.repo.find_one()
        assert a.nombre == b.nombre

    def test_insert_multiple(self):
        a = Book('test1', '', '', '')
        b = Book('test2', '', '', '')
        self.repo.insert_many([a, b])
        c = self.repo.count_all()
        assert c == 2

    def test_insert_vacio(self):
        self.repo.insert_many([])
        c = self.repo.count_all()
        assert c == 0

    def insertar_libros(self, n):
        books = [Book(f'test{b}', '', '', '') for b in range(n)]
        self.repo.insert_many(books)

    def test_replace(self):
        self.insertar_libros(1)
        a = self.repo.count_all()
        assert a == 1
        b = self.repo.find_one()
        b.nombre = 'test_replace'
        self.repo.replace_by_id(b.id, b)
        c = self.repo.count_all()
        assert c == 1
        d = self.repo.find_one()
        assert d.nombre == 'test_replace'
