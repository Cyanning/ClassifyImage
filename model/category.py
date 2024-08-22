import os.path
from ._base_ import Path


class Category(Path):
    category = [
        "主图", "子实体", "菌盖", "菌肉", "菌褶", "菌柄", "栖息地", "菌环", "菌托", "未成熟的子实体", "其他分类"
    ]

    def __init__(self, _path: str | None, _name: str | None):
        super().__init__(_path, _name)

    def get_path(self, species_name: str, category_name: str) -> str:
        if category_name not in self.category:
            raise KeyError
        path = "{}/{}/{}".format(self.path, species_name, category_name)
        if not os.path.exists(path):
            os.makedirs(path)
        return path
