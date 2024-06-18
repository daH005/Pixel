from engine.fps import get_max_fps

__all__ = (
    'TimeCounter',
    'FramesCounter',
    'calc_count_by_fps_from_seconds',
)


class TimeCounter:
    """Example:
    hero = ...
    enemy = ...
    timer: TimeCounter = TimeCounter(5)
    while True:
        if hero.get_rect().colliderect(enemy.get_rect()) and not timer.is_working():
            hero.hit()
            timer.restart()
        timer.next()
    """

    def __init__(self, duration_as_seconds: float) -> None:
        self._duration_as_seconds = duration_as_seconds
        self._max_count: float = calc_count_by_fps_from_seconds(duration_as_seconds)
        self._current_count: int = 0

    def restart(self) -> None:
        self._current_count = self._max_count

    def stop(self) -> None:
        self._current_count = 0

    def delta(self) -> float:
        return self._max_count - self._current_count

    def next(self) -> None:
        if self._current_count > 0:
            self._current_count -= 1

    def is_working(self) -> bool:
        return self._current_count > 0


class FramesCounter:
    """Example:
    all_images = [...]
    cur_image = None
    frames_counter = FramesCounter(4, 2)
    while True:
        cur_image = all_images[frames_counter.current_index]
        frames_counter.next()
    """

    def __init__(self, frames_count: int,
                 transition_delay_as_seconds: float,
                 ) -> None:
        self._frames_count = frames_count
        self._time_counter = TimeCounter(transition_delay_as_seconds)
        self._time_counter.restart()
        self._current_index: int = 0
        self._is_end: bool = True
        self._is_last_frame: bool = False

    @property
    def current_index(self) -> int:
        return self._current_index

    @property
    def is_end(self) -> bool:
        return self._is_end

    @property
    def is_last_frame(self) -> bool:
        return self._is_last_frame

    def next(self) -> None:
        self._is_end = False
        self._is_last_frame = False
        self._time_counter.next()
        if not self._time_counter.is_working():
            self._time_counter.restart()
            self._current_index += 1
            if self._current_index >= self._frames_count - 1:
                self._is_last_frame = True
            if self._current_index > self._frames_count - 1:
                self._current_index = 0
                self._is_end = True

    def start(self) -> None:
        self._is_end = False


def calc_count_by_fps_from_seconds(seconds: float) -> float:
    return seconds * get_max_fps()
