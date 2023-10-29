__all__ = (
    'alias',
)


def alias(key: str, default=None) -> property:
    """Создаёт геттер и сеттер для работы с элементом словаря `key`.
    На примере:
    class Params(dict):
        page: int = alias('PageNum')
        name: str = alias('FullName')

    params = Params()
    params.page = 5
    print(params)  # {'PageNum': 5}
    print(params.page)  # 5
    ...
    """
    @property
    def getter(self):  # noqa
        return self.get(key, default)

    @getter.setter
    def getter(self, value):
        self[key] = value
    return getter
