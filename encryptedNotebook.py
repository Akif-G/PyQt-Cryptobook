# This application is an implementation for MPI internship application,
# previously added an cryptographic key implementation, and changed a few properties.
# note: install PyQt5 and cryptography libraries for further implementation
##
# This application is created by Akif Gultekin
# mehmetgultekin@sabanciuniv.edu
# https://github.com/Akif-G
# project start date: 28.01.2020
# last edit: 06.04.2020
##
# two main screen:
# asking the mood of the user (now used as a key screen)
# taking notes and saving them for later usage

import sys
from winsound import Beep
import os.path
import threading
import time
from datetime import date
from PyQt5.QtWidgets import QTextEdit, QSlider, QGraphicsDropShadowEffect, QLabel, QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox
from PyQt5.QtGui import QIcon, QPalette, QFont
from PyQt5.QtCore import pyqtSlot, Qt

import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# key derivation function that derive bytes suitable for cryptographic operations, from string etc. ...
# changed key to my name which will secure it more.
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=b'mehmetgultekin',
    iterations=10000000,
    backend=default_backend()
)


# main decider if password is...
askedAlready = False

# reads data file and returns the data except the last login date


def textTaker():
    readFile = open("data_pyqt_implementation", "r")
    readFile.seek(10)
    data = readFile.read()
    readFile.close()
    return data


class App(QMainWindow):
    # main app screen
    def __init__(self, Survey):
        # some settings for the app
        super().__init__()
        self.title = 'Stay Focused'
        self.left = 650
        self.top = 200
        self.width = 580
        self.height = 700
        self.key = Survey.key
        self.initUI()

    # User Interface functions
    def initUI(self):
        # settings
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # get 3 shadow for 3 box in main user interface
        self.shadow = QGraphicsDropShadowEffect(
            blurRadius=8, xOffset=6, yOffset=6)
        self.shadow2 = QGraphicsDropShadowEffect(
            blurRadius=8, xOffset=6, yOffset=6)
        self.shadow3 = QGraphicsDropShadowEffect(
            blurRadius=8, xOffset=6, yOffset=6)

        # Create textbox for title
        self.text = QLabel("Please enter your notes here", self)
        self.text.resize(600, 40)
        self.text.setFont(QFont('SansSerif', 14))
        self.text.setStyleSheet("QLabel {color : rgb(228,236,236); }")
        self.text.move(150, 10)

        # Create textbox editible with multiple lines
        self.textbox = QTextEdit(self)
        self.textbox.move(40, 50)
        self.textbox.setStyleSheet(
            "QTextEdit { border: none; background-color: rgb(240,240,240) }")

        # decyripting text
        if len(textTaker()) != 0:
            try:
                e = Fernet(self.key)
                token = textTaker().encode()
                decrypted = e.decrypt(token)
                self.textbox.setText(decrypted.decode())
            except:
                # pitch sound playing
                thread = threading.Thread(target=Beep, args=(600, 500,))
                thread.start()
                # wait here for the sound to be played
                thread.join()
                raise Exception
        # replacing placeholder text with decrypted one.

        self.textbox.setAlignment(Qt.AlignTop)
        self.textbox.setFont(QFont('SansSerif', 12))
        # set size 500,500
        self.textbox.resize(500, 500)
        # define shadow
        self.textbox.setGraphicsEffect(self.shadow3)

        # Create two button for save and exit
        self.button1 = QPushButton('Save', self)
        self.button1.move(40, 580)
        self.button1.resize(230, 70)
        self.button1.setFont(QFont('SansSerif', 12))
        # set style sheet for main and hover states of the button
        self.button1.setStyleSheet(
            "QPushButton { text-align: top;background-color: rgb(230,230,230) }" "QPushButton:hover { font-size:22px ;text-align: top; background-color: rgb(200,200,200); }")
        self.button1.setGraphicsEffect(self.shadow)

        self.button2 = QPushButton('Exit', self)
        self.button2.move(310, 580)
        self.button2.resize(230, 70)
        self.button2.setFont(QFont('SansSerif', 12))
        # set style sheet for main and hover states of the button
        self.button2.setStyleSheet(
            " QPushButton { text-align: top; background-color: rgb(230,230,230)}" "QPushButton:hover { font-size:22px ;text-align: top; background-color: rgb(200,200,200);  }")
        self.button2.setGraphicsEffect(self.shadow2)

        # connect button to function on_click
        self.button1.clicked.connect(self.on_click)
        self.button2.clicked.connect(self.exit)

    # exit function
    @pyqtSlot()
    def exit(self):
        QApplication.quit()

    # data saver function
    @pyqtSlot()
    def on_click(self):
        textboxValue = self.textbox.toPlainText()
        f = open("data_pyqt_implementation", "w")
        # encyripting text with given key
        ################################
        e = Fernet(self.key)
        f.write(str(date.today())+e.encrypt(textboxValue.encode()).decode())
        f.close()


class Survey(QMainWindow):
    # second window that asks how user feels once every day
    def __init__(self):
        super().__init__()

        self.askCounter = 0
        self.key = ""
        # main settings
        self.left = 700
        self.top = 400
        self.width = 510
        self.height = 200
        self.setWindowTitle("Dialog")
        self.setGeometry(self.left, self.top, self.width, self.height)

        # create question text
        self.text = QLabel("How are you feeling today?", self)
        self.text.setFont(QFont('SansSerif', 14))
        self.text.resize(600, 40)
        self.text.move(110, 0)

        self.password = QLineEdit(self)
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setGeometry(100, 60, 300, 50)

        # creating "close button"
        self.shadow = QGraphicsDropShadowEffect(
            blurRadius=8, xOffset=3, yOffset=4)
        self.button2 = QPushButton('open', self)
        self.button2.move(200, 140)
        self.button2.setGraphicsEffect(self.shadow)
        # change the value when it is clicked
        self.button2.clicked.connect(
            lambda: self.button2.setText("open: "+str(3-self.askCounter)))

        self.show()

        self.screens = list()
        # if pressed to the button close and switch windows
        self.button2.clicked.connect(self.continueProgram)

    @pyqtSlot()
    def decider(self):
        self.key = str(self.password.text())

    @pyqtSlot()
    def continueProgram(self):
        askedAlready = True
        self.key = base64.urlsafe_b64encode(
            kdf.derive(self.password.text().encode()))
        ex = App(self)
        self.screens.append(ex)
        ex.show()
        self.destroy()

# now useless function as we use hard encryption with keys


def is_today():
    # reads file and decides if last login was today
    readFile = open("data_pyqt_implementation", "r")
    readFile.seek(0)
    data = readFile.read(10)
    readFile.close()

    if str(date.today()) == data:
        return True

    else:
        # if the first 10 characters is not a date of today or the file is empty, put the today's date
        writeFile = open("data_pyqt_implementation", "r+")
        writeFile.seek(0)
        writeFile.write(str(date.today())+textTaker())
        writeFile.close()
        return False


if __name__ == '__main__':

    # if there is not a file named data create one since we need to use it
    if not os.path.exists("data_pyqt_implementation"):
        f = open("data_pyqt_implementation", "w")
        f.close()

    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setStyleSheet('QMainWindow{background-color: rgb(141, 145, 145);}')

    Question = Survey()
    # if the question asked already today it will not ask again and show the main screen
    # continue using screens until user closes
    sys.exit(app.exec_())

# end of the program
