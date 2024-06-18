from pygame import Rect

from engine.common.counters import FramesCounter
from engine.map_.map_ import Map
from engine.common.float_rect import FloatRect
from game.assets.images import SlugImages
from game.assets.sounds import slug_sound
from game.map_.abstract_ui import AbstractXPatrolEnemy

__all__ = (
    'Slug',
)


@Map.add_object_type
class Slug(AbstractXPatrolEnemy):

    def __init__(self, map_: Map,
                 x: int, y: int,
                 start_x: int,
                 end_x: int,
                 ) -> None:
        super().__init__(
            map_=map_,
            rect=FloatRect(SlugImages.GO[0].get_rect(x=x, y=y)),
            start_x=start_x,
            end_x=end_x,
            speed=1,
        )

        self._go_frames_counter: FramesCounter = FramesCounter(
            frames_count=len(SlugImages.GO),
            transition_delay_as_seconds=0.1,
        )
        self._death_frames_counter: FramesCounter = FramesCounter(
            frames_count=len(SlugImages.DEATH),
            transition_delay_as_seconds=0.1,
        )

        self._anim_rect: Rect = self._rect
        self._player_y_vel_for_death: float = 8
        self._y_pushing_power_after_death: float = 15

    def _move(self) -> None:
        if self._death_frames_counter.is_end:
            super()._move()

    def _handle_collision_with_player(self) -> None:
        if self._map.player.y_vel >= self._player_y_vel_for_death:
            if not self._map.player.in_god_mode():
                self._map.player.jump_from_slug(-self._y_pushing_power_after_death)
                self._death_frames_counter.start()
                slug_sound.play()
        elif self._death_frames_counter.is_end:
            super()._handle_collision_with_player()

    def _update_image(self) -> None:
        if self._death_frames_counter.is_end:
            self._image = SlugImages.GO[self._go_frames_counter.current_index]
            self._go_frames_counter.next()
        else:
            self._image = SlugImages.DEATH[self._death_frames_counter.current_index]
            self._anim_rect: Rect = self._image.get_rect()
            self._anim_rect.centerx = self._rect.centerx
            self._anim_rect.bottom = self._rect.bottom
            self._death_frames_counter.next()
            if self._death_frames_counter.is_end:
                self._to_delete = True

    def _draw(self) -> None:
        self._screen.blit(self._image, self._map.camera.apply(self._anim_rect))
