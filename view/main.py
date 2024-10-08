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
        self.finder = WorkSpace(cache["origin_path"], cache["magnitude"])
        try:
            self.finder.init_build(cache["current_species"])
        except FileNotFoundError:
            self.finder.path.set_path()

        self.classify = Category(cache["saved_path"])

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
            self.masonry.reset()
            self.masonry.img_container.show_labels(self.finder.species.imgs)
            self.control.titles.text_display(self.finder.species.path.name)

    def oppoent(self):
        # 清除界面中选择项
        self.control.clear_selected()
        self.masonry.img_container.clear_selected()

    def switch(self, e: int):
        # 切换物种
        if e == 0:
            finder_path, classify_path = self.control.path_selected
            if self.classify.path != classify_path:
                self.classify.path.set_path(classify_path)
                self.oppoent()
            if self.finder.path != finder_path:
                self.finder.path.set_path(finder_path)
                self.finder.init_build(0)
                self.refresh()
        elif abs(e) == 1:
            while True:
                try:
                    self.finder.cursor += e
                except AssertionError:
                    continue
                except IndexError:
                    QtWidgets.QMessageBox.warning(self, "错误", "没了")
                    break
                except FileNotFoundError:
                    QtWidgets.QMessageBox.warning(self, "错误", "地址错误，请重新指定地址")
                else:
                    self.refresh()
                    break

    def saved(self):
        # 执行保存
        categray_selections = self.control.categray_selected
        if len(categray_selections):
            try:
                self.masonry.img_container.saved(
                    [
                        self.classify.get_path(self.finder.species.path.name, category_name)
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
            self.masonry.img_container.deleted()
            self.finder.build()
        except PermissionError:
            QtWidgets.QMessageBox.warning(self, "错误", "没有复制文件的权限")

    def closeEvent(self, event):
        paths = self.control.path_selected
        cache = {
            "origin_path": paths[0],
            "saved_path": paths[1],
            "current_species": self.control.titles.text(),
            "magnitude": self.finder.magnitude
        }
        with open(CACHE_PATH, "w", encoding="utf-8") as f:
            f.write(json.dumps(cache, ensure_ascii=False))

    @staticmethod
    def read_path_cache() -> dict:
        cache = {"origin_path": "", "saved_path": "", "current_species": "", "magnitude": 0}
        if os.path.exists(CACHE_PATH):
            with open(CACHE_PATH, "r", encoding="utf-8") as f:
                try:
                    cache_saved = json.loads(f.read())
                except json.decoder.JSONDecodeError:
                    cache_saved = {}
            for key in cache:
                if key in cache_saved:
                    cache[key] = cache_saved[key]
        return cache

    @classmethod
    def run(cls):
        app = QtWidgets.QApplication(sys.argv)
        window = cls()
        window.show()
        app.exec()
