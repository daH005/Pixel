from pygame.image import load as load_
from pygame import Surface, SRCALPHA
from pygame.transform import flip
from pygame.draw import rect as draw_rect
from os import listdir
from typing import TypeAlias
from pathlib import Path

from game.config import GameConfig
from engine.common.colors import Color

__all__ = (
    'ImagesListType',
    'ICON_IMAGE',
    'SUN_IMAGE',
    'FINISH_IMAGE',
    'CLOUDS_IMAGES',
    'COIN_IMAGES',
    'HEART_IMAGES',
    'LOST_HEART_IMAGE',
    'TREES_IMAGES',
    'SPIKE_IMAGE',
    'HINT_IMAGES',
    'LADDER_IMAGE',
    'CHEST_IMAGES',
    'SHIELD_IMAGES',
    'BatImages',
    'BackgroundImages',
    'DirtImages',
    'BricksImages',
    'PlayerDefaultImages',
    'PlayerDefaultWhiteImages',
    'SlugImages',
    'SkeletonImages',
    'CannonImages',
    'SpiderImages',
    'GhostImages',
    'WaterImages',
    'WebImages',
)

ImagesListType: TypeAlias = list[Surface]


def load_image(path: Path, extension: str | None = 'png') -> Surface:
    if extension is not None:
        path: str = str(path) + '.' + extension
    return optimize(load_(path))


def load_images(path: Path) -> ImagesListType:
    images: ImagesListType = []
    for filename in sorted(listdir(path), key=get_index_from_filename):
        images.append(load_image(path.joinpath(filename), extension=None))
    return images


def get_index_from_filename(filename: str) -> int:
    return int(filename.split('.')[0])


def optimize(image: Surface) -> Surface:
    optimized_image = Surface(image.get_size(), SRCALPHA)
    optimized_image.blit(image, (0, 0))
    return optimized_image


def whitewash(image: Surface) -> Surface:
    image = image.copy()
    for y in range(image.get_height()):
        for x in range(image.get_width()):
            pixel_color = image.get_at((x, y))
            if pixel_color[3]:
                draw_rect(image, Color.WHITE, (x, y, 1, 1))
    return image


def whitewash_many(images: ImagesListType) -> ImagesListType:
    whitewashed_images: ImagesListType = []
    for image in images:
        whitewashed_images.append(whitewash(image))
    return whitewashed_images


def flip_many(images: ImagesListType,
              x_bool: bool = True,
              y_bool: bool = False,
              ) -> ImagesListType:
    flipped_images: ImagesListType = []
    for image in images:
        flipped_images.append(
            flip(image, x_bool, y_bool)
        )
    return flipped_images


ICON_IMAGE: Surface = load_image(GameConfig.IMAGES_PATH.joinpath('icons/icon'), extension='ico')
SUN_IMAGE: Surface = load_image(GameConfig.IMAGES_PATH.joinpath('sun'))
FINISH_IMAGE: Surface = load_image(GameConfig.IMAGES_PATH.joinpath('finish'))
CLOUDS_IMAGES: ImagesListType = load_images(GameConfig.IMAGES_PATH.joinpath('clouds'))
COIN_IMAGES: ImagesListType = load_images(GameConfig.IMAGES_PATH.joinpath('coin'))
HEART_IMAGES: ImagesListType = load_images(GameConfig.IMAGES_PATH.joinpath('heart/as_item'))
LOST_HEART_IMAGE: Surface = HEART_IMAGES[0].copy()
LOST_HEART_IMAGE.set_alpha(100)
TREES_IMAGES: ImagesListType = load_images(GameConfig.IMAGES_PATH.joinpath('trees'))
SPIKE_IMAGE: Surface = load_image(GameConfig.IMAGES_PATH.joinpath('spike'))
HINT_IMAGES: ImagesListType = load_images(GameConfig.IMAGES_PATH.joinpath('hint'))
LADDER_IMAGE: Surface = load_image(GameConfig.IMAGES_PATH.joinpath('ladder'))
CHEST_IMAGES: ImagesListType = load_images(GameConfig.IMAGES_PATH.joinpath('chest'))
SHIELD_IMAGES: ImagesListType = load_images(GameConfig.IMAGES_PATH.joinpath('shield'))


class BackgroundImages:

    __PATH: Path = GameConfig.IMAGES_PATH.joinpath('backgrounds')
    HOME: Surface = load_image(__PATH.joinpath('home'))
    BOTTOM_HOME_BORDER: Surface = load_image(__PATH.joinpath('home_border'))
    TOP_HOME_BORDER: Surface = flip(BOTTOM_HOME_BORDER, flip_x=False, flip_y=True)
    MAP: Surface = load_image(__PATH.joinpath('map'))


class DirtImages:

    __PATH: Path = GameConfig.IMAGES_PATH.joinpath('dirt')
    DEFAULT: Surface = load_image(__PATH.joinpath('default'))
    BACKGROUND: Surface = load_image(__PATH.joinpath('background'))
    LEFT: Surface = load_image(__PATH.joinpath('left'))
    RIGHT: Surface = load_image(__PATH.joinpath('right'))
    GRASS_LIST: ImagesListType = load_images(__PATH.joinpath('grass'))


class BricksImages:

    __PATH: Path = GameConfig.IMAGES_PATH.joinpath('bricks')
    DEFAULT: Surface = load_image(__PATH.joinpath('default'))
    BACKGROUND: Surface = load_image(__PATH.joinpath('background'))


class PlayerDefaultImages:

    __PATH: Path = GameConfig.IMAGES_PATH.joinpath('player/default')
    STAND_RIGHT: ImagesListType = load_images(__PATH.joinpath('stand'))
    STAND_LEFT: ImagesListType = flip_many(STAND_RIGHT)
    GO_RIGHT: ImagesListType = load_images(__PATH.joinpath('go'))
    GO_LEFT: ImagesListType = flip_many(GO_RIGHT)
    GO_VERTICAL: ImagesListType = load_images(__PATH.joinpath('go_vertical'))


class PlayerDefaultWhiteImages:

    STAND_RIGHT: ImagesListType = whitewash_many(PlayerDefaultImages.STAND_RIGHT)
    STAND_LEFT: ImagesListType = whitewash_many(PlayerDefaultImages.STAND_LEFT)
    GO_RIGHT: ImagesListType = whitewash_many(PlayerDefaultImages.GO_RIGHT)
    GO_LEFT: ImagesListType = whitewash_many(PlayerDefaultImages.GO_LEFT)
    GO_VERTICAL: ImagesListType = whitewash_many(PlayerDefaultImages.GO_VERTICAL)


class SlugImages:

    __PATH: Path = GameConfig.IMAGES_PATH.joinpath('slug')
    GO: ImagesListType = load_images(__PATH.joinpath('go'))
    DEATH: ImagesListType = load_images(__PATH.joinpath('death'))


class BatImages:

    GO_RIGHT: ImagesListType = load_images(GameConfig.IMAGES_PATH.joinpath('bat'))
    GO_LEFT: ImagesListType = flip_many(GO_RIGHT)


class SkeletonImages:

    __PATH: Path = GameConfig.IMAGES_PATH.joinpath('skeleton')
    GO_RIGHT: ImagesListType = load_images(__PATH.joinpath('go'))
    GO_LEFT: ImagesListType = flip_many(GO_RIGHT)
    ATTACK_RIGHT: ImagesListType = load_images(__PATH.joinpath('attack'))
    ATTACK_LEFT: ImagesListType = flip_many(ATTACK_RIGHT)


class CannonImages:

    __PATH: Path = GameConfig.IMAGES_PATH.joinpath('cannon')
    DEFAULT_RIGHT: Surface = load_image(__PATH.joinpath('cannon/default'))
    DEFAULT_LEFT: Surface = flip(DEFAULT_RIGHT, flip_x=True, flip_y=False)
    SHOOT_RIGHT: ImagesListType = load_images(__PATH.joinpath('cannon/shoot'))
    SHOOT_LEFT: ImagesListType = flip_many(SHOOT_RIGHT)

    class CannonballImages:

        __PATH: Path = GameConfig.IMAGES_PATH.joinpath('cannon/cannonball')
        DEFAULT: Surface = load_image(__PATH.joinpath('default'))
        DEATH: ImagesListType = load_images(__PATH.joinpath('death'))


class SpiderImages:

    __PATH: Path = GameConfig.IMAGES_PATH.joinpath('spider')
    STAND: Surface = load_image(__PATH.joinpath('stand'))
    GO: ImagesListType = load_images(__PATH.joinpath('go'))


class GhostImages:

    __PATH: Path = GameConfig.IMAGES_PATH.joinpath('ghost')
    GO_LEFT: Surface = load_image(__PATH.joinpath('go'))
    GO_LEFT.set_alpha(155)
    GO_RIGHT: Surface = flip(GO_LEFT, flip_x=True, flip_y=False)
    GO_RIGHT.set_alpha(155)
    ATTACK_LEFT: Surface = load_image(__PATH.joinpath('attack'))
    # ATTACK_LEFT.set_alpha(100)
    ATTACK_RIGHT: Surface = flip(ATTACK_LEFT, flip_x=True, flip_y=False)
    # ATTACK_RIGHT.set_alpha(100)


class WaterImages:

    ALPHA: int = 225
    __PATH: Path = GameConfig.IMAGES_PATH.joinpath('water')
    DEFAULT: Surface = load_image(__PATH.joinpath('default'))
    DEFAULT.set_alpha(ALPHA)
    TOP: Surface = load_image(__PATH.joinpath('top'))
    TOP.set_alpha(ALPHA)


class WebImages:

    LEFT: Surface = load_image(GameConfig.IMAGES_PATH.joinpath('left_web'))
    RIGHT: Surface = load_image(GameConfig.IMAGES_PATH.joinpath('right_web'))
