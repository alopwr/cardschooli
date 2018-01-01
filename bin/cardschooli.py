import sys

from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QPushButton


class Window0(QWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('cardschooli - witaj!')
        self.resize(800, 600)
        center(self)
        start_btn = QPushButton('Rozpocznij tworzenie talii >>>', self)
        start_btn.setGeometry(275, 275, 250, 50)
        self.show()
        start_btn.clicked.connect(self.next)

    def next(self):
        self.close()


def center(window):
    qr = window.frameGeometry()
    qr.moveCenter(QDesktopWidget().availableGeometry().center())
    window.move(qr.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window0 = Window0()
    sys.exit(app.exec_())
