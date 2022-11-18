from PyQt5.QtWidgets import QLineEdit, qApp
from PyQt5 import QtCore, QtWidgets
import sys
from json import dumps


class Ui_Form(object):
    def setupUi(self, Form):
        super().__init__()

        Form.setObjectName("Form")
        Form.resize(240, 230)
        Form.setMinimumSize(QtCore.QSize(240, 230))
        Form.setMaximumSize(QtCore.QSize(240, 230))
        Form.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(10, 15, 47, 13))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(10, 45, 47, 13))
        self.label_2.setObjectName("label_2")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(10, 105, 101, 16))
        self.label_4.setObjectName("label_4")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(10, 75, 101, 16))
        self.label_3.setObjectName("label_3")
        self.port = QtWidgets.QSpinBox(Form)
        self.port.setGeometry(QtCore.QRect(120, 40, 111, 22))
        self.port.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.port.setMaximum(60000)
        self.port.setProperty("value", 3306)
        self.port.setObjectName("port")

        self.password = QtWidgets.QLineEdit(Form)
        self.password.setGeometry(QtCore.QRect(120, 100, 113, 20))
        self.password.setTabletTracking(False)
        self.password.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.password.setObjectName("password")

        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(70, 180, 101, 23))
        self.pushButton.setObjectName("pushButton")
        self.user_name = QtWidgets.QLineEdit(Form)
        self.user_name.setGeometry(QtCore.QRect(120, 70, 113, 20))
        self.user_name.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.user_name.setObjectName("user_name")
        self.host = QtWidgets.QLineEdit(Form)
        self.host.setGeometry(QtCore.QRect(120, 10, 113, 20))
        self.host.setObjectName("host")

        self.pass_vis = QtWidgets.QCheckBox(Form)
        self.pass_vis.setGeometry(QtCore.QRect(70, 130, 141, 17))
        self.pass_vis.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.pass_vis.setObjectName("pass_vis")

        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(10, 150, 101, 16))
        self.label_5.setObjectName("label_5")
        self.database = QtWidgets.QLineEdit(Form)
        self.database.setGeometry(QtCore.QRect(120, 150, 113, 20))
        self.database.setTabletTracking(False)
        self.database.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.database.setObjectName("database")
        self.error = QtWidgets.QLabel(Form)
        self.error.setGeometry(QtCore.QRect(10, 200, 221, 16))
        self.error.setObjectName("error")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        self.settings()

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Подключение к серверу"))
        self.label.setText(_translate("Form", "Хост:"))
        self.label_2.setText(_translate("Form", "Порт:"))
        self.label_4.setText(_translate("Form", "Пароль:"))
        self.label_3.setText(_translate("Form", "Имя пользователя:"))
        self.pushButton.setText(_translate("Form", "Подключиться"))
        self.pass_vis.setText(_translate("Form", "Показывать пароль"))
        self.label_5.setText(_translate("Form", "База данных:"))
        self.error.setText(_translate("Form", ""))

    def settings(self):
        self.password.setEchoMode(QLineEdit.Password)
        self.pass_vis.stateChanged.connect(self.show_password)
        self.pushButton.clicked.connect(self.connect)

    def show_password(self):
        if self.pass_vis.isChecked():
            self.password.setEchoMode(QLineEdit.Normal)
        else:
            self.password.setEchoMode(QLineEdit.Password)

    def connect(self):
        host = self.host.text()
        port = self.port.text()
        user = self.user_name.text()
        password = self.password.text()
        database = self.database.text()

        from SQL.test_connect import connect
        res = connect(host, port, user, password, database)
        if not isinstance(res, tuple):
            self.error.setText(res)
        else:
            data = {'host': host, 'port': port,
                    'user': user, 'password':password,
                    'database':database}
            data = dumps(data)
            with open('user.data', 'w') as file:
                file.write(data)
            qApp.quit()

def First_Screen():
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
