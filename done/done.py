import sys
import os
from os.path import join
import string
import datetime
import re

from PySide.QtCore import *
from PySide.QtGui import *

# Configuration
TODO_DIR = os.path.expanduser("~/todo")
TODO_FILE = join(TODO_DIR, "todo.txt")

STYLESHEET = """
QPlainTextEdit
{
    font-size: 18px;
}
"""

class Done(QMainWindow):

    def __init__(self):
        super(Done, self).__init__()

        self._todoListFile = open(TODO_FILE, "r+")

        self._initUI()

    def _initUI(self):

        # Set up window.

        self.setWindowTitle(TODO_FILE)
        self.resize(600, 600)
        self._center()
        self.setStyleSheet(STYLESHEET)

        # Set up actions.
        sortDueAscendingAction = QAction("Sort by due earliest first", self)
        sortDueAscendingAction.triggered.connect(self._sortDueAscending)

        # Set up toolbar
        toolbar = self.addToolBar('')
        toolbar.setFloatable(False)
        toolbar.setMovable(False)
        toolbar.addAction(sortDueAscendingAction)

        # Set up central widget.
        
        centralWidget = QWidget(self)

        vboxLayout = QVBoxLayout()

        self._todoListEdit = QPlainTextEdit()
        todoList = self._todoListFile.read().decode('utf8')
        self._todoListEdit.setPlainText(todoList)
        self._todoListEdit.textChanged.connect(self._saveTodoList)

        vboxLayout.addWidget(self._todoListEdit)

        centralWidget.setLayout(vboxLayout)

        self.setCentralWidget(centralWidget)

        # Show window and bring to top.
        self.show()
        self.raise_()

    def _saveTodoList(self):
        todoList = self._todoListEdit.toPlainText().encode('utf8')
        self._todoListFile.seek(0)
        self._todoListFile.write(todoList)
        self._todoListFile.truncate()

    def _center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def _sortDueAscending(self):
        todoList = self._todoListEdit.toPlainText().encode('utf8')

        # due_re = r"due:([\d\-]*)"
        due_re = r"due:(.*)"
        def extract_due(t):
            match = re.search(due_re, t)
            if match:
                return match.group(1)
            else:
                return None
        def key(t):
            due = extract_due(t)
            if due:
                return " " + extract_due(t) + t
            else:
                return t

        todoList = todoList.split("\n")
        todoList.sort(key=key)
        todoList = "\n".join(todoList).decode('utf8')

        self._todoListEdit.setPlainText(todoList)



def main():
    app = QApplication(sys.argv)
    done = Done()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()