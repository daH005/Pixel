from pygame import Rect
from pygame.draw import rect as draw_rect

from game.assets.images import SpiderImages
from game.contrib.counters import FramesCounter
from game.contrib.annotations import SizeTupleType
from game.contrib.rects import FloatRect
from game.contrib.colors import Color
from game.map_.map_ import Map
from game.map_.abstract_ui import AbstractMovingAndInteractingWithPlayerMapObject
from game.contrib.screen import screen

__all__ = (
    'Spider',
)


@Map.add_object_type
class Spider(AbstractMovingAndInteractingWithPlayerMapObject):
    size: SizeTupleType = SpiderImages.STAND.get_size()
    RectType: type[FloatRect] = FloatRect
    SPEED: float = 1.75
    GO_ANIM_DELAY: float = 0.075
    SPIDERWEB_W: int = 2

    def __init__(self, x: int, y: int,
                 end_y: int,
                 ) -> None:
        super().__init__(x, y)
        self.start_y = y
        self.end_y = end_y
        self.go_frames_counter: FramesCounter = FramesCounter(
            frames_count=len(SpiderImages.GO),
            transition_delay_as_seconds=self.GO_ANIM_DELAY,
        )
        self.y_vel: float = 0
        self.attack_rect: Rect = Rect(self.rect.x, self.start_y, self.rect.w, self.end_y - self.start_y)

    def _move(self) -> None:
        self.y_vel = 0
        if self.attack_rect.colliderect(self.map.player.rect):
            if self.rect.bottom < self.map.player.rect.y:
                self.y_vel = self.SPEED
        elif self.rect.y > self.start_y:
            self.y_vel = -self.SPEED
        self.rect.float_y += self.y_vel

    def _handle_collision_with_player(self) -> None:
        self.map.player.hit()

    def _update_image(self) -> None:
        if self.y_vel:
            self.image = SpiderImages.GO[self.go_frames_counter.current_index]
            self.go_frames_counter.next()
        else:
            self.image = SpiderImages.STAND

    def _draw(self) -> None:
        self._draw_spiderweb()
        super()._draw()

    def _draw_spiderweb(self) -> None:
        draw_rect(screen, Color.WHITE, self.camera.apply(self.spiderweb_rect))

    @property
    def spiderweb_rect(self) -> Rect:
        return Rect(
            self.rect.x + self.rect.w // 2 - self.SPIDERWEB_W // 2,
            self.start_y,
            self.SPIDERWEB_W,
            self.rect.y - self.start_y + self.rect.h // 2
        )
