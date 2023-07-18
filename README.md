# Mongo Manager (0.9.0.BETA)

Libreria para el manejo de Objetos almacenados en base de datos MongoDB

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
MongoClient para la coleccion a tratar por el repositorio.

### Aggregates

Todavia no se han implementado ninguna clase que las trate a fondo, pero se pueden
usar la mayoria de las *stages* y *operators* definidos en mongo_utils. Una vez definida la clase o 
clases para tratar los Aggregates se compenetrara con estas funciones.

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
        def __init__(self) -> None:
            super().__init__('book', Book)

    class RepositoryBookOverrided(RepositoryBase[BookOverrided]):
        def __init__(self) -> None:
            super().__init__('book', BookOverrided)

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
