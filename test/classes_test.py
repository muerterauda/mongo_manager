from src.mongo_manager import ObjetoMongoAbstract


class Book(ObjetoMongoAbstract):

    def __init__(self, nombre, tipo, demografia, link,
                 _id=None, **kwargs):
        super().__init__(_id, **kwargs)
        self.nombre = nombre
        self.tipo = tipo
        self.demografia = demografia
        self.link = link

    def __str__(self) -> str:
        return "{} - {}: {}".format(self.tipo,
                                    self.demografia,
                                    self.nombre)

    @staticmethod
    def get_attr_nested_objects() -> dict:
        return {}

