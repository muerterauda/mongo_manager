from threading import Lock


class UnsafeSingletonDestruction(Exception):
    pass


class SingletonMeta(type):
    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        key = (cls, args, frozenset(kwargs.items()))
        with cls._lock:
            if key not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                instance._singleton_key = key  # Guardar la clave en la instancia
                cls._instances[key] = instance
        return cls._instances[key]

    @classmethod
    def _destroy_all(cls, target_cls, *, destroy=False):
        """
        Elimina todas las instancias Singleton de una clase específica.
        """
        if destroy:
            with cls._lock:
                cls._instances = {
                    key: inst for key, inst in cls._instances.items() if key[0] != target_cls
                }
        else:
            raise UnsafeSingletonDestruction(f'Attempt to destroy all instance of {cls.__name__} without confirmation.')
