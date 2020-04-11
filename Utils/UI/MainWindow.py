import sys
import time
import traceback

from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal, QRunnable, QThreadPool
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QFileDialog, QTableWidgetItem

from Utils.UI.Widgets import LoginWidget, EdiDownloadWidget

sys._excepthook = sys.excepthook


def exception_hook(exctype, value, traceback):
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)


sys.excepthook = exception_hook


class BServer(QObject):
    verified = pyqtSignal(int, str)
    verify_start = pyqtSignal()
    verify_complete = pyqtSignal()
    downloaded = pyqtSignal(int, str)

    is_connecting = False


class VerifyEDI(QRunnable):
    def __init__(self, row: int, edi: str):
        super(VerifyEDI, self).__init__()
        self.signals = BServer()
        self._edi = edi
        self._row = row

    def run(self) -> None:
        time.sleep(1)
        self.signals.verified.emit(self._row, str("OK"))


class Login(QRunnable):
    def __init__(self):
        super(Login, self).__init__()

    def run(self) -> None:
        time.sleep(5)


class DownloadEdi(QRunnable):
    def __init__(self, edi_list: list):
        super(DownloadEdi, self).__init__()
        self.signals = BServer()
        self._edi_list = edi_list
        self._size = len(edi_list)

    def run(self) -> None:
        for idx in range(self._size):
            time.sleep(2)
            print(idx)
            self.signals.downloaded.emit(idx, "Complete")


class MainWindow(EdiDownloadWidget, QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.show()
        self._windows = LoginWindow(self)
        self.server = BServer()

        self.line_path.setText("C:\\Blood")

        self.line_order.returnPressed.connect(self.on_btn_add_clicked)
        self.table_edi.verticalHeader().sectionClicked.connect(self.on_v_label_clicked)
        self.server.verify_start.connect(self.connecting_start)
        self.server.verify_complete.connect(self.connecting_complete)

        self.pool = QThreadPool()
        self.pool.setMaxThreadCount(1)

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

        if not BServer.is_connecting:
            BServer.is_connecting = True
            self.server.verify_start.emit()

        row = self.table_edi.rowCount()
        self.table_edi.insertRow(row)
        self.table_edi.setVerticalHeaderItem(row, QTableWidgetItem("刪"))

        edi = self.line_order.text()
        self.table_edi.setItem(row, 0, QTableWidgetItem(edi))
        work = VerifyEDI(row, edi)
        work.signals.verified.connect(self.update_check)
        self.pool.start(work)

        self.line_order.setText("")
        self.line_order.setFocus()

    @pyqtSlot()
    def on_btn_download_clicked(self):
        print("download")
        row_count = self.table_edi.rowCount()
        to_download = []
        for idx in range(row_count):
            if self.table_edi.item(idx, 1).text() == "OK":
                to_download.append(self.table_edi.item(idx, 0).text())

        print(to_download)
        download = DownloadEdi(to_download)
        download.signals.downloaded.connect(self.update_download)
        self.pool.start(download)

    @pyqtSlot()
    def on_v_label_clicked(self):
        row = self.table_edi.currentRow()
        self.table_edi.removeRow(row)

    def update_check(self, row: int, msg: str):
        self.table_edi.setItem(row, 1, QTableWidgetItem(msg))

        row_count = self.table_edi.rowCount()
        for idx in range(row_count):
            if self.table_edi.item(idx, 1) is None:
                return

        self.server.verify_complete.emit()
        self.btn_download.setEnabled(True)

    def update_download(self, row: int, msg: str):
        self.table_edi.setItem(row, 2, QTableWidgetItem(msg))

    def connecting_start(self):
        self.btn_download.setEnabled(False)
        login = Login()
        self.pool.start(login)

    def connecting_complete(self):
        BServer.is_connecting = False


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
