from PySide6 import QtWidgets
from PySide6 import QtCore
from model.category import Category


class ControlSigns(QtCore.QObject):
    executer = QtCore.Signal()
    opponent = QtCore.Signal()
    delete = QtCore.Signal()
    switch = QtCore.Signal(int)  # -2 -1 0 1 2


class CategoryButton(QtWidgets.QPushButton):
    def __init__(self, text: str, parent: QtWidgets.QWidget):
        super().__init__(parent)
        self.setText(text)
        self.setFixedSize(200, 40)
        self.selected = False
        self.setStyleSheet("color: #000000")

    def set_selected(self, is_selected: bool):
        self.selected = is_selected
        if self.selected:
            self.setStyleSheet("background-color: blue; color: #FFFFFF;")
        else:
            self.setStyleSheet("background-color: none; color: #000000;")

    def mouseReleaseEvent(self, e):
        self.set_selected(not self.selected)


class AddressEdit(QtWidgets.QLineEdit):
    def __init__(self, text: str, parent: QtWidgets.QWidget):
        super().__init__(parent)
        self.setText(text)
        self.setMinimumHeight(24)
        self.setReadOnly(True)


class ControlButton(QtWidgets.QPushButton):
    def __init__(self, text: str, parent: QtWidgets.QWidget):
        super().__init__(parent)
        self.setText(text)
        self.setMinimumHeight(28)


class TittleForm(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget):
        super().__init__(parent)
        lab1 = QtWidgets.QLabel("品种", self)
        self.line1 = QtWidgets.QLineEdit(self)
        self.line1.setReadOnly(True)

        lab2 = QtWidgets.QLabel("分组", self)
        self.line2 = QtWidgets.QLineEdit(self)
        self.line2.setReadOnly(True)

        layout = QtWidgets.QFormLayout()
        layout.addRow(lab1, self.line1)
        layout.addRow(lab2, self.line2)
        self.setLayout(layout)
        self.setFixedHeight(80)

    def text_display(self, text1: str, text2: str):
        self.line1.setText(text1)
        self.line2.setText(text2)


class ControlPanel(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget, default_origin_path: str = "", default_category_path: str = ""):
        super().__init__(parent)
        self.signs = ControlSigns()
        # 地址
        selector_origin = ControlButton("选择源文件地址", self)
        selector_origin.clicked.connect(self.path_origin_select_event)
        self.path_origin = AddressEdit(default_origin_path, self)

        selector_category = ControlButton("选择分类后的地址", self)
        selector_category.clicked.connect(self.path_category_select_event)
        self.path_category = AddressEdit(default_category_path, self)

        layout_address = QtWidgets.QVBoxLayout()
        layout_address.addWidget(selector_origin)
        layout_address.addWidget(self.path_origin)
        layout_address.addWidget(selector_category)
        layout_address.addWidget(self.path_category)

        # 分类
        self.btns = [CategoryButton(key, self) for key in Category.category]
        layout_btns = QtWidgets.QVBoxLayout()
        layout_btns.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        for btn in self.btns:
            layout_btns.addWidget(btn)

        # 命令
        self.titles = TittleForm(self)
        executer = ControlButton("确定 - 执行转移", self)
        executer.clicked.connect(self.executer_event)

        delete = ControlButton("删除 - 选中的图", self)
        delete.clicked.connect(self.delete_event)

        opponent = ControlButton("取消 - 所有选择", self)
        opponent.clicked.connect(self.opponent_event)

        pre_series = ControlButton("上一组图", self)
        pre_series.clicked.connect(lambda: self.switch_event(-1))

        nxt_series = ControlButton("下一组图", self)
        nxt_series.clicked.connect(lambda: self.switch_event(1))

        pre_species = ControlButton("上一个品种", self)
        pre_species.clicked.connect(lambda: self.switch_event(-2))

        nxt_species = ControlButton("下一个品种", self)
        nxt_species.clicked.connect(lambda: self.switch_event(2))

        layout_command = QtWidgets.QGridLayout()
        layout_command.addWidget(self.titles, 0, 0, 1, 2)
        layout_command.addWidget(executer, 1, 0, 1, 2)
        layout_command.addWidget(delete, 2, 0, 1, 2)
        layout_command.addWidget(opponent, 3, 0, 1, 2)
        layout_command.addWidget(pre_series, 4, 0)
        layout_command.addWidget(nxt_series, 4, 1)
        layout_command.addWidget(pre_species, 5, 0)
        layout_command.addWidget(nxt_species, 5, 1)

        # 总布局
        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(layout_address)
        layout.addLayout(layout_btns)
        layout.addLayout(layout_command)

        self.setLayout(layout)
        self.setFixedWidth(250)

    def executer_event(self):
        # 执行任务事件
        self.signs.executer.emit()
        self.opponent_event()

    def opponent_event(self):
        # 刷新界面事件
        for btn in self.btns:
            btn.set_selected(False)
        self.signs.opponent.emit()

    def switch_event(self, direction: int):
        # 切换图片事件
        self.opponent_event()
        self.signs.switch.emit(direction)

    def delete_event(self):
        # 删除图片事件
        self.signs.delete.emit()

    def path_origin_select_event(self):
        # 选择源文件地址
        filePath = QtWidgets.QFileDialog.getExistingDirectory(self, "选择路径")
        if filePath:
            self.path_origin.setText(filePath)
        self.switch_event(0)

    def path_category_select_event(self):
        # 选择分类后地址
        filePath = QtWidgets.QFileDialog.getExistingDirectory(self, "选择路径")
        if filePath:
            self.path_category.setText(filePath)
        self.switch_event(0)

    @property
    def categray_selected(self) -> list[str]:
        # 选择的分类
        return [btn.text() for btn in self.btns if btn.selected]

    @property
    def path_selected(self) -> tuple[str, str]:
        # 选择的地址
        return self.path_origin.text(), self.path_category.text()
