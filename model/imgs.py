import os
import shutil

from ._base_ import Path

IMG_FORMATS = (".jpg", ".jpeg", ".JPG", ".JPEG", ".png", ".PNG")


class Img:
    def __init__(self, _path: str | None):
        self.path = Path()
        self.path.set_path(_path)

    def copy_to(self, _path: str):
        shutil.copyfile(self.path.total, _path + self.path.symbol + self.path.name)

    def trash(self):
        filepath = self.path[:2] + self.path.symbol + "trash" + self.path[3:-1]
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        shutil.move(self.path.total, filepath)


class Species:
    def __init__(self, _path: str, magnitude: int):
        self.path = Path()
        self.path.set_path(_path)
        self.imgs: list[Img] = []
        if magnitude >= 0:
            assert self.count() > magnitude
        else:
            assert self.count() < abs(magnitude)
        self.build()

    def build(self):
        self.imgs.clear()
        for dirpath, dirnames, filenames in os.walk(self.path.total):
            for filename in filenames:
                if any(filename.endswith(endcode) for endcode in IMG_FORMATS):
                    self.imgs.append(Img(dirpath + self.path.symbol + filename))

    def count(self):
        count = 0
        for dirpath, dirnames, filenames in os.walk(self.path.total):
            for filename in filenames:
                if any(filename.endswith(endcode) for endcode in IMG_FORMATS):
                    count += 1
        return count


class WorkSpace:
    def __init__(self, _path: str | None, _magnitude: int):
        self.__idx: int = -1 if _path is None else 0
        self.path = Path()
        self.path.set_path(_path)
        self.species: Species | None = None
        self.magnitude = _magnitude

    @property
    def cursor(self):
        return self.__idx

    @cursor.setter
    def cursor(self, _idx: int):
        with os.scandir(self.path.total) as files:
            for i, fn in enumerate(files):
                if i == _idx:
                    self.__idx = i
                    self.species = Species(fn.path, self.magnitude)
                    break
            else:
                raise IndexError

    def build_by_name(self, item: str):
        with os.scandir(self.path.total) as files:
            for i, fn in enumerate(files):
                if fn.name == item:
                    self.__idx = i
                    self.species = Species(fn.path, self.magnitude)
                    break
            else:
                raise ValueError

    def build(self):
        with os.scandir(self.path.total) as files:
            for i, fn in enumerate(files):
                if self.__idx == i:
                    self.species = Species(fn.path, self.magnitude)
                    break

    def init_build(self, item: str | int):
        if isinstance(item, str):
            try:
                self.build_by_name(item)
                return
            except (ValueError, AssertionError):
                item = 0
        if isinstance(item, int):
            try:
                self.cursor = item
                return
            except (ValueError, AssertionError, IndexError):
                self.__idx = -1

        while True:
            try:
                self.cursor += 1
            except AssertionError:
                continue
            except IndexError:
                break
            else:
                break
