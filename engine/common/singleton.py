from abc import ABCMeta

__all__ = (
    'SingletonMeta',
    'SingletonABCMeta',
)


class SingletonMeta(type):
    __instances: dict[type, object] = {}

    def __call__(cls, *args, **kwargs) -> object:
        if cls not in cls.__instances:
            cls.__instances[cls] = super().__call__(*args, **kwargs)
        return cls.__instances[cls]


class SingletonABCMeta(SingletonMeta, ABCMeta):
    pass
