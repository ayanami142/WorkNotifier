from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QPushButton,
    QMainWindow,
)
from PyQt6.QtCore import Qt, QTimer, QTime

import constants

import sys


class Window(QMainWindow):
    def __init__(self):
        super().__init__(parent=None)

        # main window
        self.setWindowTitle("Work Helper")
        self.setGeometry(0, 0, constants.APP_WIDTH, constants.APP_HEIGHT)

        # init blocks
        self.is_timer_active = False
        self.greetings_label = None
        self.start_to_work_label = None
        self.start_work_button = None
        self.timer_label = None
        self.stop_work_button = None

        # render blocks
        self.create_start_work_block()
        self.create_greetings_block()

        # create empty timer
        self.time = QTime(0, 0, 0)
        self.timer = QTimer()

        # handle buttons click
        self.start_work_button.clicked.connect(self.handle_timer_button)
        self.stop_work_button.clicked.connect(self.handle_clear_timer_button)

        self.show()

    def create_greetings_block(self):
        self.greetings_label = QLabel("<h1>Hello, {}</h1>".format(constants.USERNAME), self)
        self.greetings_label.move(0, constants.BLOCK_MARGIN)
        self.greetings_label.setMinimumWidth(constants.APP_WIDTH)
        self.greetings_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def create_start_work_block(self):
        # start to work button
        self.start_work_button = QPushButton("Start work", self)
        self.start_work_button.setGeometry(
            10,
            constants.TIMER_BLOCK_Y_CORDS,
            constants.BUTTON_WIDTH,
            constants.BUTTON_HEIGHT
        )

        # init timer label
        self.timer_label = QLabel("00:00:00", self)
        self.timer_label.move(int(constants.APP_WIDTH // 2.3), 70)
        self.timer = QTimer()

        # stop work button
        self.stop_work_button = QPushButton("Stop work", self)
        self.stop_work_button.setGeometry(
            constants.APP_WIDTH - constants.BUTTON_WIDTH - constants.BLOCK_MARGIN,
            constants.TIMER_BLOCK_Y_CORDS,
            constants.BUTTON_WIDTH,
            constants.BUTTON_HEIGHT
        )

    def _start_timer_event(self):
        self.start_work_button.setText("Pause timer")
        self.time = self.time.addSecs(1)
        self.timer_label.setText(self.time.toString("hh:mm:ss"))

    def _stop_timer_event(self):
        self.start_work_button.setText("Continue work")
        self.timer = QTimer()
        self.timer_label.setText(self.time.toString("hh:mm:ss"))

    def handle_timer_button(self):
        self.time = self.time
        self.timer.start(1000)
        if self.is_timer_active:
            self.timer.timeout.connect(self._stop_timer_event)
        else:
            self.timer.timeout.connect(self._start_timer_event)
        self.is_timer_active = not self.is_timer_active

    def handle_clear_timer_button(self):
        self.time = QTime(0, 0, 0)
        self.timer = QTimer()

        self.is_timer_active = False
        self.start_work_button.setText("Start work")
        self.timer_label.setText(self.time.toString("hh:mm:ss"))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec())
