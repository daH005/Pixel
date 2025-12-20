import json
import pygame as pg
from pygame.event import Event

from engine.common.direction import Direction
from engine.common.typing_ import CameraBoundingLinesType, CameraBoundingLineType
from engine.scenes.abstract_scene import AbstractScene
from engine.scenes.manager import ScenesManager
from game.assets.fonts import PixelFonts
from game.common.windows.windows import Button
from game.common.windows.building import TextWindowPartBuilder
from editor.types_ import *

__all__ = (
    'ScenesManager',
    'EditorScene',
)


@ScenesManager.add(0)
class EditorScene(AbstractScene):

    _BLOCK_SIZE: int = 40
    _OFFSET_SPEED: int = 10
    _DEFAULT_FILENAME: str = 'res.json'

    def __init__(self, scenes_manager: ScenesManager) -> None:
        super().__init__(scenes_manager)
        self._panel: _ObjectTypePanel = _ObjectTypePanel(self._object_type_panel_choice)
        self._panel_is_on: bool = False
        self._selected_object_type = Dirt
        self._selected_object_kwargs = {}

        self._objects: list[AbstractEditorObject] = []
        self._camera_bounding_horizontal_lines: CameraBoundingLinesType = []

        class _CameraBoundingHorizontalLine:
            y: int | None = None
            start_x: int | None = None
            end_x: int | None = None

            @classmethod
            def nullify(cls) -> None:
                cls.y = None
                cls.start_x = None
                cls.end_x = None

            @classmethod
            def get_tuple(cls) -> CameraBoundingLineType:
                # It needs because User may set the last point more left than the first.
                x_coordinates = sorted([cls.start_x, cls.end_x])
                return x_coordinates[0], x_coordinates[1], cls.y

        self._CameraBoundingHorizontalLine = _CameraBoundingHorizontalLine

        self._x_offset: int = 0
        self._y_offset: int = 0

        self._filename: str = input('Enter the path to the map of press ENTER (without .json extension): ')
        if self._filename:
            self._filename += '.json'
            self._load_map(self._filename)
        else:
            self._filename = self._DEFAULT_FILENAME

    def _object_type_panel_choice(self, t, kwargs) -> None:
        self._selected_object_type = t
        self._selected_object_kwargs = kwargs

    def _before_exit(self) -> None:
        self._save_map()

    def _handle_event(self, event: Event) -> None:
        super()._handle_event(event)
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                if self._panel_is_on:
                    self._panel_is_on = False
                else:
                    self._panel_is_on = True
            elif event.key == pg.K_SPACE:
                self._save_map()
            elif event.key == pg.K_i:
                self._handle_camera_bounding_horizontal_line_setting()

    def _handle_camera_bounding_horizontal_line_setting(self) -> None:
        mouse_pos = pg.mouse.get_pos()
        if self._CameraBoundingHorizontalLine.y is None:
            self._CameraBoundingHorizontalLine.y = mouse_pos[1] + self._y_offset

        if self._CameraBoundingHorizontalLine.start_x is None:
            self._CameraBoundingHorizontalLine.start_x = mouse_pos[0] + self._x_offset - self._BLOCK_SIZE
        elif self._CameraBoundingHorizontalLine.end_x is None:
            self._CameraBoundingHorizontalLine.end_x = mouse_pos[0] + self._x_offset + self._BLOCK_SIZE
            self._camera_bounding_horizontal_lines.append(self._CameraBoundingHorizontalLine.get_tuple())
            self._CameraBoundingHorizontalLine.nullify()

    def update(self) -> None:
        super().update()

        self._screen.fill((255, 255, 255))
        self._handle_objects()
        self._handle_camera_bounding_horizontal_lines()
        self._handle_mouse_clicks()
        self._handle_keyboard_presses()
        self._handle_panel()

    def _handle_mouse_clicks(self) -> None:
        if self._panel_is_on:
            return

        x_diff = self._x_offset % self._BLOCK_SIZE
        y_diff = self._y_offset % self._BLOCK_SIZE

        pos = pg.mouse.get_pos()
        block_x = pos[0] - (pos[0] + x_diff) % self._BLOCK_SIZE
        block_y = pos[1] - (pos[1] + y_diff) % self._BLOCK_SIZE
        pg.draw.rect(self._screen, (0, 0, 0), (block_x, block_y, self._BLOCK_SIZE, self._BLOCK_SIZE), width=1)

        presses = pg.mouse.get_pressed()
        if presses[0]:
            self._handle_creating(block_x, block_y)

    def _handle_creating(self, block_x: int, block_y: int) -> None:
        x = block_x + self._x_offset
        y = block_y + self._y_offset
        ob = self._selected_object_type(x, y, **self._selected_object_kwargs)
        ob.attach_rect_position_to_bottom_center_of_block(self._BLOCK_SIZE)
        if ob not in self._objects:
            self._objects.append(ob)
            if isinstance(ob, AbstractEditorObjectToDisposableCollect):
                ob.set_id()

    def _handle_keyboard_presses(self) -> None:
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
        if presses[pg.K_d]:
            self._handle_camera_bounding_horizontal_line_deleting()

    def _handle_objects_deleting(self) -> None:
        for ob in self._objects:
            if ob.get_rect().move(-self._x_offset, -self._y_offset).collidepoint(pg.mouse.get_pos()):
                self._objects.remove(ob)

    def _handle_camera_bounding_horizontal_line_deleting(self) -> None:
        mouse_pos = pg.mouse.get_pos()
        for line in self._camera_bounding_horizontal_lines[:]:
            if line[0] - self._x_offset < mouse_pos[0] < line[1] - self._x_offset:
                self._camera_bounding_horizontal_lines.remove(line)

    def _handle_objects(self) -> None:
        for ob in self._objects_sorted_by_z_index():
            ob.update(self._x_offset, self._y_offset)

    def _objects_sorted_by_z_index(self) -> list[AbstractEditorObject]:
        return sorted(self._objects, key=lambda x: x.z_index)

    def _handle_camera_bounding_horizontal_lines(self) -> None:
        for line in self._camera_bounding_horizontal_lines:
            pg.draw.line(
                self._screen,
                (255, 0, 0),
                (line[0] - self._x_offset, line[2] - self._y_offset),
                (line[1] - self._x_offset, line[2] - self._y_offset),
                width=3,
            )

    def _handle_panel(self) -> None:
        if self._panel_is_on:
            self._panel.update()

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
        self._camera_bounding_horizontal_lines = data['camera_bounding_horizontal_lines']

    def _save_map(self) -> None:
        objects, max_right, max_bottom = self._prepare_json_objects_max_right_and_bottom_coordinates()
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

        with open(self._filename, 'w', encoding='utf-8') as f:
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
