from PyQt5 import QtWidgets
from PyQt5.QtCore import QMetaObject
from PyQt5.QtWidgets import QAbstractItemView, QLabel, QLineEdit, \
    QPushButton, QVBoxLayout, QHBoxLayout, QWidget
from PyQt5.uic import loadUi


class EdiDownloadWidget(QWidget):
    def __init__(self, parent=None):
        super(EdiDownloadWidget, self).__init__(parent)
        loadUi("EdiDownloadWidget.ui", self)
        self.setWindowTitle("下載 EDI")
        self.table_edi.setSelectionMode(QAbstractItemView.NoSelection)
        self.table_edi.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_edi.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.btn_download.setEnabled(False)


class LoginWidget(QWidget):
    def __init__(self, parent=None):
        super(LoginWidget, self).__init__(parent)
        self.setWindowTitle("登入")

        layout = QVBoxLayout(self)
        layout_user = QHBoxLayout()
        layout_pw = QHBoxLayout()
        self.setLayout(layout)

        self.label_name = QLabel("帳號")
        self.label_pw = QLabel("密碼")

        self.line_name = QLineEdit()
        self.line_pw = QLineEdit()
        self.line_pw.setEchoMode(QtWidgets.QLineEdit.Password)

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
