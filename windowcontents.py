from PyQt5 import QtWidgets
from pymongo import MongoClient

class ShoppingWindow(object):
	def ShoppingWindowFn(self, window):
		window.setWindowTitle("Shopping Window")
		
		welcomeMsg = QtWidgets.QMessageBox()
		welcomeMsg.setText("Welcome to your shopping cart!")
		welcomeMsg.setWindowTitle(" ")
		welcomeMsg.exec_()

		frame1 = QtWidgets.QWidget(window)
		frame1.resize(500, 600)
		frame1.move(0,0)
		frame1.setStyleSheet("border-style:solid;border-color:rgb(0, 255, 131);border-width:3px;border-radius: 5px;")

		frame2 = QtWidgets.QWidget(window)
		frame2.resize(150, 600)
		frame2.move(500,0)
		frame2.setStyleSheet("border-style:solid;border-color:rgb(0, 255, 131);border-width:3px;border-radius: 5px;")

		self.combos = QtWidgets.QComboBox(window)
		self.combos.addItems(['Beverages', 'Chips', 'Biscuits'])
		self.combos.setStyleSheet("background-color:white; color:black")
		self.combos.resize(300, 35)
		self.combos.move(100, 50)

		self.inputBox = QtWidgets.QLineEdit(window)
		self.inputBox.setStyleSheet("background-color:white; color:black")
		self.inputBox.setPlaceholderText("Enter Name here")
		self.inputBox.resize(300, 30)
		self.inputBox.move(100, 120)

		AddButton = QtWidgets.QPushButton(window)
		AddButton.setStyleSheet("background-color:white")
		AddButton.setText("Add Item")
		AddButton.move(135, 190)
		AddButton.clicked.connect(lambda: self.ItemAddFn())

		RemButton = QtWidgets.QPushButton(window)
		RemButton.setStyleSheet("background-color:white")
		RemButton.setText("Remove Item")
		RemButton.move(265, 190)
		RemButton.clicked.connect(lambda: self.ItemRemFn())

		RemAllButton = QtWidgets.QPushButton(window)
		RemAllButton.setStyleSheet("background-color:white")
		RemAllButton.setText("Remove All")
		RemAllButton.move(200, 235)
		RemAllButton.clicked.connect(lambda: self.AreYouSure())

		self.resultBox = QtWidgets.QTextEdit(frame1)
		self.resultBox.setStyleSheet("background: transparent; color:white; font-size: 16px;")
		self.resultBox.resize(300, 200)
		self.resultBox.move(100, 280)

	def ItemAddFn(self):
		CartItem = {"Name":self.inputBox.text().strip(), "Category":self.combos.currentText()}
		dbconn = MongoClient("mongodb://localhost:27017/")
		query = dbconn.ShopCartApp.Cart.update( CartItem, CartItem, upsert= True)
		self.ResultBoxPrintFn(dbconn)
		dbconn.close()

	def ItemRemFn(self):
		CartItem = {"Name":self.inputBox.text().strip(), "Category":self.combos.currentText()}		
		dbconn = MongoClient("mongodb://localhost:27017/")
		query = dbconn.ShopCartApp.Cart.remove(CartItem)
		self.ResultBoxPrintFn(dbconn)
		dbconn.close()

	def ResultBoxPrintFn(self,dbconn):
		self.resultBox.setText(" ")
		result = dbconn.ShopCartApp.Cart.find()
		for index in result:
			if self.resultBox.toPlainText().strip() == "":
				self.resultBox.setText(index['Name']+" "+index['Category'])
			else:
				self.resultBox.setText(self.resultBox.toPlainText().strip()+"\n"+index['Name']+" "+index['Category'])
		print("Result Printed")

	def AreYouSure(self):
		check = QtWidgets.QMessageBox()
		check.setText("Are you sure?")
		check.setInformativeText("Your cart will be cleared..")
		check.setWindowTitle(" ")
		check.setStandardButtons(QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Yes)
		check.buttonClicked.connect(lambda: self.RemAllFn())
		check.exec_()

	def RemAllFn(self):
		dbconn = MongoClient("mongodb://localhost:27017/")
		query = dbconn.ShopCartApp.Cart.remove({})
		self.ResultBoxPrintFn(dbconn)
		dbconn.close()