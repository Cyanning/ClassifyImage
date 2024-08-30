import os
import shutil

from ._base_ import Path

IMG_FORMATS = (".jpg", ".jpeg", ".JPG", ".JPEG", ".png", ".PNG")


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


class Species(Path):
    def __init__(self, _path: str | None, _name: str | None):
        super().__init__(_path, _name)
        self.imgs: list[Img] = []
        self.build()

    def build(self):
        self.imgs.clear()
        for dirpath, dirnames, filenames in os.walk(self.path):
            for filename in filenames:
                if any(filename.endswith(endcode) for endcode in IMG_FORMATS):
                    self.imgs.append(Img(f"{dirpath}/{filename}", filename))


class WorkSpace(Path):
    def __init__(self, _path: str | None, _name: str | None):
        super().__init__(_path, None)
        self.__idx: int = -1 if _path is None else 0
        self.name: str = _name
        self.species: Species | None = None

    @property
    def cursor(self):
        return self.__idx

    @cursor.setter
    def cursor(self, _idx: int):
        with os.scandir(self.path) as files:
            for i, fn in enumerate(files):
                if i == _idx:
                    self.__idx = i
                    self.species = Species(fn.path, fn.name)
                    break
            else:
                raise IndexError

    def build_by_name(self, item: str):
        with os.scandir(self.path) as files:
            for i, fn in enumerate(files):
                if fn.name == item:
                    self.__idx = i
                    self.species = Species(fn.path, fn.name)
                    break
            else:
                raise ValueError

    def build(self):
        with os.scandir(self.path) as files:
            for i, fn in enumerate(files):
                if self.__idx == i:
                    self.species = Species(fn.path, fn.name)
                    break
