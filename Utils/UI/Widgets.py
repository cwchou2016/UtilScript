import sys
import time
import traceback

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot, QRunnable, QThreadPool, QObject, pyqtSignal, QMetaObject
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QTableWidgetItem, QAbstractItemView, QLabel, QLineEdit, \
    QPushButton, QVBoxLayout, QHBoxLayout, QDialog
from PyQt5.uic import loadUi

sys._excepthook = sys.excepthook


def exception_hook(exctype, value, traceback):
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)


sys.excepthook = exception_hook


class Signals(QObject):
    validation = pyqtSignal(int, str)


class ValidateOrder(QRunnable):

    def __init__(self, row: int, edi: str, parent=None):
        super(ValidateOrder, self).__init__()
        self.signal = Signals()
        self.edi = edi
        self.row = row

    def run(self):
        time.sleep(5)
        self.signal.validation.emit(self.row, "OK")


class EdiDownloadWidget(QDialog):
    def __init__(self, parent=None):
        super(EdiDownloadWidget, self).__init__(parent)
        loadUi("EdiDownloadWidget.ui", self)

        self._path = ""

        self.table_edi.verticalHeader().sectionClicked.connect(self.on_label_clicked)
        self.table_edi.setSelectionMode(QAbstractItemView.NoSelection)
        self.table_edi.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.btn_download.setEnabled(False)

        self.pool = QThreadPool()

    @pyqtSlot()
    def on_label_clicked(self):
        row = self.table_edi.currentRow()
        self.table_edi.removeRow(row)

    @pyqtSlot()
    def on_btn_add_clicked(self):
        self.btn_download.setEnabled(False)

        edi = self.line_order.text()

        if edi != "":
            row = self.table_edi.rowCount()
            self.table_edi.insertRow(row)
            self.table_edi.setVerticalHeaderItem(row, QTableWidgetItem("刪"))

            self.table_edi.setItem(row, 0, QTableWidgetItem(edi))

            work = ValidateOrder(row, str(edi))
            work.signal.validation.connect(self.update_check)
            self.pool.start(work)

            self.line_order.setText("")

        self.line_order.setFocus()

    def update_check(self, row, string):
        self.table_edi.setItem(row, 1, QTableWidgetItem(string))
        row_count = self.table_edi.rowCount()
        for idx in range(row_count):
            if self.table_edi.item(idx, 1) is None:
                return

        self.btn_download.setEnabled(True)

    @pyqtSlot()
    def on_btn_dir_clicked(self):
        self._path = QFileDialog.getExistingDirectory()
        self.update()

    def update(self):
        self.line_path.setText(self._path)


class LoginWidget(QWidget):
    def __init__(self):
        super(LoginWidget, self).__init__()

        layout = QVBoxLayout(self)
        layout_user = QHBoxLayout()
        layout_pw = QHBoxLayout()
        self.setLayout(layout)

        self.label_name = QLabel("帳號")
        self.label_pw = QLabel("密碼")

        self.line_name = QLineEdit()
        self.line_pw = QLineEdit()
        self.line_pw.setEchoMode(QtWidgets.QLineEdit.Password)
        self.line_pw.returnPressed.connect(self.on_btn_login_clicked)

        self.btn_login = QPushButton("登入", self)
        self.btn_login.setObjectName("btn_login")

        layout_user.addWidget(self.label_name)
        layout_user.addWidget(self.line_name)

        layout_pw.addWidget(self.label_pw)
        layout_pw.addWidget(self.line_pw)

        layout.addLayout(layout_user, 0)
        layout.addLayout(layout_pw, 0)
        layout.addWidget(self.btn_login)

        QMetaObject.connectSlotsByName(self)

    @pyqtSlot()
    def on_btn_login_clicked(self):
        self.btn_login.setEnabled(False)
        self.btn_login.setText("登入中....")
        time.sleep(1)  # TODO: Login
        self.close()
        edi_window = EdiDownloadWidget(self)
        edi_window.show()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    try:
        window = LoginWidget()
        window.show()
    except Exception as e:
        print(e)
        traceback.print_exc()
    sys.exit(app.exec_())
