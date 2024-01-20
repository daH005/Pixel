from __future__ import annotations
from pygame import Surface, Rect
from pygame.draw import rect as draw_rect
from random import randint

from game.map_.ui.dirt import Dirt as RealDirt
from game.contrib.annotations import SizeTupleType
from game.contrib.direction import Direction
from game.assets.images import (
    DirtImages,
    BricksImages,
    PlayerDefaultImages,
    COIN_IMAGES,
    FINISH_IMAGE,
    TREES_IMAGES,
    SlugImages,
    BatImages,
    SkeletonImages,
    HEART_IMAGES,
    SPIKE_IMAGE,
    HINT_IMAGES,
    LADDER_IMAGE,
    CHEST_IMAGES,
    SHIELD_IMAGES,
    CannonImages,
    SpiderImages,
    WaterImages,
)
from game.contrib.screen import screen
from game.contrib.colors import Color
from editor.map_ import (
    Map,
    MapObjectArgsJsonType,
    AbstractEditorMapObject,
    DEFAULT_FACTORY_METHOD_NAME,
)

__all__ = (
    'Dirt',
    'BackgroundDirt',
    'Bricks',
    'BackgroundBricks',
    'Player',
    'Coin',
    'Heart',
    'Chest',
    'Finish',
    'Tree',
    'Ladder',
    'Water',
    'Spike',
    'Slug',
    'Bat',
    'Skeleton',
    'Hint',
    'AbstractEditorEnemy',
    'Cannon',
    'Spider',
    'Shield',
)

ids: list[int] = []


def make_uid() -> int:
    while True:
        id_: int = randint(0, 1024)
        if id_ not in ids:
            return id_


class FixedBySquare(AbstractEditorMapObject):

    @classmethod
    def new_with_coords_fix(cls, *args, **kwargs) -> FixedBySquare:
        obj_ = cls(*args, **kwargs)
        obj_.rect.x -= obj_.rect.x % Map.BLOCK_SCALE
        obj_.rect.y -= obj_.rect.y % Map.BLOCK_SCALE
        return obj_


class FixedByLeftAndBottom(AbstractEditorMapObject):

    @classmethod
    def new_with_coords_fix(cls, *args, **kwargs) -> FixedByLeftAndBottom:
        obj_ = cls(*args, **kwargs)
        obj_.rect.x -= obj_.rect.x % Map.BLOCK_SCALE
        obj_.rect.bottom = obj_.rect.y + (-obj_.rect.y % Map.BLOCK_SCALE)
        return obj_


class FixedByBottom(AbstractEditorMapObject):

    @classmethod
    def new_with_coords_fix(cls, *args, **kwargs) -> FixedByBottom:
        obj_ = cls(*args, **kwargs)
        obj_.rect.bottom = obj_.rect.y + (-obj_.rect.y % Map.BLOCK_SCALE)
        obj_.rect.x -= obj_.rect.w // 2
        return obj_


class FixedByTop(AbstractEditorMapObject):

    @classmethod
    def new_with_coords_fix(cls, *args, **kwargs) -> FixedByTop:
        obj_ = cls(*args, **kwargs)
        obj_.rect.top = obj_.rect.y - (obj_.rect.y % Map.BLOCK_SCALE)
        obj_.rect.x -= obj_.rect.w // 2
        return obj_


@Map.add_object_type
class Dirt(FixedBySquare):
    Z_INDEX: int = 7
    size: SizeTupleType = DirtImages.DEFAULT.get_size()

    common_direction: Direction | None = None
    common_grass_enabled: bool = False

    def __init__(self, x: int, y: int,
                 direction: Direction | None = None,
                 grass_enabled: bool = False,
                 factory_method_name: str = DEFAULT_FACTORY_METHOD_NAME,
                 ) -> None:
        super().__init__(x, y, factory_method_name)
        if self.common_direction is not None:
            direction = self.common_direction
        self.direction = direction
        if grass_enabled:
            self.grass_enabled = grass_enabled
        else:
            self.grass_enabled = self.common_grass_enabled
        if direction is not None:
            self.image: Surface = RealDirt.EDGES_IMAGES[direction].copy()
        else:
            self.image: Surface = DirtImages.DEFAULT.copy()
        if self.grass_enabled:
            self.image.blit(DirtImages.GRASS_LIST[1], (0, 0))

    def _prepare_args(self) -> MapObjectArgsJsonType:
        return dict(
            **super()._prepare_args(),
            direction=self.direction,
            grass_enabled=self.grass_enabled,
        )


@Map.add_object_type
class BackgroundDirt(FixedBySquare):
    Z_INDEX: int = -2
    image: Surface = DirtImages.BACKGROUND
    size: SizeTupleType = DirtImages.BACKGROUND.get_size()


@Map.add_object_type
class Bricks(FixedBySquare):
    Z_INDEX: int = 7
    image: Surface = BricksImages.DEFAULT
    size: SizeTupleType = BricksImages.DEFAULT.get_size()


@Map.add_object_type
class BackgroundBricks(FixedBySquare):
    Z_INDEX: int = -2
    image: Surface = BricksImages.BACKGROUND
    size: SizeTupleType = BricksImages.DEFAULT.get_size()


@Map.add_object_type
class Finish(FixedBySquare):
    image: Surface = FINISH_IMAGE
    size: SizeTupleType = image.get_size()


@Map.add_object_type
class Tree(FixedByBottom):
    Z_INDEX = -3
    common_image_index: int = 0

    def __init__(self, x: int, y: int,
                 image_index: int | None = None,
                 factory_method_name: str = DEFAULT_FACTORY_METHOD_NAME,
                 ) -> None:
        if image_index is None:
            image_index = self.common_image_index
        self.image_index = image_index
        self.image: Surface = TREES_IMAGES[self.image_index]
        self.size: SizeTupleType = self.image.get_size()
        super().__init__(x, y, factory_method_name)

    def _prepare_args(self) -> MapObjectArgsJsonType:
        return dict(
            **super()._prepare_args(),
            image_index=self.image_index,
        )


@Map.add_object_type
class Spike(FixedByBottom):
    image: Surface = SPIKE_IMAGE
    size: SizeTupleType = image.get_size()


@Map.add_object_type
class Coin(FixedByBottom):
    Z_INDEX = 2
    image: Surface = COIN_IMAGES[0]
    size: SizeTupleType = image.get_size()

    def __init__(self, x: int, y: int,
                 id_: int | None = None,
                 factory_method_name: str = DEFAULT_FACTORY_METHOD_NAME,
                 ) -> None:
        super().__init__(x, y, factory_method_name)
        if id_ is None:
            id_ = make_uid()
        self.id = id_

    def _prepare_args(self) -> MapObjectArgsJsonType:
        return dict(
            **super()._prepare_args(),
            id_=self.id,
        )


@Map.add_object_type
class Heart(FixedByBottom):
    image: Surface = HEART_IMAGES[0]
    size: SizeTupleType = image.get_size()


@Map.add_object_type
class Shield(FixedByBottom):
    image: Surface = SHIELD_IMAGES[0]
    size: SizeTupleType = image.get_size()


@Map.add_object_type
class Chest(FixedByBottom):
    image: Surface = CHEST_IMAGES[0]
    size: SizeTupleType = image.get_size()

    def __init__(self, x: int, y: int,
                 id_: int | None = None,
                 factory_method_name: str = DEFAULT_FACTORY_METHOD_NAME,
                 ) -> None:
        super().__init__(x, y, factory_method_name)
        if id_ is None:
            id_ = make_uid()
        self.id = id_

    def _prepare_args(self) -> MapObjectArgsJsonType:
        return dict(
            **super()._prepare_args(),
            id_=self.id,
        )


@Map.add_object_type
class Player(FixedByBottom):
    image: Surface = PlayerDefaultImages.STAND
    size: SizeTupleType = image.get_size()


class AbstractEditorEnemy(FixedByBottom):

    def __init__(self, x: int, y: int,
                 start_x: int | None = None,
                 end_x: int | None = None,
                 factory_method_name: str = DEFAULT_FACTORY_METHOD_NAME,
                 ) -> None:
        super().__init__(x, y, factory_method_name)
        self.start_x = start_x
        self.end_x = end_x

    def _draw(self) -> None:
        super()._draw()
        if self.start_x is not None:
            self._draw_going_border(self.start_x)
        if self.end_x is not None:
            self._draw_going_border(self.end_x)

    def _draw_going_border(self, x: int) -> None:
        draw_rect(
            screen,
            Color.RED,
            self.map.camera.apply(Rect(
                x, self.rect.y,
                5, self.rect.h
            ))
        )

    def _prepare_args(self) -> MapObjectArgsJsonType:
        return dict(
            **super()._prepare_args(),
            start_x=self.start_x,
            end_x=self.end_x,
        )


@Map.add_object_type
class Slug(AbstractEditorEnemy):
    image: Surface = SlugImages.GO[0]
    size: SizeTupleType = image.get_size()


@Map.add_object_type
class Bat(AbstractEditorEnemy):
    image: Surface = BatImages.GO_RIGHT[0]
    size: SizeTupleType = image.get_size()


@Map.add_object_type
class Skeleton(AbstractEditorEnemy):
    image: Surface = SkeletonImages.GO_RIGHT[0]
    size: SizeTupleType = image.get_size()


@Map.add_object_type
class Hint(FixedByBottom):
    Z_INDEX = 10
    image: Surface = HINT_IMAGES[0]
    size: SizeTupleType = image.get_size()

    def __init__(self, x: int, y: int,
                 text: str | None = None,
                 factory_method_name: str = DEFAULT_FACTORY_METHOD_NAME,
                 ) -> None:
        if text is None:
            text = '<FILL ME>'
        self.text = text
        super().__init__(x, y, factory_method_name)

    def _prepare_args(self) -> MapObjectArgsJsonType:
        return dict(
            **super()._prepare_args(),
            text=self.text,
        )


@Map.add_object_type
class Ladder(FixedBySquare):
    image: Surface = LADDER_IMAGE
    size: SizeTupleType = image.get_size()


@Map.add_object_type
class Water(FixedByLeftAndBottom):
    Z_INDEX: int = 6
    common_top: bool = False

    def __init__(self, x: int, y: int,
                 is_top: bool | None = None,
                 factory_method_name: str = DEFAULT_FACTORY_METHOD_NAME,
                 ) -> None:
        if is_top is None:
            is_top = self.common_top
        self.is_top = is_top
        if is_top:
            self.image: Surface = WaterImages.TOP
        else:
            self.image: Surface = WaterImages.DEFAULT
        self.size: SizeTupleType = self.image.get_size()
        super().__init__(x, y, factory_method_name)

    def _prepare_args(self) -> MapObjectArgsJsonType:
        return dict(
            **super()._prepare_args(),
            is_top=self.is_top,
        )


@Map.add_object_type
class Cannon(FixedByBottom):
    image: Surface = CannonImages.DEFAULT_RIGHT
    size: SizeTupleType = image.get_size()

    def __init__(self, x: int, y: int,
                 end_x: int | None = None,
                 factory_method_name: str = DEFAULT_FACTORY_METHOD_NAME,
                 ) -> None:
        self.end_x = end_x
        super().__init__(x, y, factory_method_name)

    def _update_image(self) -> None:
        if self.end_x is not None:
            if self.rect.centerx < self.end_x:
                self.image = CannonImages.DEFAULT_RIGHT
            else:
                self.image = CannonImages.DEFAULT_LEFT

    def _draw(self) -> None:
        super()._draw()
        if self.end_x is not None:
            self._draw_end_border()

    def _draw_end_border(self) -> None:
        draw_rect(
            screen,
            Color.GOLD,
            self.map.camera.apply(Rect(
                self.end_x, self.rect.y,
                5, self.rect.h
            ))
        )

    def _prepare_args(self) -> MapObjectArgsJsonType:
        return dict(
            **super()._prepare_args(),
            end_x=self.end_x,
        )


@Map.add_object_type
class Spider(FixedByTop):
    image: Surface = SpiderImages.STAND
    size: SizeTupleType = image.get_size()

    def __init__(self, x: int, y: int,
                 end_y: int | None = None,
                 factory_method_name: str = DEFAULT_FACTORY_METHOD_NAME,
                 ) -> None:
        self.end_y = end_y
        super().__init__(x, y, factory_method_name)

    def _draw(self) -> None:
        super()._draw()
        if self.end_y is not None:
            self._draw_end_border()

    def _draw_end_border(self) -> None:
        draw_rect(
            screen,
            Color.GREEN,
            self.map.camera.apply(Rect(
                self.rect.x, self.end_y,
                self.rect.w, 3
            ))
        )

    def _prepare_args(self) -> MapObjectArgsJsonType:
        return dict(
            **super()._prepare_args(),
            end_y=self.end_y,
        )
