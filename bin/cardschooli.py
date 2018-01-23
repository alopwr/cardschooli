import csv
import os.path
import sys

from PIL import Image, ImageDraw
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QPushButton, QLineEdit, QLabel, QFileDialog


class Window0(QWidget):
    """
    starting window
    asks for project name
    """

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('cardschooli - witaj!')
        self.resize(800, 600)
        center(self)
        self.project_name = QLineEdit(self)
        self.project_name.setToolTip('Wprowadź dowolną nazwę projektu.')
        self.project_name.move(275, 200)
        self.project_name.resize(250, 25)
        start_btn = QPushButton('Rozpocznij tworzenie talii >>>', self)
        start_btn.setGeometry(275, 275, 250, 50)
        self.show()
        self.project_name.returnPressed.connect(self.next)
        start_btn.clicked.connect(self.next)

    def next(self):
        self.project = self.project_name.text()
        print(self.project)
        self.close()
        window1.init_ui()


class Window1(QWidget):
    """
    gets data file
    """

    def __init__(self):
        super().__init__()

    def init_ui(self):
        self.setWindowTitle('cardschooli - krok 1')
        self.resize(800, 600)
        center(self)
        QLabel(
            'Wybierz plik *.csv z danymi do projektu {}. Zostanie tylko wczytany, nie będzie naruszony.'.format(
                window0.project), self)
        open_btn = QPushButton('Otwórz plik', self)
        open_btn.setGeometry(325, 250, 150, 100)
        open_btn.clicked.connect(self.open_file)
        self.show()

    def open_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename = \
            QFileDialog.getOpenFileName(self, 'Wybierz swój plik z danymi:', filter='dane do cardschooli (*.csv)',
                                        options=options)[0]
        self.filename = filename
        print(get_data(filename))
        self.next()

    def next(self):
        print(self.filename)
        self.close()
        window2.init_ui(self.filename)


class Window2(QWidget):
    """
    user creates his card
    """

    def __init__(self):
        super().__init__()

    def init_ui(self, location):
        self.resize(800, 600)
        self.setWindowTitle('cardschooli - krok 2')
        QLabel('Zaprojektuj swoją kartę.', self)
        center(self)
        preview = QLabel(self)
        path = os.path.join(os.pardir, 'cards', window0.project)
        file = os.path.join(os.pardir, 'cards', window0.project, 'preview.png')
        print(path, file, location)
        if not os.path.exists(path):
            os.makedirs(path)
        self.make_card_preview(file)
        pixmap = QPixmap(file)
        preview.setPixmap(pixmap)
        self.show()

    def make_card_preview(self, prev_file):
        prev = Image.new('RGBA', (240, 336), 'white')
        prev_draw = ImageDraw.Draw(prev)
        prev.save(prev_file)


def center(window):
    qr = window.frameGeometry()
    qr.moveCenter(QDesktopWidget().availableGeometry().center())
    window.move(qr.topLeft())


def get_data(location):
    return list(csv.reader(open(location)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window0 = Window0()
    window1 = Window1()
    window2 = Window2()
    sys.exit(app.exec_())
