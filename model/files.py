import os
import shutil

from ._base_ import Stack, Path


class Img(Path):
    def __init__(self, _path: str | None, _name: str | None):
        super().__init__(_path, _name)

    def copy_to(self, _path: str):
        shutil.copyfile(self.path, f"{_path}/{self.name}")

    def trash(self):
        idx_1st = self.path.find("/")
        idx_2ed = self.path.find("/", idx_1st + 1)
        idx_final = self.path.rfind("/")
        filepath = self.path[:idx_1st] + "/trash" + self.path[idx_2ed:idx_final]
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        shutil.move(self.path, filepath + "/" + self.name)


class Series(Stack, Path):
    def __init__(self, _path: str | None, _name: str | None):
        Path.__init__(self, _path, _name)
        Stack.__init__(self)
        self.children: list[Img] = []
        self.build()

    def current(self) -> Img:
        if self.index or len(self.children):
            return self.children[self.index]

    def build(self):
        for fn in os.scandir(self.path):
            self.children.append(Img(fn.path, fn.name))


class Species(Stack, Path):
    def __init__(self, _path: str | None, _name: str | None):
        Path.__init__(self, _path, _name)
        Stack.__init__(self)
        self.children: list[Series] = []
        self.build()

    def current(self) -> Series:
        if self.index or len(self.children):
            return self.children[self.index]

    def build(self):
        for fn in os.scandir(self.path):
            self.children.append(Series(fn.path, fn.name))


class WorkSpace(Path):
    def __init__(self, _path: str | None):
        super().__init__(_path, None)
        self.name: str = ''
        self.cursor: int = 0

    def setup(self, item: str | int) -> Species:
        if isinstance(item, str):
            for i, fn in enumerate(os.scandir(self.path)):
                if fn == item:
                    self.cursor = i
                    return Species(fn.path, fn.name)
        elif isinstance(item, int):
            for i, fn in enumerate(os.scandir(self.path)):
                if i == item:
                    self.cursor = i
                    return Species(fn.path, fn.name)

    def current(self) -> Species:
        for i, fn in enumerate(os.scandir(self.path)):
            if i == self.cursor:
                return Species(fn.path, fn.name)

    def next(self) -> Species:
        self.cursor += 1
        res = self.current()
        if res is None:
            self.cursor -= 1
        return res

    def last(self) -> Species:
        if self.cursor > 0:
            self.cursor -= 1
        return self.current()
