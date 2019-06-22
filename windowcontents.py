from PyQt5 import QtWidgets

CartItems = []

class Extender(object):
	def ExtenderFn(self, window):
		window.setWindowTitle("Extended Window")
		
		welcomeMsg = QtWidgets.QMessageBox()
		welcomeMsg.setText("Welcome to your shopping cart!")
		welcomeMsg.setWindowTitle(" ")
		welcomeMsg.exec_()

		frame1 = QtWidgets.QWidget(window)
		frame1.resize(500, 600)
		frame1.move(0,0)
		frame1.setStyleSheet("border-style:solid;border-color:rgb(0, 255, 131);border-width:3px;border-radius: 5px;")
		
		self.combos = QtWidgets.QComboBox(window)
		self.combos.addItems(['Beverages', 'Chips', 'Biscuits'])
		self.combos.setStyleSheet("background-color:white; color:black")
		self.combos.resize(300, 35)
		self.combos.move(80, 50)

		self.inputBox = QtWidgets.QTextEdit(window)
		self.inputBox.setStyleSheet("background-color:white; color:black")
		self.inputBox.setPlaceholderText("Enter Name here")
		self.inputBox.resize(300, 30)
		self.inputBox.move(80, 120)

		AddButton = QtWidgets.QPushButton(window)
		AddButton.setStyleSheet("background-color:white")
		AddButton.setText("Add Item")
		AddButton.move(120, 190)
		AddButton.clicked.connect(lambda: self.ItemAddFn())

		AddButton = QtWidgets.QPushButton(window)
		AddButton.setStyleSheet("background-color:white")
		AddButton.setText("Remove Item")
		AddButton.move(250, 190)
		AddButton.clicked.connect(lambda: self.ItemRemFn())

	def ItemAddFn(self):
		print("+++")
		CartItems.append({"Name":self.inputBox.toPlainText().strip(), "Category":self.combos.currentText()})
		print(CartItems)

	def ItemRemFn(self):
		print("---")
		for index, val in enumerate(CartItems):
			if(val["Name"]==self.inputBox.toPlainText().strip() and val["Category"]==self.combos.currentText()):
				del CartItems[index]
		print(CartItems)