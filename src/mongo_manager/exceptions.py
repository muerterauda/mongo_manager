class MongoManagerException(Exception):
    """Default exception for Mongo Manager"""

    def __init__(self, *args):
        default_message = ('\nNo se ha inicializado la base de datos, '
                           'crear con MongoManager(), ni se ha dado una conexion al repositorio.'
                           '\nMongoManager is not initialized, '
                           'create it with MongoManager(), '
                           'or provide a different connection to the repository.')
        args = (default_message,) if not args else args
        super().__init__(*args)


class MongoManagerGridFSException(Exception):
    """GridFS exception for Mongo Manager"""


class MongoManagerAggregationException(Exception):
    """Aggregation exception for Mongo Manager"""
