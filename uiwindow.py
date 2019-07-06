from PyQt5 import QtWidgets

class UIWindowClass(object):
	def UIWindowFn(self,window):
		window.setWindowTitle("UI Window")
		window.resize(650,600)
		window.setStyleSheet("background-color:rgb(10, 10, 10);")