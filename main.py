# -*- coding: utf-8 -*-

import webbrowser
import subprocess
import minecraft_launcher_lib
from PyQt5 import QtCore, QtGui, QtWidgets
from uuid import uuid1
from random_username.generate import generate_username

minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory().replace('minecraft', 'LauncherEFT')


class LaunchThread(QtCore.QThread):
    launch_setup_signal = QtCore.pyqtSignal(str, str)
    progress_update_signal = QtCore.pyqtSignal(int, int, str)
    state_update_signal = QtCore.pyqtSignal(bool)

    version_id = ''
    username = ''
    progress = 0
    progress_max = 0
    progress_label = ''

    def __init__(self):
        super().__init__()
        self.launch_setup_signal.connect(self.launch_setup)

    def launch_setup(self, version_id, username):
        self.version_id = version_id
        self.username = username

    def update_progress_label(self, value):
        self.progress_label = value
        self.progress_update_signal.emit(self.progress, self.progress_max, self.progress_label)

    def update_progress(self, value):
        self.progress = value
        self.progress_update_signal.emit(self.progress, self.progress_max, self.progress_label)

    def update_progress_max(self, value):
        self.progress_max = value
        self.progress_update_signal.emit(self.progress, self.progress_max, self.progress_label)

    def run(self):
        self.state_update_signal.emit(True)
        minecraft_launcher_lib.install.install_minecraft_version(
            version=self.version_id,
            minecraft_directory=minecraft_directory,
            callback={'setStatus': self.update_progress_label, 'setProgress': self.update_progress,
                      'setMax': self.update_progress_max}
        )

        username = self.username
        if self.username == '':
            username = generate_username()[0]

        options = {
            'username': username,
            'uuid': str(uuid1()),
            'token': ''
        }

        subprocess.call(
            minecraft_launcher_lib.command.get_minecraft_command(
                version=self.version_id,
                minecraft_directory=minecraft_directory,
                options=options
            )
        )
        self.state_update_signal.emit(False)


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(942, 620)
        Dialog.setStyleSheet("""
            background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, 
            stop:0 rgba(55, 144, 40, 255), stop:1 rgba(155, 163, 9));
        """)
        Dialog.setFixedSize(942, 620)
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(-10, 530, 951, 91))
        self.groupBox.setStyleSheet("background-color: rgb(255, 255, 255, 20%);")
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")

        self.Start = QtWidgets.QPushButton(self.groupBox)
        self.Start.setGeometry(QtCore.QRect(830, 20, 101, 23))
        self.Start.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Start.setMouseTracking(False)
        self.Start.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                 "font: 63 8pt \"Segoe UI Variable Text Semibold\";")
        self.Start.setObjectName("Start")
        self.Start.clicked.connect(self.launch_game)

        self.Username = QtWidgets.QLineEdit(self.groupBox)
        self.Username.setEnabled(True)
        self.Username.setGeometry(QtCore.QRect(40, 20, 181, 21))
        self.Username.setStyleSheet("background-color: rgb(246, 255, 220);\n"
                                    "font: 63 8pt \"Segoe UI Variable Text Semibold\";")
        self.Username.setInputMask("")
        self.Username.setText("")
        self.Username.setMaxLength(30)
        self.Username.setFrame(False)
        self.Username.setCursorPosition(0)
        self.Username.setObjectName("Username")

        self.VersionSelect = QtWidgets.QComboBox(self.groupBox)
        self.VersionSelect.setGeometry(QtCore.QRect(40, 50, 181, 22))
        self.VersionSelect.setStyleSheet("background-color: rgb(246, 255, 220);\n"
                                         "font: 63 8pt \"Segoe UI Variable Text Semibold\";")
        self.VersionSelect.setCurrentText("")
        self.VersionSelect.setObjectName("VersionSelect")

        for version in minecraft_launcher_lib.utils.get_version_list():
            if version['type'] == 'release':  # Только релизы
                self.VersionSelect.addItem(version['id'])

        self.progressBar = QtWidgets.QProgressBar(self.groupBox)
        self.progressBar.setGeometry(QtCore.QRect(230, 20, 581, 21))
        self.progressBar.setStyleSheet("color: rgb(215, 250, 255);")
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.progressBar.setVisible(False)

        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(230, 50, 581, 21))
        self.label.setText("")
        self.label.setObjectName("label")
        self.label.setVisible(False)

        self.label_1 = QtWidgets.QLabel(Dialog)
        self.label_1.setGeometry(QtCore.QRect(0, 0, 941, 621))
        self.label_1.setText("")
        self.label_1.setPixmap(QtGui.QPixmap("assets/mainimage.jpg"))
        self.label_1.setScaledContents(True)
        self.label_1.setObjectName("label_1")

        self.groupBox_2 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_2.setGeometry(QtCore.QRect(30, 30, 741, 481))
        self.groupBox_2.setStyleSheet("background-color:rgb(200, 194, 19, 45%)\n"
                                      "")
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")

        self.groupBox_3 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_3.setGeometry(QtCore.QRect(800, 30, 131, 481))
        self.groupBox_3.setStyleSheet("background-color:rgb(200, 194, 19, 45%)\n"
                                      "")
        self.groupBox_3.setTitle("")
        self.groupBox_3.setObjectName("groupBox_3")

        self.label_2 = QtWidgets.QLabel(self.groupBox_3)
        self.label_2.setGeometry(QtCore.QRect(10, 10, 111, 51))
        self.label_2.setStyleSheet("background-color: rgb(255, 238, 175);\n"
                                   "font: 63 8pt \"Segoe UI Variable Text Semibold\";")
        self.label_2.setTextFormat(QtCore.Qt.AutoText)
        self.label_2.setScaledContents(True)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")

        #связь email
        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 120, 111, 31))
        self.pushButton_2.setStyleSheet("background-color: rgb(255, 238, 175);\n"
                                        "font: 63 8pt \"Segoe UI Variable Text Semibold\";")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.email)

        #связь Тг
        self.pushButton = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton.setGeometry(QtCore.QRect(10, 80, 111, 31))
        self.pushButton.setStyleSheet("background-color: rgb(255, 238, 175);\n"
                                      "font: 63 8pt \"Segoe UI Variable Text Semibold\";")
        self.pushButton.setObjectName("pushButton")


        #связь Discord
        self.pushButton_3 = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_3.setGeometry(QtCore.QRect(10, 160, 111, 31))
        self.pushButton_3.setStyleSheet("background-color: rgb(255, 238, 175);\n"
                                        "font: 63 8pt \"Segoe UI Variable Text Semibold\";")
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.discord)

        self.pushButton_4 = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_4.setGeometry(QtCore.QRect(10, 440, 111, 31))
        self.pushButton_4.setStyleSheet("background-color: rgb(255, 238, 175);\n"
                                        "font: 63 8pt \"Segoe UI Variable Text Semibold\";")
        self.pushButton_4.setObjectName("pushButton_4")

        self.label_1.raise_()
        self.groupBox_3.raise_()
        self.groupBox.raise_()
        self.groupBox_2.raise_()

        self.retranslateUi(Dialog)

        self.launch_thread = LaunchThread()
        self.launch_thread.state_update_signal.connect(self.state_update)
        self.launch_thread.progress_update_signal.connect(self.update_progress)

        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.Start.setText(_translate("Dialog", "Запуск"))
        self.Username.setPlaceholderText(_translate("Dialog", " Username"))
        self.label_2.setText(
            _translate("Dialog", "<html><head/><body><p align=\"center\">Хочешь связаться с нами?</p></body></html>"))
        self.pushButton_2.setText(_translate("Dialog", "EMAIL"))
        self.pushButton.setText(_translate("Dialog", "TELEGRAM"))
        self.pushButton_3.setText(_translate("Dialog", "DISCORD"))
        self.pushButton_4.setText(_translate("Dialog", "Настройки"))

    def state_update(self, value):
        self.Start.setDisabled(value)
        self.label.setVisible(value)
        self.progressBar.setVisible(value)

    def update_progress(self, progress, max_progress, label):
        if max_progress > 0:
            self.progressBar.setMaximum(max_progress)
        self.progressBar.setValue(progress)
        self.label.setText(label)

    def launch_game(self):
        self.launch_thread.launch_setup_signal.emit(self.VersionSelect.currentText(), self.Username.text())
        self.launch_thread.start()

    def telegram(self):
        webbrowser.open("https://t.me/Akira_Dev_Horu")

    def email(self):
        webbrowser.open("https://mail.google.com/mail/?view=cm&fs=1&to=mangamce@gmail.com")

    def discord(self):
        webbrowser.open("https://discord.gg/7M5QGSUM")

if __name__ == "__main__":
    QtWidgets.QApplication.setAttribute(QtCore.Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())