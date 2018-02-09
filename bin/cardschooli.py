import csv
import os.path
import os.path
import sys

from PIL import Image, ImageDraw, ImageFont
from PyQt5.QtGui import QPixmap, QMovie
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QPushButton, QLineEdit, QLabel, QFileDialog, \
    QColorDialog, QInputDialog, QMessageBox


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
            'Wybierz plik *.csv z danymi do projektu {}. Zostanie tylko wczytany, nie będzie naruszony. \nKoniecznie użyj nagłówków!'.format(
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
        with open(filename, newline='') as f:
            reader = csv.reader(f)
            self.headers = next(reader)
        self.next()

    def next(self):
        print(self.filename)
        self.close()
        window2.init_ui()


class Window2(QWidget):
    """
    user creates his card's reverse
    """

    def __init__(self):
        super().__init__()

    def init_ui(self):
        self.resize(800, 600)
        self.setWindowTitle('cardschooli - krok 2')
        QLabel(
            'Zaprojektuj swoją kartę. Zacznijmy od rewersu, czyli tej strony z tyłu. Będzie taki sam dla każdej karty.',
            self)
        center(self)
        path = os.path.join(os.pardir, 'cards', window0.project)
        self.card_loc = os.path.join(os.pardir, 'cards', window0.project, 'preview_rev.png')
        print(path, self.card_loc)
        if not os.path.exists(path):
            os.makedirs(path)
        self.card = Card(os.path.join(os.pardir, 'cards', window0.project))
        self.preview = QLabel(self)
        self.pixmap = QPixmap(self.card_loc)
        self.preview.setPixmap(self.pixmap)
        self.preview.setGeometry(25, (600 - self.pixmap.height()) / 2, self.pixmap.width(), self.pixmap.height())
        color_btn = QPushButton('Wybierz kolor tła', self)
        image_btn = QPushButton('Zaimportuj grafikę PNG', self)
        text_btn = QPushButton('Dodaj tekst', self)
        finish_btn = QPushButton('Dalej >>>', self)
        color_btn.setGeometry(500, 60, 225, 35)
        image_btn.setGeometry(500, 115, 225, 35)
        text_btn.setGeometry(500, 170, 225, 35)
        finish_btn.setGeometry(500, 475, 225, 70)
        color_btn.clicked.connect(self.color_btn_act)
        image_btn.clicked.connect(self.image_btn_act)
        text_btn.clicked.connect(self.text_btn_act)
        finish_btn.clicked.connect(self.finish_btn_act)
        self.show()

    def color_btn_act(self):
        self.card.change_color_rev(self.get_color())
        self.update_preview()

    def image_btn_act(self):
        imported_rev = self.get_image()
        print(imported_rev.size)
        coords = self.get_coords()
        print(coords)
        self.card.paste_in_rev(imported_rev, coords)
        self.update_preview()

    def text_btn_act(self):
        size = self.get_size()
        text = self.get_text()
        coords = self.get_coords()
        color = self.get_color()
        font = ImageFont.truetype(os.path.join(os.pardir, 'fonts', 'font.ttf'), size)
        print(self.card.check_txt_size_rev(text, font))
        if self.card.check_txt_size_rev(text, font) > (self.width(), self.height()):
            QMessageBox().warning(self, 'Za duży!',
                                  'Tekst o tych paramentrach nie zmieści się na twojej grafice. Spróbuj z innymi ustawieniami!',
                                  QMessageBox.Ok)
            return None
        self.card.add_text_rev(coords, text, color, font)
        self.update_preview()

    def finish_btn_act(self):
        self.close()
        window3.init_ui()

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

    def get_size(self):
        i, ok_pressed = QInputDialog.getInt(self, 'Podaj rozmiar czcionki:', 'Wielkość czcionki:', 0)
        if ok_pressed:
            return i

    def get_coords(self):
        i, ok_pressed0 = QInputDialog.getInt(self, 'Podaj pozycję w poziomie obiektu:',
                                             'Anuluj aby wycentrować horyzontalnie. X:', min=0, max=180)
        j, ok_pressed1 = QInputDialog.getInt(self, 'Podaj pozycję w pionie obiektu:',
                                             'Anuluj aby wycentrować wertykalnie. Y:', min=0, max=252)
        if not ok_pressed0:
            i = -1
        if not ok_pressed1:
            j = -1
        return [i, j]

    def get_text(self):
        text, okPressed = QInputDialog.getText(self, 'Jaki tekst chcesz dodać?', 'Podaj tekst:', QLineEdit.Normal, '')
        if okPressed and text != '':
            return text


class Window3(QWidget):
    """
    user generates his card averse
    """

    def __init__(self):
        super().__init__()

    def init_ui(self):
        self.resize(800, 600)
        self.setWindowTitle('cardschooli - krok 3')
        QLabel(
            'Zaprojektuj swoją kartę. Teraz pora zaprojektować awers. Szablon dla każdej karty będzie taki sam, ale masz\nmożliwość umieszczenia na nim elementów, które dla każdej karty przetworzone zostaną na\nodpowiednią wartość z pliku danych.'.format(),
            self)
        center(self)
        self.card = window2.card
        self.card_loc = os.path.join(os.pardir, 'cards', window0.project, 'preview_ave.png')
        self.preview = QLabel(self)
        self.pixmap = QPixmap(self.card_loc)
        self.preview.setPixmap(self.pixmap)
        self.preview.setGeometry(25, (600 - self.pixmap.height()) / 2, self.pixmap.width(), self.pixmap.height())
        color_btn = QPushButton('Wybierz kolor tła', self)
        image_btn = QPushButton('Zaimportuj grafikę PNG', self)
        image_var_btn = QPushButton('Zaimportuj folder z grafikami PNG', self)
        text_btn = QPushButton('Dodaj tekst', self)
        finish_btn = QPushButton('Zakończ >>>', self)
        color_btn.setGeometry(490, 60, 235, 35)
        image_btn.setGeometry(490, 115, 235, 35)
        image_var_btn.setGeometry(490, 170, 235, 35)
        text_btn.setGeometry(490, 225, 235, 35)
        finish_btn.setGeometry(490, 475, 235, 70)
        color_btn.clicked.connect(self.color_btn_act)
        image_btn.clicked.connect(self.image_btn_act)
        image_var_btn.clicked.connect(self.image_var_btn_act)
        text_btn.clicked.connect(self.text_btn_act)
        finish_btn.clicked.connect(self.finish_btn_act)
        self.show()

    def color_btn_act(self):
        color = self.get_color()
        self.card.change_color_ave(color)
        self.update_preview()

    def image_btn_act(self):
        imported_ave = self.get_image()
        coords = self.get_coords()
        self.card.paste_in_ave(imported_ave, coords)
        self.update_preview()

    def image_var_btn_act(self):
        folder = self.get_folder()
        column = window1.headers.index(self.choose_colum())
        coords = self.get_coords()
        self.card.paste_img_folder_in_ave(folder, column, coords)
        self.update_preview()

    def text_btn_act(self):
        pass

    def finish_btn_act(self):
        self.card.save_ave_cmd_buf()
        self.close()
        window4.init_ui()

    def get_color(self):
        color = QColorDialog()
        color.setFocus()
        color_val = color.getColor()
        if color_val.isValid():
            return color_val.name()
        return "#ffffff"

    def get_folder(self):
        options = QFileDialog.Options()
        filename = \
            QFileDialog.getExistingDirectory(self, "Wybierz folder z plikami PNG:")
        return filename

    def get_image(self):
        options = QFileDialog.Options()
        filename = \
            QFileDialog.getOpenFileName(self, 'Wybierz obrazek do zaimportowania na rewers:', filter='PNG (*.png)',
                                        options=options)[0]
        return filename

    def choose_colum(self):
        response = QInputDialog.getItem(self, 'Wybierz kolumnę, która użyta zostanie do sczytania nazw plików PNG',
                                        'Kolumna z plikami PNG', window1.headers)
        if response[1]:
            return response[0]

    def get_coords(self):
        i, ok_pressed0 = QInputDialog.getInt(self, 'Podaj pozycję w poziomie obiektu:',
                                             'Anuluj aby wycentrować horyzontalnie. X:', min=0, max=180)
        j, ok_pressed1 = QInputDialog.getInt(self, 'Podaj pozycję w pionie obiektu:',
                                             'Anuluj aby wycentrować wertykalnie. Y:', min=0, max=252)
        if not ok_pressed0:
            i = -1
        if not ok_pressed1:
            j = -1
        return [i, j]

    def update_preview(self):
        self.preview.setPixmap(QPixmap(self.card_loc))
        self.update()


class Window4(QWidget):
    """
    cards are compiling info and card compilation
    """

    def __init__(self):
        super().__init__()

    def init_ui(self):
        self.resize(800, 600)
        self.setWindowTitle('cardschooli - krok 4')
        center(self)
        self.card = window3.card
        self.loading = QLabel('Twoja talia jest generowana. Zachowaj cierpliwość, to może chwilę potrwać...', self)
        self.loading.move(140, 216)
        self.preloader = QLabel(self)
        movie = QMovie(os.path.join(os.pardir, 'img', 'preloader.gif'))
        self.preloader.setMovie(movie)
        self.preloader.setGeometry(336, 236, 128, 128)
        self.show()
        movie.start()
        print(self.read_csv_data(window1.filename))
        self.compile()

    def read_csv_data(self, location):
        return list(csv.reader(open(location)))

    def compile(self):
        self.card.compile_ave(self.read_csv_data(window1.filename))


class Card(object):
    def __init__(self, location, size=(180, 252), color_rev='#ffffff', color_av='#ffffff'):
        self.location = location
        self.size = size
        self.color_rev = color_rev
        self.color_av = color_av
        self.prev_ave = Image.new('RGBA', self.size, self.color_rev)
        self.prev_rev_draw = ImageDraw.Draw(self.prev_ave)
        self.prev_ave = Image.new('RGBA', self.size, self.color_av)
        self.prev_ave_draw = ImageDraw.Draw(self.prev_ave)
        self.cmd_buf = ''
        self.preview_rev()
        self.preview_ave()

    def preview_rev(self):
        self.prev_ave.save(os.path.join(self.location, 'preview_rev.png'))

    def change_color_rev(self, color):
        self.prev_ave = Image.new('RGBA', self.size, color)
        self.prev_rev_draw = ImageDraw.Draw(self.prev_ave)
        print("color_rev is now {}".format(color))
        self.preview_rev()

    def paste_in_rev(self, thing, coords):
        if coords[0] == -1 or coords[1] == -1:
            if coords[0] == -1:
                print(self.prev_ave.width, thing.width)
                coords[0] = int((self.prev_ave.width - thing.width) / 2)
            if coords[1] == -1:
                print('h', self.prev_ave.height, thing.height)
                coords[1] = int((self.prev_ave.height - thing.height) / 2)
        print(coords)
        self.prev_ave.paste(thing, coords, thing)
        print('pasted {} in {} at {}'.format(thing, self.prev_ave, coords))
        self.preview_rev()

    def check_txt_size_rev(self, text, font=None):
        return self.prev_rev_draw.textsize(text, font)

    def add_text_rev(self, coords, text, fill=None, font=None):
        self.prev_rev_draw.text(coords, text, fill, font)
        self.preview_rev()

    def preview_ave(self):
        self.prev_ave.save(os.path.join(self.location, 'preview_ave.png'))

    def read_ave_config(self):
        cmds = []
        with open(os.path.join(self.location, 'ave.cardconfig')) as config:
            for i in config.readlines():
                cmds.append(i[:-1].split("_"))
        return cmds

    def compile_ave(self, import_data):
        cmds = self.read_ave_config()
        cards = [Image.new('RGBA', self.size, self.color_av) for i in range(len(import_data))]
        print(cards)
        print(len(cards))
        for i in cmds:
            for j in range(len(cards)):
                if i[0] == 'col':
                    cards[j] = Image.new('RGBA', self.size, i[1])
                    print('updated j to {}, now has color {}'.format(cards[j], i[1]))
                if i[0] == 'img':
                    thing = Image.open(i[1])
                    if int(i[2]) == -1 or int(i[3]) == -1:
                        if int(i[2]) == -1:
                            print('w', self.prev_ave.width, thing.width)
                            i[2] = int((self.prev_ave.width - thing.width) / 2)
                        if int(i[3]) == -1:
                            print('h', self.prev_ave.height, thing.height)
                            i[3] = int((self.prev_ave.height - thing.height) / 2)
                    cards[j].paste(thing, (int(i[2]), int(i[3])), thing)
                if i[0] == 'imgv':
                    pass
        [cards[i].save(os.path.join(self.location, 'card_{}.png'.format(i))) for i in range(len(cards))]

    def save_ave_cmd_buf(self):
        with open(os.path.join(self.location, 'ave.cardconfig'), 'w') as cmd_loc:
            cmd_loc.writelines(self.cmd_buf)
        print('config saved at {}'.format(os.path.join(self.location, 'ave.cardconfig')))

    def change_color_ave(self, color):
        self.prev_ave = Image.new('RGBA', self.size, color)
        self.prev_ave_draw = ImageDraw.Draw(self.prev_ave)
        self.cmd_buf += 'col_{}\n'.format(color)
        print(self.cmd_buf)
        self.preview_ave()

    def paste_in_ave(self, png_loc, coords):
        self.cmd_buf += 'img_{}_{}_{}\n'.format(png_loc, coords[0], coords[1])
        print(self.cmd_buf)
        thing = Image.open(png_loc)
        if coords[0] == -1 or coords[1] == -1:
            if coords[0] == -1:
                print('w', self.prev_ave.width, thing.width)
                coords[0] = int((self.prev_ave.width - thing.width) / 2)
            if coords[1] == -1:
                print('h', self.prev_ave.height, thing.height)
                coords[1] = int((self.prev_ave.height - thing.height) / 2)
        print(coords)
        self.prev_ave.paste(thing, coords, thing)
        self.preview_ave()

    def paste_img_folder_in_ave(self, folder, data_index, coords):
        self.cmd_buf += 'imgv_{}_{}_{}_{}'.format(folder, data_index, coords[0], coords[1])
        print(self.cmd_buf)
        with open(window1.filename, newline='') as f:
            reader = csv.reader(f)
            next(reader)
            first = next(reader)
        thing = Image.open(os.path.join(folder, first[data_index] + '.png'))
        print(thing.size)
        if coords[0] == -1 or coords[1] == -1:
            if coords[0] == -1:
                print('w', self.prev_ave.width, thing.width)
                coords[0] = int((self.prev_ave.width - thing.width) / 2)
            if coords[1] == -1:
                print('h', self.prev_ave.height, thing.height)
                coords[1] = int((self.prev_ave.height - thing.height) / 2)
        print(coords)
        try:
            self.prev_ave.paste(thing, coords, thing)
        except ValueError:
            self.prev_ave.paste(thing, coords)
        self.preview_ave()

    def check_txt_size_ave(self, text, font=None):
        return self.prev_ave_draw.textsize(text, font)

    def add_text_ave(self, coords, text, fill=None, font=None):
        """if coords[0] == 154 or coords[1] == 154:
            size = self.check_txt_size_ave(text, font)
            if coords[0] == 154:
                self.prev_rev_draw.text((self.prev_ave.width - size[0] / 2, coords[1]), text, fill, font)
        else:
            """
        self.prev_rev_draw.text(coords, text, fill, font)
        self.preview_ave()


def center(window):
    qr = window.frameGeometry()
    qr.moveCenter(QDesktopWidget().availableGeometry().center())
    window.move(qr.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window0 = Window0()
    window1 = Window1()
    window2 = Window2()
    window3 = Window3()
    window4 = Window4()
    sys.exit(app.exec_())
