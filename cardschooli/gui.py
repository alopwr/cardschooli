# coding=utf-8
"""
cardschooli gui
allows user creating his deck of cards
"""
import os.path
import sys

from PyQt5.QtGui import QPixmap, QMovie, QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QPushButton, QLineEdit, QLabel, QFileDialog, \
    QColorDialog, QInputDialog, QMessageBox

import cardschooli.charts
import cardschooli.fs_interaction
import cardschooli.obverse
import cardschooli.reverse


def center(window):
    """ centers window """
    qr = window.frameGeometry()
    qr.moveCenter(QDesktopWidget().availableGeometry().center())
    window.move(qr.topLeft())


def file_dialog(parent, caption, *expression, folder=False):
    """ shows file dialog """
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    if folder:
        filename = QFileDialog.getExistingDirectory(parent=parent, caption=caption)
        return filename
    filename = QFileDialog.getOpenFileName(parent=parent, caption=caption, filter=expression[0], options=options)
    return filename[0] if filename[1] and filename[0].endswith(expression[1]) else None


def color_dialog():
    """ shows color dialog """
    color = QColorDialog.getColor()
    if color.isValid():
        return color.name()
    return None


def size_dialog(parent):
    """ gets text"s size"""
    i, ok_pressed = QInputDialog.getInt(parent, "Podaj rozmiar czcionki:", "Wielkość czcionki:", 1)
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
                                         "Anuluj aby wycentrować horyzontalnie. X:", min=0, max=1500)
    j, ok_pressed1 = QInputDialog.getInt(parent, "Podaj pozycję w pionie obiektu:",
                                         "Anuluj aby wycentrować wertykalnie. Y:", min=0, max=2100)
    if not ok_pressed0:
        i = -1
    if not ok_pressed1:
        j = -1
    return [i, j]


def choose_colum(parent, caption, text, selections):
    response = QInputDialog.getItem(parent, caption, text, selections)
    if response[1]:
        return response[0]


class Window0(QWidget):
    """
    starting window
    asks user for project name
    """

    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon(os.path.join(os.pardir, "res", "img", "icon.png")))
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
        self.start_btn.setStyleSheet("background-color: aqua")
    def next(self):
        self.project = self.project_name.text()
        cardschooli.charts.window_wykr.give_project(self.project)
        if not cardschooli.fs_interaction.project_location(self.project_name.text()):
            raise_warning(self, "Tylko znaki alfanumeryczne!",
                          "W nazwie projektu wykorzystałeś znaki niealfanumeryczne. Spróbuj jeszcze raz!")
            return None

        self.close()

        window1.init_ui()


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
        open_btn = QPushButton("Otwórz plik", self)
        open_btn.setGeometry(325, 250, 150, 100)
        open_btn.clicked.connect(self.open_file)
        open_btn.setStyleSheet("background-color: aqua")
    def init_ui(self):
        self.setWindowIcon(QIcon(os.path.join(os.pardir, "res", "img", "icon.png")))
        QLabel(
            "Wybierz plik *.csv z danymi do projektu {}. Zostanie tylko wczytany, nie będzie naruszony. \nKoniecznie "
            "użyj nagłówków!".format(
                window0.project), self)
        self.show()

    def open_file(self):
        self.filename = file_dialog(self, "Wybierz plik z danymi:", "dane do cardschooli (*.csv)", ".csv")
        if not self.filename:
            raise_warning(self, "Nie wybrałeś pliku",
                          "Nie wybrałeś pliku, bądź ma on nieodpowiedni format. Użyj pliku .csv!")
            return None
        self.close()
        cardschooli.charts.window_wykr.filename = window1.filename
        window2.init_ui()


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
        color_btn = QPushButton("Wybierz kolor tła", self)
        image_btn = QPushButton("Zaimportuj grafikę PNG", self)
        text_btn = QPushButton("Dodaj tekst", self)
        finish_btn = QPushButton("Dalej >>>", self)
        color_btn.setGeometry(500, 60, 225, 35)
        image_btn.setGeometry(500, 115, 225, 35)
        text_btn.setGeometry(500, 170, 225, 35)
        finish_btn.setGeometry(500, 475, 225, 70)
        color_btn.clicked.connect(self.color_btn_act)
        color_btn.setStyleSheet("background-color: indianRed")
        image_btn.clicked.connect(self.image_btn_act)
        image_btn.setStyleSheet("background-color: lightyellow")
        text_btn.clicked.connect(self.text_btn_act)
        text_btn.setStyleSheet("background-color: lightgreen")
        finish_btn.clicked.connect(self.finish_btn_act)
        finish_btn.setStyleSheet("background-color: orange")
    def init_ui(self):
        self.setWindowIcon(QIcon(os.path.join(os.pardir, "res", "img", "icon.png")))
        self.path = cardschooli.fs_interaction.project_location(window0.project, "reverse_preview.png")
        self.card = cardschooli.reverse.CardReverse(window0.project)
        self.preview = QLabel(self)
        self.pixmap = QPixmap(self.path)
        self.preview.setPixmap(self.pixmap)
        self.preview.setGeometry(25, 60, self.pixmap.width(), self.pixmap.height())
        self.show()

    def update_preview(self):
        self.pixmap = QPixmap(self.path)
        self.preview.setPixmap(self.pixmap)
        self.update()

    def color_btn_act(self):
        color = color_dialog()
        if color:
            self.card.change_color(color)
            self.update_preview()

    def image_btn_act(self):
        paste_path = file_dialog(self, "Wybierz obrazek do zaimportowania na rewers:", "PNG (*.png)", ".png")
        if not paste_path:
            raise_warning(self, "Nie wybrałeś obrazka!", "Nie wybrałeś obrazka do zaimportowania!")
            return None
        coords = coords_dialog(self)
        self.card.paste(paste_path, coords)
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
        if self.card.add_text(coords, text, size, color):
            raise_warning(self, "Za duży tekst!", "Wybrany przez ciebie tekst nie zmieści się na karcie. Spróbuj "
                                                  "ponownie z innymi ustawieniami.")
            return None
        self.update_preview()

    def finish_btn_act(self):
        self.close()
        window3.init_ui()


class Window3(QWidget):
    """
    Designing obverse, user makes his obverse. Features: customizing background color, importing png, importing png
    folder, adding text with variables from data file
    """

    def __init__(self):
        super().__init__()
        self.resize(800, 600)
        self.setWindowTitle("cardschooli - krok 3")
        QLabel(
            "Zaprojektuj swoją kartę. Teraz pora zaprojektować awers. Szablon będzie taki sam, "
            "ale masz\nmożliwość umieszczenia na nim elementów, które dla każdej karty przetworzone zostaną "
            "na\nodpowiednią wartość z pliku danych.".format(),
            self)
        center(self)
        color_btn = QPushButton("Wybierz kolor tła", self)
        image_btn = QPushButton("Zaimportuj grafikę PNG", self)
        image_var_btn = QPushButton("Zaimportuj folder z grafikami PNG", self)
        text_btn = QPushButton("Dodaj tekst", self)
        text_seria_btn = QPushButton("Dodaj serię tekstu", self)
        finish_btn = QPushButton("Zakończ >>>", self)
        chart_btn = QPushButton("Dodaj wykres kołowy", self)
        chart_seria_btn = QPushButton("Dodaj seryjne wykresy kołowe", self)
        color_btn.setGeometry(490, 60, 235, 35)

        image_btn.setGeometry(490, 115, 235, 35)
        image_var_btn.setGeometry(490, 170, 235, 35)

        text_btn.setGeometry(490, 225, 235, 35)
        text_seria_btn.setGeometry(490, 280, 235, 35)
        chart_btn.setGeometry(490, 335, 235, 35)
        chart_seria_btn.setGeometry(490, 390, 235, 35)
        finish_btn.setGeometry(490, 475, 235, 70)

        color_btn.clicked.connect(self.color_btn_act)
        color_btn.setStyleSheet("background-color: indianRed")
        image_btn.clicked.connect(self.image_btn_act)
        image_btn.setStyleSheet("background-color: lightyellow")
        image_var_btn.clicked.connect(self.image_folder_btn_act)
        image_var_btn.setStyleSheet("background-color: lightyellow")
        text_btn.clicked.connect(self.text_btn_act)
        text_btn.setStyleSheet("background-color: lightgreen")
        text_seria_btn.clicked.connect(self.text_seria_btn_act)
        text_seria_btn.setStyleSheet("background-color: lightgreen")
        finish_btn.clicked.connect(self.finish_btn_act)
        finish_btn.setStyleSheet("background-color: orange")
        chart_btn.clicked.connect(self.chart_btn_act)
        chart_btn.setStyleSheet("background-color: lightblue")
        chart_seria_btn.clicked.connect(self.chart_seria_btn_act)
        chart_seria_btn.setStyleSheet("background-color: lightblue")

    def text_seria_btn_act(self):
        column = choose_colum(self, "Wybierz kolumnę:",
                              "Wybierz kolumnę, w której zapisane są teksty dla każdej karty: ",
                              cardschooli.fs_interaction.read_csv(window1.filename, 0))
        if not column:
            return None
        column_data = cardschooli.fs_interaction.read_csv(window1.filename, 0)
        column_nr = column_data.index(column)

        size = size_dialog(self)
        if not size:
            return None
        coords = coords_dialog(self)
        if not coords:
            return None
        color = color_dialog()
        if not color:
            return None

        self.card.add_text_series(column_nr, coords, size, color, first=True)

        self.update_preview()

    def chart_btn_act(self):
        cardschooli.charts.window_wykr.isCreatingChart = True
        cardschooli.charts.window_wykr.init_ui()

    def chart_seria_btn_act(self):
        del cardschooli.charts.window_seria_wykr
        cardschooli.charts.create_window_seria_wykr()

        column = choose_colum(self, "Wybierz kolumnę",
                              "Wybierz kolumnę, w której zapisane są nazwy kart (tytuły):",
                              cardschooli.fs_interaction.read_csv(window1.filename, 0))
        try:
            column_data = cardschooli.fs_interaction.read_csv(window1.filename, 0)
            column_nr = column_data.index(column)
        except:  # !!!
            return None
        cardschooli.charts.window_seria_wykr.init_ui([column, column_nr, column_data])

    def init_ui(self):
        self.setWindowIcon(QIcon(os.path.join(os.pardir, "res", "img", "icon.png")))
        self.path = cardschooli.fs_interaction.project_location(window0.project, "obverse_preview.png")
        self.card = cardschooli.obverse.CardObverse(window0.project, window1.filename)
        self.card.save_preview()
        self.preview = QLabel(self)
        self.pixmap = QPixmap(self.path)
        self.preview.setPixmap(self.pixmap)
        self.preview.setGeometry(25, 60, self.pixmap.width(), self.pixmap.height())
        self.show()

    def update_preview(self):
        self.card.save_preview()
        self.pixmap = QPixmap(self.path)
        self.preview.setPixmap(self.pixmap)
        self.update()

    def color_btn_act(self):
        color = color_dialog()
        if color:
            self.card.change_color(color)
            self.update_preview()

    def image_btn_act(self):
        paste_path = file_dialog(self, "Wybierz obrazek do zaimportowania na awers:", "PNG (*.png)", ".png")
        if not paste_path:
            raise_warning(self, "Nie wybrałeś obrazka!", "Nie wybrałeś obrazka do zaimportowania!")
            return None
        coords = coords_dialog(self)
        self.card.paste(paste_path, coords)
        self.update_preview()

    def image_folder_btn_act(self):
        column = choose_colum(self, "Wybierz kolumnę:",
                              "Wybierz kolumnę, w której zapisane są nazwy plików PNG dla każdej karty:",
                              cardschooli.fs_interaction.read_csv(window1.filename, 0))
        if not column:
            return None
        column_data = cardschooli.fs_interaction.read_csv(window1.filename, 0)
        column_nr = column_data.index(column)
        folder = file_dialog(self, "Wybierz folder z obrazkami:", folder=True)
        if not folder:
            return None
        coords = coords_dialog(self)
        if not coords:
            return None
        self.card.add_image_folder(folder, column_nr, coords, first=True)
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
        if self.card.add_text(coords, text, size, color):
            raise_warning(self, "Za duży tekst!", "Wybrany przez ciebie tekst nie zmieści się na karcie. Spróbuj "
                                                  "ponownie z innymi ustawieniami.")
            return None
        self.update_preview()

    def finish_btn_act(self):
        if not cardschooli.charts.window_wykr.isCreatingChart and not cardschooli.charts.window_seria_wykr.isCreatingChart:
            self.close()
            window4.init_ui()
        else:
            QMessageBox().warning(self, "W TRAKCIE CZYNNOŚCI",
                                  "Jesteś w trakcie dodawania wykresu",
                                  QMessageBox.Ok)


class Window4(QWidget):
    def __init__(self):
        super().__init__()

        self.resize(800, 600)
        self.setWindowTitle("cardschooli - krok 4")
        center(self)
        self.loading = QLabel("Twoja talia jest generowana. Zachowaj cierpliwość, to może chwilę potrwać...", self)
        self.loading.move(140, 216)
        self.preloader = QLabel(self)
        movie = QMovie(os.path.join(os.pardir, "res", "img", "preloader.gif"))
        self.preloader.setMovie(movie)
        movie.start()
        self.preloader.setGeometry(336, 236, 128, 128)

    def init_ui(self):
        self.setWindowIcon(QIcon(os.path.join(os.pardir, "res", "img", "icon.png")))
        self.show()
        self.compile()

    def compile(self):
        if cardschooli.obverse.generate(window0.project, window1.filename,
                                        cardschooli.fs_interaction.project_location(window0.project,
                                                                                    "obverse.cardconfig")):
            raise_warning(self, "Brak pliku konfiguracyjnego", "Nie udało się wczytać pliku konfiguracyjnego talii.")
            return 1
        cardschooli.fs_interaction.cleaning_files(os.path.join(os.pardir, "cards", window0.project))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window0 = Window0()
    window1 = Window1()
    window2 = Window2()
    window3 = Window3()
    window4 = Window4()

    cardschooli.charts.create_window_wykr()
    cardschooli.charts.create_window_seria_wykr()
    cardschooli.charts.window_wykr.window3 = window3

    sys.exit(app.exec_())
