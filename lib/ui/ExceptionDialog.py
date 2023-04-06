import traceback

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontDatabase
from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout, QTextEdit


class ExceptionDialog(QDialog):
    def __init__(self, exception):
        super().__init__()

        # Set the window title and layout
        self.setWindowTitle('Exception')
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setFixedWidth(600)

        layout = QVBoxLayout()

        font = QFontDatabase.systemFont(QFontDatabase.FixedFont)

        # Create a label to display the error message
        error_label = QLabel(str(exception))
        error_label.setFont(font)
        layout.addWidget(error_label)

        # Create a text edit to display the traceback
        traceback_edit = QTextEdit()
        traceback_edit.setFont(font)
        traceback_edit.setPlainText(traceback.format_exc())
        traceback_edit.setReadOnly(True)
        layout.addWidget(traceback_edit)

        # Create a button to close the window
        close_button = QPushButton('Close')
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        # Set the window layout
        self.setLayout(layout)
