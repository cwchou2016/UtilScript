from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.uic import loadUi


class EdiDownloadWidget(QWidget):
    def __init__(self, parent=None):
        super(EdiDownloadWidget, self).__init__(parent)
        loadUi("EdiDownloadWidget.ui", self)



if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    window = EdiDownloadWidget()
    window.show()

    sys.exit(app.exec_())
