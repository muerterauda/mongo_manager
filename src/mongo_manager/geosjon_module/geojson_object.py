import geojson

from mongo_manager import ObjetoMongoAbstract


class GeoJsonObjetoMongoAbstract(ObjetoMongoAbstract):

    def __init__(self, _id=None, **kwargs):
        super().__init__(_id=_id, **kwargs)

    def get_dict(self, id_mongo=True, id_as_string=False, include_private_false=False) -> dict:
        dictionary = super().get_dict(id_mongo, id_as_string, include_private_false)
        for x in GeoJsonObjetoMongoAbstract.get_attr_geojson_objects():
            dictionary[x] = geojson.dumps(dictionary[x])
        return dictionary

    @staticmethod
    def preparate_dict_for_geojson_objects(dictionary: dict, attr: list) -> dict:
        for x in attr:
            obj = dictionary.get(x, None)
            if obj is None:
                continue
            if isinstance(obj, list):
                dictionary[x] = [geojson.loads(o) for o in obj]
            else:
                dictionary[x] = geojson.loads(obj)
        return dictionary

    @classmethod
    def generar_object_from_dict(cls, dictionary):
        if dictionary is None:
            return None
        super_dict = cls.prepare_dict_for_generated_object(dictionary, cls.get_attr_nested_objects())
        final_dict = cls.preparate_dict_for_geojson_objects(super_dict, cls.get_attr_geojson_objects())
        return cls(**final_dict)

    @staticmethod
    def get_attr_geojson_objects() -> list:
        """
        Attributes which are objects of the class Geojson,
         all of them. Override parents methods.
        @return: dict format {name_attr: class_attr}
        """
        return []
