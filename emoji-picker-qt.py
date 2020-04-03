#!/usr/bin/python
# Copyright (c) 2020 Maryushi3

import emoji_data_python as edp
import sys
import pyautogui
from Xlib import display
from PyQt5.QtWidgets import QApplication, QGridLayout, QLabel, QLineEdit, QScrollArea, QSizePolicy, QStackedLayout, QVBoxLayout, QWidget
from PyQt5.QtCore import QEvent, QSettings, Qt, pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5 import QtTest


# globals
emojiGridLayout = None
mainWindow = None
emojiGridColumnCount = 5
emojiGridRowCount = 4
emojiToShowCount = 0
fullRowsCount = 0
lastRowEmojiCount = 0
emojiFontSize = 20
selectedEmojiPosition = list((0,0))
willExitOnItsOwn = False
selectedEmojiChar=''
settingsFile = None
historyList = []
foundAnyEmoji = True
layoutStack = None

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
def execute_emoji(char):
    add_char_to_history(char)
    global willExitOnItsOwn
    willExitOnItsOwn = True
    mainWindow.hide()
    QApplication.clipboard().setText(char)
    pyautogui.hotkey("ctrl","v")
    QtTest.QTest.qWait(250)
    quit()

# fills grid with given char list and takes care of layout and counting
def fill_grid_with_char_list(charList):

    # for wraparound
    global emojiToShowCount
    global fullRowsCount
    global lastRowEmojiCount
    emojiToShowCount = min(len(charList),(emojiGridColumnCount*emojiGridRowCount))
    fullRowsCount = emojiToShowCount//emojiGridColumnCount
    lastRowEmojiCount = emojiToShowCount%emojiGridColumnCount
    
    global foundAnyEmoji
    if emojiToShowCount>0:
        foundAnyEmoji = True
        layoutStack.setCurrentIndex(0)
    else:
        foundAnyEmoji = False
        layoutStack.setCurrentIndex(1)


    # clear grid
    global emojiGridLayout
    for i in reversed(range(emojiGridLayout.count())): 
        emojiGridLayout.itemAt(i).widget().setParent(None)

    # fill with new chars
    rowIdx = 0
    colIdx = 0
    for emoji in charList:
        if rowIdx>emojiGridRowCount-1:
            break;

        label = QClickableLabel(emoji)
        label.clicked.connect(execute_emoji)
        label.setFont(font)
        label.setAlignment(Qt.AlignCenter)
        label.setMinimumHeight(49)
        emojiGridLayout.addWidget(label,rowIdx,colIdx)
        emojiGridLayout.setAlignment(label,Qt.AlignTop)
        if colIdx < emojiGridColumnCount-1:
            colIdx+=1
        else:
            colIdx=0
            rowIdx+=1

    emojiGridLayout.setContentsMargins(0,0,0,0)
    emojiGridLayout.setHorizontalSpacing(0)
    emojiGridLayout.setVerticalSpacing(0)

    if emojiToShowCount>0:
        highlight_emoji([0,0])

# searches for emoji, and passes them to fill_grid_with_char_list
def execute_search(text):
    selectedEmoji = (0,0)
    if not text or text.isspace():
        fill_grid_with_history()
        return

    foundEmoji = edp.find_by_name(text)
    charList = [emoji.char for emoji in foundEmoji]

    fill_grid_with_char_list(charList)

# handles what to do after hovering over a given label
def emoji_hovered(hoveredLabel):
    parentGrid = hoveredLabel.parentWidget().layout()
    hoveredIndex = parentGrid.indexOf(hoveredLabel)
    hoveredRow, hoveredColumn, _, _ = parentGrid.getItemPosition(hoveredIndex)
    highlight_emoji([hoveredRow,hoveredColumn])

# selects, sets style and handles wraparound
def highlight_emoji(newPosition):
    global selectedEmojiPosition

    # grid is filled to a full rectangle (last row fills the window horizontally)
    if lastRowEmojiCount==0:
        if newPosition[0]<0:
            newPosition[0]=fullRowsCount-1
        elif newPosition[1]<0:
            newPosition[1]=emojiGridColumnCount-1
        elif newPosition[0]>fullRowsCount-1:
            newPosition[0]=0
        elif newPosition[1]>emojiGridColumnCount-1:
            newPosition[1]=0
    # last row is not full
    else:
        #horizontal wraparound through RIGHT edge for full rows
        if (newPosition[0]<fullRowsCount) and (newPosition[1]>emojiGridColumnCount-1):
            newPosition[1]=0
        #horizontal wraparound through LEFT edge for full rows
        elif (newPosition[0]<fullRowsCount) and (newPosition[1]<0):
            newPosition[1]=emojiGridColumnCount-1
        #horizontal wraparound through right edge for NON FULL rows
        elif (newPosition[0]==fullRowsCount) and (newPosition[1]>lastRowEmojiCount-1) and ((selectedEmojiPosition[0]-newPosition[0])==0):
            newPosition[1]=0
        #horizontal wraparound through LEFT edge for NON FULL rows
        elif (newPosition[0]>=fullRowsCount) and (newPosition[1]<0):
            newPosition[1]=lastRowEmojiCount-1
        #vertical wraparound through BOTTOM edge for full cols
        elif (newPosition[0]>fullRowsCount) and (newPosition[1]<lastRowEmojiCount):
            newPosition[0]=0
        #vertical wraparound through TOP edge for full cols
        elif (newPosition[0]<0) and (newPosition[1]<lastRowEmojiCount):
            newPosition[0]=fullRowsCount
        #vertical wraparound through BOTTOM edge for NON FULL cols
        elif (newPosition[0]>fullRowsCount-1) and (newPosition[1]>lastRowEmojiCount-1):
            newPosition[0]=0
        #vertical wraparound through TOP edge for NON FULL cols
        elif (newPosition[0]<0) and (newPosition[1]>lastRowEmojiCount-1):
            newPosition[0]=fullRowsCount-1

    oldPosition = selectedEmojiPosition
    selectedEmojiPosition = newPosition
    
    widgetToDeselect = emojiGridLayout.itemAtPosition(oldPosition[0],oldPosition[1])
    if widgetToDeselect:
        widgetToDeselect = widgetToDeselect.widget()
        widgetToDeselect.setStyleSheet("")

    global selectedEmojiChar
    widgetToSelect = emojiGridLayout.itemAtPosition(selectedEmojiPosition[0],selectedEmojiPosition[1])
    if widgetToSelect:
        widgetToSelect = widgetToSelect.widget()
        selectedEmojiChar = widgetToSelect.text()
        widgetToSelect.setStyleSheet("QLabel{background-color: palette(highlight);}")
   
# handles direction where to move emoji selection
def move_selection(direction):
    if direction=="right":
        highlight_emoji([sum(x) for x in zip(selectedEmojiPosition, [0,1])])
    elif direction=="left":
        highlight_emoji([sum(x) for x in zip(selectedEmojiPosition, [0,-1])])
    elif direction=="up":
        highlight_emoji([sum(x) for x in zip(selectedEmojiPosition, [-1,0])])
    elif direction=="down":
        highlight_emoji([sum(x) for x in zip(selectedEmojiPosition, [1,0])])

# handles Esc
def on_key(key):
    # test for a specific key
    if key == Qt.Key_Escape:
        quitNicely()

# adds given emoji to history and saves it to config file
def add_char_to_history(char):
    global settingsFile
    global historyList
    if not historyList:
        historyList = [char]
    else:
        if char in historyList:
            historyList.remove(char)
        
        tempList = [char]
        tempList.extend(historyList)
        historyList = tempList[:(emojiGridColumnCount*emojiGridRowCount)]    
    
    settingsFile.setValue('history/history',historyList)

# wrapper around filling the grid
def fill_grid_with_history():
    fill_grid_with_char_list(historyList)

# main app window class with inits
class EmojiPickerWindow(QWidget):

    def __init__(self):
        super().__init__()

        # focus handling
        self.installEventFilter(self)

        self.title = 'Emoji picker ＼(^o^)／'
        self.width = 281
        self.height = 251

        # start with text box centered at mouse pointer position
        self.left, self.top = mousePosition()  
        self.left -= self.width//2
        self.top += (24-self.height)

        self.initSettings()
        self.initUI()
        
    def initUI(self):
        # topmost window layout 
        layout = QVBoxLayout() 

        global layoutStack
        layoutStack = QStackedLayout()
        layoutStackWidget = QWidget()
        layoutStackWidget.setLayout(layoutStack)

        # scroll area setup shenanigans
        scrollArea = QScrollArea() 
        gridWidget = QWidget()
        global emojiGridLayout
        emojiGridLayout = QGridLayout(gridWidget)
        emojiGridLayout.setAlignment(Qt.AlignTop | Qt.AlignLeft)



        # stretch grid to widget
        for col in range(emojiGridColumnCount):
            emojiGridLayout.setColumnStretch(col,1)
        for row in range(emojiGridRowCount):
            emojiGridLayout.setRowStretch(row,1)

        scrollArea.setWidget(gridWidget)
        scrollArea.setWidgetResizable(True)
        layoutStack.addWidget(scrollArea)

        # info to show when no emoji has been found
        noEmojiFoundLabel = QLabel("No emoji found 🙁")
        noEmojiFoundLabel.setAlignment(Qt.AlignCenter | Qt.AlignHCenter | Qt.AlignVCenter)
        layoutStack.addWidget(noEmojiFoundLabel)     
        layout.addWidget(layoutStackWidget)

        # fill with a placeholder for now (smiling or smile)
        # execute_search('smil')
        fill_grid_with_history()
        # bottom text entry
        lineEdit = QLineEditWithArrows() 
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
    
    def initSettings(self):
        global settingsFile
        global historyList
        settingsFile = QSettings("emoji-picker-qtpy", "history");
        historyList = settingsFile.value('history/history')

    # key handling
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

    def enterEvent(self, ev):
        emoji_hovered(self)

# keyboard handling override for QlineEdit
class QLineEditWithArrows(QLineEdit):
    def keyPressEvent(self, ev):
        global selectedEmojiChar
        global foundAnyEmoji
        if(ev.key() == Qt.Key_Right):
            move_selection("right")
        if(ev.key() == Qt.Key_Left):
            move_selection("left")
        if(ev.key() == Qt.Key_Up):
            move_selection("up")
        if(ev.key() == Qt.Key_Down):
            move_selection("down")
        if(ev.key() == Qt.Key_Return or ev.key() == Qt.Key_Enter):
            if foundAnyEmoji:
                execute_emoji(selectedEmojiChar)
            else:
                quitNicely()
        if(ev.key() == Qt.Key_Tab):
            pass
        else:
            QLineEdit.keyPressEvent(self,ev)
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = EmojiPickerWindow()
    sys.exit(app.exec_())
