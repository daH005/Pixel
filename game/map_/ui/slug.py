from pygame import Rect

from game.assets.images import SlugImages
from game.assets.sounds import slug_sound
from game.contrib.counters import FramesCounter
from game.contrib.annotations import SizeTupleType
from game.map_.map_ import Map
from game.map_.abstract_ui import AbstractXPatrolEnemy
from game.contrib.screen import screen

__all__ = (
    'Slug',
)


@Map.add_object_type
class Slug(AbstractXPatrolEnemy):
    size: SizeTupleType = SlugImages.GO[0].get_size()
    SPEED: float = 1

    GO_ANIM_DELAY: float = 0.1
    DEATH_ANIM_DELAY: float = 0.1

    PLAYER_Y_VEL_FOR_DEATH: float = 8
    DEATH_Y_PUSHING_POWER: float = 15

    def __init__(self, x: int, y: int,
                 start_x: int,
                 end_x: int,
                 ) -> None:
        super().__init__(x, y, start_x, end_x)
        self._anim_rect: Rect = self.rect
        self.go_frames_counter: FramesCounter = FramesCounter(
            frames_count=len(SlugImages.GO),
            transition_delay_as_seconds=self.GO_ANIM_DELAY,
        )
        self.death_frames_counter: FramesCounter = FramesCounter(
            frames_count=len(SlugImages.DEATH),
            transition_delay_as_seconds=self.DEATH_ANIM_DELAY,
        )

    def _move(self) -> None:
        if self.death_frames_counter.is_end:
            super()._move()

    def _handle_collision_with_player(self) -> None:
        if self.map.player.y_vel >= self.PLAYER_Y_VEL_FOR_DEATH:
            if not self.map.player.god_mode_time_counter.is_work():
                self.map.player.y_vel = -self.DEATH_Y_PUSHING_POWER
                self.death_frames_counter.is_end = False
                slug_sound.play()
        elif self.death_frames_counter.is_end:
            super()._handle_collision_with_player()

    def _update_image(self) -> None:
        if self.death_frames_counter.is_end:
            self.image = SlugImages.GO[self.go_frames_counter.current_index]
            self.go_frames_counter.next()
        else:
            self.image = SlugImages.DEATH[self.death_frames_counter.current_index]
            self._anim_rect: Rect = self.image.get_rect()
            self._anim_rect.centerx = self.rect.centerx
            self._anim_rect.bottom = self.rect.bottom
            self.death_frames_counter.next()
            if self.death_frames_counter.is_end:
                self.to_delete = True

    def _draw(self) -> None:
        screen.blit(self.image, self.map.camera.apply(self._anim_rect))
