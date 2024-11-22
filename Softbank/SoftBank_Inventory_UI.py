from PyQt5 import QtWidgets, QtCore, QtGui

import softbank_app

class Main(QtWidgets.QMainWindow, softbank_app.Ui_MainWindow):
    def __init__(self):
         super().__init__()
         self.setupUi(self)

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())