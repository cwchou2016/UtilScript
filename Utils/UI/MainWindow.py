import sys
import traceback

from PyQt5 import QtGui
from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal, QRunnable, QThreadPool, Qt
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QFileDialog, QTableWidgetItem, QErrorMessage, \
    QVBoxLayout, QProgressBar

from Utils.BOS.BloodServer import BloodServer, LoginErrorException
from Utils.UI.Widgets import LoginWidget, EdiDownloadWidget

sys._excepthook = sys.excepthook


def exception_hook(exctype, value, traceback):
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)


sys.excepthook = exception_hook


class BServer(QObject):
    verified = pyqtSignal(str)
    connecting_start = pyqtSignal()
    connecting_complete = pyqtSignal()
    downloaded = pyqtSignal(str)
    download_complete = pyqtSignal()
    login_success = pyqtSignal()
    error_msg = pyqtSignal(str)

    bs = BloodServer()


class Download(QRunnable):
    def __init__(self, edi: str, path: str = ""):
        super(Download, self).__init__()
        self.signals = BServer()
        self._edi = edi
        self._path = path

    def run(self) -> None:
        if not BServer.bs.verify_edi(self._edi):
            self.signals.verified.emit("Failed")
            self.signals.downloaded.emit("Skipped")
            self.signals.download_complete.emit()
            return

        self.signals.verified.emit("OK")

        r = BServer.bs.confirm_order(self._edi)
        if r.json().get("statusCode") == "900":
            try:
                BServer.bs.download_edi(self._edi, self._path)
            except Exception as e:
                self.signals.download_complete.emit()
                self.signals.error_msg.emit(str(e))
            else:
                self.signals.downloaded.emit("Complete")
        else:
            self.signals.downloaded.emit("Error")

        self.signals.download_complete.emit()


class Login(QRunnable):
    def __init__(self, user: str, pw: str):
        super(Login, self).__init__()
        self.signals = BServer()
        self._user = user
        self._pw = pw

    def run(self) -> None:
        try:
            BServer.bs.login(self._user, self._pw)
            self.signals.login_success.emit()
        except LoginErrorException as e:
            print(e)
            self.signals.error_msg.emit("帳號或密碼錯誤")


class MainWindow(EdiDownloadWidget, QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.pool = QThreadPool()
        self.pool.setMaxThreadCount(1)
        self.server = BServer()

        self.user = ""
        self.pw = ""
        self.btn_download.setText("下載 [F12]")

        self.show()

        self._windows = LoginWindow(self)
        self._windows.exec()
        self._downloading = DownloadingDialog(self)

        self.line_path.setText("C:\\Blood")

        self.line_order.returnPressed.connect(self.on_btn_add_clicked)
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

        edi = self.line_order.text()
        self.add_edi(edi)

        self.line_order.setText("")
        self.line_order.setFocus()

    @pyqtSlot()
    def on_btn_download_clicked(self):
        row_count = self.table_edi.rowCount()
        if row_count == 0:
            return

        self.connecting_start()
        path = self.line_path.text()

        for idx in range(row_count):
            if self.table_edi.item(idx, 2).text() != "":
                continue

            edi = self.table_edi.item(idx, 0).text()
            download = Download(edi, path)
            download.signals.verified.connect(self.table_edi.item(idx, 1).setText)
            download.signals.downloaded.connect(self.table_edi.item(idx, 2).setText)
            download.signals.download_complete.connect(self.is_downloaded)
            download.signals.error_msg.connect(self._windows.on_error)
            self.pool.start(download)

        self.is_downloaded()

    @pyqtSlot()
    def on_v_label_clicked(self):
        row = self.table_edi.currentRow()
        self.table_edi.removeRow(row)

    def add_edi(self, edi: str):
        row = self.table_edi.rowCount()
        self.table_edi.insertRow(row)
        self.table_edi.setVerticalHeaderItem(row, QTableWidgetItem("刪"))

        self.table_edi.setItem(row, 0, QTableWidgetItem(edi))
        self.table_edi.setItem(row, 1, QTableWidgetItem())
        self.table_edi.setItem(row, 2, QTableWidgetItem())

    def is_downloaded(self):
        row_count = self.table_edi.rowCount()
        for idx in range(row_count):
            if self.table_edi.item(idx, 2).text() == "":
                self._downloading.progress_bar.setValue((idx / row_count) * 100)
                return

        self.connecting_complete()

    def connecting_start(self):
        self._downloading.progress_bar.setValue(0)
        self._downloading.show()
        login = Login(self.user, self.pw)
        self.pool.start(login)
        self.btn_download.setEnabled(False)
        self.btn_add.setEnabled(False)
        self.line_order.setEnabled(False)

    def connecting_complete(self):
        r = BServer.bs.logout()
        print(r.text)
        self.btn_download.setEnabled(True)
        self.btn_add.setEnabled(True)
        self.line_order.setEnabled(True)
        self._downloading.close()

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        if a0.key() == Qt.Key_F12:
            self.on_btn_download_clicked()

    def update_user(self, user: str, pw: str):
        self.user = user
        self.pw = pw


class LoginWindow(QDialog, LoginWidget):
    def __init__(self, parent=None):
        super(LoginWindow, self).__init__(parent)
        self.label_url.setText(BloodServer.Host)
        self.line_name.setFocus()

    @pyqtSlot()
    def on_btn_login_clicked(self):
        self.btn_login.setEnabled(False)
        user = self.line_name.text()
        pw = self.line_pw.text()

        login = Login(user, pw)
        login.signals.login_success.connect(self.on_login_success)
        login.signals.error_msg.connect(self.on_error)
        self.parent().pool.start(login)

    def on_login_success(self):
        user = self.line_name.text()
        pw = self.line_pw.text()

        self.parent().update_user(user, pw)
        r = BServer.bs.logout()
        print(r.text)
        self.hide()

    def on_error(self, msg):
        error = QErrorMessage(self)
        error.showMessage(msg)
        error.show()

        self.btn_login.setEnabled(True)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        sys.exit()


class DownloadingDialog(QDialog):
    def __init__(self, parent=None):
        super(DownloadingDialog, self).__init__(parent)
        self.setWindowTitle("下載中...")
        flag = Qt.WindowFlags(Qt.FramelessWindowHint | Qt.Tool)
        self.setWindowFlags(flag)
        layout = QVBoxLayout(self)
        self.setLayout(layout)

        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    try:
        window = MainWindow()
    except Exception as e:
        print(e)
        traceback.print_exc()
    sys.exit(app.exec_())
