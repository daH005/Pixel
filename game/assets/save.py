from engine.common.files import save_json, load_json
from game.config import GameConfig

__all__ = (
    'get_coins_count',
    'set_coins_count',
)

FILE_PATH = GameConfig.ASSETS_PATH.joinpath('save.json')


def get_coins_count() -> int:
    return load_json(FILE_PATH)['coins_count']


def set_coins_count(count: int) -> None:
    return save_json(FILE_PATH, dict(coins_count=count))
