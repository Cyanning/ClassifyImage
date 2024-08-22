import os.path
import sys
import json
from PySide6 import QtWidgets
from .widget_masonry import Masonry
from .widget_control import ControlPanel
from model.imgs import WorkSpace
from model.category import Category

CACHE_PATH = "cache.json"


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("图片分类器")

        cache = self.read_path_cache()
        self.finder = WorkSpace(cache["origin_path"], None)
        try:
            self.finder.build_by_name(cache["current_species"])
            species_name = self.finder.species.name
        except ValueError:
            self.finder.build()
            species_name = self.finder.species.name
        except FileNotFoundError:
            species_name = None
        self.classify = Category(cache["saved_path"], None)

        self.masonry = Masonry(self)
        self.control = ControlPanel(
            self, default_origin_path=cache["origin_path"], default_category_path=cache["saved_path"]
        )
        self.control.signs.switch.connect(self.switch)
        self.control.signs.oppoent.connect(self.oppoent)
        self.control.signs.executer.connect(self.saved)
        self.control.signs.delete.connect(self.deleted)

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.masonry)
        layout.addWidget(self.control)
        center_widget = QtWidgets.QWidget()
        center_widget.setLayout(layout)

        self.setCentralWidget(center_widget)
        self.showMaximized()
        self.refresh()

    def refresh(self):
        # 刷新图片和选择器
        if self.finder.species is not None:
            if self.masonry.labs:
                self.masonry.clear_labels()
                self.masonry.labs.clear()
            self.masonry.show_labels(self.finder.species.imgs)
            self.control.titles.text_display(self.finder.species.name)

    def oppoent(self):
        self.control.clear_selected()
        self.masonry.clear_selected()

    def switch(self, e: int):
        # 切换物种
        if e == 0:
            finder_path, classify_path = self.control.path_selected
            if self.classify.path != classify_path:
                self.classify.path = classify_path
                self.oppoent()
            if self.finder.path != finder_path:
                self.finder.path = finder_path
                self.finder.cursor = 0
                self.refresh()
        elif abs(e) == 1:
            try:
                self.finder.cursor += e
            except IndexError:
                QtWidgets.QMessageBox.warning(self, "错误", "没了")
            else:
                self.refresh()

    def saved(self):
        # 执行保存
        categray_selections = self.control.categray_selected
        if len(categray_selections):
            try:
                self.masonry.saved(
                    [
                        self.classify.get_path(self.finder.species.name, category_name)
                        for category_name in categray_selections
                    ]
                )
                self.oppoent()
            except PermissionError:
                QtWidgets.QMessageBox.warning(self, "错误", "没有复制文件的权限")
        else:
            QtWidgets.QMessageBox.warning(self, "错误", "至少选择一个分类")

    def deleted(self):
        # 执行删除
        try:
            self.masonry.deleted()
            self.finder.build()
            self.refresh()
        except PermissionError:
            QtWidgets.QMessageBox.warning(self, "错误", "没有复制文件的权限")

    def closeEvent(self, event):
        paths = self.control.path_selected
        cache = {
            "origin_path": paths[0],
            "saved_path": paths[1],
            "current_species": self.control.titles.text()
        }
        with open(CACHE_PATH, "w", encoding="utf-8") as f:
            f.write(json.dumps(cache, ensure_ascii=False))

    @staticmethod
    def read_path_cache() -> dict:
        cache = {"origin_path": "", "saved_path": "", "current_species": ""}
        if os.path.exists(CACHE_PATH):
            with open(CACHE_PATH, "r", encoding="utf-8") as f:
                try:
                    cache_saved = json.loads(f.read())
                except json.decoder.JSONDecodeError:
                    cache_saved = {}
            for key in cache:
                try:
                    cache[key] = cache_saved[key]
                except KeyError:
                    continue
        return cache

    @classmethod
    def run(cls):
        app = QtWidgets.QApplication(sys.argv)
        window = cls()
        window.show()
        app.exec()
