import sys
import os
from os.path import join
import string
import datetime
import re
import logging
import subprocess
import argparse

from PySide.QtCore import *
from PySide.QtGui import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
TODO_DIR = os.path.expanduser("~/todo")
TODO_FILE = join(TODO_DIR, "todo.txt")
DONE_FILE = join(TODO_DIR, "done.txt")

STYLESHEET = """
QWidget
{
    font-size: 16px;
}

QPlainTextEdit
{
    font-size: 14px;
    font-family: "Menlo";
}
"""

WIDTH, HEIGHT = (800, 400)

DONE_WEBSITE = "https://github.com/CalumJEadie/done"

TODO_SH = "/usr/local/bin/todo.sh"

class Done(QMainWindow):

    def __init__(self, debug):
        super(Done, self).__init__()
        self._debug = debug

        self._initUI()

        self._loadTodoList()

        # Show window and bring to top.
        self.show()
        self.raise_()

    def _initUI(self):

        # Set up window.

        self.setWindowTitle(TODO_FILE)
        self.resize(WIDTH, HEIGHT)
        self._center()
        self.setStyleSheet(STYLESHEET)
        self.setUnifiedTitleAndToolBarOnMac(True)

        # Set up actions.
        sortDueAscendingAction = QAction("Sort", self)
        sortDueAscendingAction.setToolTip("Sort by due earliest first")
        sortDueAscendingAction.triggered.connect(self._sortDueAscending)
        sortDueAscendingAction.setShortcut(QKeySequence("Ctrl+S"))

        reloadAction = QAction("Reload", self)
        reloadAction.triggered.connect(self._loadTodoList)
        reloadAction.setShortcut(QKeySequence.Refresh)

        archiveAction = QAction("Archive", self)
        archiveAction.setToolTip("Archive completed actions")
        archiveAction.triggered.connect(self._archive)
        archiveAction.setShortcut(QKeySequence("Ctrl+E"))

        debugAction = QAction("Debug", self)
        debugAction.triggered.connect(self._startDebug)

        doneWebsiteAction = QAction("Done Website", self)
        doneWebsiteAction.triggered.connect(self._doneWebsite)

        openDoneAction = QAction("Open done.txt", self)
        openDoneAction.triggered.connect(self._openDone)

        # Set up toolbar
        toolbar = self.addToolBar('')
        toolbar.setFloatable(False)
        toolbar.setMovable(False)
        toolbar.addAction(reloadAction)
        toolbar.addAction(sortDueAscendingAction)
        toolbar.addAction(archiveAction)
        if self._debug:
            toolbar.addAction(debugAction)

        # Set up menu bar
        menubar = QMenuBar()

        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(reloadAction)
        fileMenu.addSeparator()
        fileMenu.addAction(openDoneAction)
        editMenu = menubar.addMenu('&Edit')
        editMenu.addAction(sortDueAscendingAction)
        editMenu.addAction(archiveAction)
        helpMenu = menubar.addMenu('&Help')
        helpMenu.addAction(doneWebsiteAction)

        self.setMenuBar(menubar)

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

    def _startDebug(self):
        from pudb import set_trace
        set_trace()

    def _archive(self):
        subprocess.call([TODO_SH, "archive"])
        self._loadTodoList()

    def _doneWebsite(self):
        QDesktopServices.openUrl(QUrl(DONE_WEBSITE, QUrl.TolerantMode))

    def _openDone(self):
        QDesktopServices.openUrl(QUrl(DONE_FILE, QUrl.TolerantMode))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action="store_true")
    args = parser.parse_args()

    app = QApplication(sys.argv)
    done = Done(args.debug)
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
