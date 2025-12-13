from pygame import Rect
from typing import Any

__all__ = (
    'FloatRect',
)


class FloatRect(Rect):

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

    def __copy__(self) -> 'FloatRect':
        return FloatRect(self)
