# -*- coding: utf-8 -*-
import json
import os


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Setings(object):
    def setupUi(self, Setings):
        Setings.setObjectName("Setings")
        Setings.resize(521, 353)
        Setings.setStyleSheet("\n"
"background-color: rgb(255, 208, 114);")

        self.gridLayoutWidget = QtWidgets.QWidget(Setings)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 0, 501, 351))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)

        #Мин память
        self.gridLayout.setObjectName("gridLayout")
        self.comboBox_2 = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.comboBox_2.setStyleSheet("background-color: rgb(255, 240, 202);\n"
                                      "font: \"10pt Segoe UI Variable Text Semibold\";")
        self.comboBox_2.setObjectName("comboBox_2")
        self.gridLayout.addWidget(self.comboBox_2, 1, 1, 1, 1)
        self.comboBox_2.addItems(["Xms2G", "Xms4G", "Xms6G", "Xms8G"])

        self.MaxMemory_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.MaxMemory_3.setStyleSheet("background-color: rgb(255, 240, 202);\n"
                                       "padding:5%;\n"
                                       "font: 10pt \"Segoe UI Variable Text Semibold\";\n"
"")
        self.MaxMemory_3.setObjectName("MaxMemory_3")
        self.gridLayout.addWidget(self.MaxMemory_3, 2, 0, 1, 1)
        self.MaxMemory_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.MaxMemory_2.setStyleSheet("background-color: rgb(255, 240, 202);\n"
                                       "padding:5%;\n"
                                       "font: 10pt \"Segoe UI Variable Text Semibold\";\n"
                                       "")
        self.MaxMemory_2.setObjectName("MaxMemory_2")
        self.gridLayout.addWidget(self.MaxMemory_2, 0, 0, 1, 1)

        #макс память
        self.comboBox = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.comboBox.setStyleSheet("background-color: rgb(255, 240, 202);\n"
                                    "font: \"10pt Segoe UI Variable Text Semibold\";")
        self.comboBox.setObjectName("comboBox")
        self.gridLayout.addWidget(self.comboBox, 0, 1, 1, 1)
        self.comboBox.addItems(["Xms2G","Xms4G","Xms6G","Xms8G"])



        self.MaxMemory = QtWidgets.QLabel(self.gridLayoutWidget)
        self.MaxMemory.setStyleSheet("background-color: rgb(255, 240, 202);\n"
                                     "padding:5%;\n"
                                     "font: 10pt \"Segoe UI Variable Text Semibold\";\n"
"")
        self.MaxMemory.setObjectName("MaxMemory")
        self.gridLayout.addWidget(self.MaxMemory, 1, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 4, 0, 1, 1)


        self.comboBox_3 = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.comboBox_3.setStyleSheet("background-color: rgb(255, 240, 202);\n "
                                      "font: \"10pt Segoe UI Variable Text Semibold\";")
        self.comboBox_3.setObjectName("comboBox_3")
        self.gridLayout.addWidget(self.comboBox_3, 2, 1, 1, 1)
        self.comboBox_3.addItems(["Русский"])


        self.checkBox = QtWidgets.QCheckBox(self.gridLayoutWidget)
        self.checkBox.setStyleSheet("background-color: rgb(255, 240, 202);\n"
                                    "padding:5%;\n"
                                    "font: 10pt \"Segoe UI Variable Text Semibold\";\n"
                                    "font: \"10pt Segoe UI Variable Text Semibold\";")
        self.checkBox.setObjectName("checkBox")
        self.gridLayout.addWidget(self.checkBox, 3, 0, 1, 1)

        self.gridLayout.addWidget(self.MaxMemory_2, 0, 0, 1, 1)
        self.Save = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.Save.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Save.setMouseTracking(False)
        self.Save.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                "font: 63 8pt \"Segoe UI Variable Text Semibold\";")
        self.Save.setObjectName("Save")
        self.gridLayout.addWidget(self.Save, 5, 0, 1, 1)
        self.Save.clicked.connect(self.save_setting)


        self.Cancel = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.Cancel.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Cancel.setMouseTracking(False)
        self.Cancel.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                  "font: 63 8pt \"Segoe UI Variable Text Semibold\";")
        self.Cancel.setObjectName("Cancel")
        self.gridLayout.addWidget(self.Cancel, 5, 1, 1, 1)


        #загрузка настроек
        settings = self.load_setting()

        self.comboBox.setCurrentText(settings.get("memoryMax", "Xmx4G"))
        self.comboBox_2.setCurrentText(settings.get("memoryMin", "Xms2G"))
        self.comboBox_3.setCurrentText(settings.get("language", "Русский"))

        self.retranslateUi(Setings)
        QtCore.QMetaObject.connectSlotsByName(Setings)

    def load_setting(self):
        if os.path.exists("settings.json"):
            with open("settings.json", "r") as f:
                data = json.load(f)
                return data
        else:
            return {}

    def save_setting(self):
        settings = self.load_setting()

        settings["memoryMax"] = self.comboBox.currentText()
        settings["memoryMin"] = self.comboBox_2.currentText()
        settings["language"] = self.comboBox_3.currentText()

        with open("settings.json", "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=4)

    def retranslateUi(self, Setings):
        _translate = QtCore.QCoreApplication.translate
        Setings.setWindowTitle(_translate("Setings", "Настройки"))
        self.MaxMemory_3.setText(_translate("Setings", "Язык"))
        self.MaxMemory_2.setText(_translate("Setings", "Максимальный размер выделенной памяти"))
        self.MaxMemory.setText(_translate("Setings", "Минимальный размер выделенной памяти"))
        self.checkBox.setText(_translate("Setings", "Только релизы / Все версии"))
        self.Save.setText(_translate("Setings", "Сохранить"))
        self.Cancel.setText(_translate("Setings", "Отмена"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Setings = QtWidgets.QWidget()
    ui = Ui_Setings()
    ui.setupUi(Setings)
    Setings.show()
    sys.exit(app.exec_())
