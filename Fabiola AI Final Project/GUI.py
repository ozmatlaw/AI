from fabiola import *
from agents import *
import fabiola
import constants
import time
import sys
from PyQt5.uic import loadUi  # uic: Python UI Compiler
from PyQt5.QtWidgets import QApplication, QMessageBox, QDialog, QStackedWidget
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QSize


# -------------------------- MAGIC NUMBERS AND GLOBAL VARIABLES --------------------------

MAX_ORDER_TIME = 300  # The maximal time to receive orders
MAX_ORDERS_NUM = 4  # The maximal number of orders that can be received
MAX_INGREDIENTS_NUM = 3  # The maximal number of ingredients for each order
CURR_ORDER_NUM = 0  # The current order number
ORDER_LIST = []  # A list containing Orders objects
app = QApplication(sys.argv)  # The application that runs the program interface
initTime = int(time.time())  # The initial time of execution of the app
widget = QStackedWidget()  # The widget at the basis of the application


# -------------------------- STATIC FUNCTIONS -----------------------------

def openStartScreen():
    """
    A function to open a StartScreen widget and add it to the widget stack.
    """
    startScreen = StartScreen()
    widget.addWidget(startScreen)
    widget.setCurrentIndex(widget.currentIndex() + 1)


def openMenuScreen():
    """
    A function to open a MenuScreen widget and add it to the widget stack.
    """
    menuScreen = MenuScreen()
    widget.addWidget(menuScreen)
    widget.setCurrentIndex(widget.currentIndex() + 1)


def coffeeMenuScreen():
    """
    A function to open a CoffeeMenuScreen widget and add it to the widget stack.
    """
    coffeeMenu = CoffeeMenuScreen()
    widget.addWidget(coffeeMenu)
    widget.setCurrentIndex(widget.currentIndex() + 1)


def pastaMenuScreen():
    """
    A function to open a PastaMenuScreen widget and add it to the widget stack.
    """
    pastaMenu = PastaMenuScreen()
    widget.addWidget(pastaMenu)
    widget.setCurrentIndex(widget.currentIndex() + 1)


def sandwichMenuScreen():
    """
    A function to open a SaladMenuScreen widget and add it to the widget stack.
    """
    sandwichMenu = SandwichMenuScreen()
    widget.addWidget(sandwichMenu)
    widget.setCurrentIndex(widget.currentIndex() + 1)


def toastMenuScreen():
    """
    A function to open a ToastMenuScreen widget and add it to the widget stack.
    """
    toastMenu = ToastMenuScreen()
    widget.addWidget(toastMenu)
    widget.setCurrentIndex(widget.currentIndex() + 1)


def saladMenuScreen():
    """
    A function to open a SaladMenuScreen widget and add it to the widget stack.
    """
    saladMenu = SaladMenuScreen()
    widget.addWidget(saladMenu)
    widget.setCurrentIndex(widget.currentIndex() + 1)


def drinksMenuScreen():
    """
    A function to open a DrinksMenuScreen widget and add it to the widget stack.
    """
    drinksMenu = DrinksMenuScreen()
    widget.addWidget(drinksMenu)
    widget.setCurrentIndex(widget.currentIndex() + 1)


# -------------------------- CLASSES --------------------------

class StartScreen(QDialog):
    """
    A class that represents the start screen of the application
    """
    def __init__(self):
        """
        The init method of the class. The method downloads the corresponding .ui file and defines
        the members of the class. If they are labels or buttons, it sets their stylesheet, signals
        and handlers.
        """
        super(StartScreen, self).__init__()
        loadUi("GUI_sources/startScreen.ui", self)

        self.imageLabel.setPixmap(QPixmap('GUI_sources/DONA FABIOLA.png'))
        self.menuButton.setIcon(QIcon("GUI_sources/menuicon black background.png"))
        self.menuButton.setIconSize(QSize(41, 41))
        self.menuButton.clicked.connect(openMenuScreen)


class MenuScreen(QDialog):
    """
    A class that represents the general menu screen of the application
    """
    def __init__(self):
        """
        The init method of the class. The method downloads the corresponding .ui file and defines
        the members of the class. If they are labels or buttons, it sets their stylesheet, signals
        and handlers.
        """
        super(MenuScreen, self).__init__()
        loadUi("GUI_sources/menuScreen.ui", self)

        self.imageLabel.setPixmap(QPixmap('GUI_sources/DONA FABIOLA.png'))
        self.menuButton.setIcon(QIcon("GUI_sources/menuicon black background.png"))
        self.menuButton.setIconSize(QSize(41, 41))
        self.menuButton.clicked.connect(openStartScreen)
        self.coffeeButton.clicked.connect(coffeeMenuScreen)
        self.pastaButton.clicked.connect(pastaMenuScreen)
        self.sandwichButton.clicked.connect(sandwichMenuScreen)
        self.toastButton.clicked.connect(toastMenuScreen)
        self.saladButton.clicked.connect(saladMenuScreen)
        self.drinksButton.clicked.connect(drinksMenuScreen)


class CoffeeMenuScreen(QDialog):
    """
    A class that represents the coffee menu screen of the application
    """
    def __init__(self):
        """
        The init method of the class. The method downloads the corresponding .ui file and defines
        the members of the class. If they are labels or buttons, it sets their stylesheet, signals
        and handlers.
        orderList: a set containing all ingredients added to the current order
        price: the current price of the order
        """
        super(CoffeeMenuScreen, self).__init__()
        loadUi("GUI_sources/coffeeScreen.ui", self)
        self.orderList = set()
        self.price = 6

        self.imageLabel.setPixmap(QPixmap('GUI_sources/DONA FABIOLA tag.png'))
        self.backButton.setIcon(QIcon("GUI_sources/backbuttonicon5.png"))
        self.backButton.setIconSize(QSize(41, 41))
        self.backButton.clicked.connect(openMenuScreen)
        self.coffeeButton.clicked.connect(self.addCoffee)
        self.milkButton.clicked.connect(self.addMilk)
        self.oatmilkButton.clicked.connect(self.addOatmilk)
        self.iceButton.clicked.connect(self.addIce)
        self.plasticButton.clicked.connect(self.choosePlastic)
        self.reusableButton.clicked.connect(self.chooseReusable)
        self.nextButton.clicked.connect(self.showPrice)

    def addCoffee(self):
        """
        A method to add coffee to the current order when the corresponding button is pressed.
        """
        if not self.coffeeButton.isChecked():
            self.coffeeButton.setChecked(True)
            self.coffeeButton.setStyleSheet("background-color: rgb(255, 182, 193);")
            self.price += 6
            if len(self.orderList) < MAX_INGREDIENTS_NUM:
                self.orderList.add("coffee")
        else:
            self.coffeeButton.setChecked(False)
            self.coffeeButton.setStyleSheet("background-color:rgb(255, 255, 255);")
            self.price -= 6
            if "coffee" in self.orderList:
                self.orderList.remove("coffee")

    def addMilk(self):
        """
        A method to add milk to the current order when the corresponding button is pressed.
        """
        if not self.milkButton.isChecked():
            self.milkButton.setChecked(True)
            self.milkButton.setStyleSheet("background-color: rgb(255, 182, 193);")
            if len(self.orderList) < MAX_INGREDIENTS_NUM:
                self.orderList.add("milk")
        else:
            self.milkButton.setChecked(False)
            self.milkButton.setStyleSheet("background-color:rgb(255, 255, 255);")
            if "milk" in self.orderList:
                self.orderList.remove("milk")

    def addOatmilk(self):
        """
        A method to add oat milk to the current order when the corresponding button is pressed.
        """
        if not self.oatmilkButton.isChecked():
            self.oatmilkButton.setChecked(True)
            self.oatmilkButton.setStyleSheet("background-color: rgb(255, 182, 193);")
            self.price += 2
            if len(self.orderList) < MAX_INGREDIENTS_NUM:
                self.orderList.add("oat milk")
        else:
            self.oatmilkButton.setChecked(False)
            self.oatmilkButton.setStyleSheet("background-color:rgb(255, 255, 255);")
            self.price -= 2
            if "oat milk" in self.orderList:
                self.orderList.remove("oat milk")

    def addIce(self):
        """
        A method to add ice to the current order when the corresponding button is pressed.
        """
        if not self.iceButton.isChecked():
            self.iceButton.setChecked(True)
            self.iceButton.setStyleSheet("background-color: rgb(255, 182, 193);")
            self.price += 4
            if len(self.orderList) < MAX_INGREDIENTS_NUM:
                self.orderList.add("ice")
        else:
            self.iceButton.setChecked(False)
            self.iceButton.setStyleSheet("background-color: rgb(255, 255, 255);")
            self.price -= 4
            if "ice" in self.orderList:
                self.orderList.remove("ice")

    def choosePlastic(self):
        """
        A method to select a plastic cup for the current order when the corresponding button is
        pressed.
        """
        if not self.plasticButton.isChecked():
            if self.reusableButton.isChecked():
                msg = QMessageBox()
                msg.setGeometry(500, 500, 100, 100)
                msg.setIcon(QMessageBox.Icon.Information)
                msg.setText("Reusable Cup is selected")
                msg.setInformativeText(
                    "Deselect reusable cup option first, and then select plastic cup")
                msg.setWindowTitle("Cup Type Selection")
                msg.exec()
                return
            self.plasticButton.setChecked(True)
            self.plasticButton.setStyleSheet("background-color: rgb(255, 182, 193);")
            self.price += 2
        else:
            self.plasticButton.setChecked(False)
            self.plasticButton.setStyleSheet("background-color:rgb(255, 255, 255);")
            self.price -= 2

    def chooseReusable(self):
        """
        A method to select a reusable cup for the current order when the corresponding button is
        pressed.
        """
        if not self.reusableButton.isChecked():
            if self.reusableButton.isChecked():
                msg = QMessageBox()
                msg.setGeometry(500, 500, 100, 100)
                msg.setIcon(QMessageBox.Icon.Information)
                msg.setText("Plastic Cup is selected")
                msg.setInformativeText(
                    "Deselect plastic cup option first, and then select reusable cup")
                msg.setWindowTitle("Cup Type Selection")
                msg.exec()
                return
            self.reusableButton.setChecked(True)
            self.reusableButton.setStyleSheet("background-color: rgb(255, 182, 193);")
        else:
            self.reusableButton.setChecked(False)
            self.reusableButton.setStyleSheet("background-color:rgb(255, 255, 255);")

    def showPrice(self):
        """
        A method to complete the order and add it to ORDER_LIST. A message is displayed whether the
        order has been successfully placed or not.
        """
        global CURR_ORDER_NUM, ORDER_LIST
        msg = QMessageBox()
        msg.setGeometry(500, 500, 100, 100)
        msg.setIcon(QMessageBox.Icon.Information)
        if CURR_ORDER_NUM >= MAX_ORDERS_NUM:
            msg = QMessageBox()
            msg.setGeometry(500, 500, 100, 100)
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setText("Order cannot be placed")
            msg.setInformativeText("The maximal number of orders has been reached, please try later")
            msg.setWindowTitle("Order not Placed")
            msg.exec()
            widget.close()
            return

        currTime = time.time() - initTime
        if currTime > MAX_ORDER_TIME:
            msg.setText("Order cannot be placed")
            msg.setInformativeText("Fabiola is closing, orders cannot be taken")
            msg.setWindowTitle("Order not Placed")
            msg.exec()
            widget.close()
            return

        CURR_ORDER_NUM += 1
        currTime = time.time() - initTime
        order = fabiola.Order("coffee", self.orderList, int(currTime), CURR_ORDER_NUM)
        ORDER_LIST.append(order)
        msg.setText("Order Placed")
        msg.setInformativeText("Order successfully placed\n\nPrice: " + str(self.price) + "₪")
        msg.setWindowTitle("Order Placed")
        msg.exec()
        openStartScreen()


class PastaMenuScreen(QDialog):
    """
    A class that represents the pasta menu screen of the application
    """
    def __init__(self):
        """
        The init method of the class. The method downloads the corresponding .ui file and defines
        the members of the class. If they are labels or buttons, it sets their stylesheet, signals
        and handlers.
        orderList: a set containing all ingredients added to the current order
        price: the current price of the order
        """
        super(PastaMenuScreen, self).__init__()
        loadUi("GUI_sources/pastaScreen.ui", self)
        self.orderList = set()
        self.price = 22

        self.imageLabel.setPixmap(QPixmap('GUI_sources/DONA FABIOLA tag.png'))
        self.backButton.setIcon(QIcon("GUI_sources/backbuttonicon5.png"))
        self.backButton.setIconSize(QSize(41, 41))
        self.backButton.clicked.connect(openMenuScreen)
        self.tomatoButton.clicked.connect(self.addTomato)
        self.pestoButton.clicked.connect(self.addPesto)
        self.cheeseButton.clicked.connect(self.addCheese)
        self.alfredoButton.clicked.connect(self.addAlfredo)
        self.parmesanButton.clicked.connect(self.addParmesan)
        self.nextButton.clicked.connect(self.showPrice)

    def addTomato(self):
        """
        A method to add tomatoes to the current order when the corresponding button is pressed.
        """
        if not self.tomatoButton.isChecked():
            self.tomatoButton.setChecked(True)
            self.tomatoButton.setStyleSheet("background-color: rgb(255, 182, 193);")
            if len(self.orderList) < MAX_INGREDIENTS_NUM:
                self.orderList.add("tomato")
        else:
            self.tomatoButton.setChecked(False)
            self.tomatoButton.setStyleSheet("background-color:rgb(255, 255, 255);")
            if "tomato" in self.orderList:
                self.orderList.remove("tomato")

    def addPesto(self):
        """
        A method to add pesto to the current order when the corresponding button is pressed.
        """
        if not self.pestoButton.isChecked():
            self.pestoButton.setChecked(True)
            self.pestoButton.setStyleSheet("background-color: rgb(255, 182, 193);")
            self.price += 5
            if len(self.orderList) < MAX_INGREDIENTS_NUM:
                self.orderList.add("pesto")
        else:
            self.pestoButton.setChecked(False)
            self.pestoButton.setStyleSheet("background-color:rgb(255, 255, 255);")
            self.price -= 5
            if "pesto" in self.orderList:
                self.orderList.remove("pesto")

    def addCheese(self):
        """
        A method to add cheese to the current order when the corresponding button is pressed.
        """
        if not self.cheeseButton.isChecked():
            self.cheeseButton.setChecked(True)
            self.cheeseButton.setStyleSheet("background-color: rgb(255, 182, 193);")
            self.price += 3
            if len(self.orderList) < MAX_INGREDIENTS_NUM:
                self.orderList.add("cheese")
        else:
            self.cheeseButton.setChecked(False)
            self.cheeseButton.setStyleSheet("background-color:rgb(255, 255, 255);")
            self.price -= 3
            if "cheese" in self.orderList:
                self.orderList.remove("cheese")

    def addAlfredo(self):
        """
        A method to add alfeso sauce to the current order when the corresponding button is pressed.
        """
        if not self.alfredoButton.isChecked():
            self.alfredoButton.setChecked(True)
            self.alfredoButton.setStyleSheet("background-color: rgb(255, 182, 193);")
            self.price += 5
            if len(self.orderList) < MAX_INGREDIENTS_NUM:
                self.orderList.add("alfredo")
        else:
            self.alfredoButton.setChecked(False)
            self.alfredoButton.setStyleSheet("background-color: rgb(255, 255, 255);")
            self.price -= 5
            if "alfredo" in self.orderList:
                self.orderList.remove("alfredo")

    def addParmesan(self):
        """
        A method to add parmesan to the current order when the corresponding button is pressed.
        """
        if not self.parmesanButton.isChecked():
            self.parmesanButton.setChecked(True)
            self.parmesanButton.setStyleSheet("background-color: rgb(255, 182, 193);")
            self.price += 3
            if len(self.orderList) < MAX_INGREDIENTS_NUM:
                self.orderList.add("parmesan")
        else:
            self.parmesanButton.setChecked(False)
            self.parmesanButton.setStyleSheet("background-color:rgb(255, 255, 255);")
            self.price -= 3
            if "parmesan" in self.orderList:
                self.orderList.remove("parmesan")

    def showPrice(self):
        """
        A method to complete the order and add it to ORDER_LIST. A message is displayed whether the
        order has been successfully placed or not.
        """
        global CURR_ORDER_NUM, ORDER_LIST
        msg = QMessageBox()
        msg.setGeometry(500, 300, 300, 100)
        msg.setIcon(QMessageBox.Icon.Information)

        if CURR_ORDER_NUM >= MAX_ORDERS_NUM:
            msg = QMessageBox()
            msg.setGeometry(500, 500, 100, 100)
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setText("Order cannot be placed")
            msg.setInformativeText("The maximal number of orders has been reached, please try later")
            msg.setWindowTitle("Order not Placed")
            msg.exec()
            widget.close()
            return

        currTime = time.time() - initTime
        if currTime > MAX_ORDER_TIME:
            msg.setText("Order cannot be placed")
            msg.setInformativeText("Fabiola is closing, orders cannot be taken")
            msg.setWindowTitle("Order not Placed")
            msg.exec()
            widget.close()
            return

        CURR_ORDER_NUM += 1
        currTime = time.time() - initTime
        order = fabiola.Order("pasta", self.orderList, int(currTime), CURR_ORDER_NUM)
        ORDER_LIST.append(order)
        msg.setText("Order Placed")
        msg.setInformativeText("Order successfully placed\n\nPrice:  " + str(self.price) + "₪")
        msg.setWindowTitle("Order Placed")
        msg.exec()
        openStartScreen()


class SandwichMenuScreen(QDialog):
    """
    A class that represents the sandwich menu screen of the application
    """
    def __init__(self):
        """
        The init method of the class. The method downloads the corresponding .ui file and defines
        the members of the class. If they are labels or buttons, it sets their stylesheet, signals
        and handlers.
        orderList: a set containing all ingredients added to the current order
        price: the current price of the order
        """
        super(SandwichMenuScreen, self).__init__()
        loadUi("GUI_sources/sandwichScreen.ui", self)
        self.orderList = set()
        self.price = 16

        self.imageLabel.setPixmap(QPixmap('GUI_sources/DONA FABIOLA tag.png'))
        self.backButton.setIcon(QIcon("GUI_sources/backbuttonicon5.png"))
        self.backButton.setIconSize(QSize(41, 41))
        self.backButton.clicked.connect(openMenuScreen)
        self.cheeseButton.clicked.connect(self.addCheese)
        self.tomatoButton.clicked.connect(self.addTomato)
        self.onionButton.clicked.connect(self.addOnion)
        self.tunaButton.clicked.connect(self.addTuna)
        self.olivesButton.clicked.connect(self.addOlives)
        self.eggButton.clicked.connect(self.addEgg)
        self.cucumberButton.clicked.connect(self.addCucumber)
        self.avocadoButton.clicked.connect(self.addAvocado)
        self.lettuceButton.clicked.connect(self.addLettuce)
        self.ketchupButton.clicked.connect(self.addKetchup)
        self.nextButton.clicked.connect(self.showPrice)

    def addCheese(self):
        """
        A method to add cheese to the current order when the corresponding button is pressed.
        """
        if not self.cheeseButton.isChecked():
            self.cheeseButton.setChecked(True)
            self.cheeseButton.setStyleSheet("background-color: rgb(255, 182, 193);")
            self.price += 3
            if len(self.orderList) < MAX_INGREDIENTS_NUM:
                self.orderList.add("cheese")
        else:
            self.cheeseButton.setChecked(False)
            self.cheeseButton.setStyleSheet("background-color:rgb(255, 255, 255);")
            self.price -= 3
            if "cheese" in self.orderList:
                self.orderList.remove("cheese")

    def addTomato(self):
        """
        A method to add tomatoes to the current order when the corresponding button is pressed.
        """
        if not self.tomatoButton.isChecked():
            self.tomatoButton.setChecked(True)
            self.tomatoButton.setStyleSheet("background-color: rgb(255, 182, 193);")
            if len(self.orderList) < MAX_INGREDIENTS_NUM:
                self.orderList.add("tomato")
        else:
            self.tomatoButton.setChecked(False)
            self.tomatoButton.setStyleSheet("background-color:rgb(255, 255, 255);")
            if "tomato" in self.orderList:
                self.orderList.remove("tomato")

    def addOnion(self):
        """
        A method to add onions to the current order when the corresponding button is pressed.
        """
        if not self.onionButton.isChecked():
            self.onionButton.setChecked(True)
            self.onionButton.setStyleSheet("background-color: rgb(255, 182, 193);")
            if len(self.orderList) < MAX_INGREDIENTS_NUM:
                self.orderList.add("onion")
        else:
            self.onionButton.setChecked(False)
            self.onionButton.setStyleSheet("background-color:rgb(255, 255, 255);")
            if "onion" in self.orderList:
                self.orderList.remove("onion")

    def addTuna(self):
        """
        A method to add tuna to the current order when the corresponding button is pressed.
        """
        if not self.tunaButton.isChecked():
            self.tunaButton.setChecked(True)
            self.tunaButton.setStyleSheet("background-color: rgb(255, 182, 193);")
            self.price += 3
            if len(self.orderList) < MAX_INGREDIENTS_NUM:
                self.orderList.add("tuna")
        else:
            self.tunaButton.setChecked(False)
            self.tunaButton.setStyleSheet("background-color:rgb(255, 255, 255);")
            self.price -= 3
            if "tuna" in self.orderList:
                self.orderList.remove("tuna")

    def addOlives(self):
        """
        A method to add olives to the current order when the corresponding button is pressed.
        """
        if not self.olivesButton.isChecked():
            self.olivesButton.setChecked(True)
            self.olivesButton.setStyleSheet("background-color: rgb(255, 182, 193);")
            if len(self.orderList) < MAX_INGREDIENTS_NUM:
                self.orderList.add("olives")
        else:
            self.olivesButton.setChecked(False)
            self.olivesButton.setStyleSheet("background-color:rgb(255, 255, 255);")
            if "olives" in self.orderList:
                self.orderList.remove("olives")

    def addEgg(self):
        """
        A method to add eggs to the current order when the corresponding button is pressed.
        """
        if not self.eggButton.isChecked():
            self.eggButton.setChecked(True)
            self.eggButton.setStyleSheet("background-color: rgb(255, 182, 193);")
            if len(self.orderList) < MAX_INGREDIENTS_NUM:
                self.orderList.add("egg")
        else:
            self.eggButton.setChecked(False)
            self.eggButton.setStyleSheet("background-color:rgb(255, 255, 255);")
            if "egg" in self.orderList:
                self.orderList.remove("egg")

    def addCucumber(self):
        """
        A method to add cucumbers to the current order when the corresponding button is pressed.
        """
        if not self.cucumberButton.isChecked():
            self.cucumberButton.setChecked(True)
            self.cucumberButton.setStyleSheet("background-color: rgb(255, 182, 193);")
            if len(self.orderList) < MAX_INGREDIENTS_NUM:
                self.orderList.add("cucumber")
        else:
            self.cucumberButton.setChecked(False)
            self.cucumberButton.setStyleSheet("background-color:rgb(255, 255, 255);")
            if "cucumber" in self.orderList:
                self.orderList.remove("cucumber")

    def addAvocado(self):
        """
        A method to add avocado to the current order when the corresponding button is pressed.
        """
        if not self.avocadoButton.isChecked():
            self.avocadoButton.setChecked(True)
            self.avocadoButton.setStyleSheet("background-color: rgb(255, 182, 193);")
            if len(self.orderList) < MAX_INGREDIENTS_NUM:
                self.orderList.add("avocado")
        else:
            self.avocadoButton.setChecked(False)
            self.avocadoButton.setStyleSheet("background-color:rgb(255, 255, 255);")
            if "avocado" in self.orderList:
                self.orderList.remove("avocado")

    def addLettuce(self):
        """
        A method to add lettuce to the current order when the corresponding button is pressed.
        """
        if not self.lettuceButton.isChecked():
            self.lettuceButton.setChecked(True)
            self.lettuceButton.setStyleSheet("background-color: rgb(255, 182, 193);")
            if len(self.orderList) < MAX_INGREDIENTS_NUM:
                self.orderList.add("lettuce")
        else:
            self.lettuceButton.setChecked(False)
            self.lettuceButton.setStyleSheet("background-color:rgb(255, 255, 255);")
            if "lettuce" in self.orderList:
                self.orderList.remove("lettuce")

    def addKetchup(self):
        """
        A method to add ketchup to the current order when the corresponding button is pressed.
        """
        if not self.ketchupButton.isChecked():
            self.ketchupButton.setChecked(True)
            self.ketchupButton.setStyleSheet("background-color: rgb(255, 182, 193);")
            if len(self.orderList) < MAX_INGREDIENTS_NUM:
                self.orderList.add("ketchup")
        else:
            self.lettuceButton.setChecked(False)
            self.lettuceButton.setStyleSheet("background-color:rgb(255, 255, 255);")
            if "ketchup" in self.orderList:
                self.orderList.remove("ketchup")

    def showPrice(self):
        """
        A method to complete the order and add it to ORDER_LIST. A message is displayed whether the
        order has been successfully placed or not.
        """
        global CURR_ORDER_NUM, ORDER_LIST
        msg = QMessageBox()
        msg.setGeometry(500, 300, 300, 100)
        msg.setIcon(QMessageBox.Icon.Information)

        if CURR_ORDER_NUM >= MAX_ORDERS_NUM:
            msg = QMessageBox()
            msg.setGeometry(500, 500, 100, 100)
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setText("Order cannot be placed")
            msg.setInformativeText("The maximal number of orders has been reached, please try later")
            msg.setWindowTitle("Order not Placed")
            msg.exec()
            widget.close()
            return

        currTime = time.time() - initTime
        if currTime > MAX_ORDER_TIME:
            msg.setText("Order cannot be placed")
            msg.setInformativeText("Fabiola is closing, orders cannot be taken")
            msg.setWindowTitle("Order not Placed")
            msg.exec()
            widget.close()
            return

        CURR_ORDER_NUM += 1
        order = fabiola.Order("sandwich", self.orderList, int(currTime), CURR_ORDER_NUM)
        ORDER_LIST.append(order)
        msg.setText("Order Placed")
        msg.setInformativeText("Order successfully placed\n\nPrice:  " + str(self.price) + "₪")
        msg.setWindowTitle("Order Placed")
        msg.exec()
        openStartScreen()


class SaladMenuScreen(QDialog):
    """
    A class that represents the salad menu screen of the application
    """
    def __init__(self):
        """
        The init method of the class. The method downloads the corresponding .ui file and defines
        the members of the class. If they are labels or buttons, it sets their stylesheet, signals
        and handlers.
        orderList: a set containing all ingredients added to the current order
        price: the current price of the order
        """
        super(SaladMenuScreen, self).__init__()
        loadUi("GUI_sources/saladScreen.ui", self)
        self.orderList = set()
        self.price = 22

        self.imageLabel.setPixmap(QPixmap('GUI_sources/DONA FABIOLA tag.png'))
        self.backButton.setIcon(QIcon("GUI_sources/backbuttonicon5.png"))
        self.backButton.setIconSize(QSize(41, 41))
        self.backButton.clicked.connect(openMenuScreen)
        self.cheeseButton.clicked.connect(self.addCheese)
        self.tomatoButton.clicked.connect(self.addTomato)
        self.onionButton.clicked.connect(self.addOnion)
        self.tunaButton.clicked.connect(self.addTuna)
        self.olivesButton.clicked.connect(self.addOlives)
        self.eggButton.clicked.connect(self.addEgg)
        self.cucumberButton.clicked.connect(self.addCucumber)
        self.avocadoButton.clicked.connect(self.addAvocado)
        self.lettuceButton.clicked.connect(self.addLettuce)
        self.bellButton.clicked.connect(self.addBellPepper)
        self.ketchupButton.clicked.connect(self.addKetchup)
        self.nextButton.clicked.connect(self.showPrice)

    def addCheese(self):
        """
        A method to add cheese to the current order when the corresponding button is pressed.
        """
        if not self.cheeseButton.isChecked():
            self.cheeseButton.setChecked(True)
            self.cheeseButton.setStyleSheet("background-color: rgb(255, 182, 193);")
            self.price += 3
            if len(self.orderList) < MAX_INGREDIENTS_NUM:
                self.orderList.add("cheese")
        else:
            self.cheeseButton.setChecked(False)
            self.cheeseButton.setStyleSheet("background-color:rgb(255, 255, 255);")
            self.price -= 3
            if "cheese" in self.orderList:
                self.orderList.remove("cheese")

    def addTomato(self):
        """
        A method to add tomatoes to the current order when the corresponding button is pressed.
        """
        if not self.tomatoButton.isChecked():
            self.tomatoButton.setChecked(True)
            self.tomatoButton.setStyleSheet("background-color: rgb(255, 182, 193);")
            if len(self.orderList) < MAX_INGREDIENTS_NUM:
                self.orderList.add("tomato")
        else:
            self.tomatoButton.setChecked(False)
            self.tomatoButton.setStyleSheet("background-color:rgb(255, 255, 255);")
            if "tomato" in self.orderList:
                self.orderList.remove("tomato")

    def addOnion(self):
        """
        A method to add onions to the current order when the corresponding button is pressed.
        """
        if not self.onionButton.isChecked():
            self.onionButton.setChecked(True)
            self.onionButton.setStyleSheet("background-color: rgb(255, 182, 193);")
            if len(self.orderList) < MAX_INGREDIENTS_NUM:
                self.orderList.add("onion")
        else:
            self.onionButton.setChecked(False)
            self.onionButton.setStyleSheet("background-color:rgb(255, 255, 255);")
            if "onion" in self.orderList:
                self.orderList.remove("onion")

    def addTuna(self):
        """
        A method to add tuna to the current order when the corresponding button is pressed.
        """
        if not self.tunaButton.isChecked():
            self.tunaButton.setChecked(True)
            self.tunaButton.setStyleSheet("background-color: rgb(255, 182, 193);")
            self.price += 3
            if len(self.orderList) < MAX_INGREDIENTS_NUM:
                self.orderList.add("tuna")
        else:
            self.tunaButton.setChecked(False)
            self.tunaButton.setStyleSheet("background-color:rgb(255, 255, 255);")
            self.price -= 3
            if "tuna" in self.orderList:
                self.orderList.remove("tuna")

    def addOlives(self):
        """
        A method to add olives to the current order when the corresponding button is pressed.
        """
        if not self.olivesButton.isChecked():
            self.olivesButton.setChecked(True)
            self.olivesButton.setStyleSheet("background-color: rgb(255, 182, 193);")
            if len(self.orderList) < MAX_INGREDIENTS_NUM:
                self.orderList.add("olives")
        else:
            self.olivesButton.setChecked(False)
            self.olivesButton.setStyleSheet("background-color:rgb(255, 255, 255);")
            if "olives" in self.orderList:
                self.orderList.remove("olives")

    def addEgg(self):
        """
        A method to add eggs to the current order when the corresponding button is pressed.
        """
        if not self.eggButton.isChecked():
            self.eggButton.setChecked(True)
            self.eggButton.setStyleSheet("background-color: rgb(255, 182, 193);")
            if len(self.orderList) < MAX_INGREDIENTS_NUM:
                self.orderList.add("egg")
        else:
            self.eggButton.setChecked(False)
            self.eggButton.setStyleSheet("background-color:rgb(255, 255, 255);")
            if "egg" in self.orderList:
                self.orderList.remove("egg")

    def addCucumber(self):
        """
        A method to add cucumbers to the current order when the corresponding button is pressed.
        """
        if not self.cucumberButton.isChecked():
            self.cucumberButton.setChecked(True)
            self.cucumberButton.setStyleSheet("background-color: rgb(255, 182, 193);")
            if len(self.orderList) < MAX_INGREDIENTS_NUM:
                self.orderList.add("cucumber")
        else:
            self.cucumberButton.setChecked(False)
            self.cucumberButton.setStyleSheet("background-color:rgb(255, 255, 255);")
            if "cucumber" in self.orderList:
                self.orderList.remove("cucumber")

    def addAvocado(self):
        """
        A method to add avocado to the current order when the corresponding button is pressed.
        """
        if not self.avocadoButton.isChecked():
            self.avocadoButton.setChecked(True)
            self.avocadoButton.setStyleSheet("background-color: rgb(255, 182, 193);")
            if len(self.orderList) < MAX_INGREDIENTS_NUM:
                self.orderList.add("avocado")
        else:
            self.avocadoButton.setChecked(False)
            self.avocadoButton.setStyleSheet("background-color:rgb(255, 255, 255);")
            if "avocado" in self.orderList:
                self.orderList.remove("avocado")

    def addLettuce(self):
        """
        A method to add lettuce to the current order when the corresponding button is pressed.
        """
        if not self.lettuceButton.isChecked():
            self.lettuceButton.setChecked(True)
            self.lettuceButton.setStyleSheet("background-color: rgb(255, 182, 193);")
            if len(self.orderList) < MAX_INGREDIENTS_NUM:
                self.orderList.add("lettuce")
        else:
            self.lettuceButton.setChecked(False)
            self.lettuceButton.setStyleSheet("background-color:rgb(255, 255, 255);")
            if "lettuce" in self.orderList:
                self.orderList.remove("lettuce")

    def addBellPepper(self):
        """
        A method to add bell peppers to the current order when the corresponding button is pressed.
        """
        if not self.bellButton.isChecked():
            self.bellButton.setChecked(True)
            self.bellButton.setStyleSheet("background-color:rgb(255, 182, 193);")
            if len(self.orderList) < MAX_INGREDIENTS_NUM:
                self.orderList.add("bell pepper")
        else:
            self.bellButton.setChecked(False)
            self.bellButton.setStyleSheet("background-color:rgb(255, 255, 255);")
            if "bell pepper" in self.orderList:
                self.orderList.remove("bell pepper")

    def addKetchup(self):
        """
        A method to add ketchup to the current order when the corresponding button is pressed.
        """
        if not self.ketchupButton.isChecked():
            self.ketchupButton.setChecked(True)
            self.ketchupButton.setStyleSheet("background-color: rgb(255, 182, 193);")
            if len(self.orderList) < MAX_INGREDIENTS_NUM:
                self.orderList.add("ketchup")
        else:
            self.lettuceButton.setChecked(False)
            self.lettuceButton.setStyleSheet("background-color:rgb(255, 255, 255);")
            if "ketchup" in self.orderList:
                self.orderList.remove("ketchup")

    def showPrice(self):
        """
        A method to complete the order and add it to ORDER_LIST. A message is displayed whether the
        order has been successfully placed or not.
        """
        global CURR_ORDER_NUM, ORDER_LIST
        msg = QMessageBox()
        msg.setGeometry(500, 300, 300, 100)
        msg.setIcon(QMessageBox.Icon.Information)

        if CURR_ORDER_NUM >= MAX_ORDERS_NUM:
            msg.setText("Order cannot be placed")
            msg.setInformativeText("The maximal number of orders has been reached, please try later")
            msg.setWindowTitle("Order not Placed")
            msg.exec()
            widget.close()
            return

        currTime = time.time() - initTime
        if currTime > MAX_ORDER_TIME:
            msg.setText("Order cannot be placed")
            msg.setInformativeText("Fabiola is closing, orders cannot be taken")
            msg.setWindowTitle("Order not Placed")
            msg.exec()
            widget.close()
            return

        CURR_ORDER_NUM += 1
        order = fabiola.Order("salad", self.orderList, int(currTime), CURR_ORDER_NUM)
        ORDER_LIST.append(order)
        msg.setText("Order Placed")
        msg.setInformativeText("Order successfully placed\n\nPrice:  " + str(self.price) + "₪")
        msg.setWindowTitle("Order Placed")
        msg.exec()
        openStartScreen()


class ToastMenuScreen(QDialog):
    """
    A class that represents the toast menu screen of the application
    """
    def __init__(self):
        """
        The init method of the class. The method downloads the corresponding .ui file and defines
        the members of the class. If they are labels or buttons, it sets their stylesheet, signals
        and handlers.
        orderList: a set containing all ingredients added to the current order
        price: the current price of the order
        """
        super(ToastMenuScreen, self).__init__()
        loadUi("GUI_sources/toastScreen.ui", self)
        self.orderList = set()
        self.price = 16

        self.imageLabel.setPixmap(QPixmap('GUI_sources/DONA FABIOLA tag.png'))
        self.backButton.setIcon(QIcon("GUI_sources/backbuttonicon5.png"))
        self.backButton.setIconSize(QSize(41, 41))
        self.backButton.clicked.connect(openMenuScreen)
        self.cheeseButton.clicked.connect(self.addCheese)
        self.onionButton.clicked.connect(self.addOnion)
        self.tunaButton.clicked.connect(self.addTuna)
        self.olivesButton.clicked.connect(self.addOlives)
        self.ketchupButton.clicked.connect(self.addKetchup)
        self.nextButton.clicked.connect(self.showPrice)

    def addCheese(self):
        """
        A method to add cheese to the current order when the corresponding button is pressed.
        """
        if not self.cheeseButton.isChecked():
            self.cheeseButton.setChecked(True)
            self.cheeseButton.setStyleSheet("background-color: rgb(255, 182, 193);")
            if len(self.orderList) < MAX_INGREDIENTS_NUM:
                self.orderList.add("cheese")
        else:
            self.cheeseButton.setChecked(False)
            self.cheeseButton.setStyleSheet("background-color:rgb(255, 255, 255);")
            if "cheese" in self.orderList:
                self.orderList.remove("cheese")

    def addOnion(self):
        """
        A method to add onions to the current order when the corresponding button is pressed.
        """
        if not self.onionButton.isChecked():
            self.onionButton.setChecked(True)
            self.onionButton.setStyleSheet("background-color: rgb(255, 182, 193);")
            if len(self.orderList) < MAX_INGREDIENTS_NUM:
                self.orderList.add("onion")
        else:
            self.onionButton.setChecked(False)
            self.onionButton.setStyleSheet("background-color:rgb(255, 255, 255);")
            if "onion" in self.orderList:
                self.orderList.remove("onion")

    def addTuna(self):
        """
        A method to add tuna to the current order when the corresponding button is pressed.
        """
        if not self.tunaButton.isChecked():
            self.tunaButton.setChecked(True)
            self.tunaButton.setStyleSheet("background-color: rgb(255, 182, 193);")
            self.price += 3
            if len(self.orderList) < MAX_INGREDIENTS_NUM:
                self.orderList.add("tuna")
        else:
            self.tunaButton.setChecked(False)
            self.tunaButton.setStyleSheet("background-color:rgb(255, 255, 255);")
            self.price -= 3
            if "tuna" in self.orderList:
                self.orderList.remove("tuna")

    def addOlives(self):
        """
        A method to add olives to the current order when the corresponding button is pressed.
        """
        if not self.olivesButton.isChecked():
            self.olivesButton.setChecked(True)
            self.olivesButton.setStyleSheet("background-color: rgb(255, 182, 193);")
            if len(self.orderList) < MAX_INGREDIENTS_NUM:
                self.orderList.add("olives")
        else:
            self.olivesButton.setChecked(False)
            self.olivesButton.setStyleSheet("background-color:rgb(255, 255, 255);")
            if "olives" in self.orderList:
                self.orderList.remove("olives")

    def addKetchup(self):
        """
        A method to add ketchup to the current order when the corresponding button is pressed.
        """
        if not self.ketchupButton.isChecked():
            self.ketchupButton.setChecked(True)
            self.ketchupButton.setStyleSheet("background-color: rgb(255, 182, 193);")
            if len(self.orderList) < MAX_INGREDIENTS_NUM:
                self.orderList.add("ketchup")
        else:
            self.lettuceButton.setChecked(False)
            self.lettuceButton.setStyleSheet("background-color:rgb(255, 255, 255);")
            if "ketchup" in self.orderList:
                self.orderList.remove("ketchup")

    def showPrice(self):
        """
        A method to complete the order and add it to ORDER_LIST. A message is displayed whether the
        order has been successfully placed or not.
        """
        global CURR_ORDER_NUM, ORDER_LIST
        msg = QMessageBox()
        msg.setGeometry(500, 300, 300, 100)
        msg.setIcon(QMessageBox.Icon.Information)

        if CURR_ORDER_NUM >= MAX_ORDERS_NUM:
            msg.setText("Order cannot be placed")
            msg.setInformativeText("The maximal number of orders has been reached, please try later")
            msg.setWindowTitle("Order not Placed")
            msg.exec()
            widget.close()
            return

        currTime = time.time() - initTime
        if currTime > MAX_ORDER_TIME:
            msg.setText("Order cannot be placed")
            msg.setInformativeText("Fabiola is closing, orders cannot be taken")
            msg.setWindowTitle("Order not Placed")
            msg.exec()
            widget.close()
            return

        CURR_ORDER_NUM += 1
        order = fabiola.Order("toast", self.orderList, int(currTime), CURR_ORDER_NUM)
        ORDER_LIST.append(order)
        msg.setText("Order Placed")
        msg.setInformativeText("Order successfully placed\n\nPrice:  " + str(self.price) + "₪")
        msg.setWindowTitle("Order Placed")
        msg.exec()
        openStartScreen()


class DrinksMenuScreen(QDialog):
    """
    A class that represents the drink menu screen of the application
    """
    def __init__(self):
        """
        The init method of the class. The method downloads the corresponding .ui file and defines
        the members of the class. If they are labels or buttons, it sets their stylesheet, signals
        and handlers.
        orderList: a set containing all ingredients added to the current order
        price: the current price of the order
        """
        super(DrinksMenuScreen, self).__init__()
        loadUi("GUI_sources/drinksScreen.ui", self)
        self.orderList = set()
        self.price = 6

        self.imageLabel.setPixmap(QPixmap('GUI_sources/DONA FABIOLA tag.png'))
        self.backButton.setIcon(QIcon("GUI_sources/backbuttonicon5.png"))
        self.backButton.setIconSize(QSize(41, 41))
        self.backButton.clicked.connect(openMenuScreen)
        self.coffeeButton.clicked.connect(self.addCoffee)
        self.oatmilkButton.clicked.connect(self.addOatmilk)
        self.iceButton.clicked.connect(self.addIce)
        self.plasticButton.clicked.connect(self.choosePlastic)
        self.reusableButton.clicked.connect(self.chooseReusable)
        self.nextButton.clicked.connect(self.showPrice)

    def addCoffee(self):
        """
        A method to add coffee to the current order when the corresponding button is pressed.
        """
        if not self.coffeeButton.isChecked():
            self.coffeeButton.setChecked(True)
            self.coffeeButton.setStyleSheet("background-color: rgb(255, 182, 193);")
            self.price += 6
            if len(self.orderList) < MAX_INGREDIENTS_NUM:
                self.orderList.add("coffee")
        else:
            self.coffeeButton.setChecked(False)
            self.coffeeButton.setStyleSheet("background-color:rgb(255, 255, 255);")
            self.price -= 6
            if "coffee" in self.orderList:
                self.orderList.remove("coffee")

    def addMilk(self):
        """
        A method to add milk to the current order when the corresponding button is pressed.
        """
        if not self.milkButton.isChecked():
            self.milkButton.setChecked(True)
            self.milkButton.setStyleSheet("background-color: rgb(255, 182, 193);")
            if len(self.orderList) < MAX_INGREDIENTS_NUM:
                self.orderList.add("milk")
        else:
            self.milkButton.setChecked(False)
            self.milkButton.setStyleSheet("background-color:rgb(255, 255, 255);")
            if "milk" in self.orderList:
                self.orderList.remove("milk")

    def addOatmilk(self):
        """
        A method to add oat milk to the current order when the corresponding button is pressed.
        """
        if not self.oatmilkButton.isChecked():
            self.oatmilkButton.setChecked(True)
            self.oatmilkButton.setStyleSheet("background-color: rgb(255, 182, 193);")
            self.price += 2
            if len(self.orderList) < MAX_INGREDIENTS_NUM:
                self.orderList.add("oat milk")
        else:
            self.oatmilkButton.setChecked(False)
            self.oatmilkButton.setStyleSheet("background-color:rgb(255, 255, 255);")
            self.price -= 2
            if "oat milk" in self.orderList:
                self.orderList.remove("oat milk")

    def addIce(self):
        """
        A method to add ice to the current order when the corresponding button is pressed.
        """
        if not self.iceButton.isChecked():
            self.iceButton.setChecked(True)
            self.iceButton.setStyleSheet("background-color: rgb(255, 182, 193);")
            self.price += 4
            if len(self.orderList) < MAX_INGREDIENTS_NUM:
                self.orderList.add("ice")
        else:
            self.iceButton.setChecked(False)
            self.iceButton.setStyleSheet("background-color: rgb(255, 255, 255);")
            self.price -= 4
            if "ice" in self.orderList:
                self.orderList.remove("ice")

    def choosePlastic(self):
        """
        A method to select a plastic cup for the current order when the corresponding button is
        pressed.
        """
        if not self.plasticButton.isChecked():
            if self.reusableButton.isChecked():
                msg = QMessageBox()
                msg.setGeometry(500, 500, 100, 100)
                msg.setIcon(QMessageBox.Icon.Information)
                msg.setText("Reusable Cup is selected")
                msg.setInformativeText(
                    "Deselect reusable cup option first, and then select plastic cup")
                msg.setWindowTitle("Cup Type Selection")
                msg.exec()
                return
            self.plasticButton.setChecked(True)
            self.plasticButton.setStyleSheet("background-color: rgb(255, 182, 193);")
            self.price += 2
        else:
            self.plasticButton.setChecked(False)
            self.plasticButton.setStyleSheet("background-color:rgb(255, 255, 255);")
            self.price -= 2

    def chooseReusable(self):
        """
        A method to select a reusable cup for the current order when the corresponding button is
        pressed.
        """
        if not self.reusableButton.isChecked():
            if self.plasticButton.isChecked():
                msg = QMessageBox()
                msg.setGeometry(500, 500, 100, 100)
                msg.setIcon(QMessageBox.Icon.Information)
                msg.setText("Plastic Cup is selected")
                msg.setInformativeText(
                    "Deselect plastic cup option first, and then select reusable cup")
                msg.setWindowTitle("Cup Type Selection")
                msg.exec()
                return
            self.reusableButton.setChecked(True)
            self.reusableButton.setStyleSheet("background-color: rgb(255, 182, 193);")
        else:
            self.reusableButton.setChecked(False)
            self.reusableButton.setStyleSheet("background-color:rgb(255, 255, 255);")

    def showPrice(self):
        """
        A method to complete the order and add it to ORDER_LIST. A message is displayed whether the
        order has been successfully placed or not.
        """
        global CURR_ORDER_NUM, ORDER_LIST
        msg = QMessageBox()
        msg.setGeometry(500, 500, 100, 100)
        msg.setIcon(QMessageBox.Icon.Information)

        if CURR_ORDER_NUM >= MAX_ORDERS_NUM:
            msg.setText("Order cannot be placed")
            msg.setInformativeText("The maximal number of orders has been reached, please try later")
            msg.setWindowTitle("Order not Placed")
            msg.exec()
            widget.close()
            return

        currTime = time.time() - initTime
        if currTime > MAX_ORDER_TIME:
            msg.setText("Order cannot be placed")
            msg.setInformativeText("Fabiola is closing, orders cannot be taken")
            msg.setWindowTitle("Order not Placed")
            msg.exec()
            widget.close()
            return

        CURR_ORDER_NUM += 1
        order = fabiola.Order("coffee", self.orderList, int(currTime), CURR_ORDER_NUM)
        ORDER_LIST.append(order)
        msg.setText("Order Placed")
        msg.setInformativeText("Order successfully placed\n\nPrice: " + str(self.price) + "₪")
        msg.setWindowTitle("Order Placed")
        msg.exec()
        openStartScreen()


def run_Gui():
    """
    A main function to run the program with input obtained by the app interface.
    :return: the results of an online simulator that runs using different online agent according to
    the heuristic implemented.
    """
    welcome = StartScreen()
    widget.setWindowTitle("Fabiola")
    widget.addWidget(welcome)
    widget.setFixedHeight(HEIGHT)
    widget.setFixedWidth(WIDTH)
    widget.show()
    ret_val = app.exec()
    if ret_val != 0:
        app.exit(ret_val)

    online = OnlineSimulator(OnlineMainAgent(lost_score_heuristic), pre_as_set=set(ORDER_LIST))
    return online
