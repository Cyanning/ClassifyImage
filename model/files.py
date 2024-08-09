import shutil

from ._base_ import Stack, Path


class Img(Path):
    def __init__(self, _path: str):
        super().__init__(_path)

    def copy_to(self, _path: str):
        shutil.copyfile(self.path, f"{_path}/{self.name}")


class Series(Stack):
    def __init__(self, _path: str | None):
        super().__init__(_path)

    def current(self) -> Img:
        if self.index or len(self.children):
            return self.children[self.index]

    def build(self):
        for fn in self.file_list():
            self.children.append(Img(f"{self.path}/{fn}"))


class Species(Stack):
    def __init__(self, _path: str | None):
        super().__init__(_path)

    def current(self) -> Series:
        if self.index or len(self.children):
            return self.children[self.index]

    def build(self):
        for fn in self.file_list():
            self.children.append(Series(f"{self.path}/{fn}"))


class Origin(Stack):
    def __init__(self, _path: str | None):
        super().__init__(_path)

    def current(self) -> Species:
        if self.index or len(self.children):
            return self.children[self.index]

    def build(self):
        for fn in self.file_list():
            self.children.append(Species(f"{self.path}/{fn}"))
