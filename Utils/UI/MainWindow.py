import sys
import traceback

from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QFileDialog

from Utils.UI.Widgets import LoginWidget, EdiDownloadWidget

sys._excepthook = sys.excepthook


def exception_hook(exctype, value, traceback):
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)


sys.excepthook = exception_hook


class Signals(QObject):
    pass


class MainWindow(EdiDownloadWidget, QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.show()
        self._windows = LoginWindow(self)

        self.line_path.setText("C:\\Blood")

    @pyqtSlot()
    def on_btn_dir_clicked(self):
        path = QFileDialog().getExistingDirectory()
        self.line_path.setText(path)

    @pyqtSlot()
    def on_btn_add_clicked(self):
        pass

    @pyqtSlot()
    def on_btn_download_clicked(self):
        pass


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
