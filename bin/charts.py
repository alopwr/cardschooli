import os.path
import matplotlib.pyplot as plt
from PIL import Image
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlaylist, QMediaPlayer, QMediaContent
import platform

from PyQt5.QtCore import QSize, pyqtSlot
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QLabel, \
    QInputDialog, QMessageBox, QListWidget, QVBoxLayout, QListWidgetItem, \
    QHBoxLayout, QDoubleSpinBox, QComboBox, QSpinBox, QMainWindow, QTabWidget

import fs_interaction
import gui, obverse


def czyPol():
    question1 = quesTion()

class QListWidgetItem2(QListWidgetItem):
    def __init__(self, number=0, imie=""):
        super().__init__()
        self.number = number
        self.name = imie
    def changeNUMB(self, new_number):
        self.number = new_number
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
        if window_wykr.czy_per:
            layout.addWidget(label2)
        else:
            layout.addWidget(label3)
        layout.addWidget(combobox)
        layout.addWidget(delt_btn)

        self.setLayout(layout)

    def spiinCHANGE(self, newvalue):

        newvalue = window_wykr.spin_str_2_float(newvalue)
        if window_wykr.czy_per:
            oldvalue = window_wykr.LIST_OF_GOD[window_wykr.values][self.name]
            if not window_wykr.maxim - (newvalue - oldvalue) >= 0:
                QMessageBox().warning(self, '!!! LIMIT !!!',
                                      '!!!       Przekroczono sumę 100 %      !!! \n zmniejsz procent innego elementu',
                                      QMessageBox.Ok)
                window_wykr.maxim += (oldvalue - newvalue)

                window_wykr.LIST_OF_GOD[window_wykr.values][self.name] = newvalue

    def comboCHANGE(self, value):
        window_wykr.LIST_OF_GOD[window_wykr.colors][self.name] = value

    def delt_btn_act(self):
        window_wykr.deleting(self.number)

    def adding_to_combo(self, combobox):
        if not window_wykr.czyP:
            List_of_colors = window_wykr.list_of_colors
        else:
            List_of_colors = window_wykr.list_of_colors_P
        combobox.addItems(List_of_colors)
        combobox.setCurrentText(self.color)
        return combobox

class quesTion(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon(os.path.join(os.pardir, "img", 'iconka.png')))
        gui.center(self)
        buttonReply = QMessageBox.question(self, 'language',
                                           "Czy przedłumaczyć nazwy kolorów na polski? (słabe tłumaczenie)",
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if buttonReply == QMessageBox.Yes:
            window_wykr.changeczyP(True)
        else:
            window_wykr.changeczyP(False)

        self.show()
def play_():
    try:
        if platform.system() == "Windows":
            global playlist, player
            playlist = QMediaPlaylist()
            url = QUrl.fromLocalFile(os.path.join(os.pardir, "res", "fonts", "music.mp3"))
            playlist.addMedia(QMediaContent(url))
            playlist.setPlaybackMode(QMediaPlaylist.Loop)

            player = QMediaPlayer()
            player.setPlaylist(playlist)
            player.play()
    except:
        pass
class Window_Wykr(QWidget):
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
        self.czy_per = False
        self.project = ""
        self.filename = ""
        self.card3 = None
        play_()
    def init_ui(self):
        self.setWindowIcon(QIcon(os.path.join(os.pardir, "img", 'iconka.png')))
        czyPol()

        self.loadCOLORS()

        add_btn = QPushButton("ADD", self)
        add_btn.setIcon(QIcon(os.path.join(os.pardir, 'img', 'plusiik.png')))
        add_btn.setGeometry(30, 30, 50, 50)
        add_btn.clicked.connect(self.AddNew)
        add_btn.setToolTip("dodaje element do wykresu")

        self.LIST = QListWidget()
        self.LIST.setToolTip("pozycje na wykresie")

        self.resize(800, 600)
        self.setWindowTitle('cardschooli wykresy')

        gui.center(self)

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

    def changeczyP(self, new):
        self.czyP = new

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
        if self.czy_per:
            self.maxim += float(xd)

    def ok_act(self):
        if self.LIST.count() > 0 and self.suma() == 100.0:
            if self.czyP:
                self.exchange()
            size = self.get_size()

            self.generating_chart(self.LIST_OF_GOD, size)

            self.transp()
            self.adding_chart([self.X, self.Y])

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
        if self.czy_per:
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
            if self.czy_per:
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
            if self.czy_per:
                self.maxim -= value

        else:
            QMessageBox().warning(self, '!!! LIMIT !!!',
                                  '!!!       wykorzystano sumę 100 %      !!! \n możesz zmiejszyć procent innego elementu',
                                  QMessageBox.Ok)

    def get_value(self):
        if self.czy_per:
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
                                             'Podaj szerokość diagramu. \n(piksele)', 100,
                                             min=1)

        j, ok_pressed1 = QInputDialog.getInt(self, 'WYSOKOŚĆ',
                                             'Podaj wysokość diagramu \n(piksele)\n Anuluj by stworzyć kwadrat', i,
                                             min=1)
        if not ok_pressed1:
            j = i

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
        with open(os.path.join(os.pardir, 'res', 'files', 'colors.txt')) as f:
            self.list_of_colors = f.readlines()
        self.list_of_colors = [x.strip() for x in self.list_of_colors]

        with open(os.path.join(os.pardir, 'res', 'files', 'colorsPOLISH.txt')) as f:
            self.list_of_colors_P = f.readlines()
        self.list_of_colors_P = [x.strip() for x in self.list_of_colors_P]

        self.dict_of_colors = {}
        for i in range(len(self.list_of_colors)):
            self.dict_of_colors[self.list_of_colors_P[i]] = self.list_of_colors[i]

    def suma(self):

        if self.czy_per:
            summ = 0

            for i in self.LIST_OF_GOD[self.values].values():
                summ += i

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

    def adding_chart(self, coords):

        imported = fs_interaction.project_location(window_wykr.project, "wykres.png")
        self.window3.card.paste(imported, coords)
        self.window3.update_preview()

    def calculate(self, names):
        dlugosci = []
        for name in names:
            dlugosci.append(len(name))
        dl = max(dlugosci)
        dl2 = (dl * 0.1 + 0.5)
        wys = len(names)
        wys2 = (wys * 0.25) + 0.11
        return (dl2, wys2)

    def transp(self):

        new_img = Image.open(fs_interaction.project_location(window_wykr.project, "wykresOLD.png"))
        new_img.convert("RGBA")
        datas = new_img.getdata()
        newData = []
        for item in datas:
            if item[0] == 255 and item[1] == 255 and item[2] == 255:
                newData.append((255, 255, 255, 0))
            else:
                newData.append(item)
        new_img.putdata(newData)
        new_img.save(fs_interaction.project_location(window_wykr.project, "wykres.png"), 'png')

    def dym_font(self, texts, size):

        newTEXTS = []
        if size[0] >= 300 or size[1] >= 300:
            for txt in texts:
                txt.set_fontsize(8)
                newTEXTS.append(txt)
        elif size[0] >= 100 or size[1] >= 100:
            for txt in texts:
                txt.set_fontsize(4)
                newTEXTS.append(txt)
        elif size[0] < 40 or size[1] < 40:
            for txt in texts:
                txt.set_fontsize(1)
                newTEXTS.append(txt)
        elif size[0] < 10 or size[1] < 10:
            for txt in texts:
                txt.set_fontsize(0.6)
                newTEXTS.append(txt)
        else:
            for txt in texts:
                txt.set_fontsize(2)
                newTEXTS.append(txt)

        return newTEXTS

    def generating_chart(self, LIST_OF_GOD, size):
        if not self.czy_per:
            names = []
            for name in LIST_OF_GOD[0].values():  # names = 0
                names.append(name)

            labels = []
            for name in LIST_OF_GOD[1].values():  # values = 1
                if int(name) == name:
                    labels.append((str(name)[:2] + " g"))
                else:
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
            plt.figure(figsize=(size[0] / 100, size[1] / 100))
            patches, texts = plt.pie(sizes, labels=labels, shadow=False, startangle=90, colors=colors,
                                     labeldistance=0.5)

            texts = self.dym_font(texts, size)
            plt.axis('equal')
            plt.savefig(fs_interaction.project_location(window_wykr.project, "wykresOLD.png"), dpi=600)
            x, y = self.calculate(names)
            figlegend = plt.figure(figsize=(x, y))
            figlegend.legend(patches, names)
            figlegend.savefig(fs_interaction.project_location(window_wykr.project, "legend.png"), dpi=600)


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

            plt.figure(figsize=(size[0] / 100, size[1] / 100))
            plt.pie(sizes, explode=explode, colors=colors, labels=labels,
                    autopct='%1.1f%%', shadow=False, startangle=140)
            plt.axis('equal')
            plt.savefig(fs_interaction.project_location(window_wykr.project, "wykresOLD.png"))


def choose_colum(parent, caption, text, selections):
    response = QInputDialog.getItem(parent, caption, text, selections)

    if response[1]:
        return response[0]
    """
    elif not (response[0] in selections):
        mes = QMessageBox.warning("brak kolumny","podana kolumna nie istnieje",QMessageBox.Ok)
        mes.show()
        choose_colum(parent, caption, text, selections)
    """
class My_Cool_Widget(QWidget):
    def __init__(self):
        super().__init__()
        self.czyP = False
        self.columnlist = window_seria_wykr.columnlist
        self.load_rows()

        self.load_labels()

        self.LIST_OF_TABS = {}
        self.LIST = {}
        self.layout = QVBoxLayout(self)

        self.tabs = QTabWidget()


        for label in self.labels:
            tab = QWidget()
            self.tabs.addTab(tab, label)

            tab.laj = QVBoxLayout(self)

            tab.list = QListWidget()
            tab.laj.addWidget(tab.list)

            tab.setLayout(tab.laj)
            self.LIST_OF_TABS[label] = tab


            lista = [{}, {}, {}, {}]
            window_seria_wykr.LIST_OF_GOD[label] = lista

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    """
    @pyqtSlot()
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())
    """
    def load_labels(self):
        labels = []
        for row in self.rows:
            labels.append(row[self.columnlist[1]])
        self.labels = labels

    def load_rows(self):
        numb_r = obverse.get_numb_rows(window_wykr.project, window_wykr.filename) + 1
        rows = []
        for i in range(numb_r):
            row = fs_interaction.read_csv_line(window_wykr.card3.data_path, i)
            rows.append(row)
        self.rows = rows[1::]
        self.row0 = rows[0]

class Window_Seria_Wykr(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("cardschooli wykresy seryjne")
        self.setWindowIcon(QIcon(os.path.join(os.pardir, "img", 'iconka.png')))
        gui.center(self)
        self.resize(800, 600)
        self.liczbapoz = 0
        self.LIST_OF_GOD = {}
        self.names = 0
        self.values = 1
        self.colors = 2
        self.explodings = 3
        self.number_of_layouts = -1
        self.X = 0
        self.Y = 0
    def init_ui(self, columnlist):
        self.loadCOLORS()
        self.columnlist = columnlist

        self.coolWidget = My_Cool_Widget()

        add_btn = QPushButton("ADD", self)
        add_btn.setIcon(QIcon(os.path.join(os.pardir, 'img', 'plusiik.png')))
        add_btn.setGeometry(30, 30, 50, 50)
        add_btn.clicked.connect(self.AddNew)
        add_btn.setToolTip("dodaje element do wykresu")

        OK_btn = QPushButton('Dodaj wykres na karte >>>')
        OK_btn.setGeometry(450, 450, 300, 70)
        # OK_btn.clicked.connect(self.ok_act)

        xSPIN = QSpinBox()
        ySPIN = QSpinBox()
        xSPIN.setRange(0, 9999)
        xSPIN.setValue(self.X)
        ySPIN.setRange(0, 9999)
        ySPIN.setValue(self.Y)

        laj3 = QHBoxLayout()
        laj4 = QHBoxLayout()

        laj3.addWidget(QLabel("X: "))
        laj3.addWidget(xSPIN)
        laj4.addWidget(QLabel("Y: "))
        laj4.addWidget(ySPIN)

        lajout = QVBoxLayout()
        lajout.addWidget(QLabel("WSPÓŁRZĘDNE\n WYKRESU \nNA KARCIE: "))

        lajout.addLayout(laj3)

        lajout.addLayout(laj4)

        layout2 = QVBoxLayout()
        layout2.addWidget(add_btn)
        layout2.addWidget(OK_btn)

        self.layout = QHBoxLayout()
        self.layout.addLayout(layout2)
        self.layout.addWidget(self.coolWidget)
        self.layout.addLayout(lajout)
        self.setLayout(self.layout)
        self.show()

    def deleting(self, number, Cname):
        i = 0
        i2 = self.coolWidget.LIST_OF_TABS[Cname].list.count()
        while i < i2:
            iitem = self.coolWidget.LIST_OF_TABS[Cname].list.item(i)
            if iitem.number == number:
                self.removing(i, Cname)
                self.coolWidget.LIST_OF_TABS[Cname].list.removeItemWidget(iitem)

            i += 1

    def removing(self, numbeer, Cname):
        name = self.LIST_OF_GOD[Cname][self.names].pop(numbeer)

        xd = self.LIST_OF_GOD[Cname][self.values].pop(name)
        xd1 = self.LIST_OF_GOD[Cname][self.colors].pop(name)
        xd2 = self.LIST_OF_GOD[Cname][self.explodings].pop(name)
    def AddNew(self):

        self.liczbapoz += 1
        self.number_of_layouts += 1
        column = choose_colum(self, "wybierz pozycję", "wybierz kolumnę z wartościami na pierwsze pozycje na wykresach",
                              self.coolWidget.row0)
        column_nr = self.columnlist[2].index(column)

        data = []
        for row in self.coolWidget.rows:
            data.append(row[column_nr])

        namess, valuess = [], []
        for dat in data:
            czyprzed = True
            name = ""
            val = ""
            for lit in dat:
                if czyprzed and lit != ":":
                    name += (lit)
                elif not czyprzed and lit != " " and lit != ":":
                    val += (lit)
                elif lit == ":":
                    czyprzed = False
            namess.append(name)
            valuess.append(val)

        if self.coolWidget.czyP:
            listofcolors = self.list_of_colors_P
        else:
            listofcolors = self.list_of_colors

        i = 0

        for thing in self.LIST_OF_GOD:
            if not namess[i] == "":
                if namess[i][0].isalpha():
                    self.LIST_OF_GOD[thing][self.names][self.number_of_layouts] = namess[i]
                    self.LIST_OF_GOD[thing][self.values][namess[i]] = valuess[i]
                    self.LIST_OF_GOD[thing][self.colors][namess[i]] = listofcolors[0]
                    self.LIST_OF_GOD[thing][self.explodings][namess[i]] = 0.0

                    itemek = QListWidgetItem2(imie=thing)
                    name = self.LIST_OF_GOD[thing][self.names][self.number_of_layouts]

                    my_itemek = MyWidget2(name,
                                          self.LIST_OF_GOD[thing][self.values][name],
                                          self.LIST_OF_GOD[thing][self.colors][name],
                                          "deleting.png", self.number_of_layouts, itm=itemek,
                                          maxx=999999999, dok=1)

                    itemek.setSizeHint(my_itemek.sizeHint())

                    self.coolWidget.LIST_OF_TABS[thing].list.addItem(itemek)
                    self.coolWidget.LIST_OF_TABS[thing].list.setItemWidget(itemek, my_itemek)

            i += 1

    def xSPINchange(self, newvalue):
        self.X = self.spin_str_2_float(newvalue)

    def ySPINchange(self, newvalue):
        self.Y = self.spin_str_2_float(newvalue)
    def loadCOLORS(self):
        with open(os.path.join(os.pardir, 'res', 'files', 'colors.txt')) as f:
            self.list_of_colors = f.readlines()
        self.list_of_colors = [x.strip() for x in self.list_of_colors]
        self.list_of_colors[0] = "automatically generated color"

        with open(os.path.join(os.pardir, 'res', 'files', 'colorsPOLISH.txt')) as f:
            self.list_of_colors_P = f.readlines()
        self.list_of_colors_P = [x.strip() for x in self.list_of_colors_P]
        self.list_of_colors_P[0] = "automatycznie generowane koloru"

        self.dict_of_colors = {}
        for i in range(len(self.list_of_colors)):
            self.dict_of_colors[self.list_of_colors_P[i]] = self.list_of_colors[i]


class MyWidget2(QWidget):
    def __init__(self, txt, value, color, image, number, itm=QListWidgetItem2(), maxx=100, dok=2, parent=None):
        super().__init__()

        self.color = color
        self.number = number
        self.value = value
        self.name = txt
        self.itm = itm
        self.itm.changeNUMB(self.number)

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
        try:
            spiinbox.setValue(float(value))
        except:
            QMessageBox().warning(self, '!!! WARTOŚĆ NIENUMERYCZNA !!!',
                                  '!!!   wartość komórki {} w karcie {} jest nienumeryczna    !!!\ \n ustawiono wartość 0 '.format(
                                      self.name, itm.name),
                                  QMessageBox.Ok)
        spiinbox.setDecimals(dok)

        combobox = QComboBox()
        combobox = self.adding_to_combo(combobox)

        spiinbox.valueChanged[str].connect(self.spiin_change)
        combobox.currentIndexChanged[str].connect(self.combo_change)

        layout = QHBoxLayout()

        layout.addWidget(label)
        layout.addWidget(spiinbox)

        layout.addWidget(label3)

        layout.addWidget(combobox)
        layout.addWidget(delt_btn)

        self.setLayout(layout)

    def spiin_change(self, newvalue):
        window_seria_wykr.LIST_OF_GOD[self.itm.name][window_seria_wykr.values][
            self.name] = window_wykr.spin_str_2_float(newvalue)

    def combo_change(self, value):
        window_seria_wykr.LIST_OF_GOD[self.itm.name][window_seria_wykr.colors][self.name] = value


    def delt_btn_act(self):
        window_seria_wykr.deleting(self.number, self.itm.name)

    def adding_to_combo(self, combobox):
        if not window_seria_wykr.coolWidget.czyP:
            List_of_colors = window_seria_wykr.list_of_colors
        else:
            List_of_colors = window_seria_wykr.list_of_colors_P
        combobox.addItems(List_of_colors)
        combobox.setCurrentText(self.color)
        return combobox

def create_window_wykr():
    global window_wykr, window_seria_wykr
    window_wykr = Window_Wykr()
    window_seria_wykr = Window_Seria_Wykr()
