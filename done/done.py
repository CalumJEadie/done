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

DEBUG = True

class Done(QMainWindow):

    def __init__(self):
        super(Done, self).__init__()

        self._initUI()

        self._loadTodoList()

        # Show window and bring to top.
        self.show()
        self.raise_()

    def _initUI(self):

        # Set up window.

        self.setWindowTitle(TODO_FILE)
        self.resize(600, 600)
        self._center()
        self.setStyleSheet(STYLESHEET)

        # Set up actions.
        sortDueAscendingAction = QAction("Sort", self)
        sortDueAscendingAction.setToolTip("Sort by due earliest first")
        sortDueAscendingAction.triggered.connect(self._sortDueAscending)

        loadAction = QAction("Reload", self)
        loadAction.triggered.connect(self._loadTodoList)

        debugAction = QAction("Debug", self)
        debugAction.triggered.connect(self._debug)

        # Set up toolbar
        toolbar = self.addToolBar('')
        toolbar.setFloatable(False)
        toolbar.setMovable(False)
        toolbar.addAction(loadAction)
        toolbar.addAction(sortDueAscendingAction)
        if DEBUG:
            toolbar.addAction(debugAction)

        # Set up central widget.
        
        centralWidget = QWidget(self)

        vboxLayout = QVBoxLayout()

        self._todoListEdit = QPlainTextEdit()
        self._todoListEdit.textChanged.connect(self._saveTodoList)

        vboxLayout.addWidget(self._todoListEdit)

        centralWidget.setLayout(vboxLayout)

        self.setCentralWidget(centralWidget)

    def _loadTodoList(self):
        todoList = self._todoList
        self._todoListEdit.setPlainText(todoList)

    def _saveTodoList(self):
        todoList = self._todoListEdit.toPlainText().encode('utf8')
        self._todoList = todoList

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

    @property
    def _todoList(self):
        with open(TODO_FILE, "r+") as todoListFile:
            return todoListFile.read().decode('utf8')

    @_todoList.setter
    def _todoList(self, todoList):
        with open(TODO_FILE, "r+") as todoListFile:
            todoListFile.write(todoList)
            todoListFile.truncate()

    def _debug(self):
        from pudb import set_trace
        set_trace()

def main():
    app = QApplication(sys.argv)
    done = Done()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()