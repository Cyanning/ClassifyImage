from PySide6 import QtWidgets
from PySide6 import QtCore
from PySide6 import QtGui
from model.imgs import Img


class ImgLabel(QtWidgets.QLabel):
    frame_width = 5

    def __init__(self, parent: QtWidgets.QWidget, init_size: QtCore.QSize, source: Img):
        super().__init__(parent)
        self.source: Img = source
        self.selected = False
        self.setStyleSheet(f"border: 0px; padding: {self.frame_width}px;")
        self.resize(init_size)
        self.load_img()

    def load_img(self):
        pixmap = QtGui.QPixmap(self.source.path)
        pixmap = pixmap.scaled(
            self.size(),
            QtCore.Qt.AspectRatioMode.KeepAspectRatio,
            QtCore.Qt.TransformationMode.SmoothTransformation
        )
        self.setPixmap(pixmap)

    def set_selected(self, is_selected: bool = None):
        if is_selected is None:
            self.selected = not self.selected
        else:
            self.selected = is_selected
        if self.selected:
            self.setStyleSheet(f"border: {self.frame_width}px solid blue; padding: 0px;")
        else:
            self.setStyleSheet(f"border: 0px; padding: {self.frame_width}px;")


class ImgContainer(QtWidgets.QWidget):
    column = 5
    img_size = QtCore.QSize(320, 320)

    def __init__(self, parent: QtWidgets.QWidget):
        super().__init__(parent=parent)
        self.labs: list[ImgLabel] = []
        self.__focus_lab: ImgLabel | None = None
        layout = QtWidgets.QGridLayout()
        self.setLayout(layout)

    def show_labels(self, imgs: list[Img]):
        while self.layout().count():
            layout_item_widget = self.layout().itemAt(0)
            layout_item_widget.widget().deleteLater()
            self.layout().removeItem(layout_item_widget)
        self.labs.clear()

        for i, img in enumerate(imgs):
            imglab = ImgLabel(self, self.img_size, img)
            self.labs.append(imglab)
            self.layout().addWidget(imglab, i // self.column, i % self.column)
        self.__img_board_resize()

    def reload_labels(self):
        while self.layout().count():
            layout_item_widget = self.layout().itemAt(0)
            self.layout().removeItem(layout_item_widget)

        for i, imglab in enumerate(self.labs):
            self.layout().addWidget(imglab, i // self.column, i % self.column)
        self.__img_board_resize()

    def __img_board_resize(self):
        widget_count = len(self.labs)
        colum = min(widget_count, self.column)
        quotient, remainder = divmod(widget_count, self.column)
        row = quotient + (1 if remainder else 0)
        self.resize(colum * self.img_size.width(), row * self.img_size.height())

    def saved(self, pathes: list[str]):
        for lab in self.labs:
            if not lab.selected:
                continue
            for _path in pathes:
                lab.source.copy_to(_path)

    def deleted(self):
        labs = []
        while self.labs:
            imglab = self.labs.pop()
            if imglab.selected:
                imglab.source.trash()
                imglab.deleteLater()
            else:
                labs.append(imglab)
        labs.reverse()
        self.labs = labs
        self.reload_labels()

    def clear_selected(self):
        for lab in self.labs:
            if lab.selected:
                lab.set_selected(False)

    def grid_of_mouse_target(self, mouse_pos: QtCore.QPointF | QtCore.QPoint):
        col = int(mouse_pos.x() // self.img_size.width())
        row = int(mouse_pos.y() // self.img_size.height())
        item = self.layout().itemAt(row * self.column + col)
        if item is not None:
            return item.widget()

    def loads(self, height: int):
        """
        当前的位置除以图片控件高度取整，得到当前界面显示的行的序数；
        每次加载四行的图片；
        """
        idx_base = height // self.img_size.height() * self.column
        for i in range(self.column * 4):
            item = self.layout().itemAt(idx_base + i)
            if item is None:
                continue
            widget = item.widget()
            if isinstance(widget, ImgLabel) and widget.pixmap() is not None:
                widget.load_img()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            lab = self.grid_of_mouse_target(event.position())
            if isinstance(lab, ImgLabel):
                lab.set_selected()
                self.__focus_lab = lab

    def mouseMoveEvent(self, event):
        if self.__focus_lab is None:
            return
        lab = self.grid_of_mouse_target(event.position())
        if self.__focus_lab is not lab and isinstance(lab, ImgLabel):
            lab.set_selected()
            self.__focus_lab = lab

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.__focus_lab = None


class Masonry(QtWidgets.QScrollArea):
    column = 5

    def __init__(self, parent: QtWidgets.QWidget):
        super().__init__(parent=parent)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.img_container = ImgContainer(self)
        self.setWidget(self.img_container)

    def reset(self):
        self.verticalScrollBar().setValue(0)
        self.horizontalScrollBar().setValue(0)
