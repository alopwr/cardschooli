# coding=utf-8
"""
cardschooli gui
allows user creating his deck of cards
"""
import sys

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QPushButton, QLineEdit, QLabel, QFileDialog, \
    QColorDialog, QInputDialog, QMessageBox

import fs_interaction
import reverse


def center(window):
    """ centers window """
    qr = window.frameGeometry()
    qr.moveCenter(QDesktopWidget().availableGeometry().center())
    window.move(qr.topLeft())


def file_dialog(parent, caption, expression, ext):
    """ shows file dialog """
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    filename = QFileDialog.getOpenFileName(parent=parent, caption=caption, filter=expression, options=options)
    return filename[0] if filename[1] or filename[0].endswith(ext) else None


def color_dialog():
    """ shows color dialog """
    color = QColorDialog.getColor()
    if color.isValid():
        return color.name()
    return None


def size_dialog(parent):
    """ gets text's size"""
    i, ok_pressed = QInputDialog.getInt(parent, parent, "Podaj rozmiar czcionki:", "Wielkość czcionki:", 1)
    if ok_pressed:
        return i


def text_dialog(parent):
    """ gets text """
    text, ok_pressed = QInputDialog.getText(parent, "Jaki tekst chcesz dodać?", "Podaj tekst:", QLineEdit.Normal)
    if ok_pressed and text:
        return text


def raise_warning(parent, caption, text):
    """ raises PyQt warning """
    QMessageBox.warning(parent, caption, text, QMessageBox.Ok)


def coords_dialog(parent):
    """ asks user for coords """
    i, ok_pressed0 = QInputDialog.getInt(parent, "Podaj pozycję w poziomie obiektu:",
                                         "Anuluj aby wycentrować horyzontalnie. X:", min=0, max=180)
    j, ok_pressed1 = QInputDialog.getInt(parent, "Podaj pozycję w pionie obiektu:",
                                         "Anuluj aby wycentrować wertykalnie. Y:", min=0, max=252)
    if not ok_pressed0:
        i = -1
    if not ok_pressed1:
        j = -1
    return [i, j]


class Window0(QWidget):
    """
    starting window
    asks user for project name
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("cardschooli - witaj!")
        self.resize(800, 600)
        center(self)
        self.project_name = QLineEdit(self)
        self.project_name.setToolTip("Wprowadź dowolną nazwę projektu.")
        self.project_name.move(275, 200)
        self.project_name.resize(250, 25)
        self.start_btn = QPushButton("Rozpocznij tworzenie talii >>>", self)
        self.start_btn.setGeometry(275, 275, 250, 50)
        self.show()
        self.project_name.returnPressed.connect(self.next)
        self.start_btn.clicked.connect(self.next)

    def next(self):
        if not fs_interaction.project_location(self.project_name.text()):
            raise_warning(self, "Tylko znaki alfanumeryczne!",
                          "W nazwie projektu wykorzystałeś znaki niealfanumeryczne. Spróbuj jeszcze raz!")
            return None
        self.project = self.project_name.text()
        self.close()
        window1.show()


class Window1(QWidget):
    """
    csv import window
    asks user for his data file (*.csv)
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("cardschooli - krok 1")
        self.resize(800, 600)
        center(self)
        QLabel(
            "Wybierz plik *.csv z danymi do projektu {}. Zostanie tylko wczytany, nie będzie naruszony. \nKoniecznie "
            "użyj nagłówków!".format(
                window0.project), self)
        open_btn = QPushButton("Otwórz plik", self)
        open_btn.setGeometry(325, 250, 150, 100)
        open_btn.clicked.connect(self.open_file)

    def open_file(self):
        self.filename = file_dialog(self, "Wybierz plik z danymi:", "dane do cardschooli (*.csv)", ".csv")
        if not self.filename:
            raise_warning(self, "Nie wybrałeś pliku",
                          "Nie wybrałeś pliku, bądź ma on nieodpowiedni format. Użyj pliku .csv!")
            return None
        self.close()
        window2.show()


class Window2(QWidget):
    """
    designing reverse
    user makes his reverse
    Features: customizing background color, importing png, adding text
    """

    def __init__(self):
        super().__init__()
        self.resize(800, 600)
        self.setWindowTitle("cardschooli - krok 2")
        QLabel(
            "Zaprojektuj swoją kartę. Zacznijmy od rewersu, czyli tej strony z tyłu. Będzie taki sam dla każdej karty.",
            self)
        center(self)
        path = fs_interaction.project_location(window0.project, "reverse.png")
        self.card = reverse.CardReverse(path)
        self.preview = QLabel(self)
        self.pixmap = QPixmap(path)
        self.preview.setPixmap(self.pixmap)
        self.preview.setGeometry(25, (600 - self.pixmap.height()) / 2, self.pixmap.width(), self.pixmap.height())
        color_btn = QPushButton("Wybierz kolor tła", self)
        image_btn = QPushButton("Zaimportuj grafikę PNG", self)
        text_btn = QPushButton("Dodaj tekst", self)
        finish_btn = QPushButton("Dalej >>>", self)
        color_btn.setGeometry(500, 60, 225, 35)
        image_btn.setGeometry(500, 115, 225, 35)
        text_btn.setGeometry(500, 170, 225, 35)
        finish_btn.setGeometry(500, 475, 225, 70)
        color_btn.clicked.connect(self.color_btn_act)
        image_btn.clicked.connect(self.image_btn_act)
        text_btn.clicked.connect(self.text_btn_act)
        finish_btn.clicked.connect(self.finish_btn_act)

    def update_preview(self):
        self.pixmap = QPixmap(self.card_loc)
        self.preview.setPixmap(self.pixmap)
        self.update()

    def color_btn_act(self):
        color = color_dialog()
        if color:
            self.card.change_color(color)
            self.update_preview()

    def image_btn_act(self):
        imported_rev = file_dialog(self, "Wybierz obrazek do zaimportowania na rewers:", "PNG (*.png)", ".png")
        if imported_rev:
            coords = coords_dialog(self)
            self.card.paste(imported_rev, coords)
            self.update_preview()

    def text_btn_act(self):
        text = text_dialog(self)
        if not text:
            return None
        size = size_dialog(self)
        if not size:
            return None
        coords = coords_dialog(self)
        if not coords:
            return None
        color = color_dialog()
        if not color:
            return None
        font = ImageFont.truetype(os.path.join(os.pardir, 'fonts', 'font.ttf'), size)
        print(self.card.check_txt_size_rev(text, font))
        if self.card.check_txt_size_rev(text, font) > (self.width(), self.height()):
            QMessageBox().warning(self, "Za duży!",
                                  "Tekst o tych paramentrach nie zmieści się na twojej grafice. Spróbuj z innymi ustawieniami!",
                                  QMessageBox.Ok)
            return None
        self.card.add_text_rev(coords, text, color, font)
        self.update_preview()

    def finish_btn_act(self):
        self.close()
        window3.init_ui()

    def get_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename = \
            QFileDialog.getOpenFileName(self, 'Wybierz obrazek do zaimportowania na rewers:', filter='PNG (*.png)',
                                        options=options)[0]
        return Image.open(filename)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    coords_dialog()
    """window0 = Window0()
    window1 = Window1()
    window2 = Window2()
    window3 = Window3()
    window4 = Window4()"""
    sys.exit(app.exec_())
