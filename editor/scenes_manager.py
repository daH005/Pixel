import json
from pathlib import Path
from traceback import print_exc
import pygame as pg
from pygame.event import Event
from tempfile import mktemp

from engine.common.direction import Direction
from engine.common.typing_ import CameraBoundingLinesType
from engine.exceptions import ExitFromGame
from engine.scenes.abstract_scene import AbstractScene
from game.scenes import ScenesManager
from game.scenes.level.scene import LevelScene
from game.scenes.keys import SceneKey
from game.assets.fonts import PixelFonts
from game.common.windows.windows import Button
from game.common.windows.building import TextWindowPartBuilder
from game.common.windows.rect_relative_position_names import RectRelativePositionName
from editor.types_ import *

__all__ = (
    'ScenesManager',
    'EDITOR_SCENE_KEY',
    'EditorScene',
)

EDITOR_SCENE_KEY = 999


@ScenesManager.add(EDITOR_SCENE_KEY)
class EditorScene(AbstractScene):

    _BACKGROUND_COLOR = (0, 191, 255)
    _BLOCK_SIZE: int = 40
    _HALF_BLOCK_SIZE: int = _BLOCK_SIZE // 2
    _OFFSET_SPEED: int = 10
    _DEFAULT_FILENAME: str = 'default.json'
    _BOTTOM_UNCLICKABLE_AREA_H: int = 50

    def __init__(self, scenes_manager: ScenesManager) -> None:
        super().__init__(scenes_manager)
        self._panel: _ObjectTypePanel = _ObjectTypePanel(self._object_type_panel_choice)
        self._panel_is_on: bool = False
        self._selected_object_type = Dirt
        self._selected_object_kwargs = {}

        self._overlay_deleting_mode_is_on: bool = False
        self._camera_bounding_horizontal_line_deleting_mode_is_on: bool = False

        self._init_buttons()

        self._objects: list[AbstractEditorObject] = []
        self._camera_bounding_horizontal_lines: CameraBoundingLinesType = []

        self._points: list[tuple[int, int]] = []

        self._x_offset: int = 0
        self._y_offset: int = 0

        self._filename: str = input('Enter the path to the map of press ENTER (without .json extension): ')
        if self._filename:
            self._filename += '.json'
        else:
            self._filename = self._DEFAULT_FILENAME

        try:
            self._load_map(self._filename)
        except FileNotFoundError:
            pass

    def _object_type_panel_choice(self, t, kwargs) -> None:
        if issubclass(t, AbstractXPatrolEnemyEditorObject) and len(self._points) < 2:
            print('This type requires two points!')
        if issubclass(t, (Spider, Cannon)) and len(self._points) < 1:
            print('This type requires at least one point!')
        self._selected_object_type = t
        self._selected_object_kwargs = kwargs

    def _load_map(self, filename: str) -> None:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for ob in data['objects']:
            try:
                t = globals()[ob['type']]
            except KeyError:
                print(f'Type {ob["type"]} does not exist.')
                continue
            self._objects.append(t(**ob['args']))
            if t == Player:
                self._set_xy_offsets(self._objects[-1].get_rect())
        self._camera_bounding_horizontal_lines = data['camera_bounding_horizontal_lines']

    def _set_xy_offsets(self, rect: pg.Rect) -> None:
        self._x_offset = rect.x - self._screen.get_width() // 2
        self._y_offset = rect.y - self._screen.get_height() // 2

    def _init_buttons(self) -> None:
        self._buttons: list[Button] = []

        save: Button = Button(
            builder=TextWindowPartBuilder(
                text='Save',
                font=PixelFonts.VERY_SMALL,
            ),
            position_name=RectRelativePositionName.BOTTOMLEFT,
            x=0,
            y=self._screen.get_height(),
            on_click=self.save_map,
        )
        self._buttons.append(save)

        open_close_panel: Button = Button(
            builder=TextWindowPartBuilder(
                text='Panel',
                font=PixelFonts.VERY_SMALL,
            ),
            position_name=RectRelativePositionName.BOTTOMLEFT,
            x=save.get_rect().right,
            y=self._screen.get_height(),
            on_click=self._switch_panel,
        )
        self._buttons.append(open_close_panel)

        clear_points: Button = Button(
            builder=TextWindowPartBuilder(
                text='Clear points',
                font=PixelFonts.VERY_SMALL,
            ),
            position_name=RectRelativePositionName.BOTTOMLEFT,
            x=open_close_panel.get_rect().right,
            y=self._screen.get_height(),
            on_click=self._clear_points,
        )
        self._buttons.append(clear_points)

        add_camera_bounding_horizontal_line: Button = Button(
            builder=TextWindowPartBuilder(
                text='Camera bounding horizontal line',
                font=PixelFonts.VERY_SMALL,
            ),
            position_name=RectRelativePositionName.BOTTOMLEFT,
            x=clear_points.get_rect().right,
            y=self._screen.get_height(),
            on_click=self._add_camera_bounding_horizontal_line,
        )
        self._buttons.append(add_camera_bounding_horizontal_line)

        add_overlay_object: Button = Button(
            builder=TextWindowPartBuilder(
                text='Add overlay',
                font=PixelFonts.VERY_SMALL,
            ),
            position_name=RectRelativePositionName.BOTTOMLEFT,
            x=add_camera_bounding_horizontal_line.get_rect().right,
            y=self._screen.get_height(),
            on_click=self._add_overlay_object,
        )
        self._buttons.append(add_overlay_object)

        overlay_deleting_mode: Button = Button(
            builder=TextWindowPartBuilder(
                text='Overlay deleting',
                font=PixelFonts.VERY_SMALL,
            ),
            position_name=RectRelativePositionName.BOTTOMLEFT,
            x=add_overlay_object.get_rect().right,
            y=self._screen.get_height(),
            on_click=self._switch_overlay_deleting_mode,
        )
        self._buttons.append(overlay_deleting_mode)

        camera_bounding_hor_line: Button = Button(
            builder=TextWindowPartBuilder(
                text='Camera bounding hor. line del.',
                font=PixelFonts.VERY_SMALL,
            ),
            position_name=RectRelativePositionName.BOTTOMLEFT,
            x=overlay_deleting_mode.get_rect().right,
            y=self._screen.get_height(),
            on_click=self._switch_camera_bounding_horizontal_line_deleting_mode,
        )
        self._buttons.append(camera_bounding_hor_line)

        run_level: Button = Button(
            builder=TextWindowPartBuilder(
                text='Run level',
                font=PixelFonts.VERY_SMALL,
            ),
            position_name=RectRelativePositionName.BOTTOMLEFT,
            x=camera_bounding_hor_line.get_rect().right,
            y=self._screen.get_height(),
            on_click=self._run_level,
        )
        self._buttons.append(run_level)

    def save_map(self, file_path: Path | str | None = None) -> None:
        if file_path is None:
            file_path = self._filename

        objects, max_right, max_bottom = self._prepare_json_objects_max_right_and_bottom_coordinates()
        max_right = max(max_right, self._screen.get_width())
        max_bottom = max(max_bottom, self._screen.get_height())
        m = {
            'objects': objects,
            'is_available': True,
            'is_completed': False,
            'w': max_right,
            'h': max_bottom,
            'extra_data': {
                'ids': []
            },
            'camera_bounding_horizontal_lines': self._camera_bounding_horizontal_lines,
        }

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(m, f)

    def _prepare_json_objects_max_right_and_bottom_coordinates(self) -> tuple[list[dict], int, int]:
        obs = []
        max_right: int = 0
        max_bottom: int = 0
        for ob in self._objects:
            obs.append(ob.to_json())
            rect = ob.get_rect()
            max_right = max(max_right, rect.right)
            max_bottom = max(max_bottom, rect.bottom)

        return obs, max_right, max_bottom

    def _switch_panel(self) -> None:
        if self._panel_is_on:
            self._panel_is_on = False
        else:
            self._panel_is_on = True

    def _clear_points(self) -> None:
        self._points.clear()
        print('The points have been cleared.')

    def _add_camera_bounding_horizontal_line(self) -> None:
        if len(self._points) < 2:
            print('It takes two points!')
            return

        x1 = self._points[0][0] - self._HALF_BLOCK_SIZE
        x2 = self._points[1][0] + self._HALF_BLOCK_SIZE
        y = self._points[0][1] - self._HALF_BLOCK_SIZE
        self._camera_bounding_horizontal_lines.append(
            (min(x1, x2), max(x1, x2), y)
        )

    def _add_overlay_object(self) -> None:
        if len(self._points) < 2:
            print('It takes two points!')
            return

        x, y = self._points[0]
        x -= self._HALF_BLOCK_SIZE
        y -= self._HALF_BLOCK_SIZE
        w = self._points[1][0] - x + self._HALF_BLOCK_SIZE
        h = self._points[1][1] - y + self._HALF_BLOCK_SIZE
        self._objects.append(Overlay(x, y, w, h))

    def _switch_overlay_deleting_mode(self) -> None:
        if self._overlay_deleting_mode_is_on:
            self._overlay_deleting_mode_is_on = False
        else:
            self._overlay_deleting_mode_is_on = True

    def _switch_camera_bounding_horizontal_line_deleting_mode(self) -> None:
        if self._camera_bounding_horizontal_line_deleting_mode_is_on:
            self._camera_bounding_horizontal_line_deleting_mode_is_on = False
        else:
            self._camera_bounding_horizontal_line_deleting_mode_is_on = True

    def _run_level(self) -> None:
        file_path: Path = Path(mktemp())
        self.save_map(file_path)
        self._scenes_manager.levels_manager.add_level(file_path)
        self._scenes_manager.levels_manager.switch_to(self._scenes_manager.levels_manager.last_index)
        self._scenes_manager.switch_to(SceneKey.LEVEL).reset()

    def _handle_event(self, event: Event) -> None:
        super()._handle_event(event)
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_i:
                self._add_point()

    def _add_point(self) -> None:
        pos = pg.mouse.get_pos()
        x = pos[0] + self._x_offset
        x = x - x % self._BLOCK_SIZE + self._HALF_BLOCK_SIZE
        y = pos[1] + self._y_offset
        y = y - y % self._BLOCK_SIZE + self._HALF_BLOCK_SIZE
        self._points.append((x, y))
        print('The point has been added.')

    def update(self) -> None:
        try:
            super().update()

            self._update_background()
            self._update_objects()
            self._update_camera_bounding_horizontal_lines()
            self._update_points()
            self._update_mouse()
            self._update_keyboard_presses()
            self._update_buttons()
            self._update_panel()
        except ExitFromGame:
            raise
        except:
            print_exc()

    def _update_background(self) -> None:
        self._screen.fill(self._BACKGROUND_COLOR)

    def _update_objects(self) -> None:
        for ob in self._objects_sorted_by_z_index():
            ob.update(self._x_offset, self._y_offset)

    def _objects_sorted_by_z_index(self) -> list[AbstractEditorObject]:
        return sorted(self._objects, key=lambda x: x.z_index)

    def _update_camera_bounding_horizontal_lines(self) -> None:
        for line in self._camera_bounding_horizontal_lines:
            pg.draw.line(
                self._screen,
                (255, 0, 0),
                (line[0] - self._x_offset, line[2] - self._y_offset),
                (line[1] - self._x_offset, line[2] - self._y_offset),
                width=3,
            )

    def _update_points(self) -> None:
        for i, point in enumerate(self._points):
            surface = PixelFonts.VERY_SMALL.render(str(i + 1), 1, (0, 0, 255))
            x = point[0] - self._x_offset - surface.get_width() // 2
            y = point[1] - self._y_offset - surface.get_height() // 2
            self._screen.blit(surface, (x, y))

    def _update_mouse(self) -> None:
        if self._panel_is_on:
            return

        pos = pg.mouse.get_pos()
        if pos[1] >= self._screen.get_height() - self._BOTTOM_UNCLICKABLE_AREA_H:
            return

        block_x = self._x_offset + pos[0]
        block_x = block_x - block_x % self._BLOCK_SIZE

        block_y = self._y_offset + pos[1]
        block_y = block_y - block_y % self._BLOCK_SIZE

        mouse_block_x = block_x - self._x_offset
        mouse_block_y = block_y - self._y_offset
        pg.draw.rect(self._screen, (0, 0, 0), (mouse_block_x, mouse_block_y, self._BLOCK_SIZE, self._BLOCK_SIZE), width=1)

        presses = pg.mouse.get_pressed()
        if presses[0]:
            self._handle_creating(block_x, block_y)

    def _handle_creating(self, block_x: int, block_y: int) -> None:
        ob = self._selected_object_type(block_x, block_y, **self._selected_object_kwargs)
        ob.attach_rect_position_to_bottom_center_of_block(self._BLOCK_SIZE)
        if ob not in self._objects:
            self._objects.append(ob)
            if isinstance(ob, AbstractEditorObjectToDisposableCollect):
                ob.set_id()
            elif isinstance(ob, AbstractXPatrolEnemyEditorObject):
                start_x = self._points[0][0] - self._HALF_BLOCK_SIZE
                end_x = self._points[1][0] + self._HALF_BLOCK_SIZE
                ob.set_start_and_end_xs(start_x, end_x)
            elif isinstance(ob, Spider):
                end_y = self._points[0][1] + self._HALF_BLOCK_SIZE
                ob.set_end_y(end_y)
            elif isinstance(ob, Cannon):
                end_x = self._points[0][0]
                if end_x < ob.get_rect().centerx:
                    end_x -= self._HALF_BLOCK_SIZE
                else:
                    end_x += self._HALF_BLOCK_SIZE
                ob.set_end_x(end_x)

    def _update_keyboard_presses(self) -> None:
        presses = pg.key.get_pressed()
        if presses[pg.K_RIGHT]:
            self._x_offset += self._OFFSET_SPEED
        elif presses[pg.K_LEFT]:
            self._x_offset -= self._OFFSET_SPEED
        elif presses[pg.K_DOWN]:
            self._y_offset += self._OFFSET_SPEED
        elif presses[pg.K_UP]:
            self._y_offset -= self._OFFSET_SPEED

        if self._x_offset < 0:
            self._x_offset = 0
        if self._y_offset < 0:
            self._y_offset = 0

        if presses[pg.K_DELETE]:
            self._handle_objects_deleting()
            if self._camera_bounding_horizontal_line_deleting_mode_is_on:
                self._handle_camera_bounding_horizontal_lines_deleting()

    def _handle_objects_deleting(self) -> None:
        mouse_pos = pg.mouse.get_pos()
        for ob in self._objects:
            if isinstance(ob, Overlay) and not self._overlay_deleting_mode_is_on:
                continue
            if ob.get_rect().move(-self._x_offset, -self._y_offset).collidepoint(mouse_pos):
                self._objects.remove(ob)

    def _handle_camera_bounding_horizontal_lines_deleting(self) -> None:
        mouse_pos = pg.mouse.get_pos()
        for line in self._camera_bounding_horizontal_lines[:]:
            if line[0] - self._x_offset < mouse_pos[0] < line[1] - self._x_offset:
                self._camera_bounding_horizontal_lines.remove(line)

    def _update_buttons(self) -> None:
        for button in self._buttons:
            button.update()

    def _update_panel(self) -> None:
        if self._panel_is_on:
            self._panel.update()


class _ObjectTypePanel:

    _TYPES_AND_ARGS = [
        (Dirt, dict()),
        (Dirt, dict(direction=Direction.LEFT)),
        (Dirt, dict(direction=Direction.RIGHT)),

        (Dirt, dict(grass_enabled=True)),
        (Dirt, dict(grass_enabled=True, direction=Direction.LEFT)),
        (Dirt, dict(grass_enabled=True, direction=Direction.RIGHT)),

        (BackgroundDirt, dict()),

        (Bricks, dict()),
        (BackgroundBricks, dict()),

        (Tree, dict(image_index=0)),
        (Tree, dict(image_index=1)),
        (Tree, dict(image_index=2)),

        (Player, dict()),
        (Finish, dict()),
        (Hint, dict()),

        (Coin, dict()),
        (Chest, dict()),
        (Heart, dict()),
        (Shield, dict()),

        (Spike, dict()),
        (Ladder, dict()),

        (Water, dict(is_top=False)),
        (Water, dict(is_top=True)),

        (Web, dict(direction=Direction.LEFT)),
        (Web, dict(direction=Direction.RIGHT)),

        (Slug, dict()),
        (Skeleton, dict()),
        (Bat, dict()),
        (Spider, dict()),
        (Cannon, dict()),
        (Ghost, dict()),
    ]

    def __init__(self, on_click) -> None:
        self._on_click = on_click
        self._buttons: list[Button] = []
        y: int = 0
        for t, kwargs in self._TYPES_AND_ARGS:
            button = self._new_button(t, kwargs, y)
            self._buttons.append(button)
            y += button.get_rect().h

    def _new_button(self, t, kwargs, y: int) -> Button:
        return Button(
            builder=TextWindowPartBuilder(
                text=t.__name__ + ' ' + str(kwargs),
                font=PixelFonts.VERY_SMALL,
                inner_indent=5,
                border_wh=2,
            ),
            x=0,
            y=y,
            on_click=lambda: self._on_click(t, kwargs),
        )

    def update(self) -> None:
        for button in self._buttons:
            button.update()


@ScenesManager.add(SceneKey.LEVEL)
class TestLevelScene(LevelScene):
    _SCENE_KEY_TO_SWITCH_ON_PLAYER_WAS_NOT_CREATED_EXCEPTION = EDITOR_SCENE_KEY

    def __init__(self, scenes_manager: ScenesManager) -> None:
        super().__init__(scenes_manager)
        self._back_to_editor_button: Button = Button(
            builder=TextWindowPartBuilder(
                text='Back to Editor',
                font=PixelFonts.VERY_SMALL,
            ),
            x=self._screen.get_width(),
            y=self._screen.get_height(),
            position_name=RectRelativePositionName.BOTTOMRIGHT,
            on_click=self._back_to_editor,
        )

    def _back_to_editor(self) -> None:
        self._scenes_manager.switch_to(EDITOR_SCENE_KEY)

    def update(self) -> None:
        super().update()
        self._back_to_editor_button.update()
