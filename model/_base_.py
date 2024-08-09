import os
from abc import abstractmethod


class Path:
    def __init__(self, _path: str | None):
        self._path: str | None = None
        self.name: str | None = None
        if _path is not None:
            self.name = _path[_path.rfind("/") + 1:]
            self.path = _path

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, _path: str):
        self._path = _path.replace("\\", "/")
        self.name = _path[_path.rfind("/") + 1:]

    def file_list(self):
        return os.listdir(self.path)


class Stack(Path):
    def __init__(self, _path: str | None):
        super().__init__(_path)
        self._idx: int = 0
        self.children: list = []
        if self.path:
            self.build()

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

    @abstractmethod
    def current(self):
        ...

    @abstractmethod
    def build(self):
        ...


class Folder:
    def __init__(self, _path: str | None):
        self.fullpath: str = ''
        self.name: str = ''
        self.cursor: int = -1
        if _path is not None:
            self.fullpath = _path.replace("\\", "/")
            self.name = self.fullpath[self.fullpath.rfind("/") + 1:]

    def __getitem__(self, item):
        if isinstance(item, str):
            for i, fn in enumerate(os.listdir(self.fullpath)):
                if fn == item:
                    self.cursor = i
                    return "{}/{}".format(self.fullpath, fn)
        elif isinstance(item, int):
            for i, fn in enumerate(os.listdir(self.fullpath)):
                if i == item:
                    self.cursor = i
                    return "{}/{}".format(self.fullpath, fn)
        raise KeyError

    def current(self):
        for i, fn in enumerate(os.listdir(self.fullpath)):
            if i == self.cursor:
                return "{}/{}".format(self.fullpath, fn)

    def next(self):
        pass

    def last(self):
        if self.cursor > 0:
            self.cursor -= 1
        return self[self.cursor]

