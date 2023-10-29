from game.config import GameConfig

__all__ = (
    'calc_count_by_fps_from_seconds',
    'TimeCounter',
    'FramesCounter',
)


def calc_count_by_fps_from_seconds(seconds: float) -> float:
    """Рассчитывает, сколько итераций главного игрового цикла должно пройти,
    чтобы по времени это было равно `seconds`.
    """
    return seconds * GameConfig.MAX_FPS


class TimeCounter:
    """Счётчик итераций игрового цикла, занимающих заданное количество
    времени `duration_as_seconds`.
    На примере:
    Допустим, у нас есть главный герой, при получении урона который входит
    на непродолжительное время в god mod.
    Реализовать это можно примерно так:
    hero = ...
    enemy = ...
    timer: TimeCounter = TimeCounter(5)
    while True:  # Игровой цикл.
        if hero.rect.colliderect(enemy.rect) and not timer.is_work():
            hero.hit()
            timer.restart()
        timer.next()
    """

    def __init__(self, duration_as_seconds: float) -> None:
        self.duration_as_seconds = duration_as_seconds
        self.max_count: float = calc_count_by_fps_from_seconds(duration_as_seconds)
        self.current_count: int = 0

    def restart(self) -> None:
        self.current_count = self.max_count

    def stop(self) -> None:
        self.current_count = 0

    def delta(self) -> float:
        return self.max_count - self.current_count

    def next(self) -> None:
        if self.current_count > 0:
            self.current_count -= 1

    def is_work(self) -> bool:
        return self.current_count > 0


class FramesCounter:
    """Счётчик для смены изображений и образования анимации.
    Работает в связке с `TimeCounter`.
    На примере:
    Всего у нас 4 картинки и мы хотим, чтобы они сменялись каждые 2 секунды.
    Реализация в коде будет выглядеть следующим образом:
    all_images = [...]
    cur_image = None
    frames_counter = FramesCounter(4, 2)
    while True:  # Игровой цикл.
        cur_image = all_images[frames_counter.current_index]
        frames_counter.next()

    В этом классе также выделены флаги `is_end` и `is_last_frame`:
    - При переходе с последнего индекса на 0 включается `is_end`;
    - При переходе на последний индекс включается `is_last_frame`.
    После чего они выключаются.
    """

    def __init__(self, frames_count: int,
                 transition_delay_as_seconds: float,
                 ) -> None:
        self.frames_count = frames_count
        self.time_counter = TimeCounter(transition_delay_as_seconds)
        self.time_counter.restart()
        self.current_index: int = 0
        self.is_end: bool = True
        self.is_last_frame: bool = False

    def next(self) -> None:
        self.is_end = False
        self.is_last_frame = False
        self.time_counter.next()
        if not self.time_counter.is_work():
            self.time_counter.restart()
            self.current_index += 1
            if self.current_index >= self.frames_count - 1:
                self.is_last_frame = True
            if self.current_index > self.frames_count - 1:
                self.current_index = 0
                self.is_end = True
