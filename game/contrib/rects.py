from pygame import Rect
from typing import Any

__all__ = (
    'FloatRect',
)


class FloatRect(Rect):
    """Подкласс `Rect`, позволяющий хранить дробные Х и У координаты.
    `FloatRect` предоставляет два новых свойства - `float_x` и `float_y`
    для перемещения прямоугольника с "дробной" скоростью.
    При этом класс гарантирует взаимосвязь `float_x` с `x`, `float_y` с `y`,
    а также и тех и других со свойствами типа `topleft`, `bottomleft` и др.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.float_x: float = self.x
        self.float_y: float = self.y

    def __setattr__(self, key: str, value: int | float | Any) -> None:
        old_x = self.x
        old_y = self.y
        super().__setattr__(key, value)
        if self.x != old_x:
            super().__setattr__('float_x', self.x)
        if self.y != old_y:
            super().__setattr__('float_y', self.y)
        if key == 'float_x':
            super().__setattr__('x', int(self.float_x))
        elif key == 'float_y':
            super().__setattr__('y', int(self.float_y))
