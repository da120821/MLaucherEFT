# -*- coding: utf-8 -*-
import json
import os

import webbrowser
import subprocess
import minecraft_launcher_lib
from PyQt5 import QtCore, QtGui, QtWidgets
from uuid import uuid1
from PyQt5.QtWidgets import QMessageBox
from random_username.generate import generate_username
from setup import Ui_Setings

minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory().replace('minecraft', 'LauncherEFT')




class LoadVersion(QtCore.QThread):
    versions_loaded = QtCore.pyqtSignal(list)

    def run(self):
        versions = []
        for version in minecraft_launcher_lib.utils.get_version_list():
            if version['type'] == 'release':
                versions.append(version['id'])
        self.versions_loaded.emit(versions)



class LaunchThread(QtCore.QThread):
    launch_setup_signal = QtCore.pyqtSignal(str, str,str)
    progress_update_signal = QtCore.pyqtSignal(int, int, str)
    state_update_signal = QtCore.pyqtSignal(bool)
    message_signal = QtCore.pyqtSignal(str)

    version_id = ''
    username = ''
    progress = 0
    progress_max = 0
    progress_label = ''

    def __init__(self):
        super().__init__()
        self.launch_setup_signal.connect(self.launch_setup)

    def launch_setup(self, version_id, username, type_id):
        self.version_id = version_id
        self.username = username
        self.type_id = type_id

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

        if self.type_id.lower() == 'vanilla':
            minecraft_launcher_lib.install.install_minecraft_version(
                version=self.version_id,
                minecraft_directory=minecraft_directory,
                callback={
                    'setStatus': self.update_progress_label,
                    'setProgress': self.update_progress,
                    'setMax': self.update_progress_max
                }
            )

        elif self.type_id.lower() == 'forge':
            """minecraft_launcher_lib.forge.install_forge_version(
                self.version_id,
                minecraft_directory
            )"""
            print("Forge пока не реализован")


        elif self.type_id.lower() == 'fabric':
            """
            minecraft_launcher_lib.fabric.install_fabric(
                self.version_id,
                minecraft_directory
            )"""
            print("fabric пока не реализован")

        elif self.type_id.lower() == 'neoforge':
            """
            minecraft_launcher_lib.neoforge.install_neoforge_version(
                self.version_id,
                minecraft_directory
            )"""
            print("neoforge пока не реализован")


        username = self.username
        if self.username == '':
            username = generate_username()[0]

        options = {
            'username': username,
            'uuid': str(uuid1()),
            'token': '',
            'jvmArguments': [
            '-Xms2G',
            '-Xmx4G']
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
            stop:0 rgba(158, 114, 47, 1), stop:1 rgba(87, 87, 87, 1));
        """)
        Dialog.setFixedSize(942, 620)
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(-10, 530, 951, 90))
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
        self.Username.textChanged.connect(self.save_settings)


        self.VersionSelect = QtWidgets.QComboBox(self.groupBox)
        self.VersionSelect.setGeometry(QtCore.QRect(40, 50, 181, 22))
        self.VersionSelect.setStyleSheet("background-color: rgb(246, 255, 220);\n"
                                         "font: 63 8pt \"Segoe UI Variable Text Semibold\";")
        self.VersionSelect.setCurrentText("")
        self.VersionSelect.setObjectName("VersionSelect")
        self.VersionSelect.addItem("Загрузка...")
        self.VersionSelect.currentTextChanged.connect(self.save_settings)



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
        self.label_1.setPixmap(QtGui.QPixmap("assets/image/mainimage.jpg"))
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
        self.pushButton.clicked.connect(self.telegram)


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
        self.pushButton_4.clicked.connect(self.open_settings)

        self.open_folder = QtWidgets.QPushButton(self.groupBox)
        self.open_folder.setGeometry(QtCore.QRect(830, 50, 101, 23))
        self.open_folder.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.open_folder.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                       "font: 63 8pt \"Segoe UI Variable Text Semibold\";")
        self.open_folder.setObjectName("open_folder")
        self.open_folder.clicked.connect(self.open_dir_launcher)


        #выбрать версию vanila,fabric,neofogre,forge
        self.VersionSelect_2 = QtWidgets.QComboBox(self.groupBox)
        self.VersionSelect_2.setGeometry(QtCore.QRect(230, 50, 151, 22))
        self.VersionSelect_2.setStyleSheet("background-color: rgb(246, 255, 220);\n"
                                           "font: 63 8pt \"Segoe UI Variable Text Semibold\";")
        self.VersionSelect_2.setObjectName("VersionSelect_2")
        self.VersionSelect_2.addItems(["Vanilla","fabric","Forge","NeoForge"])
        self.VersionSelect_2.currentTextChanged.connect(self.save_settings)

        settings = self.load_setting()

        self.Username.setText(settings.get("username", ""))
        self.VersionSelect_2.setCurrentText(settings.get("type", "Vanilla"))

        self.label_1.raise_()
        self.groupBox_3.raise_()
        self.groupBox.raise_()
        self.groupBox_2.raise_()

        self.retranslateUi(Dialog)

        #поток обновления версий

        self.version_thread = LoadVersion()
        self.version_thread.versions_loaded.connect(self.on_versions_loaded)
        self.version_thread.start()

        #поток установки и запуска
        self.launch_thread = LaunchThread()
        self.launch_thread.state_update_signal.connect(self.state_update)
        self.launch_thread.progress_update_signal.connect(self.update_progress)
       # self.launch_thread.message_signal.connect(self.show_message)

        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "MLauncherEFT"))
        self.Start.setText(_translate("Dialog", "Запуск"))
        self.Username.setPlaceholderText(_translate("Dialog", " Username"))
        self.label_2.setText(
            _translate("Dialog", "<html><head/><body><p align=\"center\">Хочешь связаться с нами?</p></body></html>"))
        self.pushButton_2.setText(_translate("Dialog", "EMAIL"))
        self.pushButton.setText(_translate("Dialog", "TELEGRAM"))
        self.pushButton_3.setText(_translate("Dialog", "DISCORD"))
        self.pushButton_4.setText(_translate("Dialog", "Настройки"))
        self.open_folder.setText(_translate("Dialog", "Открыть папку"))

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
        version_id = self.VersionSelect.currentText()
        type_id = self.VersionSelect_2.currentText()
        username = self.Username.text()
        self.launch_thread.launch_setup_signal.emit(version_id,  username, type_id)
        self.launch_thread.start()


    def telegram(self):
        webbrowser.open("https://t.me/Akira_Dev_Horu")

    def email(self):
        webbrowser.open("https://mail.google.com/mail/?view=cm&fs=1&to=mangamce@gmail.com")

    def discord(self):
        webbrowser.open("https://discord.gg/7M5QGSUM")

    def open_settings(self):

        self.settings_window = QtWidgets.QWidget()
        self.ui_settings = Ui_Setings()
        self.ui_settings.setupUi(self.settings_window)
        self.settings_window.show()

    def open_dir_launcher(self):
        os.startfile(minecraft_directory)

    def on_versions_loaded(self, versions):
        self.VersionSelect.clear()
        self.VersionSelect.addItems(versions)
        self.VersionSelect.setEnabled(True)  # включаем обратно

    def load_setting(self):
        if os.path.exists("settings.json"):
            with open("settings.json", "r") as f:
                data = json.load(f)
                return data
        else:
            return {}

    def save_settings(self):
        settings = self.load_setting()

        settings["version"] = self.VersionSelect.currentText()
        settings["type"] = self.VersionSelect_2.currentText()
        settings["username"] = self.Username.text()

        with open("settings.json", "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=4)

    def show_message(self, text):
        QtWidgets.QMessageBox.warning(self, "Внимание", text)



if __name__ == "__main__":
    import sys


    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())