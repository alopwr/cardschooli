import os.path

from PIL import Image
from PyQt5.QtCore import QObject, QPointF, QPropertyAnimation, pyqtProperty
from PyQt5.QtGui import QPainter, QPixmap, QMovie, QIcon
from PyQt5.QtWidgets import QWidget, QGraphicsView, QGraphicsPixmapItem, QGraphicsScene, QLabel, QPushButton

import cardschooli.fs_interaction

CZY_BOOM_MENU = True

def make_transparent(name):
    img = Image.open(os.path.join(os.pardir, "res", "img", name))
    new_img = img.convert("RGBA")
    datas = new_img.getdata()
    newData = []
    for item in datas:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)
    new_img.putdata(newData)
    new_img.save(os.path.join(os.pardir, "res", "img", name[:len(name) - 4] + "_new.png"), "png")


class ElementOfAnimation(QObject):

    def __init__(self, name):
        super().__init__()
        item = QPixmap(name)
        self.name = name
        self.pixmap_item = QGraphicsPixmapItem(item)

        self.width = item.width()
        self.height = item.height()

    def _set_pos(self, pos):
        self.pixmap_item.setPos(pos)

    pos = pyqtProperty(QPointF, fset=_set_pos)


class BoomWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon(os.path.join(os.pardir, "res", "img", "icon.png")))
        self.setFixedSize(550, 400)
        self.setWindowTitle("WELCOME in CARDCHOOLI")
        self.time = 0
        self.window_label = QLabel(self)
        self.movie = QMovie(os.path.join(os.pardir, "res", "img", "bomb.gif"))
        self.movie.updated.connect(self.update)
        self.window_label.setMovie(self.movie)
        self.window0 = None

    def init_ui(self):
        self.movie.start()
        self.show()

    def update(self):
        self.time += 0.1
        if self.time > 6:
            self.movie.stop()
            self.close()
            boom_menu.init_ui()


class BoomMenu(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.width = 800
        self.height = 600

    def init_ui(self):
        self.setWindowTitle("WELCOME in CARDSCHOOLI")
        self.setWindowIcon(QIcon(os.path.join(os.pardir, "res", "img", "icon.png")))
        make_transparent("napistest.png")
        self.load()
        self.animation()

    def update(self):
        time = self.anim.currentLoopTime()
        if time == self.anim.duration():
            self.button.show()
            self.movie2.start()
            self.movie.start()
            self.fire_movie.start()
            title = QPixmap(self.title_thing.name)
            self.title_window = QLabel(self)
            self.title_window.setPixmap(title)
            self.title_window.setGeometry((self.width - self.title_thing.width) // 2,
                                          (self.height - self.title_thing.height) // 4,
                                          self.title_thing.width, self.title_thing.height)
            self.title_window.show()

    def animation(self):
        self.title_thing = ElementOfAnimation(os.path.join(os.pardir, "res", "img", "napistest_new.png"))
        self.anim = QPropertyAnimation(self.title_thing, b'pos')
        self.anim.setDuration(1500)
        self.anim.setStartValue(QPointF(-(self.title_thing.width), self.height // 2))
        self.anim.setEndValue(QPointF((self.width - self.title_thing.width) // 2,
                                      (self.height - self.title_thing.height) // 4))
        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, self.width - 10, self.height - 10)
        self.scene.addItem(self.title_thing.pixmap_item)
        self.setScene(self.scene)
        self.setRenderHint(QPainter.Antialiasing)
        self.setFixedSize(self.width, self.height)
        self.anim.valueChanged.connect(self.update)
        self.anim.start()

        self.show()

    def load(self):
        self.movie_label = QLabel(self)
        self.movie = QMovie(os.path.join(os.pardir, "res", "img", "background.gif"))
        bck_width = self.width // 2
        self.movie_label.setGeometry((self.width - bck_width) // 2, 0, bck_width, self.height // 4 * 3)
        self.movie_label.setMovie(self.movie)

        self.button = QPushButton("START", self)
        self.button.clicked.connect(self.next)
        self.button.setStyleSheet("background-color: gold")
        b_width = self.button.size().width() * 3
        b_height = self.button.size().height() * 3

        coords = ((self.width - b_width) // 2, (self.height - b_height) // 16 * 15)
        self.button.setGeometry(coords[0], coords[1], b_width, b_height)
        self.button.hide()

        self.movie_label2 = QLabel(self)
        self.movie2 = QMovie(os.path.join(os.pardir, "res", "img", "palcuch.gif"))
        self.movie_label2.setGeometry(coords[0] - 160 - 20, coords[1], 160, 100)
        self.movie_label2.setMovie(self.movie2)

        self.firework_label = QLabel(self)
        self.firework_label2 = QLabel(self)
        self.fire_movie = QMovie(os.path.join(os.pardir, "res", "img", "fireworks_smaller.gif"))
        self.firework_label.setGeometry(0, 0, 200, 240)
        self.firework_label2.setGeometry(self.width - 200, 0, 200, 240)
        self.firework_label.setMovie(self.fire_movie)
        self.firework_label2.setMovie(self.fire_movie)

    def closeEvent(self, QCloseEvent):
        cardschooli.fs_interaction.clean_files2(os.path.join(os.pardir, "res", "img"))
        QCloseEvent.accept()

    def next(self):
        self.close()
        boom_window.window0.show()
        cardschooli.fs_interaction.clean_files2(os.path.join(os.pardir, "res", "img"))


def create_windows():
    #make_transparent("done.png")
    if  CZY_BOOM_MENU:
        global boom_menu, boom_window
        boom_menu = BoomMenu()
        boom_window = BoomWindow()
