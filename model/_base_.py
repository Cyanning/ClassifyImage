class Path:
    def __init__(self, _path: str | None, _name: str | None):
        self._path: str | None = None
        if _path is not None:
            self.path = _path
        self.name: str | None = _name

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, _path: str):
        self._path = _path.replace("\\", "/")
        self.name = _path[_path.rfind("/") + 1:]


class Stack:
    def __init__(self):
        self._idx: int = 0
        self.children: list = []

    @property
    def index(self):
        return self._idx

    @index.setter
    def index(self, idx: int):
        if not isinstance(idx, int):
            raise TypeError
        if abs(self._idx + idx) >= len(self.children):
            raise IndexError
        self._idx = idx
