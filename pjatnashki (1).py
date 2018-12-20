from PyQt5.QtWidgets import QApplication, QAction, QPushButton, QMainWindow, QMenu, QMenuBar
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QRect
from random import shuffle
import sys


class Application(QMainWindow):
    def __init__(self, size):
        super().__init__()
        self.size = size
        self.field = None
        self.no_game = 1
        self.resize(size * 100, size * 100 + 22)
        self.size = size
        self.menubar = QMenuBar(self)
        self.menubar.setGeometry(QRect(0, 0, 396, 22))
        self.menubar.setObjectName("menubar")
        self.menuSize = QMenu(self.menubar)
        self.menuSize.setObjectName("menuSize")
        self.initUI()

    def initUI(self):
        self.action3_3 = QAction(self)
        self.action3_3.setObjectName("action3_3")
        self.action4_4 = QAction(self)
        self.action4_4.setObjectName("action4_4")
        self.action5_5 = QAction(self)
        self.action5_5.setObjectName("action5_5")
        self.action6_6 = QAction(self)
        self.action6_6.setObjectName("action6_6")
        self.action7_7 = QAction(self)
        self.action7_7.setObjectName("action7_7")
        self.menuSize.addAction(self.action3_3)
        self.menuSize.addAction(self.action4_4)
        self.menuSize.addAction(self.action5_5)
        self.menuSize.addAction(self.action6_6)
        self.menuSize.addAction(self.action7_7)
        self.menubar.addAction(self.menuSize.menuAction())
        self.menuSize.setTitle("Size")

        self.action3_3.setText("3*3")
        self.action3_3.triggered.connect(self.new_trig)
        self.action4_4.setText("4*4")
        self.action5_5.setText("5*5")
        self.action6_6.setText("6*6")
        self.action7_7.setText("7*7")

        self.jeu = Game(self.size, self)


    def gen_button(self, i, j, m, gm):
        exec('self.button_{} = m\ngm.res.append(m)'.format(str(i + 1) + str(j + 1) + str(self.no_game)))

    def new_trig(self):
        if self.sender() == self.action3_3:
            self.new(3)

    def new(self, s):
        for i in range(self.size):
            for j in range(self.size):
                exec('self.button_{}.deleteLater()\nself.button_{} = None'.format(str(i + 1) + str(j + 1) + str(self.no_game), str(i + 1) + str(j + 1) + str(self.no_game)))
        self.res = []
        self.no_game += 1
        self.resize(s * 100, s * 100 + 22)
        self.size = s
        self.jeu = None

        self.jeu = Game(s, self)

    def swap(self, first, free):
        free.setNum(first._num)
        first.setNum(0)

        

class Element(QPushButton):
    def __init__(self, num, x, y, slf):
        super().__init__(str(num), slf)
        self._num = num
        self._pos = [x, y]
        self.appli = slf
        self.clicked.connect(self.clk)

    def clk(self):
        me = self.sender()
        self.appli.jeu.move_(me)

    def setNum(self, n):
        self._num = n
        if n != 0:
            self.setText(str(n))
            self.setDisabled(False)
        else:
            self.setText('')
            self.setDisabled(True)


class Game:
    def __init__(self, size, w):
        self.size = size
        self.splitter = lambda lst, sz: [lst[i:i+sz] for i in range(0, len(lst), sz)]
        self.res = []
        f = self.generate_field()
        for i in range(self.size):
            for j in range(self.size):
                m = Element(f[i][j], j, i, w)
                m.setFont(QFont('Arial', 25))
                if f[i][j] != 0:
                    m.setText(str(f[i][j]))
                else:
                    m.setText('')
                    m.setDisabled(True)
                m.setGeometry(j * 100, i * 100 + 22, 100, 100)
                w.gen_button(i, j, m, self)
                self.field = self.splitter(self.res, self.size)


    def check_solvable(self, tr):
        res = 0
        m = []
        for row in tr:
            m += row

        for i in range(len(m) - 1):
            for j in range(i, len(m) - 1):
                if m[i] > m[j]:
                    res += 1
#///////////////////////////////////

        if res % 2 == 0:
            return True
        return False

    def generate_field(self):
        max_num = self.size ** 2
        q = list(range(1, max_num))
        q.append(0)

        solvable = False
        while not solvable:
            q.__delitem__(q.index(0))
            shuffle(q)
            q.append(0)
            d = self.splitter(q, self.size)
            solvable = self.check_solvable(d)

        return d

    def find_free(self):
        for a in self.field:
            for elem in a:
                if elem._num == 0:
                    return elem




    def movable(self, elem):
        pos_free = []
        for a in self.field:
            for e in a:
                if e._num == 0:
                    pos_free = [a.index(e), self.field.index(a)]
        pos_elem = []
        for a in self.field:
            for e in a:
                if e._num == elem._num:
                    pos_elem = [a.index(e), self.field.index(a)]

        if ((pos_free[0] - pos_elem[0] in (-1, 1)) and (pos_free[1] - pos_elem[1] == 0)) or ((pos_free[0] - pos_elem[0] == 0) and (pos_free[1] - pos_elem[1] in (-1, 1))):
            return True
        return False

    def move_(self, first):
        if not self.movable(first):
            return False
        free = self.find_free()
        window.swap(first, free)
        if self.check_gameover():
            print('YOU WIN')

    def check_gameover(self):
        must = 1
        for row in self.field:
            for el in row:
                if el._num != must:
                    if el._num == 0:
                        if row.index(el) == self.size - 1 and self.field.index(row) == self.size - 1:
                            return True
                    return False
                must += 1


def main():
    global window
    app = QApplication(sys.argv)  # Новый экземпляр QApplication
    window = Application(2)  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':
    main()
