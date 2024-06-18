from pygame.mixer import init as init_mixer, Sound

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


def load_sound(sound_name: str) -> Sound:
    return Sound(GameConfig.SOUNDS_PATH.joinpath(sound_name + '.wav'))


def play_mainscreen_music() -> None:
    if mainscreen_music.get_num_channels() == 0:
        mainscreen_music.play(-1)


mainscreen_music: Sound = load_sound('mainscreen')
level_music: Sound = load_sound('level')
level_ending_music: Sound = load_sound('level_ending')
coin_sound: Sound = load_sound('coin')
heart_sound: Sound = load_sound('heart')
hit_sound: Sound = load_sound('hit')
shield_sound: Sound = load_sound('shield')
slug_sound: Sound = load_sound('slug')
cannon_sound: Sound = load_sound('cannon')
