# -*- coding: utf-8 -*-

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
            callback={'setStatus': self.update_progress_label, 'setProgress': self.update_progress, 'setMax': self.update_progress_max}
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
        self.groupBox.setGeometry(QtCore.QRect(-1, 530, 951, 100))
        self.groupBox.setStyleSheet("background-color: rgb(255, 255, 255, 20%);")
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")

        self.Start = QtWidgets.QPushButton(self.groupBox)
        self.Start.setGeometry(QtCore.QRect(830, 20, 101, 23))
        self.Start.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Start.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.Start.setObjectName("Start")
        self.Start.clicked.connect(self.launch_game)

        self.Username = QtWidgets.QLineEdit(self.groupBox)
        self.Username.setGeometry(QtCore.QRect(40, 20, 181, 21))
        self.Username.setStyleSheet("background-color: rgb(246, 255, 220);")
        self.Username.setMaxLength(30)
        self.Username.setPlaceholderText("Username")
        self.Username.setObjectName("Username")

        self.VersionSelect = QtWidgets.QComboBox(self.groupBox)
        self.VersionSelect.setGeometry(QtCore.QRect(40, 50, 181, 22))
        self.VersionSelect.setStyleSheet("background-color: rgb(246, 255, 220);")
        self.VersionSelect.setObjectName("VersionSelect")

        # Получение списка версий
        for version in minecraft_launcher_lib.utils.get_version_list():
            self.VersionSelect.addItem(version['id'])

        self.progressBar = QtWidgets.QProgressBar(self.groupBox)
        self.progressBar.setGeometry(QtCore.QRect(230, 20, 581, 21))
        self.progressBar.setStyleSheet("color: rgb(215, 250, 255);")
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.progressBar.setVisible(False)

        self.label = QtWidgets.QLabel(self.groupBox)  # ИСПРАВЛЕНО: название из UI
        self.label.setGeometry(QtCore.QRect(230, 50, 541, 21))
        self.label.setText("")
        self.label.setStyleSheet("color: white;")
        self.label.setVisible(False)
        self.label.setObjectName("label")

        self.label_1 = QtWidgets.QLabel(Dialog)  # ИСПРАВЛЕНО: название из UI
        self.label_1.setGeometry(QtCore.QRect(0, 0, 942, 620))
        self.label_1.setText("")
        self.label_1.setPixmap(QtGui.QPixmap("assets/mainimage.jpg"))
        self.label_1.setScaledContents(True)
        self.label_1.setObjectName("label_1")

        self.groupBox_2 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_2.setGeometry(QtCore.QRect(30, 30, 761, 481))
        self.groupBox_2.setStyleSheet("background-color:rgb(200, 194, 19, 45%)")
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")

        # Порядок отображения
        self.label_1.raise_()
        self.groupBox.raise_()
        self.groupBox_2.raise_()

        self.retranslateUi(Dialog)

        self.launch_thread = LaunchThread()
        self.launch_thread.state_update_signal.connect(self.state_update)
        self.launch_thread.progress_update_signal.connect(self.update_progress)

        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Minecraft Launcher"))
        self.Start.setText(_translate("Dialog", "Запуск"))

    def state_update(self, value):
        self.Start.setDisabled(value)
        self.label.setVisible(value)  # ИСПРАВЛЕНО: используем label
        self.progressBar.setVisible(value)

    def update_progress(self, progress, max_progress, label):
        if max_progress > 0:
            self.progressBar.setMaximum(max_progress)
        self.progressBar.setValue(progress)
        self.label.setText(label)  # ИСПРАВЛЕНО: используем label

    def launch_game(self):
        version = self.VersionSelect.currentText()
        username = self.Username.text()

        if not version:
            QtWidgets.QMessageBox.warning(None, "Ошибка", "Выберите версию Minecraft")
            return

        self.launch_thread.launch_setup_signal.emit(version, username)
        self.launch_thread.start()


if __name__ == "__main__":
    QtWidgets.QApplication.setAttribute(QtCore.Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())