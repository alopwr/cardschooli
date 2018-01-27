import csv
import os.path
import sys

from PIL import Image, ImageDraw, ImageFont
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QPushButton, QLineEdit, QLabel, QFileDialog, \
    QColorDialog, QInputDialog, QFontDialog


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
        QLabel(
            'Zaprojektuj swoją kartę. Zacznijmy od rewersu, czyli tej strony z tyłu. Będzie taki sam dla każdej karty.',
            self)
        center(self)
        path = os.path.join(os.pardir, 'cards', window0.project)
        self.card_loc = os.path.join(os.pardir, 'cards', window0.project, 'preview_rev.png')
        print(path, self.card_loc, location)
        if not os.path.exists(path):
            os.makedirs(path)
        self.card = Card(os.path.join(os.pardir, 'cards', window0.project, 'preview_rev.png'))
        self.card.preview_rev()
        self.preview = QLabel(self)
        self.pixmap = QPixmap(self.card_loc)
        self.preview.setPixmap(self.pixmap)
        self.preview.setGeometry(25, (600 - self.pixmap.height()) / 2, self.pixmap.width(), self.pixmap.height())
        color_btn = QPushButton('Wybierz kolor tła', self)
        image_btn = QPushButton('Zaimportuj grafikę PNG', self)
        text_btn = QPushButton('Dodaj tekst', self)
        color_btn.setGeometry(500, 60, 225, 35)
        image_btn.setGeometry(500, 115, 225, 35)
        text_btn.setGeometry(500, 170, 225, 35)
        color_btn.clicked.connect(self.color_btn_act)
        image_btn.clicked.connect(self.image_btn_act)
        text_btn.clicked.connect(self.text_btn_act)
        self.show()

    def color_btn_act(self):
        self.card.change_color(self.get_color())
        self.update_preview()

    def image_btn_act(self):
        imported_rev = self.get_image()
        print(imported_rev.size)
        coords = self.get_integer()
        print(coords)
        self.card.paste_in_rev(imported_rev, coords)
        self.update_preview()

    def text_btn_act(self):
        # font = self.get_font()
        font = ImageFont.truetype('../fonts/impact.ttf', 15)
        text = self.get_text()
        # print(font.toString())
        # font_prop = font.toString().split(',')
        # print(font_prop)
        print(self.card.check_txt_size(text, font))
        self.card.add_text((0, 0), text, font=font)
        self.update_preview()

    def update_preview(self):
        self.pixmap = QPixmap(self.card_loc)
        self.preview.setPixmap(self.pixmap)
        self.update()

    def get_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            return color.name()
        return "#ffffff"

    def get_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename = \
            QFileDialog.getOpenFileName(self, 'Wybierz obrazek do zaimportowania na rewers:', filter='PNG (*.png)',
                                        options=options)[0]
        return Image.open(filename)

    def get_integer(self):
        i, ok_pressed0 = QInputDialog.getInt(self, "Podaj pozycję dodawanego obiektu:", "Pozycja x:", 0)
        if ok_pressed0:
            j, ok_pressed1 = QInputDialog.getInt(self, "Podaj pozycję dodawanego obiektu:", "Pozycja y:", 0)
            if ok_pressed1:
                return (i, j)

    def get_text(self):
        text, okPressed = QInputDialog.getText(self, "Jaki tekst chcesz dodać?", "Podaj tekst:", QLineEdit.Normal, "")
        if okPressed and text != '':
            return text

    def get_font(self):
        font, ok = QFontDialog.getFont()
        if ok:
            return font


class Card(object):
    def __init__(self, location, size=(180, 252), color='#ffffff'):
        self.location = location
        self.size = size
        self.color = color
        self.prev = Image.new('RGBA', self.size, self.color)
        self.prev_draw = ImageDraw.Draw(self.prev)

    def preview_rev(self):
        self.prev.save(self.location)

    def change_color(self, color):
        self.color = color
        self.prev = Image.new('RGBA', self.size, self.color)
        self.prev_draw = ImageDraw.Draw(self.prev)
        print("color is now {}".format(color))
        self.preview_rev()

    def paste_in_rev(self, thing, coords):
        self.prev.paste(thing, coords, thing)
        print('pasted {} in {} at {!s}'.format(thing, self.prev, coords))
        self.preview_rev()

    def check_txt_size(self, text, font=None):
        return self.prev_draw.textsize(text, font)

    def add_text(self, coords, text, fill=None, font=None):
        self.prev_draw.text(coords, text, fill, font)
        self.preview_rev()


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
