from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QPushButton,
    QMainWindow,
    QComboBox,
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
        self.is_work_timer_active = False
        self.is_notification_timer_active = False
        self.greetings_label = None
        self.start_to_work_label = None
        self.start_work_button = None
        self.work_timer_label = None
        self.stop_work_button = None
        self.notification_label = None
        self.notification_dropdown = None
        self.set_notification_button = None
        self.notification_timer_label = None
        self.notification_timer_text_label = None
        self.stop_notification_button = None

        # render blocks
        self.create_start_work_block()
        self.create_greetings_block()
        self.create_notification_block()
        self.create_notification_timer()

        # create empty work timer
        self.work_time = QTime(0, 0, 0)
        self.work_timer = QTimer()

        # create empty notification timer
        self.notification_time = QTime(0, 0, 0)
        self.notification_timer = QTimer()

        # handle buttons click
        self.start_work_button.clicked.connect(self.handle_timer_button)
        self.stop_work_button.clicked.connect(self.handle_clear_timer_button)
        self.set_notification_button.clicked.connect(self.handle_notification_timer_button)
        self.stop_notification_button.clicked.connect(self.handle_stop_notification_timer_button)

        self.show()

    def create_greetings_block(self):
        self.greetings_label = QLabel("<h1>Hello, {}</h1>".format(constants.USERNAME.capitalize()), self)
        self.greetings_label.move(0, constants.BLOCK_MARGIN)
        self.greetings_label.setMinimumWidth(constants.APP_WIDTH)
        self.greetings_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def create_start_work_block(self):
        # start to work button
        self.start_work_button = QPushButton("Start working", self)
        self.start_work_button.setGeometry(
            constants.BLOCK_MARGIN,
            constants.TIMER_BLOCK_Y_CORDS,
            constants.BUTTON_WIDTH,
            constants.BUTTON_HEIGHT
        )

        # init timer label
        self.work_timer_label = QLabel("00:00:00", self)
        self.work_timer_label.move(int(constants.APP_WIDTH // 2.4), constants.TIMER_BLOCK_Y_CORDS)
        self.work_timer_label.setFont(QFont("Arial", 14))
        self.work_timer = QTimer()

        # stop work button
        self.stop_work_button = QPushButton("Stop working", self)
        self.stop_work_button.setGeometry(
            constants.APP_WIDTH - constants.BUTTON_WIDTH - constants.BLOCK_MARGIN,
            constants.TIMER_BLOCK_Y_CORDS,
            constants.BUTTON_WIDTH,
            constants.BUTTON_HEIGHT
        )

    def create_notification_block(self):
        # notification label
        self.notification_label = QLabel("Set notification\ntimer:", parent=self)
        self.notification_label.move(
            constants.BLOCK_MARGIN + 5,
            constants.NOTIFICATION_BLOCK_Y_CORDS
        )
        self.notification_label.setMinimumWidth(constants.APP_WIDTH // 3)

        # notification dropdown
        self.notification_dropdown = QComboBox(parent=self)
        self.notification_dropdown.addItem("5 minutes")
        self.notification_dropdown.addItem("10 minutes")
        self.notification_dropdown.addItem("20 minutes")
        self.notification_dropdown.addItem("30 minutes")
        self.notification_dropdown.addItem("40 minutes")
        self.notification_dropdown.addItem("50 minutes")
        self.notification_dropdown.addItem("60 minutes")

        self.notification_dropdown.setGeometry(
            constants.APP_WIDTH // 3,
            constants.NOTIFICATION_BLOCK_Y_CORDS,
            constants.BUTTON_WIDTH,
            constants.BUTTON_HEIGHT,
        )

        # set notification button
        self.set_notification_button = QPushButton("Set timer", self)
        notification_button_x_cords = (
                constants.APP_WIDTH // 2 + self.notification_dropdown.width() // 2 + 20
        )
        self.set_notification_button.setGeometry(
            notification_button_x_cords,
            constants.NOTIFICATION_BLOCK_Y_CORDS,
            constants.APP_WIDTH - notification_button_x_cords - constants.BLOCK_MARGIN,
            constants.BUTTON_HEIGHT,
        )

    def create_notification_timer(self):
        self.notification_timer_text_label = QLabel("Next break in:", self)
        self.notification_timer_text_label.setGeometry(
            constants.BLOCK_MARGIN,
            constants.NOTIFICATION_TIMER_Y_CORDS + constants.BUTTON_HEIGHT // 2 + 5,
            constants.APP_WIDTH // 3 - constants.BLOCK_MARGIN * 2,
            constants.BUTTON_HEIGHT,
        )
        self.notification_timer_text_label.setFont(QFont("Arial", 16))

        self.notification_timer_label = QLabel("00:00:00", self)
        timer_x_cords = int(constants.APP_WIDTH // 3) + constants.BLOCK_MARGIN
        self.notification_timer_label.setGeometry(
            timer_x_cords,
            constants.NOTIFICATION_TIMER_Y_CORDS,
            constants.APP_WIDTH - timer_x_cords * 2 - constants.BLOCK_MARGIN * 2,
            70,
        )
        self.notification_timer_label.setFont(QFont("Arial", 22))

        # stop notification timer button
        self.stop_notification_button = QPushButton("Stop timer", self)
        self.stop_notification_button.setGeometry(
            constants.APP_WIDTH - constants.BUTTON_WIDTH - constants.BLOCK_MARGIN,
            constants.NOTIFICATION_TIMER_Y_CORDS + constants.BUTTON_HEIGHT // 2 + 5,
            constants.BUTTON_WIDTH,
            constants.BUTTON_HEIGHT,
        )
        self.stop_notification_button.setFont(QFont("Arial", 16))

    def _start_timer_event(self):
        self.start_work_button.setText("Pause timer")
        self.work_time = self.work_time.addSecs(1)
        self.work_timer_label.setText(self.work_time.toString("hh:mm:ss"))

    def _stop_timer_event(self):
        self.start_work_button.setText("Continue working")
        self.work_timer = QTimer()
        self.work_timer_label.setText(self.work_time.toString("hh:mm:ss"))

    def _start_notification_timer(self):
        self.notification_time = self.notification_time.addSecs(-1)
        self.notification_timer_label.setText(self.notification_time.toString("hh:mm:ss"))
        self.is_notification_timer_active = True

    def handle_timer_button(self):
        self.work_time = self.work_time
        self.work_timer.start(1000)
        if self.is_work_timer_active:
            self.work_timer.timeout.connect(self._stop_timer_event)
        else:
            self.work_timer.timeout.connect(self._start_timer_event)
        self.is_work_timer_active = not self.is_work_timer_active

    def handle_clear_timer_button(self):
        self.work_time = QTime(0, 0, 0)
        self.work_timer = QTimer()

        self.is_work_timer_active = False
        self.start_work_button.setText("Start working")
        self.work_timer_label.setText(self.work_time.toString("hh:mm:ss"))

    def handle_notification_timer_button(self):
        self.notification_time = None
        self.notification_timer = QTimer()
        notification_interval = int(self.notification_dropdown.currentText().split()[0])
        if notification_interval != 60:
            self.notification_time = QTime(0, notification_interval, 0)
        else:
            self.notification_time = QTime(1, 0, 0)
        self.notification_timer_label.setText(self.notification_time.toString("hh:mm:ss"))

        self.notification_timer.start(1000)
        self.notification_timer.timeout.connect(self._start_notification_timer)

    def handle_stop_notification_timer_button(self):
        self.notification_time = QTime(0, 0, 0)
        self.notification_timer_label.setText(self.notification_time.toString("hh:mm:ss"))
        self.notification_timer = QTimer()
        self.is_notification_timer_active = False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec())
