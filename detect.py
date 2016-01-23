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



class MainWindow(QtGui.QMainWindow):
    path = ''
    image =  Image.new("RGB", (1000, 1000))
        #self.outfilename = self.path + '_edge'
    roberts_cross_x = np.array([[1, 0],
                                [0, -1]])

    roberts_cross_y = np.array([[0, 1],
                                [-1, 0]])

    sobel_x = np.array([[-1, 0, 1],
                        [-2, 0, 2],
                         [-1, 0, 1]])

    sobel_y = np.array(([-1, -2, -1],
                        [0, 0, 0],
                        [1, 2, 1]))

    prewitt_x = np.array(([-1, 0, 1],
                          [-1, 0, 1],
                          [-1, 0, 1]))

    prewitt_y = np.array(([-1, -1, -1],
                          [0, 0, 0],
                          [1, 1, 1]))

    scharr_x = np.array(([3, 0, -3],
                         [10, 0, -10],
                         [3, 0, -3]))

    scharr_y = np.array(([3, 10, 3],
                         [0, 0, 0],
                         [-3, -10, -3]))


    def __init__(self):
        super(MainWindow, self).__init__()
        self.resize(800,600)
        self.initUI()

    def initUI(self):
        #MainWindow.setObjectName(_fromUtf8("MainWindow"))

        #self.path1Label = QtGui.QLabel(self.path)

        #self.centralwidget = QtGui.QWidget(MainWindow)
        #self.centralwidget.setObjectName(_fromUtf8("centralwidget"))

        self.pushButton = QtGui.QPushButton("Krzyz Robertsa", self)
        self.pushButton.setGeometry(QtCore.QRect(50, 150, 121, 31))
        self.pushButton.clicked.connect(lambda: self.roberts_cross("OutputRC"))

        self.pushButton_2 = QtGui.QPushButton("Sobel", self)
        self.pushButton_2.setGeometry(QtCore.QRect(50, 190, 121, 31))
        self.pushButton_2.clicked.connect(lambda: self.sobel("OutputSOBEL"))

        self.pushButton_3 = QtGui.QPushButton("Prewitt", self)
        self.pushButton_3.setGeometry(QtCore.QRect(50, 230, 121, 31))
        self.pushButton_3.clicked.connect(lambda: self.prewitt("OutputPREWITT"))

        self.pushButton_4 = QtGui.QPushButton("Scharr", self)
        self.pushButton_4.setGeometry(QtCore.QRect(50, 270, 121, 31))
        self.pushButton_4.clicked.connect(lambda: self.scharr("OutputSCHARR"))

        self.pushButton_5 = QtGui.QPushButton("Zaladuj zdjecie", self)
        self.pushButton_5.setGeometry(QtCore.QRect(50, 80, 121, 31))
        self.pushButton_5.clicked.connect(self.showOpenFileDialog)

        self.pathLabel = QtGui.QLabel(self)
        self.pathLabel.setGeometry(QtCore.QRect(200, 80, 421, 31))
        #self.pathLabel.setText("costamcotam")
        #font1 = QtGui.QFont()
        #font1.setFamily(_fromUtf8("Arial"))
        #font1.setPointSize(12)
        #font1.setBold(False)
        #font1.setWeight(75)
        #self.pathLabel.setFont(font1)

        #self.label.setObjectName(_fromUtf8("label"))

        self.label = QtGui.QLabel(self)
        self.label.setText("Detekcja krawędzi w obrazach - projekt")
        self.label.setGeometry(QtCore.QRect(50, 20, 371, 41))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))

       # self.menubar = QtGui.QMenuBar(MainWindow)
       # self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
       # self.menubar.setObjectName(_fromUtf8("menubar"))
       # MainWindow.setMenuBar(self.menubar)
       # self.statusbar = QtGui.QStatusBar(MainWindow)
       # self.statusbar.setObjectName(_fromUtf8("statusbar"))
       # MainWindow.setStatusBar(self.statusbar)

        self.show()


    def showOpenFileDialog(self):
        self.path = QtGui.QFileDialog.getOpenFileName(self, 'Otworz plik')
        self.pathLabel.setText(self.path)
        #if fname != '':
        #    self.image = Image.open(fname)
        #    print('format:', self.image.format, "%dx%d" % self.image.size, self.image.mode)
        #    self.image.load()
        #    self.image = self.image.convert('L')

         #   return np.asarray(self.image, dtype="int32")

    def chooseFile(self):
        self.path = self.showOpenFileDialog()
        self.pathLabel.setText(self.path)

    def load_image(self):
        if self.path != '':
            print(self.path)
            img = Image.open(self.path)
            print('format:', img.format, "%dx%d" % img.size, img.mode)
            img.load()
            img = img.convert('L');
            return np.asarray(img, dtype="int32")

    @staticmethod
    def save_image(data, outfilename):
        image = Image.fromarray(np.asarray(np.clip(data, 0, 255), dtype="uint8"), "L")
        print(outfilename + ' file saved')
        image.show()
        image.save(outfilename + '.jpg')

    def show_image(imagefilename):
        img = Image.open(imagefilename)
        img.show()

    def roberts_cross(self, outfilename):
        if self.path != '':
            #a = self.load_image
            img = Image.open(self.path)
            print('format:', img.format, "%dx%d" % img.size, img.mode)
            img.load()
            img = img.convert('L');
            image = np.asarray(img, dtype="int32")
            vertical = ndimage.convolve(image, self.roberts_cross_x)
            horizontal = ndimage.convolve(image, self.roberts_cross_y)
            output_image = np.sqrt(np.square(horizontal) + np.square(vertical))
            self.save_image(output_image, outfilename)

    def sobel(self, outfilename):
        #image = Image.open(self.path)
        if self.path != '':
            #a = self.load_image
            img = Image.open(self.path)
            print('format:', img.format, "%dx%d" % img.size, img.mode)
            img.load()
            img = img.convert('L');
            image = np.asarray(img, dtype="int32")
            vertical = ndimage.convolve(image, self.sobel_x)
            horizontal = ndimage.convolve(image, self.sobel_y)
            output_image = np.sqrt(np.square(horizontal) + np.square(vertical))
            self.save_image(output_image, outfilename)

    def prewitt(self, outfilename):
        #image = Image.open(self.path)
        if self.path != '':
            #a = self.load_image
            img = Image.open(self.path)
            print('format:', img.format, "%dx%d" % img.size, img.mode)
            img.load()
            img = img.convert('L');
            image = np.asarray(img, dtype="int32")
            vertical = ndimage.convolve(image, self.prewitt_x)
            horizontal = ndimage.convolve(image, self.prewitt_y)
            output_image = np.sqrt(np.square(horizontal) + np.square(vertical))
            self.save_image(output_image, outfilename)

    def scharr(self, outfilename):
        #image = Image.open(self.path)
        if self.path != '':
            #a = self.load_image
            img = Image.open(self.path)
            print('format:', img.format, "%dx%d" % img.size, img.mode)
            img.load()
            img = img.convert('L');
            image = np.asarray(img, dtype="int32")
            vertical = ndimage.convolve(image, self.prewitt_x)
            horizontal = ndimage.convolve(image, self.prewitt_y)
            output_image = np.sqrt(np.square(horizontal) + np.square(vertical))
            self.save_image(output_image, outfilename)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())

    # infilename = sys.argv[1]
    # outfilename = sys.argv[2]
