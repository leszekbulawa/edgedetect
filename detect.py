import os, sys
from PIL import Image
import numpy as np
from scipy import ndimage
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8


    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class Ui_MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QWidget.__init__(self)

        self.path = ''
        #self.outfilename = self.path + '_edge'
        self.roberts_cross_x = np.array([[1, 0],
                                         [0, -1]])

        self.roberts_cross_y = np.array([[0, 1],
                                         [-1, 0]])

        self.sobel_x = np.array([[-1, 0, 1],
                                 [-2, 0, 2],
                                 [-1, 0, 1]])

        self.sobel_y = np.array(([-1, -2, -1],
                                 [0, 0, 0],
                                 [1, 2, 1]))

        self.prewitt_x = np.array(([-1, 0, 1],
                                   [-1, 0, 1],
                                   [-1, 0, 1]))

        self.prewitt_y = np.array(([-1, -1, -1],
                                   [0, 0, 0],
                                   [1, 1, 1]))

        self.scharr_x = np.array(([3, 0, -3],
                                  [10, 0, -10],
                                  [3, 0, -3]))

        self.scharr_y = np.array(([3, 10, 3],
                                  [0, 0, 0],
                                  [-3, -10, -3]))

        self.setupUi(self)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(800, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(50, 150, 121, 31))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton_2 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(50, 190, 121, 31))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.pushButton_3 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(50, 230, 121, 31))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.pushButton_4 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(50, 270, 121, 31))
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.pushButton_5 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(50, 80, 121, 31))
        self.pushButton_5.setObjectName(_fromUtf8("pushButton_5"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(50, 20, 371, 41))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.pushButton_5.setText(_translate("MainWindow", "Załaduj zdjęcie", None))
        self.pushButton.clicked.connect(self.chooseFile)
        self.pushButton.setText(_translate("MainWindow", "Krzyż Robertsa", None))
        self.pushButton.clicked.connect(self.roberts_cross)
        self.pushButton_2.setText(_translate("MainWindow", "Sobel", None))
        self.pushButton.clicked.connect(self.sobel)
        self.pushButton_3.setText(_translate("MainWindow", "Prewitt", None))
        self.pushButton.clicked.connect(self.prewitt)
        self.pushButton_4.setText(_translate("MainWindow", "Scharr", None))
        self.pushButton.clicked.connect(self.scharr)
        self.label.setText(_translate("MainWindow", "Detekcja krawędzi w obrazach - projekt", None))

    def showOpenFileDialog(self):
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Otworz plik')
        return str(fname)

    def chooseFile(self):
        self.path = self.showOpenFileDialog()
        # self.path1Label.setText(self.path)

    def load_image(self):
        if self.path != '':
            img = Image.open(open(self.path, "rb"))
            print('format:', img.format, "%dx%d" % img.size, img.mode)
            img.load()
            img = img.convert('L');
            return np.asarray(img, dtype="int32")

    def save_image(data, self):
        img = Image.fromarray(np.asarray(np.clip(data, 0, 255), dtype="uint8"), "L")
        print(self.outfilename + ' file saved')
        img.save(self.outfilename)

    def show_image(imagefilename):
        img = Image.open(imagefilename)
        img.show()

    def roberts_cross(self, outfilename):
        if self.path != '':
            image = self.load_image
            vertical = ndimage.convolve(image, self.roberts_cross_x)
            horizontal = ndimage.convolve(image, self.roberts_cross_y)
            output_image = np.sqrt(np.square(horizontal) + np.square(vertical))
            self.save_image(output_image, outfilename)

    def sobel(self, outfilename):
        image = Image.open(self.path)
        vertical = ndimage.convolve(image, self.sobel_x)
        horizontal = ndimage.convolve(image, self.sobel_y)
        output_image = np.sqrt(np.square(horizontal) + np.square(vertical))
        self.save_image(output_image, outfilename)

    def prewitt(self, outfilename):
        image = Image.open(self.path)
        vertical = ndimage.convolve(image, self.prewitt_x)
        horizontal = ndimage.convolve(image, self.prewitt_y)
        output_image = np.sqrt(np.square(horizontal) + np.square(vertical))
        self.save_image(output_image, outfilename)

    def scharr(self, outfilename):
        image = Image.open(self.path)
        vertical = ndimage.convolve(image, self.prewitt_x)
        horizontal = ndimage.convolve(image, self.prewitt_y)
        output_image = np.sqrt(np.square(horizontal) + np.square(vertical))
        self.save_image(output_image, outfilename)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    ex = Ui_MainWindow()
    ex.show()
    sys.exit(app.exec_())

    # infilename = sys.argv[1]
    # outfilename = sys.argv[2]
