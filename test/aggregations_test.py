from test.abstract_mongo_manager_test import AbstractMongoManagerTest
from src.mongo_manager import RepositoryBase
from src.mongo_manager.aggregations import (agg_de, agg_st,
                                            AggregationExecutor)
from test.classes_test import Book


class RepositoryBook(RepositoryBase[Book]):
    def __init__(self) -> None:
        super().__init__('book', Book)

    @agg_de.aggregation_decorator
    def aggregation_1(self, agg: AggregationExecutor):
        b = agg_st.AggStGroup(id_mapping={'name': '$nombre'})
        b['counter'] = {'$sum': 1}
        c = agg_st.AggStProject({'name': '$_id.name', 'counter': 1, '_id': 0})
        agg.add_steps(b, c)
        return agg


class TestAgreggation(AbstractMongoManagerTest):

    def setUp(self) -> None:
        self.repo = RepositoryBook()

    def tearDown(self) -> None:
        self.repo.drop_collection(drop=True)
        del self.repo

    def test_aggregation_pipeline(self):
        a = Book('test_aggregation', '', '', '')
        b = Book('test_aggregation', '', '', '')
        c = Book('test_aggregation2', '', '', '')
        self.repo.insert_many([a, b, c])
        d = self.repo.aggregation_1()
        assert len(d) == 2
        e = list(filter(lambda x: x['name'] == 'test_aggregation', d))[0]
        f = list(filter(lambda x: x['name'] == 'test_aggregation2', d))[0]
        assert e['counter'] == 2 and f['counter'] == 1
