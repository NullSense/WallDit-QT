import sys

from PySide.QtGui import QMainWindow, QApplication, QWidget, QPushButton, QCheckBox, QSpinBox
from output_ui import Ui_MainWindow
import WallDit

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.widget = QWidget()
        self.setupUi(self.widget)
        self.setCentralWidget(self.widget)

        # Checkboxes
        self.nsfw_checkbox.toggled.connect(self.handle_nsfw_checkbox)
        self.boot_checkbox.toggled.connect(self.handle_boot_checkbox)

        # Spinboxes
        self.post_amount_spinbox.valueChanged.connect(self.handle_post_spinbox)

        # Lines
        self.subreddit_line.textChanged.connect(self.handle_subreddit_line)

        # Combo Boxes
        self.post_type_combo_box.currentIndexChanged.connect(self.handle_post_type_combo_box)

        # Buttons
        self.start_btn.clicked.connect(self.handle_start_btn)

    def handle_nsfw_checkbox(self):
        if self.nsfw_checkbox.isChecked():
            print("NSFW: checked")
        if not self.nsfw_checkbox.isChecked():
            print("NSFW: unchecked")

    def handle_post_spinbox(self):
        spinbox_value = self.post_amount_spinbox.value()
        return spinbox_value

    def handle_boot_checkbox(self):
        if self.boot_checkbox.isChecked():
            print("boot: checked")
        if not self.boot_checkbox.isChecked():
            print("boot: unchecked")

    def handle_subreddit_line(self):
        sub_line = self.subreddit_line.text()
        return sub_line

    def handle_post_type_combo_box(self):
        post_type = self.post_type_combo_box.currentIndex()
        return post_type

    def handle_start_btn(self):
        if self.start_btn.isDown:
            print("Button pressed")
        WallDit.set_wallpaper(self)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    frame = MainWindow()
    frame.show()
    sys.exit(app.exec_())