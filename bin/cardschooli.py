import sys

from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QPushButton, QLineEdit, QLabel, QFileDialog


class Window0(QWidget):

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
        start_btn.clicked.connect(self.next)

    def next(self):
        self.project = self.project_name.text()
        print(self.project)
        self.close()
        window1.init_ui()


class Window1(QWidget):

    def __init__(self):
        super().__init__()

    def init_ui(self):
        self.setWindowTitle('cardschooli - krok 1')
        self.resize(800, 600)
        center(self)
        QLabel(
            'Wybierz plik *.csv z danymi do projektu {}. Dane zostaną skopiowane, plik nie zostanie naruszony.'.format(
                window0.project), self)
        open_btn = QPushButton('Otwórz plik', self)
        open_btn.clicked.connect(self.open_file)
        self.show()

    def open_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getOpenFileName(self, "Wybierz swój plik z danymi:", "",
                                                  "dane do cardschooli (*.csv)", options=options)
        self.filename = filename
        self.next()

    def next(self):
        print(self.filename)
        self.close()


def center(window):
    qr = window.frameGeometry()
    qr.moveCenter(QDesktopWidget().availableGeometry().center())
    window.move(qr.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window0 = Window0()
    window1 = Window1()
    sys.exit(app.exec_())
