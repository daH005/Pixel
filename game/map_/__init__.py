"""Модуль формирует полностью готовый к работе класс `Map`."""

from game.map_.map_ import Map
from game.map_.ui.player import Player
from game.map_.ui.barrier import InvisibleBarrier
from game.map_.ui.dirt import Dirt, BackgroundDirt
from game.map_.ui.bricks import Bricks, BackgroundBricks
from game.map_.ui.finish import Finish
from game.map_.ui.ladder import Ladder
from game.map_.ui.water import Water
from game.map_.ui.tree import Tree
from game.map_.ui.spike import Spike
from game.map_.ui.cannon import Cannon
from game.map_.ui.slug import Slug
from game.map_.ui.bat import Bat
from game.map_.ui.skeleton import Skeleton
from game.map_.ui.spider import Spider
from game.map_.ui.coin import Coin
from game.map_.ui.heart import Heart
from game.map_.ui.shield import Shield
from game.map_.ui.chest import Chest
from game.map_.ui.hint import Hint

__all__ = (
    'Map',
)
