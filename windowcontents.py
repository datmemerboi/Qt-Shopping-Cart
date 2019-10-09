from PyQt5 import QtWidgets
from pymongo import MongoClient

class ShoppingWindow(object):
	def ShoppingWindowFn(self, window):
		window.setWindowTitle("Shopping Window")
		
		welcomeMsg = QtWidgets.QMessageBox()
		welcomeMsg.setText("Welcome to your shopping cart!")
		welcomeMsg.setWindowTitle(" ")
		welcomeMsg.exec_()

		File = open("css/frame.css", 'r')
		frameCSS = File.read()
		File.close()
		File = open("css/input.css", 'r')
		inputCSS = File.read()
		File.close()
		File = open("css/resultbox.css", 'r')
		resultboxCSS = File.read()
		File.close()
		
		frame1 = QtWidgets.QWidget(window)
		frame1.resize(500, 600)
		frame1.move(0,0)
		frame1.setStyleSheet(frameCSS)


		frame2 = QtWidgets.QWidget(window)
		frame2.resize(150, 600)
		frame2.move(500,0)
		frame2.setStyleSheet(frameCSS)

		self.combos = QtWidgets.QComboBox(window)
		self.combos.addItems(['Beverages', 'Chips', 'Biscuits'])
		self.combos.setStyleSheet(inputCSS)
		self.combos.resize(300, 35)
		self.combos.move(100, 50)

		self.inputBox = QtWidgets.QLineEdit(window)
		self.inputBox.setStyleSheet(inputCSS)
		self.inputBox.setPlaceholderText("Enter Name here")
		self.inputBox.resize(300, 30)
		self.inputBox.move(100, 120)

		AddButton = QtWidgets.QPushButton(window)
		AddButton.setStyleSheet(inputCSS)
		AddButton.setText("Add Item")
		AddButton.move(135, 190)
		AddButton.clicked.connect(lambda: self.ItemAddFn())

		RemButton = QtWidgets.QPushButton(window)
		RemButton.setStyleSheet(inputCSS)
		RemButton.setText("Remove Item")
		RemButton.move(265, 190)
		RemButton.clicked.connect(lambda: self.ItemRemFn())

		RemAllButton = QtWidgets.QPushButton(window)
		RemAllButton.setStyleSheet(inputCSS)
		RemAllButton.setText("Remove All")
		RemAllButton.move(200, 235)
		RemAllButton.clicked.connect(lambda: self.AreYouSure())

		self.resultBox = QtWidgets.QTextEdit(frame1)
		self.resultBox.setStyleSheet(resultboxCSS)
		self.resultBox.resize(300, 200)
		self.resultBox.move(100, 280)

		self.SearchBar = QtWidgets.QLineEdit(window)
		self.SearchBar.move(510, 20)
		self.SearchBar.resize(130, 30)
		self.SearchBar.setStyleSheet(inputCSS)
		self.SearchBar.setPlaceholderText("Search Item")

		SearchButton = QtWidgets.QPushButton(window)
		SearchButton.setStyleSheet(inputCSS)
		SearchButton.move(550, 70)
		SearchButton.resize(35, 30)
		SearchButton.setText("Go")
		SearchButton.clicked.connect(lambda: self.SearchItems())

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

	def SearchItems(self):
		query = self.SearchBar.text()
		print("Searching for: "+ query)
		dbconn = MongoClient("mongodb://localhost:27017/")
		result = dbconn.ShopCartApp.Stonks.find( {"Name":{'$regex' : query, '$options' : 'i'}} )
		if(result):
			for index in result:
				print(index["Name"]+" found in "+index["Category"])