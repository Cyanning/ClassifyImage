class Path:
    def __init__(self):
        self.chunks: list[str] = []

    def __getitem__(self, item):
        if isinstance(item, int):
            for i, path in self.generate_chunk():
                if i == item:
                    return path
        elif isinstance(item, slice):
            if item.start is not None and item.start < 0:
                raise IndexError
            if item.stop is not None and item.stop < 0:
                raise IndexError
            if item.step is not None:
                raise IndexError

            path = ""
            for i, _path in self.generate_chunk():
                if item.start is not None and item.start > i:
                    continue
                elif item.stop is None or item.stop > i:
                    path += _path
                else:
                    break
            return path
        else:
            raise IndexError

    def generate_chunk(self):
        lev = 0
        chunk = ""
        for strings in self.chunks:
            chunk += strings
            if len(strings) > 0:
                yield lev, chunk
                chunk = ""
                lev += 1
            chunk += "/"

    @property
    def name(self) -> str:
        return self.chunks[-1]

    @property
    def total(self) -> str:
        return "/".join(self.chunks)

    def set_path(self, _path: str = None):
        if _path is None:
            self.chunks.clear()
        elif isinstance(_path, str):
            self.chunks = _path.replace("\\", "/").split("/")
        else:
            raise ValueError
