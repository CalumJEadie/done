import sys
import os
import string
import datetime

from PySide.QtCore import *
from PySide.QtGui import *

# Configuration
TODO_DIR = os.path.expanduser("~/todo")

# STYLESHEET = """
# QToolBar QWidget
# {
#     font-size: 14px
# }
# """

class Done(QMainWindow):

    def __init__(self):
        super(Done, self).__init__()

        self._initUI()

    def _initUI(self):

        # Set up window.

        self.setWindowTitle("Done")
        self.resize(400, 400)
        # self.setStyleSheet(STYLESHEET)

        # Set up central widget.
        
        centralWidget = QWidget(self)

        vboxLayout = QVBoxLayout()

        self._notesView = QPlainTextEdit()
        vboxLayout.addWidget(self._notesView)

        centralWidget.setLayout(vboxLayout)

        self.setCentralWidget(centralWidget)

        # Show window.
        self.show()


def main():
    app = QApplication(sys.argv)
    done = Done()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()