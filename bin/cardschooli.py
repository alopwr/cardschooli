import csv
import os.path
import os.path
import sys

import matplotlib.pyplot as plt
from math import ceil
from PIL import Image, ImageDraw, ImageFont
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPixmap, QMovie, QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QPushButton, QLineEdit, QLabel, QFileDialog, \
    QColorDialog, QInputDialog, QMessageBox, QAction, QListWidget, QVBoxLayout, QListWidgetItem, \
    QHBoxLayout, QDoubleSpinBox, QComboBox, QSpinBox


class QListWidgetItem2(QListWidgetItem):
    def __init__(self, number=0):
        super().__init__()
        self.number = number

    def changeNUMB(self, new_number):
        self.number = new_number


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
        self.start_btn = QPushButton('Rozpocznij tworzenie talii >>>', self)
        self.start_btn.setGeometry(275, 275, 250, 50)
        self.show()
        self.project_name.returnPressed.connect(self.next)
        self.start_btn.clicked.connect(self.next)

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
        self.show()


class MyWidget(QWidget):
    def __init__(self, txt, value, color, image, number, itm=QListWidgetItem2(), maxx=100, dok=2, parent=None):
        super(MyWidget, self).__init__(parent)

        self.color = color
        self.number = number
        self.value = value
        self.name = txt
        itm.changeNUMB(self.number)

        delt_btn = QPushButton()
        delt_btn.setIcon(QIcon(os.path.join(os.pardir, 'img', image)))
        delt_btn.setIconSize(QSize(35, 35))
        delt_btn.resize(10, 10)
        delt_btn.clicked.connect(self.delt_btn_act)

        label = QLabel(txt)
        label2 = QLabel(" % ")
        label3 = QLabel("g")
        spiinbox = QDoubleSpinBox()
        spiinbox.setMinimum(0.01)
        spiinbox.setMaximum(maxx)
        spiinbox.setValue(value)
        spiinbox.setDecimals(dok)

        combobox = QComboBox()
        combobox = self.adding_to_combo(combobox)

        spiinbox.valueChanged[str].connect(self.spiinCHANGE)

        combobox.currentIndexChanged[str].connect(self.comboCHANGE)

        layout = QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(spiinbox)
        if windowWYKR.czyPer:
            layout.addWidget(label2)
        else:
            layout.addWidget(label3)
        layout.addWidget(combobox)
        layout.addWidget(delt_btn)

        self.setLayout(layout)

    def spiinCHANGE(self, newvalue):

        newvalue = windowWYKR.spin_str_2_float(newvalue)
        if windowWYKR.czyPer:
            oldvalue = windowWYKR.LIST_OF_GOD[windowWYKR.values][self.name]
            if not windowWYKR.maxim - (newvalue - oldvalue) >= 0:
                QMessageBox().warning(self, '!!! LIMIT !!!',
                                      '!!!       Przekroczono sumę 100 %      !!! \n zmniejsz procent innego elementu',
                                      QMessageBox.Ok)
            windowWYKR.maxim += (oldvalue - newvalue)

        windowWYKR.LIST_OF_GOD[windowWYKR.values][self.name] = newvalue


    def comboCHANGE(self, value):
        windowWYKR.LIST_OF_GOD[windowWYKR.colors][self.name] = value

    def delt_btn_act(self):
        windowWYKR.deleting(self.number)

    def adding_to_combo(self, combobox):
        if not windowWYKR.czyP:
            List_of_colors = windowWYKR.list_of_colors
        else:
            List_of_colors = windowWYKR.list_of_colors_P
        combobox.addItems(List_of_colors)
        combobox.setCurrentText(self.color)
        return combobox


class quesTion(QMessageBox):
    def __init__(self):
        super().__init__()
        center(self)
        buttonReply = QMessageBox.question(self, 'language',
                                           "Czy przedłumaczyć nazwy kolorów na polski? (słabe tłumaczenie)",
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.Yes:
            windowWYKR.czyP = True
        else:
            windowWYKR.czyP = False
        self.show()


class Window__Wykr(QWidget):
    def __init__(self):
        super().__init__()
        self.czyP = False
        self.isCreatingChart = False
        self.number_of_layouts = -1
        self.LIST_OF_GOD = [{}, {}, {}, {}]
        self.names = 0
        self.values = 1
        self.colors = 2
        self.explodings = 3
        self.maxim = 100
        self.X = 0
        self.Y = 0
        self.czyPer = False
    def init_ui(self):
        czyPol()
        self.loadCOLORS()

        adding = QAction(QIcon(os.path.join(os.pardir, 'img', 'plusiik.png')), "ADD", self)
        adding.setShortcut('Ctrl+N')
        adding.triggered.connect(self.AddNew)
        """
        self.toolbar = self.addToolBar('ADD')
        self.toolbar.addAction(adding)
        """
        add_btn = QPushButton("ADD", self)
        add_btn.setIcon(QIcon(os.path.join(os.pardir, 'img', 'plusiik.png')))
        add_btn.setGeometry(30, 30, 50, 50)
        add_btn.clicked.connect(self.AddNew)
        add_btn.setToolTip("dodaje element do wykresu")

        self.LIST = QListWidget()
        self.LIST.setWindowTitle("Pozycje na wykresie")

        self.resize(800, 600)
        self.setWindowTitle('cardschooli wykresy')
        center(self)

        qr = self.frameGeometry()
        qr2 = qr.getRect()

        self.LIST.setGeometry(50, qr2[1], 400, 600)

        xSPIN = QSpinBox()
        ySPIN = QSpinBox()
        xSPIN.setRange(0, 9999)
        xSPIN.setValue(self.X)
        ySPIN.setRange(0, 9999)
        ySPIN.setValue(self.Y)

        xSPIN.valueChanged[str].connect(self.xSPINchange)
        ySPIN.valueChanged[str].connect(self.ySPINchange)

        OK_btn = QPushButton('Dodaj wykres na karte >>>')
        OK_btn.setGeometry(450, 450, 300, 70)
        OK_btn.clicked.connect(self.ok_act)
        LAJ = QVBoxLayout()
        laj = QHBoxLayout()
        laj3 = QHBoxLayout()
        laj4 = QHBoxLayout()
        LAJ2 = QVBoxLayout()

        LAJ2.addWidget(QLabel("WSPÓŁRZĘDNE\n WYKRESU \nNA KARCIE: "))
        LAJ2.addLayout(laj3)
        LAJ2.addLayout(laj4)

        laj.addWidget(add_btn)
        laj.addWidget(self.LIST)
        laj.addLayout(LAJ2)

        LAJ.addLayout(laj)

        LAJ.addWidget(OK_btn)

        laj3.addWidget(QLabel("X: "))
        laj3.addWidget(xSPIN)
        laj4.addWidget(QLabel("Y: "))
        laj4.addWidget(ySPIN)

        self.setLayout(LAJ)

        self.show()

    def spin_str_2_float(self, newvalueSTR):
        newvalue = ""
        for l in newvalueSTR:
            if l == ",":
                newvalue += "."
            else:
                newvalue += l
        newvalue = float(newvalue)
        return newvalue

    def xSPINchange(self, newvalue):
        self.X = self.spin_str_2_float(newvalue)

    def ySPINchange(self, newvalue):
        self.Y = self.spin_str_2_float(newvalue)

    def deleting(self, number):
        i = 0
        i2 = self.LIST.count()
        while i < i2:
            iitem = self.LIST.item(i)
            if iitem.number == number:
                self.removing(i)
                self.LIST.removeItemWidget(iitem)

            i += 1

    def removing(self, numbeer):
        name = self.LIST_OF_GOD[self.names].pop(numbeer)

        xd = self.LIST_OF_GOD[self.values].pop(name)
        xd1 = self.LIST_OF_GOD[self.colors].pop(name)
        xd2 = self.LIST_OF_GOD[self.explodings].pop(name)
        if self.czyPer:
            self.maxim += float(xd)

    def ok_act(self):
        if self.LIST.count() > 0 and self.suma() == 100.0:
            if self.czyP:
                self.exchange()
            size = self.get_size()
            generating_chart(self.LIST_OF_GOD)
            rescale_and_transp(size)
            adding_chart([self.X, self.Y])
            self.isCreatingChart = False
            self.close()
        elif self.LIST.count() == 0:
            QMessageBox().warning(self, '!!! PUSTO !!!',
                                  '!!!        nie możesz dodać pustego wykresu        !!!', QMessageBox.Ok)
        elif self.suma() > 100.0:
            QMessageBox().warning(self, '!!! LIMIT !!!',
                                  '!!!       Przekroczono sumę 100 %      !!! \n',
                                  QMessageBox.Ok)
        else:
            if self.czyPer:
                QMessageBox().warning(self, '!!! ZA MAŁO !!!',
                                      '!!!       brakuje do sumy 100%      !!! \n',
                                      QMessageBox.Ok)

    def exchange(self):
        for name in self.LIST_OF_GOD[self.colors]:
            color = self.LIST_OF_GOD[self.colors][name]
            self.LIST_OF_GOD[self.colors][name] = self.dict_of_colors[color]

    def smaxim(self):
        if self.czyPer:
            return self.maxim
        else:
            return 999
    def AddNew(self):
        if self.smaxim() > 0:
            itemek = QListWidgetItem2()
            self.number_of_layouts += 1

            name = self.get_text()
            value = self.get_value()
            color = self.get_color()
            if self.czyPer:
                my_itemek = MyWidget(name, value, color, "deleting.png", self.number_of_layouts, itm=itemek, dok=2)
            else:
                my_itemek = MyWidget(name, value, color, "deleting.png", self.number_of_layouts, itm=itemek,
                                     maxx=999999999, dok=1)
            itemek.setSizeHint(my_itemek.sizeHint())

            self.LIST.addItem(itemek)
            self.LIST.setItemWidget(itemek, my_itemek)

            self.LIST_OF_GOD[self.names][self.number_of_layouts] = name
            self.LIST_OF_GOD[self.values][name] = value
            self.LIST_OF_GOD[self.colors][name] = color
            self.LIST_OF_GOD[self.explodings][name] = 0
            if self.czyPer:
                self.maxim -= value

        else:
            QMessageBox().warning(self, '!!! LIMIT !!!',
                                  '!!!       wykorzystano sumę 100 %      !!! \n możesz zmiejszyć procent innego elementu',
                                  QMessageBox.Ok)

    def get_value(self):
        if self.czyPer:
            i, ok_pressed = QInputDialog.getDouble(self, 'Podaj wartość',
                                                   'Podaj wartość elementu na wykresie (%) : ', 1, 0.1, 100, 2)

            if ok_pressed and self.maxim - i >= 0:
                return i
            elif self.maxim - i < 0:
                QMessageBox().warning(self, '!!! LIMIT !!!',
                                      '!!!       Przekroczono sumę 100 %      !!! \n spróbuj ponownie',
                                      QMessageBox.Ok)
                self.get_value()

            return i
        else:
            i, ok_pressed = QInputDialog.getDouble(self, 'Podaj wartość',
                                                   'Podaj wartość elementu na wykresie (q) : ', 1, 1, 999999999, 1)
            if ok_pressed:
                return i
    def get_size(self):
        i, ok_pressed0 = QInputDialog.getInt(self, 'SZEROKOŚĆ',
                                             'Podaj szerokość diagramu. \n(piksele)\n wysokość zostanie wygenerowana z zachowaniem odpowiednich proporcji',
                                             min=1)
        """
        j, ok_pressed1 = QInputDialog.getInt(self, 'WYSOKOŚĆ',
                                             'Podaj wysokość diagramu \n(piksele)\n Anuluj by stworzyć kwadrat', min=1)
        if not ok_pressed1:
            j = i
        """
        j = ceil(i * 0.75)
        print([i, j])
        return [i, j]

    def get_text(self):
        text, okPressed = QInputDialog.getText(self, 'Podaj nazwę elementu', 'NAZWA:', QLineEdit.Normal, '')

        if okPressed and (text != '' or text != " " or text != None):
            return text
        else:
            QMessageBox().warning(self, '!!! PUSTE !!!',
                                  '!!!       Wypełnij nazwę      !!! \n ',
                                  QMessageBox.Ok)
            self.get_text()

    def loadCOLORS(self):
        with open(os.path.join(os.pardir, 'files', 'colors.txt')) as f:
            self.list_of_colors = f.readlines()
        self.list_of_colors = [x.strip() for x in self.list_of_colors]

        with open(os.path.join(os.pardir, 'files', 'colorsPOLISH.txt')) as f:
            self.list_of_colors_P = f.readlines()
        self.list_of_colors_P = [x.strip() for x in self.list_of_colors_P]

        self.dict_of_colors = {}
        for i in range(len(self.list_of_colors)):
            self.dict_of_colors[self.list_of_colors_P[i]] = self.list_of_colors[i]

    def suma(self):

        if self.czyPer:
            summ = 0

            for i in self.LIST_OF_GOD[self.values].values():
                summ += i
            print(summ)
            return summ

        else:
            return 100.0
    def get_color(self):
        if not self.czyP:
            self.List_of_colors = self.list_of_colors
        else:
            self.List_of_colors = self.list_of_colors_P

        item, okPressed = QInputDialog.getItem(self, "wybierz kolor", "KOLOR ELEMENTU NA WYKRESIE: ",
                                               self.List_of_colors, 0, False)
        if okPressed and item:
            return item


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

        chart_btn = QPushButton('dodaj wykres kołowy', self)
        chart_btn.setGeometry(490, 225, 235, 35)
        chart_btn.clicked.connect(self.chart_btn_act)

        self.show()

    def chart_btn_act(self):
        windowWYKR.isCreatingChart = True
        windowWYKR.init_ui()

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
        size = self.get_size()
        text = self.get_text()
        coords = self.get_coords()
        color = self.get_color()
        font = ImageFont.truetype(os.path.join(os.pardir, 'fonts', 'font.ttf'), size)
        if self.card.check_txt_size_ave(text, font) > (self.width(), self.height()):
            QMessageBox().warning(self, 'Za duży!',
                                  'Tekst o tych paramentrach nie zmieści się na twojej grafice. Spróbuj z innymi ustawieniami!',
                                  QMessageBox.Ok)
            return None
        print(color)
        self.card.add_text_ave(coords, text, color, font, size)
        self.update_preview()

    def finish_btn_act(self):
        if not windowWYKR.isCreatingChart:
            self.card.save_ave_cmd_buf()
            self.close()
            window4.init_ui()
        else:
            QMessageBox().warning(self, 'W TRAKCIE CZYNNOŚCI',
                                  'Jesteś w trakcie dodawania wykresu',
                                  QMessageBox.Ok)

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

    def get_size(self):
        i, ok_pressed = QInputDialog.getInt(self, 'Podaj rozmiar czcionki:', 'Wielkość czcionki:', 1)
        if ok_pressed:
            return i

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

    def get_text(self):
        text, okPressed = QInputDialog.getText(self, 'Jaki tekst chcesz dodać?', 'Podaj tekst:', QLineEdit.Normal, '')
        if okPressed and text != '':
            return text

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
        if coords[0] == -1 or coords[1] == -1:
            if coords[0] == -1:
                coords[0] = int((self.prev_rev.width - self.check_txt_size_rev(text, font)[0]) / 2)
            if coords[1] == -1:
                coords[1] = int((self.prev_rev.height - self.check_txt_size_rev(text, font)[1]) / 2)
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
        cards = [Image.new('RGBA', self.size, self.color_av) for i in range(1, len(import_data))]
        print(cards)
        print(len(cards))
        for i in cmds:
            for j in range(len(cards)):
                if i[0] == 'col':
                    cards[j] = Image.new('RGBA', self.size, i[1])
                    print('updated j to {}, now has color {}'.format(cards[j], i[1]))
                elif i[0] == 'img':
                    thing = Image.open(i[1])
                    if int(i[2]) == -1 or int(i[3]) == -1:
                        if int(i[2]) == -1:
                            print('w', self.prev_ave.width, thing.width)
                            i[2] = int((self.prev_ave.width - thing.width) / 2)
                        if int(i[3]) == -1:
                            print('h', self.prev_ave.height, thing.height)
                            i[3] = int((self.prev_ave.height - thing.height) / 2)
                    cards[j].paste(thing, (int(i[2]), int(i[3])), thing)
                elif i[0] == 'imgv':
                    print(i)
                    thing = Image.open(os.path.join(i[1], import_data[j + 1][int(i[2])] + '.png')).convert("RGBA")
                    if int(i[3]) == -1 or int(i[4]) == -1:
                        if int(i[3]) == -1:
                            x = int((self.prev_ave.width - thing.width) / 2)
                        if int(i[4]) == -1:
                            y = int((self.prev_ave.height - thing.height) / 2)
                        cards[j].paste(thing, (x, y), thing)
                    else:
                        cards[j].paste(thing, (int(i[3]), int(i[4])), thing)
                elif i[0] == 'txt':
                    print(i)
                    print(int(i[5]))
                    font = ImageFont.truetype(os.path.join(os.pardir, 'fonts', 'font.ttf'), int(i[5]))
                    obj = ImageDraw.Draw(cards[j])
                    if i[1] == '-1' or i[2] == '-1':
                        if i[1] == '-1':
                            i[1] = int((self.prev_ave.width - self.check_txt_size_ave(i[3], font)[0]) / 2)
                        if i[2] == '-1':
                            i[2] = int((self.prev_ave.height - self.check_txt_size_ave(i[3], font)[1]) / 2)
                    obj.text((int(i[1]), int(i[2])), i[3], i[4], font)
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
        self.cmd_buf += 'imgv_{}_{}_{}_{}\n'.format(folder, data_index, coords[0], coords[1])
        print(self.cmd_buf)
        with open(window1.filename, newline='') as f:
            reader = csv.reader(f)
            next(reader)
            first = next(reader)
        thing = Image.open(os.path.join(folder, first[data_index] + '.png')).convert("RGBA")
        print(thing.size)
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

    def check_txt_size_ave(self, text, font=None):
        return self.prev_ave_draw.textsize(text, font)

    def add_text_ave(self, coords, text, fill=None, font=None, size=None):
        print(font)
        self.cmd_buf += "txt_{}_{}_{}_{}_{}\n".format(coords[0], coords[1], text, fill, size)
        print(self.cmd_buf)
        if coords[0] == -1 or coords[1] == -1:
            if coords[0] == -1:
                coords[0] = int((self.prev_ave.width - self.check_txt_size_ave(text, font)[0]) / 2)
            if coords[1] == -1:
                coords[1] = int((self.prev_ave.height - self.check_txt_size_ave(text, font)[1]) / 2)
        self.prev_ave_draw.text(coords, text, fill, font)
        self.preview_ave()


def generating_chart(LIST_OF_GOD):
    if not windowWYKR.czyPer:
        names = []
        for name in LIST_OF_GOD[0].values():  # names = 0
            names.append(name)

        labels = []
        for name in LIST_OF_GOD[1].values():  # values = 1
            labels.append((str(name) + " g"))

        sizes = []
        for value in LIST_OF_GOD[1].values():  # values = 1
            sizes.append(value)

        colors = []
        for color in LIST_OF_GOD[2].values():  # colors = 2
            colors.append(color)

        explode = []
        for expld in LIST_OF_GOD[3].values():  # explode = 3
            explode.append(expld)

        patches, texts = plt.pie(sizes, labels=labels, colors=colors, shadow=True, startangle=90, labeldistance=0.5)
        plt.axis('equal')
        plt.savefig(os.path.join(os.pardir, "cards", window0.project, "wykresOLD.png"))

        x, y = calculate(names)
        figlegend = plt.figure(figsize=(x, y))
        figlegend.legend(patches, names)
        figlegend.savefig(os.path.join(os.pardir, "cards", window0.project, "legend.png"))


    else:
        labels = []
        for name in LIST_OF_GOD[0].values():  # names = 0
            labels.append(name)

        sizes = []
        for value in LIST_OF_GOD[1].values():  # values = 1
            sizes.append(value)

        colors = []
        for color in LIST_OF_GOD[2].values():  # colors = 2
            colors.append(color)

        explode = []
        for expld in LIST_OF_GOD[3].values():  # explode = 3
            explode.append(expld)

        plt.pie(sizes, explode=explode, colors=colors, labels=labels,
                autopct='%1.1f%%', shadow=True, startangle=140)

        plt.axis('equal')
        plt.savefig(os.path.join(os.pardir, "cards", window0.project, "wykresOLD.png"))
def adding_chart(coords):
    pass


def calculate(names):
    dlugosci = []
    for name in names:
        dlugosci.append(len(name))
    dl = max(dlugosci)
    DL = (dl * 0.1 + 0.5)
    wys = len(names)
    WYS = (wys * 0.25) + 0.11
    return (DL, WYS)


def rescale_and_transp(size):
    img = Image.open(os.path.join(os.pardir, "cards", window0.project, "wykresOLD.png"))
    new_img = img.resize(size)
    new_img.save(os.path.join(os.pardir, "cards", window0.project, "wykres.png"), 'png')

    new_img = Image.open(os.path.join(os.pardir, "cards", window0.project, "wykres.png"))
    new_img.convert("RGBA")
    datas = new_img.getdata()
    newData = []
    for item in datas:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)
    new_img.putdata(newData)
    new_img.save(os.path.join(os.pardir, "cards", window0.project, "wykresnew.png"), 'png')



def center(window):
    qr = window.frameGeometry()

    qr.moveCenter(QDesktopWidget().availableGeometry().center())
    window.move(qr.topLeft())


def czyPol():
    question1 = quesTion()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    windowWYKR = Window__Wykr()
    window0 = Window0()
    window1 = Window1()
    window2 = Window2()
    window3 = Window3()
    window4 = Window4()
    sys.exit(app.exec_())
