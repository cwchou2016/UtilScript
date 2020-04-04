from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog
from PyQt5.uic import loadUi


class EdiDownloadWidget(QWidget):
    def __init__(self, parent=None):
        super(EdiDownloadWidget, self).__init__(parent)
        loadUi("EdiDownloadWidget.ui", self)

        self._path = ""

    @QtCore.pyqtSlot()
    def on_btn_dir_clicked(self):
        self._path = QFileDialog.getExistingDirectory()
        self.update()

    def update(self):
        self.line_path.setText(self._path)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = EdiDownloadWidget()
    window.show()
    sys.exit(app.exec_())
