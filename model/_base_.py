import sys


class Path:
    def __init__(self, symbol: str = None):
        self.chunks: list[str] = []
        if symbol is not None:
            self.symbol = symbol
        else:
            match sys.platform:
                case "win32":
                    self.symbol = "\\"
                case _:
                    self.symbol = "/"

    def __getitem__(self, item) -> str:
        if isinstance(item, int):
            return self.total_slices[item].strip(self.symbol)
        elif isinstance(item, slice):
            _pathes = self.total_slices[item]
            _path = "".join(_pathes)
            return _path
        else:
            raise IndexError

    @property
    def name(self) -> str:
        return self.chunks[-1]

    @property
    def total(self) -> str:
        return self.symbol.join(self.chunks)

    @property
    def total_slices(self) -> list[str]:
        chunk = ""
        slices = []
        for strings in self.chunks:
            chunk += strings
            if len(strings) > 0:
                slices.append(chunk)
                chunk = ""
            chunk += self.symbol
        return slices

    def total_add(self, *filenames: str) -> str:
        return self.total + self.symbol + self.symbol.join(filenames)

    def total_insert(self, filename: str, index: int) -> str:
        path = ""
        for i, _path in enumerate(self.total_slices):
            if i == index:
                path += filename + self.symbol
            else:
                path += _path
        return path

    def set_path(self, _path: str = None):
        if _path is None:
            self.chunks.clear()
        elif isinstance(_path, str):
            self.chunks = _path.replace("\\", "/").split("/")
        else:
            raise ValueError
