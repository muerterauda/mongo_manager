from __future__ import annotations

import json
from abc import ABC

from bson import ObjectId
from pymongo.cursor import Cursor


class ObjetoMongoAbstract(ABC):

    def __init__(self, _id=None, **kwargs):
        self._id = _id
        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def id(self) -> ObjectId:
        return self._id

    def get_dict(self, id_mongo=True, id_as_string=False) -> dict:
        """
        Return all variables from this object, similar to vars(object)
         with exception for _id
        @param id_mongo: True -> Return dict with _id
        @param id_as_string: True -> Return _id as str if id_mongo is True
        @return: dict with object variables, similar to vars(object)
        """
        d = vars(self).copy()
        if not id_mongo:
            d.pop('_id')
        elif id_as_string and self._id is not None:
            d['_id'] = str(self._id)
        for x, y in self.get_attr_nested_objects().items():
            obj = d.get(x, None)
            if obj is None:
                continue
            if isinstance(obj, list):
                d[x] = y.generar_list_dicts_from_list_objects(d[x], False, False)
            else:
                d[x] = d[x].get_dict(False, False)
        return d

    def get_dict_no_id(self) -> dict:
        """
        Facade for get_dict(id_mongo=False). Return all variables from this object,
         similar to vars(object)
         with exception for _id
        @return: dict with object variables, similar to vars(object)
        """
        return self.get_dict(id_mongo=False)

    def serialize(self, id_mongo=True) -> str:
        """
        Serialize object to JSON format
        @param id_mongo: True -> Append _id to json
        @return: str in Json format
        """
        return json.dumps(self.get_dict(id_mongo=id_mongo, id_as_string=True))

    @staticmethod
    def serialize_all(objetos, id_mongo=True) -> str:
        """
        Serialize all objects to JSON format
        @param objetos: List for object to convert to JSON
        @param id_mongo: True -> Append _id to json
        @return: str in Json format
        """
        return json.dumps(
            ObjetoMongoAbstract.generar_list_dicts_from_list_objects(objetos,
                                                                     id_mongo=id_mongo,
                                                                     id_as_string=True))

    @staticmethod
    def prepare_dict_for_generated_object(dictionary: dict, attr: dict) -> dict:
        for x, y in attr.items():
            obj = dictionary.get(x, None)
            if obj is None:
                continue
            if isinstance(obj, list):
                dictionary[x] = y.generar_objects_from_list_dicts(obj)
            else:
                dictionary[x] = y.generar_object_from_dict(obj)
        return dictionary

    @classmethod
    def generar_object_from_dict(cls, dictionary):
        if dictionary is None:
            return None
        return cls(**cls.prepare_dict_for_generated_object(
            dictionary, cls.get_attr_nested_objects()))

    def __repr__(self):
        return str(self.get_dict(True, True))

    def __str__(self):
        return f'Class: {self.__class__.__name__} -> ObjectID {self._id}'

    @classmethod
    def generar_objects_from_list_dicts(cls, dictionaries: list | Cursor):
        return [cls.generar_object_from_dict(dictionary) for dictionary in dictionaries]

    @staticmethod
    def generar_list_dicts_from_list_objects(lista_objetos: list,
                                             id_mongo=True, id_as_string=False):
        return [c.get_dict(id_mongo=id_mongo, id_as_string=id_as_string)
                for c in lista_objetos]

    @staticmethod
    def get_attr_nested_objects() -> dict:
        """
        Attributes which are objects of the class ObjetoMongoAbstract,
         all of them. Override parents methods.
        @return: dict format {name_attr: class_attr}
        """
        return {}
