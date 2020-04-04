from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QTableWidgetItem, QAbstractItemView
from PyQt5.uic import loadUi


class EdiDownloadWidget(QWidget):
    def __init__(self, parent=None):
        super(EdiDownloadWidget, self).__init__(parent)
        loadUi("EdiDownloadWidget.ui", self)

        self._path = ""

        self.table_edi.verticalHeader().sectionClicked.connect(self.on_label_clicked)
        self.table_edi.setSelectionMode(QAbstractItemView.NoSelection)
        self.table_edi.setEditTriggers(QAbstractItemView.NoEditTriggers)

    @pyqtSlot()
    def on_label_clicked(self):
        row = self.table_edi.currentRow()
        self.table_edi.removeRow(row)

    @pyqtSlot()
    def on_btn_add_clicked(self):
        edi = self.line_order.text()

        if edi != "":
            row = self.table_edi.rowCount()
            self.table_edi.insertRow(row)
            self.table_edi.setItem(row, 0, QTableWidgetItem(edi))
            self.table_edi.setVerticalHeaderItem(row, QTableWidgetItem("刪"))
            self.line_order.setText("")

        self.line_order.setFocus()

        self.update()

    @pyqtSlot()
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
