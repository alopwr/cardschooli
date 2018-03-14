# coding=utf-8

import os.path
from random import randrange

import matplotlib.pyplot as plt
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QLabel, \
    QInputDialog, QMessageBox, QListWidget, QVBoxLayout, QListWidgetItem, \
    QHBoxLayout, QDoubleSpinBox, QComboBox, QSpinBox, QTabWidget

import cardschooli.fs_interaction
import cardschooli.gui


class QListWidgetItem2(QListWidgetItem):
    """ my own version of QListWidgetItem """

    def __init__(self, number=0, name=""):
        super().__init__()
        self.number = number
        self.name = name

    def change_numb(self, new_number):
        self.number = new_number

    def give_combo(self, combobox):
        self.combobox = combobox


class MyWidget2(QWidget):
    """a simple position on QListWidgetItem(series of charts version)"""

    def __init__(self, name, value, color, image, number, item=QListWidgetItem2(), max_value=100, accurancy=2):
        super().__init__()
        self.color = color
        self.number = number
        self.value = value
        self.name = name
        self.item = item
        self.item.change_numb(self.number)

        delt_btn = QPushButton()
        delt_btn.setIcon(QIcon(os.path.join(os.pardir, "res", "img", image)))
        delt_btn.setIconSize(QSize(35, 35))
        delt_btn.clicked.connect(self.delt_btn_act)

        label = QLabel(name)
        label2 = QLabel("g")

        spinbox = QDoubleSpinBox()
        spinbox.setMinimum(0.01)
        spinbox.setMaximum(max_value)
        spinbox.setValue(float(value))
        spinbox.setDecimals(accurancy)

        combobox = QComboBox()
        self.combobox = self.adding_to_combo(combobox)

        spinbox.valueChanged[str].connect(self.spin_change)
        self.combobox.currentIndexChanged[str].connect(self.combo_change)

        main_layout = QHBoxLayout()

        main_layout.addWidget(label)
        main_layout.addWidget(spinbox)

        main_layout.addWidget(label2)

        main_layout.addWidget(self.combobox)
        main_layout.addWidget(delt_btn)

        self.setLayout(main_layout)

    def spin_change(self, value):
        window_seria_wykr.LIST_OF_GOD[self.item.name][window_seria_wykr.values][
            self.name] = window_wykr.spin_str_2_float(value)

    def combo_change(self, newvalue):
        for thing in window_seria_wykr.LIST_OF_GOD:
            colors = window_seria_wykr.LIST_OF_GOD[thing][window_seria_wykr.colors]
            for name in colors:
                if name == self.name:
                    window_seria_wykr.LIST_OF_GOD[thing][window_seria_wykr.colors][name] = newvalue

                    i = 0
                    i2 = window_seria_wykr.coolWidget.LIST_OF_TABS[thing].QLIST.count()
                    while i < i2:
                        item = window_seria_wykr.coolWidget.LIST_OF_TABS[thing].QLIST.item(i)
                        if item.number == self.number:
                            window_seria_wykr.coolWidget.LIST_OF_TABS[thing].QLIST.item(i).combobox.setCurrentText(
                                newvalue)

                        i += 1

    def delt_btn_act(self):
        window_seria_wykr.deleting(self.number, self.item.name)

    def adding_to_combo(self, combobox):
        if not window_seria_wykr.coolWidget.is_polish_names:
            list_of_colors = window_seria_wykr.list_of_colors
        else:
            list_of_colors = window_seria_wykr.list_of_colors_P
        combobox.addItems(list_of_colors)
        combobox.setCurrentText(self.color)
        return combobox


class MyWidget(QWidget):
    """a simple position on QListWidgetItem"""

    def __init__(self, name, value, color, image, number, item=QListWidgetItem2(), max_value=100, accurancy=2,
                 parent=None):
        super(MyWidget, self).__init__(parent)

        self.color = color
        self.number = number
        self.value = value
        self.name = name
        item.change_numb(self.number)

        delt_btn = QPushButton()
        delt_btn.setIcon(QIcon(os.path.join(os.pardir, "res", "img", image)))
        delt_btn.setIconSize(QSize(35, 35))
        delt_btn.resize(10, 10)
        delt_btn.clicked.connect(self.delt_btn_act)

        label = QLabel(name)
        label_percnt = QLabel(" % ")
        label_grams = QLabel("g")
        spinbox = QDoubleSpinBox()
        spinbox.setMinimum(0.01)
        spinbox.setMaximum(max_value)
        spinbox.setValue(value)
        spinbox.setDecimals(accurancy)

        combobox = QComboBox()
        combobox = self.adding_to_combo(combobox)

        spinbox.valueChanged[str].connect(self.spin_change)

        combobox.currentIndexChanged[str].connect(self.combo_change)

        layout = QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(spinbox)

        if window_wykr.is_percent:
            layout.addWidget(label_percnt)
        else:
            layout.addWidget(label_grams)

        layout.addWidget(combobox)
        layout.addWidget(delt_btn)

        self.setLayout(layout)

    def spin_change(self, newvalue):

        newvalue = window_wykr.spin_str_2_float(newvalue)
        if window_wykr.is_percent:
            oldvalue = window_wykr.LIST_OF_GOD[window_wykr.values][self.name]
            if not window_wykr.maxim - (newvalue - oldvalue) >= 0:
                QMessageBox().warning(self, "!!! LIMIT !!!",
                                      "!!!       Przekroczono sumę 100 %      !!! \n zmniejsz procenty innego elementu",
                                      QMessageBox.Ok)
                window_wykr.maxim += (oldvalue - newvalue)

        window_wykr.LIST_OF_GOD[window_wykr.values][self.name] = newvalue

    def combo_change(self, value):
        window_wykr.LIST_OF_GOD[window_wykr.colors][self.name] = value

    def delt_btn_act(self):
        window_wykr.deleting(self.number)

    def adding_to_combo(self, combobox):
        if not window_wykr.is_polish_names:
            list_of_colors = window_wykr.list_of_colors
        else:
            list_of_colors = window_wykr.list_of_colors_P
        combobox.addItems(list_of_colors)
        combobox.setCurrentText(self.color)
        return combobox


class ChartsWindow(QWidget):
    """
    user can create, customize and add chart to the card
    """

    def __init__(self):
        super().__init__()
        self.is_polish_names = False
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
        self.is_percent = False
        self.project = ""
        self.filename = ""

        self.setWindowIcon(QIcon(os.path.join(os.pardir, "res", "img", "icon.png")))
        self.resize(800, 600)
        self.setWindowTitle("cardschooli - dodaj wykres")
        cardschooli.gui.center(self)

        self.load_colors()

        add_btn = QPushButton("ADD", self)
        add_btn.setIcon(QIcon(os.path.join(os.pardir, "res", "img", "plusik.png")))
        add_btn.clicked.connect(self.add_new)
        add_btn.setToolTip("dodaje element do wykresu")
        add_btn.setStyleSheet("background-color: mediumSeaGreen")

        self.QLIST = QListWidget()
        self.QLIST.setToolTip("pozycje na wykresie")

        x_spin = QSpinBox()
        y_spin = QSpinBox()
        x_spin.setRange(0, 9999)
        x_spin.setValue(self.X)
        y_spin.setRange(0, 9999)
        y_spin.setValue(self.Y)
        x_spin.valueChanged[str].connect(self.x_spin_change)
        y_spin.valueChanged[str].connect(self.y_spin_change)

        OK_btn = QPushButton("Dodaj wykres na karte >>>")
        OK_btn.clicked.connect(self.ok_act)
        OK_btn.setStyleSheet("background-color: gold")

        self.main_layout = QVBoxLayout()
        layout1 = QHBoxLayout()
        layout3 = QHBoxLayout()
        layout4 = QHBoxLayout()
        layout2 = QVBoxLayout()
        layout2.addWidget(QLabel("WSPÓŁRZĘDNE\n WYKRESU \nNA KARCIE: "))
        layout2.addLayout(layout3)
        layout2.addLayout(layout4)
        layout1.addWidget(add_btn)
        layout1.addWidget(self.QLIST)
        layout1.addLayout(layout2)
        self.main_layout.addLayout(layout1)
        self.main_layout.addWidget(OK_btn)
        layout3.addWidget(QLabel("X: "))
        layout3.addWidget(x_spin)
        layout4.addWidget(QLabel("Y: "))
        layout4.addWidget(y_spin)

    def init_ui(self):
        ask_for_polish_names()
        self.QLIST.clear()
        self.LIST_OF_GOD = [{}, {}, {}, {}]
        self.setLayout(self.main_layout)
        self.show()

    def closeEvent(self, QCloseEvent):
        self.isCreatingChart = False
        QCloseEvent.accept()

    def give_project(self, prjct):
        self.project = prjct

    def change_is_polish_names(self, new):
        self.is_polish_names = new

    def spin_str_2_float(self, newvalues):
        new_value = ""
        for l in newvalues:
            if l == ",":
                new_value += "."
            else:
                new_value += l
        new_value = float(new_value)
        return new_value

    def x_spin_change(self, newvalue):
        self.X = int(window_wykr.spin_str_2_float(newvalue))

    def y_spin_change(self, newvalue):
        self.Y = int(window_wykr.spin_str_2_float(newvalue))

    def deleting(self, number):
        i = 0
        i2 = self.QLIST.count()
        while i < i2:
            item = self.QLIST.item(i)
            if item.number == number:
                self.QLIST.removeItemWidget(item)
                self.removing(i)

            i += 1

    def removing(self, number):
        name = self.LIST_OF_GOD[self.names].pop(number)

        remov_val = self.LIST_OF_GOD[self.values].pop(name)
        self.LIST_OF_GOD[self.colors].pop(name)
        self.LIST_OF_GOD[self.explodings].pop(name)
        if self.is_percent:
            self.maxim += float(remov_val)

    def adding_chart(self):
        self.window3.card.adding_chart("wykres.png", (self.X, self.Y), self.project)
        self.window3.update_preview()

    def ok_act(self):
        if len(self.LIST_OF_GOD[0]) > 0 and self.suma() == 100.0:
            size = self.get_size()
            if not size:
                return None
            if self.is_polish_names:
                self.exchange_colors_name()

            self.generating_chart(self.LIST_OF_GOD, size)
            self.adding_chart()

            self.isCreatingChart = False
            self.close()
        elif len(self.LIST_OF_GOD[0]) == 0:
            QMessageBox().warning(self, "!!! PUSTO !!!",
                                  "!!!        nie możesz dodać pustego wykresu        !!!", QMessageBox.Ok)
        elif self.suma() > 100.0:
            QMessageBox().warning(self, "!!! LIMIT !!!",
                                  "!!!       Przekroczono sumę 100 %      !!! \n",
                                  QMessageBox.Ok)
        else:
            if self.is_percent:
                QMessageBox().warning(self, "!!! ZA MAŁO !!!",
                                      "!!!       brakuje do sumy 100%      !!! \n",
                                      QMessageBox.Ok)

    def exchange_colors_name(self):
        for name in self.LIST_OF_GOD[self.colors]:
            color = self.LIST_OF_GOD[self.colors][name]
            self.LIST_OF_GOD[self.colors][name] = self.dict_of_colors[color]

    def return_maxim(self):
        if self.is_percent:
            return self.maxim
        else:
            return 999

    def add_new(self):
        if self.return_maxim() > 0:
            name = self.get_text()
            value = self.get_value()
            if not value:
                return None
            color = self.get_color()
            if not color:
                return None

            itemek = QListWidgetItem2()
            self.number_of_layouts += 1

            if self.is_percent:
                my_itemek = MyWidget(name, value, color, "deleting.png", self.number_of_layouts, item=itemek,
                                     accurancy=2)
            else:
                my_itemek = MyWidget(name, value, color, "deleting.png", self.number_of_layouts, item=itemek,
                                     max_value=999999999, accurancy=1)
            itemek.setSizeHint(my_itemek.sizeHint())

            self.QLIST.addItem(itemek)
            self.QLIST.setItemWidget(itemek, my_itemek)

            self.LIST_OF_GOD[self.names][self.number_of_layouts] = name
            self.LIST_OF_GOD[self.values][name] = value
            self.LIST_OF_GOD[self.colors][name] = color
            self.LIST_OF_GOD[self.explodings][name] = 0

            if self.is_percent:
                self.maxim -= value

        else:
            QMessageBox().warning(self, "!!! LIMIT !!!",
                                  "!!!       wykorzystano sumę 100 %      !!! \n możesz zmiejszyć procent innego elementu",
                                  QMessageBox.Ok)

    def get_value(self):
        if self.is_percent:
            i, ok_pressed = QInputDialog.getDouble(self, "Podaj wartość",
                                                   "Podaj wartość elementu na wykresie (%) : ", 1, 0.1, 100, 2)

            if ok_pressed and self.maxim - i >= 0:
                return i
            elif self.maxim - i < 0:
                QMessageBox().warning(self, "!!! LIMIT !!!",
                                      "!!!       Przekroczono sumę 100 %      !!! \n spróbuj ponownie",
                                      QMessageBox.Ok)
                self.get_value()

            return i
        else:
            i, ok_pressed = QInputDialog.getDouble(self, "Podaj wartość",
                                                   "Podaj wartość elementu na wykresie (q) : ", 1, 1, 999999999, 1)
            if ok_pressed:
                return i

    def get_size(self):
        i, ok_pressed0 = QInputDialog.getInt(self, "SZEROKOŚĆ",
                                             "Podaj szerokość diagramu. \n(piksele)", 500,
                                             min=1)
        if not ok_pressed0:
            return False
        j, ok_pressed1 = QInputDialog.getInt(self, "WYSOKOŚĆ",
                                             "Podaj wysokość diagramu \n(piksele)\n Anuluj by stworzyć kwadrat", i,
                                             min=1)
        if not ok_pressed1:
            j = i

        return [i, j]

    def get_text(self):
        text, okPressed = QInputDialog.getText(self, "Podaj nazwę elementu", "NAZWA:", QLineEdit.Normal, "")

        if okPressed and (text != "" or text != " " or text != None):
            return text
        else:
            QMessageBox().warning(self, "!!! PUSTE !!!",
                                  "!!!       Wypełnij nazwę      !!! \n ",
                                  QMessageBox.Ok)
            self.get_text()

    def load_colors(self):
        with open(os.path.join(os.pardir, "res", "files", "colors.txt")) as f:
            self.list_of_colors = f.readlines()
        self.list_of_colors = [x.strip() for x in self.list_of_colors]

        with open(os.path.join(os.pardir, "res", "files", "colorsPOLISH.txt")) as f:
            self.list_of_colors_P = f.readlines()
        self.list_of_colors_P = [x.strip() for x in self.list_of_colors_P]

        self.dict_of_colors = {}
        for i in range(len(self.list_of_colors)):
            self.dict_of_colors[self.list_of_colors_P[i]] = self.list_of_colors[i]

    def suma(self):

        if self.is_percent:
            summ = 0

            for i in self.LIST_OF_GOD[self.values].values():
                summ += i

            return summ

        else:
            return 100.0

    def get_color(self):
        if not self.is_polish_names:
            self.List_of_colors = self.list_of_colors
        else:
            self.List_of_colors = self.list_of_colors_P

        item, okPressed = QInputDialog.getItem(self, "wybierz kolor", "KOLOR ELEMENTU NA WYKRESIE: ",
                                               self.List_of_colors, 0, False)
        if okPressed and item:
            return item

    def calculate_the_legends_size(self, names):
        dlugosci = []
        for name in names:
            dlugosci.append(len(name))
        dl = max(dlugosci)
        dl2 = (dl * 0.1 + 0.5)
        wys = len(names)
        wys2 = (wys * 0.25) + 0.11
        return dl2, wys2

    def dynamic_font(self, texts, size):

        new_texts = []
        if size[0] >= 300 or size[1] >= 300:
            for txt in texts:
                txt.set_fontsize(8)
                new_texts.append(txt)
        elif size[0] >= 100 or size[1] >= 100:
            for txt in texts:
                txt.set_fontsize(4)
                new_texts.append(txt)
        elif size[0] < 40 or size[1] < 40:
            for txt in texts:
                txt.set_fontsize(1)
                new_texts.append(txt)
        elif size[0] < 10 or size[1] < 10:
            for txt in texts:
                txt.set_fontsize(0.6)
                new_texts.append(txt)
        else:
            for txt in texts:
                txt.set_fontsize(2)
                new_texts.append(txt)

        return new_texts

    def generating_chart(self, LIST_OF_GOD, size):
        dpi = 600
        if not self.is_percent:
            names = []
            for name in LIST_OF_GOD[0].values():  # names = 0
                names.append(name)

            labels = []
            for name in LIST_OF_GOD[1].values():  # values = 1
                if int(name) == name:
                    labels.append((str(name)[:(len(str(name)) - 2)] + " g"))
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
            plt.figure(figsize=(size[0] / dpi, size[1] / dpi))
            patches, texts = plt.pie(sizes, labels=labels, shadow=False, startangle=90, colors=colors,
                                     labeldistance=0.5)

            texts = self.dynamic_font(texts, size)
            plt.axis("equal")
            plt.savefig(cardschooli.fs_interaction.project_location(window_wykr.project, "wykres.png"), dpi=dpi,
                        transparent=True)
            x, y = self.calculate_the_legends_size(names)
            figlegend = plt.figure(figsize=(x, y))
            figlegend.legend(patches, names)
            figlegend.savefig(cardschooli.fs_interaction.project_location(window_wykr.project, "legend2.png"), dpi=600)

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

            plt.figure(figsize=(size[0] / dpi, size[1] / dpi))
            plt.pie(sizes, explode=explode, colors=colors, labels=labels,
                    autopct="%1.1f%%", shadow=False, startangle=140)
            plt.axis("equal")
            plt.savefig(cardschooli.fs_interaction.project_location(window_wykr.project, "wykres.png", ), dpi=600,
                        transparent=True)


class SerialChartsWindow(QWidget):
    """
    user can create, customize and add series of charts
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("cardschooli - dodaj wykresy seryjne")
        self.setWindowIcon(QIcon(os.path.join(os.pardir, "res", "img", "icon.png")))
        cardschooli.gui.center(self)
        self.resize(800, 600)
        self.names = 0
        self.values = 1
        self.colors = 2
        self.explodings = 3
        self.isCreatingChart = False
        self.load_colors()
        self.LIST_OF_GOD = {}
        self.X = 0
        self.Y = 0
        self.number_of_layouts = -1
        self.LEGEND_NAME_BASE = []
        self.LEGEND_PATCHES_BASE = []

    def init_ui(self, columnlist):
        self.isCreatingChart = True
        self.columnlist = columnlist
        self.load_ui()
        self.show()

    def load_ui(self):

        add_btn = QPushButton("ADD", self)
        add_btn.setIcon(QIcon(os.path.join(os.pardir, "res", "img", "plusik.png")))
        add_btn.clicked.connect(self.add_new)
        add_btn.setToolTip("dodaje element do wykresu")
        add_btn.setStyleSheet("background-color: mediumSeaGreen")

        OK_btn = QPushButton("Dodaj wykres na kartę >>>")
        OK_btn.clicked.connect(self.ok_act)
        OK_btn.setStyleSheet("background-color: gold")

        x_spin = QSpinBox()
        y_spin = QSpinBox()
        x_spin.setRange(0, 9999)
        x_spin.setValue(self.X)
        y_spin.setRange(0, 9999)
        y_spin.setValue(self.Y)
        x_spin.valueChanged[str].connect(self.x_spin_change)
        y_spin.valueChanged[str].connect(self.y_spin_change)

        layout3 = QHBoxLayout()
        layout4 = QHBoxLayout()

        layout3.addWidget(QLabel("X: "))
        layout3.addWidget(x_spin)
        layout4.addWidget(QLabel("Y: "))
        layout4.addWidget(y_spin)

        layout2 = QVBoxLayout()
        layout2.addWidget(QLabel("WSPÓŁRZĘDNE\n WYKRESU \nNA KARCIE: "))

        layout2.addLayout(layout3)

        layout2.addLayout(layout4)
        self.coolWidget = ChartControlWidget()
        layout = QHBoxLayout()
        layout.addWidget(add_btn)
        layout.addWidget(self.coolWidget)
        layout.addLayout(layout2)

        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(layout)
        self.main_layout.addWidget(OK_btn)
        self.setLayout(self.main_layout)

    def deleting(self, number, thing_name):
        i = 0
        i2 = self.coolWidget.LIST_OF_TABS[thing_name].QLIST.count()
        while i < i2:
            item = self.coolWidget.LIST_OF_TABS[thing_name].QLIST.item(i)
            if item.number == number:
                self.removing(i, thing_name)
                self.coolWidget.LIST_OF_TABS[thing_name].QLIST.removeItemWidget(item)

            i += 1

    def closeEvent(self, QCloseEvent):
        self.isCreatingChart = False
        QCloseEvent.accept()

    def removing(self, number, thing_name):
        name = self.LIST_OF_GOD[thing_name][self.names].pop(number)

        remov_val = self.LIST_OF_GOD[thing_name][self.values].pop(name)
        remov_val = self.LIST_OF_GOD[thing_name][self.colors].pop(name)
        remov_val = self.LIST_OF_GOD[thing_name][self.explodings].pop(name)

    def calculate_the_legends_size(self, names):
        dlugosci = []
        for name in names:
            dlugosci.append(len(name))
        dlug = max(dlugosci)
        dlug2 = (dlug * 0.1 + 0.5)
        wys = len(names)
        wys2 = (wys * 0.25) + 0.11
        return (dlug2, wys2)

    def dynamic_font(self, texts, size):
        new_texts = []
        if size[0] >= 300 or size[1] >= 300:
            for txt in texts:
                txt.set_fontsize(8)
                new_texts.append(txt)
        elif size[0] >= 100 or size[1] >= 100:
            for txt in texts:
                txt.set_fontsize(4)
                new_texts.append(txt)
        elif size[0] < 40 or size[1] < 40:
            for txt in texts:
                txt.set_fontsize(1)
                new_texts.append(txt)
        elif size[0] < 10 or size[1] < 10:
            for txt in texts:
                txt.set_fontsize(0.6)
                new_texts.append(txt)
        else:
            for txt in texts:
                txt.set_fontsize(2)
                new_texts.append(txt)

        return new_texts

    def generating_legend(self):
        x, y = self.calculate_the_legends_size(self.LEGEND_NAME_BASE)
        figlegend = plt.figure(figsize=(x, y))
        figlegend.legend(self.LEGEND_PATCHES_BASE, self.LEGEND_NAME_BASE)
        figlegend.savefig(cardschooli.fs_interaction.project_location(window_wykr.project, "legend.png"), dpi=600,
                          transparent=True)

    def generating_chart(self, master_list):
        LIST_OF_GOD, size, thing = master_list
        names = []
        for name in LIST_OF_GOD[0].values():  # names = 0
            names.append(name)

        labels = []
        for name in LIST_OF_GOD[1].values():  # values = 1
            if name != 0.0:
                if int(name) == name:
                    labels.append((str(name)[:(len(str(name)) - 2)] + " g"))
                else:
                    labels.append((str(name) + " g"))

        sizes = []
        for value in LIST_OF_GOD[1].values():  # values = 1
            sizes.append(value)

        colors = []
        for color in LIST_OF_GOD[2].values():
            colors.append(color)

        explode = []
        for expld in LIST_OF_GOD[3].values():  # explode = 3
            explode.append(expld)

        dpi = 600

        plt.figure(figsize=(size[0] / dpi, size[1] / dpi))
        patches, texts = plt.pie(sizes, labels=labels, shadow=False, startangle=90, colors=colors,
                                 labeldistance=0.5)

        texts = self.dynamic_font(texts, size)
        plt.axis("equal")
        plt.savefig(cardschooli.fs_interaction.project_location(window_wykr.project,
                                                                "{}_wykres.png".format(str(thing).strip())),
                    dpi=dpi, transparent=True)

        self.legend_base_update(names, patches)
        plt.close()

    def legend_base_update(self, texts, patches):
        i = 0
        for text in texts:
            if text not in self.LEGEND_NAME_BASE:
                self.LEGEND_NAME_BASE.append(text)
                self.LEGEND_PATCHES_BASE.append(patches[i])
            i += 1

    def exchange_colors_name(self):
        for thing in self.LIST_OF_GOD:
            for name in self.LIST_OF_GOD[thing][self.colors]:
                color = self.LIST_OF_GOD[thing][self.colors][name]
                self.LIST_OF_GOD[thing][self.colors][name] = self.dict_of_colors[color]

    def add_new(self):
        column = choose_colum(self, "Wybierz pozycję", "Wybierz kolumnę z wartościami na pozycję na wykresach",
                              self.coolWidget.headers)
        try:
            column_nr = self.columnlist[2].index(column)
        except ValueError:
            return None
        self.number_of_layouts += 1

        data = []
        for row in self.coolWidget.rows[1::]:
            data.append(row[column_nr])

        namess, values = [], []
        i = 0
        skip = False
        for dat in data:
            if dat.strip() != "":
                namess.append(column)
                try:
                    values.append(float(dat.strip()))
                except ValueError:
                    if not skip:
                        msg = QMessageBox()
                        msg.setWindowIcon(QIcon(os.path.join(os.pardir, "res", "img", "icon.png")))
                        msg.setWindowTitle("WARTOŚĆ NIENUMERYCZNA!!!")
                        msg.setText("Na karcie {} wartość {} jest nienumeryczna! \n Ustawiono na 0.0.".format(self.coolWidget.labels[i], namess[len(namess) - 1]))
                        msg.addButton(QMessageBox.Ok)
                        msg.setIcon(QMessageBox.Warning)
                        msg.addButton("OK (DLA WSZYTSKICH)",QMessageBox.YesRole)
                        returned = msg.exec_()
                        print(returned)
                        if returned == 0: # Ich don`t know why but it is 0 (printing test)
                            skip = True
                    values.append(0.0)
            else:
                namess.append("")
                values.append(0.0)
            i += 1

        if self.coolWidget.is_polish_names:
            listofcolors = self.list_of_colors_P
        else:
            listofcolors = self.list_of_colors

        i = 0
        for thing in self.LIST_OF_GOD:
            if not namess[i] == "":
                self.LIST_OF_GOD[thing][self.names][self.number_of_layouts] = namess[i]
                self.LIST_OF_GOD[thing][self.values][namess[i]] = values[i]
                self.LIST_OF_GOD[thing][self.colors][namess[i]] = listofcolors[0]
                self.LIST_OF_GOD[thing][self.explodings][namess[i]] = 0.0

                itemek = QListWidgetItem2(name=thing)
                name = self.LIST_OF_GOD[thing][self.names][self.number_of_layouts]

                my_itemek = MyWidget2(name,
                                      self.LIST_OF_GOD[thing][self.values][name],
                                      self.LIST_OF_GOD[thing][self.colors][name],
                                      "deleting.png", self.number_of_layouts, item=itemek,
                                      max_value=999999999, accurancy=1)

                itemek.setSizeHint(my_itemek.sizeHint())

                itemek.give_combo(my_itemek.combobox)

                self.coolWidget.LIST_OF_TABS[thing].QLIST.addItem(itemek)
                self.coolWidget.LIST_OF_TABS[thing].QLIST.setItemWidget(itemek, my_itemek)
            i += 1

    def is_empty(self):
        puste = []
        for thing in self.LIST_OF_GOD:
            dlug = len(self.LIST_OF_GOD[thing][self.values])
            if dlug == 0:
                puste.append(thing)
        if len(puste) > 0:
            return True, puste
        else:
            return False, puste

    def colors_random(self):
        list_of_colors = self.list_of_colors
        czarna_lista = []
        dzienniczek_kolorkow = {}
        for thing in self.LIST_OF_GOD:

            for colorKey in self.LIST_OF_GOD[thing][self.colors]:
                if self.LIST_OF_GOD[thing][self.colors][colorKey] == "automatically generated color":
                    if colorKey not in czarna_lista:
                        numb = randrange(1, len(self.list_of_colors))
                        self.LIST_OF_GOD[thing][self.colors][colorKey] = list_of_colors[numb]
                        czarna_lista.append(colorKey)
                        dzienniczek_kolorkow[colorKey] = list_of_colors[numb]
                        xd = list_of_colors.pop(numb)
                    else:
                        self.LIST_OF_GOD[thing][self.colors][colorKey] = dzienniczek_kolorkow[colorKey]

    def ok_act(self):
        self.master_generator_dict = {}
        returned_from_isempty = self.is_empty()
        isempty = returned_from_isempty[0]
        if not isempty:
            size = self.get_size()
            if not size:
                return None
            if self.coolWidget.is_polish_names:
                self.exchange_colors_name()

            self.colors_random()
            for thing in self.LIST_OF_GOD:
                if len(self.LIST_OF_GOD[thing][self.names]) > 0:
                    lista = self.LIST_OF_GOD[thing]
                    self.master_generator_dict[thing.strip()] = (lista, size, thing)
            window_wykr.window3.card.add_series_of_charts(self.columnlist[1], (self.X, self.Y), window_wykr.project,
                                                          first=True)
            window_wykr.window3.update_preview()
            self.isCreatingChart = False
            self.close()
        else:
            names = ""
            i = 0
            for empty in returned_from_isempty[1]:

                if i == 0 and len(returned_from_isempty[1]) == 1:
                    names += str(empty)

                elif i != len(returned_from_isempty[1]) - 1:
                    names += empty
                    names += ", "
                i += 1
            QMessageBox().warning(self, "!!! PUSTO !!!",
                                  "!!!        nie możesz dodać pustego wykresu        !!!\n wykres {} nie ma żadnych pozycji".format(
                                      names), QMessageBox.Ok)

    def x_spin_change(self, newvalue):
        self.X = int(window_wykr.spin_str_2_float(newvalue))

    def y_spin_change(self, newvalue):
        self.Y = int(window_wykr.spin_str_2_float(newvalue))

    def get_size(self):
        i, ok_pressed0 = QInputDialog.getInt(self, "SZEROKOŚĆ",
                                             "Podaj szerokość diagramu. \n(piksele)", 500,
                                             min=1)
        if not ok_pressed0:
            return False
        j, ok_pressed1 = QInputDialog.getInt(self, "WYSOKOŚĆ",
                                             "Podaj wysokość diagramu \n(piksele)\n Anuluj by stworzyć kwadrat", i,
                                             min=1)
        if not ok_pressed1:
            j = i

        return [i, j]

    def load_colors(self):
        with open(os.path.join(os.pardir, "res", "files", "colors.txt")) as f:
            self.list_of_colors = f.readlines()
        self.list_of_colors = [x.strip() for x in self.list_of_colors]
        self.list_of_colors[0] = "automatically generated color"

        with open(os.path.join(os.pardir, "res", "files", "colorsPOLISH.txt")) as f:
            self.list_of_colors_P = f.readlines()
        self.list_of_colors_P = [x.strip() for x in self.list_of_colors_P]
        self.list_of_colors_P[0] = "automatycznie generowane koloru"

        self.dict_of_colors = {}
        for i in range(len(self.list_of_colors)):
            self.dict_of_colors[self.list_of_colors_P[i]] = self.list_of_colors[i]


class ChartControlWidget(QWidget):
    """
    class to managment of tabs
    """

    def __init__(self):
        super().__init__()
        self.is_polish_names = False
        self.columnlist = window_seria_wykr.columnlist
        self.rows = cardschooli.fs_interaction.read_csv(window_wykr.window3.card.data_path)
        self.headers = self.rows[0]
        self.labels = [i[0] for i in self.rows[1:]]
        self.LIST_OF_TABS = {}
        main_layout = QVBoxLayout()

        self.tabs = QTabWidget()

        for label in self.labels:
            tab = QWidget()
            self.tabs.addTab(tab, label)

            tab.layout = QVBoxLayout()

            tab.QLIST = QListWidget()
            tab.layout.addWidget(tab.QLIST)

            tab.setLayout(tab.layout)
            self.LIST_OF_TABS[label] = tab

            lista = [{}, {}, {}, {}]
            window_seria_wykr.LIST_OF_GOD[label] = lista

        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)


class Question(QMessageBox):
    """asking for language of colors window"""

    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon(os.path.join(os.pardir, "res", "img", "icon.png")))
        cardschooli.gui.center(self)
        buttonReply = QMessageBox.question(self, "language",
                                           "Czy przedłumaczyć nazwy kolorów na polski? (słabe tłumaczenie)",
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.Yes:
            window_wykr.change_is_polish_names(True)
        else:
            window_wykr.change_is_polish_names(False)
        self.show()


def ask_for_polish_names():
    """create a asking window"""
    question1 = Question()


def choose_colum(parent, caption, text, selections):
    "ask for column"
    response = QInputDialog.getItem(parent, caption, text, selections)
    if response[1]:
        return response[0]


def create_window_wykr():
    """creating a charts window"""
    global window_wykr
    window_wykr = ChartsWindow()


def create_window_seria_wykr():
    """creating a series of charts window"""
    global window_seria_wykr
    window_seria_wykr = SerialChartsWindow()
