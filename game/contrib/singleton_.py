from __future__ import annotations
from abc import ABCMeta

__all__ = (
    'SingletonMeta',
    'SingletonABCMeta',
)


class SingletonMeta(type):
    """Метакласс для реализации шаблона 'Одиночка'.
    Методы `__new__` и `__init__` вызываются
    исключительно один единственный раз при первом
    создании экземпляра класса.
    """

    __instances: dict[type, object] = {}

    def __call__(cls, *args, **kwargs) -> object:
        if cls not in cls.__instances:
            cls.__instances[cls] = super().__call__(*args, **kwargs)
        return cls.__instances[cls]


class SingletonABCMeta(SingletonMeta, ABCMeta):
    """Метакласс для реализации шаблона 'Одиночка' для абстрактных классов."""
    pass
