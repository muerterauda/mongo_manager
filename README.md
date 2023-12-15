# Mongo Manager (0.9.7)

Libreria para el manejo de Objetos almacenados en base de datos MongoDB.

Testeado el funcionamiento basico en Python 3.7, 3.8, 3.9, 3.10, 3.11 y 3.12 y para las versiones de Mongo 4.2, 4.4, 5.0 y 6.0.

## Clases

### MongoManager

Crea la conexion con la base de datos, se debe inicilizar antes de 
invocar ningun repositorio de objetos.

### ObjetoMongoAbstract

Clase abstracta en la que se representa un objeto mongo predefinido,
su constructor recibe un object _id haciendo referencia al '_id' del
objeto Mongo y **kwargs con los argumentos desechados por el
constructor concreto de tu clase. Es recomendable llamar al contructor 
padre para establecer los atributos.

### Objetos internos

En caso de tener objetos interno dentro del objeto principal es necesario
reescribir las funciones internas get_dict y generar_object_from_dict de 
forma que el objeto se transforme y destransforme en un diccionario.

En caso de que el objeto o la lista de objetos internos hereden de la clase ObjetoMongoAbstract
se puede modificar el metodo get_attr_nested_objects de la siguiente manera
*{nombre_atributo: clase_atributo(aunque sea una lista)}* y automaticamente se instanciaran y desinstanciaran
solos.

### RepositoryBase

Repositorio base de mongo, recibe como parametros en el constructor,
la coleccion a la que se hace referencia y el objeto al que va a convertir
los resultados de las query que se realicen.

En caso de querer usar una coleccion no perteneciente a la base de datos instanciada,
se puede pasar el atributo *connection_collection* que debe ser una instancia de la conexion 
*MongoClient* para la coleccion a tratar por el repositorio.

## Ejemplo 1

En este ejemplo veremos el uso de la libreria definiendo un objeto <i>Book</i> 
que hereda de ObjetoMongoAbstract y para el que implementa un <i>RepositoryBook</i>
 para poder manejar el objeto de manera más comoda.

    class Book(ObjetoMongoAbstract):
            def __init__(self, name, id_mongo=None, **kwargs):
                super().__init__(id_mongo, **kwargs)
                self.name = name
        
            def __str__(self) -> str:
                return "{}".format(self.name)

    class BookOverrided(ObjetoMongoAbstract):
            def __init__(self, name, id_mongo=None, **kwargs):
                super().__init__(id_mongo, **kwargs)
                self.name = name

            def get_dict(self, id_mongo=True, id_as_string=False) -> dict:
                d = super().get_dict(id_mongo, id_as_string)
                d.pop('name')
                d['nombre'] = self.name
                return d
        
            @classmethod
            def generar_object_from_dict(cls, dictionary):
                if dictionary is None:
                    return None
                return cls(name=dictionary.get('nombre'))


            def __str__(self) -> str:
                return "{}".format(self.name)

    class RepositoryBook(RepositoryBase[Book]):
        def __init__(self, conection_collection=None) -> None:
            super().__init__('book', Book, conection_collection)

    class RepositoryBookOverrided(RepositoryBase[BookOverrided]):
        def __init__(self, conection_collection=None) -> None:
            super().__init__('book', BookOverrided, conection_collection)

    def main():
        a = RepositoryBook()
        b = Book('test')
        c = RepositoryBookOverrided()
        d = BookOverrided('test')
        a.insert_one(b)
        c.insert_one(d)
        print(a.find_all()[-1])
        print(c.find_all()[-1])


    if __name__ == '__main__':
        MongoManager('user', 'psw', 'bd', 'authenticationDatabase')
        main()


### Aggregates

Los Aggregates se han dispuesto para poder ser creados de dos maneras distintas.

 - Usando los decoradores definidos en el fichero _aggregation_decorator.py_ en combinacion
con las clases _AggregationStage_ y _AggregationOperation_ cuyos hijos implementan los distintas 
funciones permitidas en MongoDB, asi como los parametros que reciben.

   El decorador permite a la función definida dentro de una clase que herede de _RepositoryBase_, recibir un
AggregationExecutor que se ejecutar una vez finalizada la función, para ello todas las funciones usen estos decoradores
deberán devolver dicho parametro.

   Un ejemplo se puede ver a continuación, en el que se realiza un match a todos los libros que tengan en su nombre una *s* mayuscula 
o minuscula, agrupa el resultado por nombre y cuenta los integrantes de cada grupo y finalmente genera el resultado con
el formato {name: book_name_group, counter: total_books}:

       class RepositoryBook(RepositoryBase[Book]):
           def __init__(self, conection_collection=None) -> None:
               super().__init__('book', Book, conection_collection)
       
           @agg_de.aggregation_decorator
           def test_aggregation(self, agg: AggregationExecutor):
               a = agg_st.AggStMatch()
               a['nombre'] = agg_op_re.AggOpRegex('test',
                                                  agg_op_re.AggOpRegex.get_options_regex(insensitive=True))
               b = agg_st.AggStGroup(id_mapping={'name': '$name'})
               b['counter'] = {'$sum': 1}
               c = agg_st.AggStProject({'name': '$_id.name', 'counter': 1})
               agg.add_steps(a, b, c)
               return agg

 - Usando los antigüos metodos definidos en el _mongo_utils.py_ que sirven de ayuda para poder generar los aggregates.
