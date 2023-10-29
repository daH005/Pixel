from pygame import (
    # Rect,
    KEYDOWN,
    KEYUP,
    K_DELETE,
    K_s,
    K_d,
    K_1,
    K_2,
    K_3,
    K_4,
    K_5,
    K_6,
    K_8,
    K_9,
    K_0,
    K_p,
    K_i,
    K_f,
    K_t,
    K_e,
    K_b,
    K_c,
    K_w,
    K_RIGHT,
    K_LEFT,
    K_UP,
    K_DOWN,
    HWSURFACE,
    DOUBLEBUF,
    SCALED,
)
from pygame.event import Event
from pygame.mouse import get_pressed
from pygame.key import get_pressed as get_keys
# from pygame.draw import rect as draw_rect

from game.config import GameConfig
GameConfig.WINDOW_FLAGS = HWSURFACE | DOUBLEBUF | SCALED
from game.main import Game as Editor
from game.scenes.base import ScenesManager, AbstractScene
from game.contrib.screen import screen
from game.contrib.colors import Color
from game.assets.levels import LEVELS_PATH
from game.contrib.files import save_json
from game.contrib.annotations import XYTupleType
from game.contrib.direction import Direction
from editor.map_ import Map, SomeEditorMapObjectType
from editor.ui import *

__all__ = (
    'Editor',
)

EDITOR_SCENE_KEY: int = 100500


@ScenesManager.add(EDITOR_SCENE_KEY)
class EditorScene(AbstractScene):
    """Сцена редактора карт."""

    NEW_MAP_FILENAME: str = 'new.json'
    camera_mouse_coords: XYTupleType

    def __init__(self) -> None:
        self.map: Map = Map()
        self.CurrentMapObjectType: type[SomeEditorMapObjectType] = Dirt

        self._mouse_is_pressed: bool = False
        self.pressed_keys: list[int] = []
        self._selected_object: SomeEditorMapObjectType | None = None

    def on_switch(self) -> None:
        self.map.reset()

    def _handle_event(self, event: Event) -> None:
        if event.type == KEYDOWN:
            self.pressed_keys.append(event.key)
            if event.key == K_s:
                self.save_level()
            if event.key == K_p:
                self.CurrentMapObjectType = Player

            if event.key == K_d:
                self.CurrentMapObjectType = Dirt
            if K_d in self.pressed_keys:
                if event.key == K_1:
                    Dirt.common_direction = None
                if event.key == K_2:
                    Dirt.common_direction = Direction.LEFT
                if event.key == K_3:
                    Dirt.common_direction = Direction.RIGHT
                if event.key == K_4:
                    Dirt.common_grass_enabled = not Dirt.common_grass_enabled
                if event.key == K_5:
                    self.CurrentMapObjectType = BackgroundDirt
            if K_b in self.pressed_keys:
                if event.key == K_1:
                    self.CurrentMapObjectType = Bricks
                if event.key == K_2:
                    self.CurrentMapObjectType = BackgroundBricks
                if event.key == K_3:
                    self.CurrentMapObjectType = Hint
                if event.key == K_4:
                    self.CurrentMapObjectType = Ladder

            if K_w in self.pressed_keys:
                if event.key == K_1:
                    self.CurrentMapObjectType = Water
                if event.key == K_2:
                    Water.common_top = not Water.common_top

            if K_i in self.pressed_keys:
                if event.key == K_1:
                    self.CurrentMapObjectType = Coin
                if event.key == K_2:
                    self.CurrentMapObjectType = Heart
                if event.key == K_3:
                    self.CurrentMapObjectType = Chest
                if event.key == K_4:
                    self.CurrentMapObjectType = Shield

            if event.key == K_f:
                self.CurrentMapObjectType = Finish

            if event.key == K_t:
                self.CurrentMapObjectType = Tree
            if K_t in self.pressed_keys:
                if event.key == K_1:
                    Tree.common_image_index = 0
                if event.key == K_2:
                    Tree.common_image_index = 1
                if event.key == K_3:
                    Tree.common_image_index = 2

            if K_e in self.pressed_keys:
                if event.key == K_1:
                    self.CurrentMapObjectType = Slug
                if event.key == K_2:
                    self.CurrentMapObjectType = Bat
                if event.key == K_3:
                    self.CurrentMapObjectType = Skeleton
                if event.key == K_4:
                    self.CurrentMapObjectType = Spike
                if event.key == K_5:
                    self.CurrentMapObjectType = Cannon
                if event.key == K_6:
                    self.CurrentMapObjectType = Spider

            try:
                if event.key == K_9:
                    self._selected_object.start_x = self.camera_mouse_coords[0]
                if event.key == K_0:
                    self._selected_object.end_x = self.camera_mouse_coords[0]
                if event.key == K_8:
                    self._selected_object.end_y = self.camera_mouse_coords[1]
            except AttributeError:
                pass

            if event.key == K_LEFT:
                self.map.decrease_w()
            if event.key == K_RIGHT:
                self.map.increase_w()
            if event.key == K_UP:
                self.map.decrease_h()
            if event.key == K_DOWN:
                self.map.increase_h()

        if event.type == KEYUP:
            try:
                self.pressed_keys.remove(event.key)
            except ValueError:
                pass

    def update(self):
        self.camera_mouse_coords: XYTupleType = self.map.camera.get_cursor()
        super().update()

    def _update(self) -> None:
        screen.fill(Color.BLUE)
        self.map.update()
        self._update_object_creating()
        self._mouse_is_pressed = False
        if get_pressed()[0]:
            self._mouse_is_pressed = True

    def _update_object_creating(self) -> None:
        if get_keys()[K_DELETE]:
            self._del_object()
        elif get_keys()[K_c]:
            self._select_object()
        elif get_pressed()[0]:
            self._create_object()

    def _create_object(self) -> None:
        xy: XYTupleType = self.map.camera.get_cursor()
        for ob in self.map.grid.visible_objects:
            if type(ob) == self.CurrentMapObjectType and ob.rect.collidepoint(xy):
                break
        else:
            new_obj = self.CurrentMapObjectType.new_with_coords_fix(*xy)
            self.map.grid.add(new_obj)
            self._selected_object = new_obj

    def _select_object(self) -> None:
        for ob in self.map.grid.visible_objects:
            if ob.rect.collidepoint(self.map.camera.get_cursor()):
                self._selected_object = ob
                break

    def _del_object(self) -> None:
        for ob in self.map.grid.visible_objects:
            if ob.rect.collidepoint(self.map.camera.get_cursor()):
                ob.remove()

    def save_level(self) -> None:
        filename: str = self.NEW_MAP_FILENAME
        if self.map.level:
            filename = f'{self.map.level.index}.json'
        save_json(LEVELS_PATH.joinpath(filename), self.map.prepare_json())


if __name__ == '__main__':
    GameConfig.MAX_FPS = 60
    editor: Editor = Editor(initial_scene_key=EDITOR_SCENE_KEY)
    editor.run()
