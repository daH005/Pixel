from engine.common.typing_ import AnyRectType

__all__ = (
    'CollisionCheckableMixin',
)


class CollisionCheckableMixin:

    _x_vel: float
    _y_vel: float
    _rect: AnyRectType

    def _handle_collision_with_bounding_rect(self, bounding_rect: AnyRectType,
                                             x_vel: float,
                                             y_vel: float,
                                             ) -> None:
        if self._rect.colliderect(bounding_rect):
            if x_vel > 0:
                self._handle_right_collision(bounding_rect)
            elif x_vel < 0:
                self._handle_left_collision(bounding_rect)
            elif y_vel > 0:
                self._handle_bottom_collision(bounding_rect)
            elif y_vel < 0:
                self._handle_top_collision(bounding_rect)

    def _handle_right_collision(self, bounding_rect: AnyRectType) -> None:
        self._rect.right = bounding_rect.left
        self._x_vel = 0

    def _handle_left_collision(self, bounding_rect: AnyRectType) -> None:
        self._rect.left = bounding_rect.right
        self._x_vel = 0

    def _handle_bottom_collision(self, bounding_rect: AnyRectType) -> None:
        self._rect.bottom = bounding_rect.top
        self._y_vel = 0

    def _handle_top_collision(self, bounding_rect: AnyRectType) -> None:
        self._rect.top = bounding_rect.bottom
        self._y_vel = 0
