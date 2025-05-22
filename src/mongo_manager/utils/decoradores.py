import warnings
import functools


def experimental_stage(stage="alpha"):
    """Decorador para marcar funciones o clases como alpha, beta, etc."""

    def decorator(obj):
        message = f"{obj.__name__} está en fase {stage.upper()} y puede cambiar en futuras versiones."

        if isinstance(obj, type):
            original_init = obj.__init__

            @functools.wraps(original_init)
            def new_init(self, *args, **kwargs):
                warnings.warn(message, category=UserWarning, stacklevel=2)
                return original_init(self, *args, **kwargs)

            obj.__init__ = new_init
            return obj
        else:
            @functools.wraps(obj)
            def wrapper(*args, **kwargs):
                warnings.warn(message, category=UserWarning, stacklevel=2)
                return obj(*args, **kwargs)

            return wrapper

    return decorator
