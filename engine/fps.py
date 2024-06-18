__all__ = (
    'init_max_fps',
    'get_max_fps',
)

_max_fps: float = 0


def init_max_fps(max_fps: float) -> None:
    global _max_fps
    _max_fps = max_fps


def get_max_fps() -> float:
    return _max_fps
