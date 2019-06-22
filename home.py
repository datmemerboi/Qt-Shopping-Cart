import sys
from PyQt5 import QtWidgets
import uiwindow, windowcontents

if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
	ThisWindow = QtWidgets.QMainWindow()
	uiwindow.UIWindowClass().UIWindowFn(ThisWindow)
	windowcontents.Extender().ExtenderFn(ThisWindow)
	ThisWindow.show()
	sys.exit(app.exec_())