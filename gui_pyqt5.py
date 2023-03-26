from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

def clicked_OK_button():
    print("OK button clicked")

def clicked_Back_button():
    print("Back button clicked")

def clicked_Up_button():
    print("Up button clicked")

def clicked_Down_button():
    print("Down button clicked")

def clicked_Menu_button():
    print("Menu button clicked")


def window():
    app = QApplication(sys.argv)
    window = QMainWindow()

    winXPos = 100
    winYPos = 100
    # television will be built with 16:9 aspect ratio
    winWidth = 1600
    winHeight = 900

    window.setGeometry(winXPos, winYPos, winWidth, winHeight)
    window.setWindowTitle("Television")

    label = QtWidgets.QLabel(window)
    label.setText("SAMSUNG")
    label.move(780,85)

    button_OK = QtWidgets.QPushButton(window)
    button_OK.setText("OK")
    
    button_Back = QtWidgets.QPushButton(window)
    button_Back.setText("Back")
    
    button_Up = QtWidgets.QPushButton(window)
    button_Up.setText("Up")
    
    button_Down = QtWidgets.QPushButton(window)
    button_Down.setText("Down")
    
    button_Menu = QtWidgets.QPushButton(window)
    button_Menu.setText("Menu")

    button_OK.move(780,185)
    button_Back.move(780,285)
    button_Up.move(780,385)
    button_Down.move(780,485)
    button_Menu.move(780,585)

    button_OK.clicked.connect(clicked_OK_button)
    button_Back.clicked.connect(clicked_Back_button)
    button_Up.clicked.connect(clicked_Up_button)
    button_Down.clicked.connect(clicked_Down_button)
    button_Menu.clicked.connect(clicked_Menu_button)
    



    window.show()
    sys.exit(app.exec_())

window()