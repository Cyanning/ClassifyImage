import os.path
from ._base_ import Path


class Category(Path):
    category = [
        "主图", "子实体", "菌盖", "菌肉", "菌褶", "菌柄", "栖息地", "菌环", "菌托", "未成熟的子实体", "其他分类"
    ]

    def __init__(self, _path: str | None, _name: str | None):
        super().__init__(_path)
        self.name = _name

    def __getitem__(self, item):
        if not isinstance(item, str) and item not in self.category:
            raise KeyError
        path = "{}/{}/{}".format(self.path, self.name, item)
        if not os.path.exists(path):
            os.makedirs(path)
        return path
