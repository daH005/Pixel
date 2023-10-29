from pygame.mixer import init as init_mixer, Sound, Channel
from pathlib import Path

# from pygame.mixer_music import queue

from game.config import GameConfig

__all__ = (
    'mainscreen_music',
    'play_mainscreen_music',
    'level_music',
    'level_ending_music',
    'coin_sound',
    'heart_sound',
    'hit_sound',
    'shield_sound',
    'slug_sound',
    'cannon_sound',
)

init_mixer()
SOUNDS_PATH: Path = GameConfig.ASSETS_PATH.joinpath('sounds')

mainscreen_music: Sound = Sound(SOUNDS_PATH.joinpath('mainscreen.wav'))
level_music: Sound = Sound(SOUNDS_PATH.joinpath('level.wav'))
level_ending_music: Sound = Sound(SOUNDS_PATH.joinpath('level_ending.wav'))
coin_sound: Sound = Sound(SOUNDS_PATH.joinpath('coin.wav'))
heart_sound: Sound = Sound(SOUNDS_PATH.joinpath('heart.wav'))
hit_sound: Sound = Sound(SOUNDS_PATH.joinpath('hit.wav'))
shield_sound: Sound = Sound(SOUNDS_PATH.joinpath('shield.wav'))
slug_sound: Sound = Sound(SOUNDS_PATH.joinpath('slug.wav'))
cannon_sound: Sound = Sound(SOUNDS_PATH.joinpath('cannon.wav'))


def play_mainscreen_music() -> None:
    if mainscreen_music.get_num_channels() == 0:
        mainscreen_music.play(-1)
