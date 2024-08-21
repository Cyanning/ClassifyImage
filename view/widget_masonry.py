from PySide6 import QtWidgets
from PySide6 import QtCore
from PySide6 import QtGui
from model.imgs import Img


class ImgLabel(QtWidgets.QWidget):
    default_size = QtCore.QSize(320, 320)
    frame_width = 5

    def __init__(self, parent: QtWidgets.QWidget, source: Img):
        super().__init__(parent)
        self.lab = QtWidgets.QLabel(self)
        layout = QtWidgets.QStackedLayout()
        layout.addWidget(self.lab)
        self.setLayout(layout)

        self.source = source
        self.selected = False
        pic = QtGui.QPixmap(self.source.path)
        pic = pic.scaled(
            self.default_size,
            QtCore.Qt.AspectRatioMode.KeepAspectRatio,
            QtCore.Qt.TransformationMode.SmoothTransformation
        )
        self.lab.setPixmap(pic)
        self.setStyleSheet(f"border: 0px; padding: {self.frame_width}px;")

    def set_selected(self, is_selected: bool):
        self.selected = is_selected
        if self.selected:
            self.lab.setStyleSheet(f"border: {self.frame_width}px solid blue; padding: 0px;")
        else:
            self.lab.setStyleSheet(f"border: 0px; padding: {self.frame_width}px;")

    def mouseReleaseEvent(self, event):
        self.set_selected(not self.selected)


class Masonry(QtWidgets.QScrollArea):
    column = 5

    def __init__(self, parent: QtWidgets.QWidget):
        super().__init__(parent=parent)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.img_board = QtWidgets.QWidget(self)
        self.img_board.setContentsMargins(5, 5, 7, 5)
        self.img_board.setLayout(QtWidgets.QGridLayout())
        self.setWidget(self.img_board)

        self.labs: list[ImgLabel] = []

    def show_labels(self, imgs: list[Img]):
        for i, img in enumerate(imgs):
            imglab = ImgLabel(self.img_board, img)
            self.labs.append(imglab)
            self.img_board.layout().addWidget(imglab, i // self.column, i % self.column)

        self.img_board.resize(
            self.column * ImgLabel.default_size.width(),
            (len(self.labs) // self.column + 1) * ImgLabel.default_size.height()
        )

    def clear_labels(self):
        while self.img_board.layout().count():
            layout_item_widget = self.img_board.layout().itemAt(0)
            layout_item_widget.widget().deleteLater()
            self.img_board.layout().removeItem(layout_item_widget)
        self.labs.clear()

    def saved(self, pathes: list[str]):
        for lab in self.labs:
            if not lab.selected:
                continue
            for _path in pathes:
                lab.source.copy_to(_path)

    def deleted(self):
        for lab in self.labs:
            if lab.selected:
                lab.source.trash()

    def clear_selected(self):
        for lab in self.labs:
            if lab.selected:
                lab.set_selected(False)
