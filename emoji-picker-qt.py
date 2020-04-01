#!/usr/bin/python
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import emoji_data_python as edp
from Xlib import display
import pyautogui
import time
from PyQt5 import QtTest

# globals
emojiGridLayout = None
mainWindow = None
emojiGridColumnCount = 7
emojiGridRowCount = 4
emojiFontSize = 20
willExitOnItsOwn = False

font = QFont()
font.setPointSize(emojiFontSize)

# quits without a lag
def quitNicely():
    mainWindow.hide()
    quit()


# gets mouse position from Xlib
def mousePosition():
    pointerData = display.Display().screen().root.query_pointer()._data
    return pointerData["root_x"], pointerData["root_y"]

# copies and pastes selected emoji
def emojiClicked(char):
    global willExitOnItsOwn
    willExitOnItsOwn = True
    mainWindow.hide()
    QApplication.clipboard().setText(char)
    pyautogui.hotkey("ctrl","v")
    QtTest.QTest.qWait(250)
    quit()

# searches for emoji, and fills grid with labels
def execute_search(text):

    if not text or text.isspace():
        return

    global emojiGridLayout
    for i in reversed(range(emojiGridLayout.count())): 
        emojiGridLayout.itemAt(i).widget().setParent(None)

    rowIdx = 0
    colIdx = 0

    for emoji in edp.find_by_name(text):
        if rowIdx>emojiGridRowCount-1:
            break;

        label = QClickableLabel(emoji.char)
        label.clicked.connect(emojiClicked)
        label.setFont(font)
        label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        emojiGridLayout.addWidget(label,rowIdx,colIdx)
        emojiGridLayout.setAlignment(label,Qt.AlignTop)
        if colIdx < emojiGridColumnCount-1:
            colIdx+=1
        else:
            colIdx=0
            rowIdx+=1

def on_key(key):
    # test for a specific key
    if key == Qt.Key_Escape:
        quitNicely()

# main app window class with inits
class EmojiPickerWindow(QWidget):

    def __init__(self):
        super().__init__()

        # focus handling
        self.installEventFilter(self)

        self.title = 'Emoji picker ＼(^o^)／'
        self.width = 274
        self.height = 250

        # start with text box centered at mouse pointer position
        self.left, self.top = mousePosition()  
        self.left -= self.width//2
        self.top += (24-self.height)

        self.initUI()
        
    def initUI(self):
        # topmost window layout 
        layout = QVBoxLayout() 

        # scroll area setup shenanigans
        scrollArea = QScrollArea() 
        gridWidget = QWidget()
        global emojiGridLayout
        emojiGridLayout = QGridLayout(gridWidget)
        emojiGridLayout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        gridWidget.setStyleSheet("QLabel:hover{background-color:palette(highlight);}")
        scrollArea.setWidget(gridWidget)
        scrollArea.setWidgetResizable(True)
        layout.addWidget(scrollArea)

        # fill with a placeholder for now (smiling or smile)
        execute_search('smil')

        # bottom text entry
        lineEdit = QLineEdit() 
        lineEdit.textChanged.connect(execute_search)
        layout.addWidget(lineEdit)

        # align it to the bottom, so that it won't stay centered vertically
        layout.setAlignment(lineEdit, Qt.AlignBottom)


        self.setLayout(layout)
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setFixedSize(self.width, self.height)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        # needed for filling the grid out from the outside
        global mainWindow
        mainWindow = self

        # esc handling
        self.keyPressed.connect(on_key)

        self.show()
        lineEdit.setFocus()

    # esc handling
    keyPressed = pyqtSignal(int)
    def keyPressEvent(self, event):
        super(EmojiPickerWindow, self).keyPressEvent(event)
        self.keyPressed.emit(event.key())

    # focus handling
    global willExitOnItsOwn
    def eventFilter(self, object, event):
        if event.type()== QEvent.WindowDeactivate or event.type()== QEvent.FocusOut:
            if (not willExitOnItsOwn):
                quitNicely()
        return False

# clickable label
class QClickableLabel(QLabel):
    clicked=pyqtSignal(str)
    def __init__(self, parent=None):
        QLabel.__init__(self, parent)

    def mousePressEvent(self, ev):
        self.clicked.emit(self.text())        
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = EmojiPickerWindow()
    sys.exit(app.exec_())
