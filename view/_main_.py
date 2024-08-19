import os.path
import sys
from PySide6 import QtWidgets
from .widget_masonry import Masonry
from .widget_control import ControlPanel
from model.files import WorkSpace
from model.category import Category


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("图片分类器")

        path = self.read_path_cache()
        self.finder = WorkSpace(path[0])
        try:
            species = self.finder.current().name
        except AttributeError:
            species = None
        self.classify = Category(path[1], None, species)
        self.masonry = Masonry(self)
        self.control = ControlPanel(self, default_origin_path=path[0], default_category_path=path[1])
        self.control.signs.opponent.connect(self.refresh)
        self.control.signs.switch.connect(self.switch)
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
        if self.finder.path:
            if self.masonry.labs:
                self.masonry.clear_labels()
            species = self.finder.current()
            self.masonry.show_labels(species.current().children)
            self.control.titles.text_display(species.name, species.current().name)

    def switch(self, e: int):
        # 切换物种
        if e == 0:
            self.finder.path, self.classify.path = self.control.path_selected
            self.finder.setup(0)
            self.classify.name = self.finder.current().name
        else:
            try:
                match abs(e):
                    case 1:
                        self.finder.current().index += e
                    case 2:
                        self.finder.next()
                    case -2:
                        self.finder.last()
                    case _:
                        raise IndexError
            except IndexError:
                QtWidgets.QMessageBox.warning(self, "错误", "没了")
        self.refresh()

    def saved(self):
        # 执行保存
        target_classify = self.control.categray_selected
        if len(target_classify):
            try:
                self.masonry.saved([self.classify[tc] for tc in target_classify])
            except PermissionError:
                QtWidgets.QMessageBox.warning(self, "错误", "没有复制文件的权限")
        else:
            QtWidgets.QMessageBox.warning(self, "错误", "至少选择一个分类")

    def deleted(self):
        # 执行删除
        try:
            self.masonry.deleted()
            self.refresh()
        except PermissionError:
            QtWidgets.QMessageBox.warning(self, "错误", "没有复制文件的权限")

    def closeEvent(self, event):
        paths = self.control.path_selected
        with open("cache.txt", "w", encoding="utf-8") as f:
            f.write("{}\n{}".format(*paths))

    @staticmethod
    def read_path_cache() -> list[str]:
        paths = [None, None]
        if os.path.exists("cache.txt"):
            with open("cache.txt", "r", encoding="utf-8") as f:
                context = f.readlines()
                if (lines := len(context)) > 1:
                    paths[0] = context[0].strip()
                    paths[1] = context[1].strip()
                elif lines == 1:
                    paths[0] = context[0].strip()
        return paths

    @classmethod
    def run(cls):
        app = QtWidgets.QApplication(sys.argv)
        window = cls()
        window.show()
        app.exec()
