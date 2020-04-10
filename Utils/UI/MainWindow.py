import sys
import time
import traceback

from PyQt5.QtCore import QObject, pyqtSlot, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QFileDialog, QTableWidgetItem

from Utils.UI.Widgets import LoginWidget, EdiDownloadWidget

sys._excepthook = sys.excepthook


def exception_hook(exctype, value, traceback):
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)


sys.excepthook = exception_hook


class Signals(QObject):
    pass


class VerifyEDI(QThread):
    verified = pyqtSignal(int, str)

    def __init__(self, row: int, edi: str):
        super(VerifyEDI, self).__init__()
        self._edi = edi
        self._row = row

    def run(self) -> None:
        time.sleep(3)
        self.verified.emit(self._row, str("OK"))


class MainWindow(EdiDownloadWidget, QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.show()
        self._windows = LoginWindow(self)

        self.line_path.setText("C:\\Blood")

        self.table_edi.verticalHeader().sectionClicked.connect(self.on_v_label_clicked)

    @pyqtSlot()
    def on_btn_dir_clicked(self):
        path = QFileDialog().getExistingDirectory()
        self.line_path.setText(path)

    @pyqtSlot()
    def on_btn_add_clicked(self):
        edi = self.line_order.text()

        if edi == "":
            self.line_order.setFocus()
            return

        row = self.table_edi.rowCount()
        self.table_edi.insertRow(row)
        self.table_edi.setVerticalHeaderItem(row, QTableWidgetItem("刪"))

        edi = self.line_order.text()
        self.table_edi.setItem(row, 0, QTableWidgetItem(edi))
        self.verify_thread = VerifyEDI(row, edi)
        self.verify_thread.verified.connect(self.update_check)
        self.verify_thread.start()

        self.line_order.setText("")
        self.line_order.setFocus()

    @pyqtSlot()
    def on_btn_download_clicked(self):
        pass

    @pyqtSlot()
    def on_v_label_clicked(self):
        row = self.table_edi.currentRow()
        self.table_edi.removeRow(row)

    def update_check(self, row: int, msg: str):
        self.table_edi.setItem(row, 1, QTableWidgetItem(msg))


class LoginWindow(QDialog, LoginWidget):
    def __init__(self, parent=None):
        super(LoginWindow, self).__init__(parent)

    @pyqtSlot()
    def on_btn_login_clicked(self):
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    try:
        window = MainWindow()
    except Exception as e:
        print(e)
        traceback.print_exc()
    sys.exit(app.exec_())