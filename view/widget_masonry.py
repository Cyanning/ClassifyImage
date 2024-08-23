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

    def set_selected(self, is_selected: bool = None):
        if is_selected is None:
            self.selected = not self.selected
        else:
            self.selected = is_selected
        if self.selected:
            self.lab.setStyleSheet(f"border: {self.frame_width}px solid blue; padding: 0px;")
        else:
            self.lab.setStyleSheet(f"border: 0px; padding: {self.frame_width}px;")


class ImgContainer(QtWidgets.QWidget):
    column = 5

    def __init__(self, parent: QtWidgets.QWidget):
        super().__init__(parent=parent)
        self.labs: list[ImgLabel] = []
        self.selecting = False
        self.setContentsMargins(5, 5, 7, 5)
        self.setLayout(QtWidgets.QGridLayout())

    def show_labels(self, imgs: list[Img]):
        for i, img in enumerate(imgs):
            imglab = ImgLabel(self, img)
            self.labs.append(imglab)
            self.layout().addWidget(imglab, i // self.column, i % self.column)
        self.img_board_resize()

    def reload_labels(self):
        for i, imglab in enumerate(self.labs):
            self.layout().addWidget(imglab, i // self.column, i % self.column)
        self.img_board_resize()

    def img_board_resize(self):
        self.resize(
            self.column * ImgLabel.default_size.width(),
            (len(self.labs) // self.column + 1) * ImgLabel.default_size.height()
        )

    def clear_labels(self):
        while self.layout().count():
            layout_item_widget = self.layout().itemAt(0)
            layout_item_widget.widget().deleteLater()
            self.layout().removeItem(layout_item_widget)

    def saved(self, pathes: list[str]):
        for lab in self.labs:
            if not lab.selected:
                continue
            for _path in pathes:
                lab.source.copy_to(_path)

    def deleted(self):
        labs = []
        while self.labs:
            imglab = self.labs.pop(0)
            if imglab.selected:
                imglab.source.trash()
            else:
                labs.append(imglab)
        self.labs = labs
        self.clear_labels()
        self.reload_labels()

    def clear_selected(self):
        for lab in self.labs:
            if lab.selected:
                lab.set_selected(False)

    # def mousePressEvent(self, arg__1):
    #     print("开启框选")
    #     self.selecting = True

    def mouseMoveEvent(self, event):
        pos = event.position()
        col = int(pos.x() // ImgLabel.default_size.width())
        row = int(pos.y() // ImgLabel.default_size.height())
        select_widget = self.layout().itemAt(row * self.column + col).widget()
        if isinstance(select_widget, ImgLabel):
            select_widget.set_selected(True)
        print(col, row)

    def mouseReleaseEvent(self, arg__1):
        print("框选完毕")


class Masonry(QtWidgets.QScrollArea):
    column = 5

    def __init__(self, parent: QtWidgets.QWidget):
        super().__init__(parent=parent)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.img_container = ImgContainer(self)
        self.setWidget(self.img_container)
