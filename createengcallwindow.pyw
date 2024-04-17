from PyQt5.QtCore import (
    Qt,
    QSortFilterProxyModel
    )

from PyQt5.QtGui import (
    QFont,
    QIcon,
    QTextCharFormat,
    QIntValidator,
    QStandardItemModel,
    QStandardItem
    )

from PyQt5.QtWidgets import (
        QMdiSubWindow,
        QComboBox,
        QLabel,
        QLineEdit,
        QCompleter,
        QVBoxLayout,
        QHBoxLayout,
        QWidget,
        QPlainTextEdit,
        QPushButton,
        QMessageBox
    )


from myExceptions import *
import clientscontainer
import productscontainer

from callscontainer import CallCreator

__version__ = "2.0.0"


###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################
       

class MyQFilterComboBox(QComboBox):
    """
    This class extends the QcomboBox, adding a text filter
    """
    def __init__(self, parent=None):
        super(MyQFilterComboBox, self).__init__(parent)
        # --> self configuration #
        self.setFocusPolicy(Qt.StrongFocus)
        self.setEditable(True)
        self.myCompleter = QCompleter(self)
        self.setMinimumWidth(177)
        #self.lineEdit().setEnabled(False)

        regularFont = QFont()
        regularFont.setBold(False)
        self.setFont(regularFont)
        
        # --> new functionalities #
        self.myCompleter.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.pFilterModel = QSortFilterProxyModel(self)
        self.pFilterModel.setFilterCaseSensitivity(Qt.CaseInsensitive)

        self.myCompleter.setPopup(self.view())
        self.setCompleter(self.myCompleter)

        self.lineEdit().textEdited.connect(self.pFilterModel.setFilterFixedString)
        self.lineEdit().textEdited.connect(self.textToUpper)
        self.myCompleter.activated.connect(self.setTextIfCompleterIsClicked)

###############################################################################################################################################################################

    def textToUpper(self, text):
        self.lineEdit().setText(self.lineEdit().text().upper())

###############################################################################################################################################################################
    
    def setModel(self, model):
        super(MyQFilterComboBox, self).setModel(model)
        self.pFilterModel.setSourceModel(model)
        self.myCompleter.setModel(self.pFilterModel)

###############################################################################################################################################################################

    def focusInEvent(self, event):
        self.myCompleter.complete()

###############################################################################################################################################################################

    def clearSearchFilter(self):
        self.myCompleter.setCompletionPrefix("")
        self.pFilterModel.setFilterFixedString("")
        self.lineEdit().clear()
        self.setCurrentIndex(-1)

###############################################################################################################################################################################

    def focusOutEvent(self, event):
        index = self.findText(self.lineEdit().text())
        if index > 0:
            self.setCurrentIndex(index)
            self.clearFocus()
        else:
            self.myCompleter.setCompletionPrefix("")
            self.pFilterModel.setFilterFixedString("")
            self.lineEdit().clear()
            self.clearFocus()
            self.setCurrentIndex(-1)

###############################################################################################################################################################################
    
    def setModelColumn(self, column):
        self.myCompleter.setCompletionColumn(column)
        self.pFilterModel.setFilterKeyColumn(column)
        super(MyQFilterComboBox, self).setModelColumn(column)

###############################################################################################################################################################################

    def setTextIfCompleterIsClicked(self, text):
        index = self.findText(text)
        if index > 0:
            self.setCurrentIndex(index)
            self.clearFocus()
        else:
            self.myCompleter.setCompletionPrefix("")
            self.pFilterModel.setFilterFixedString("")
            self.lineEdit().clear()
            self.clearFocus()
            self.setCurrentIndex(-1)


###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################

class MyQLabel(QLabel):
    """
    This class reimplements the qlabel class
    """
    def __init__(self, text="", parent=None):
        super(MyQLabel, self).__init__(text, parent)
        boldFont = QFont()
        boldFont.setBold(True)

        self.setFixedWidth(80)
        self.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.setFont(boldFont)

###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################


class MyQNumberLineEdit(QLineEdit):
    """
    This class reimplements qlineedit class
    """
    def __init__(self, parent=None):
        super(MyQNumberLineEdit, self).__init__(parent)

        regularFont = QFont()
        regularFont.setBold(False)
        self.setFont(regularFont)
        self.setMaxLength(6)
        # --> Validator that allows only integers #
        validator = QIntValidator()
        self.setValidator(validator)

        self.setFixedWidth(50)

    def focusInEvent(self, event):
        if len(self.text()):
            self.setText(str(int(self.text())))



###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################

class MyQLineEdit(QLineEdit):
    """
    This class reimplements the qlineedit class
    """
    def __init__(self, parent=None):
        super(MyQLineEdit, self).__init__(parent)

        regularFont = QFont()
        regularFont.setBold(False)
        
        self.setMinimumWidth(204)
        self.setFont(regularFont)

###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################


class CreateEngCallWindow(QMdiSubWindow):
    """
    This class is responsible for rendering the "Criar Chamado de Engenharia" window
    as a MDI sub Window and for managing the data inside it
    """
    # --> Constant id, used for location inside the openedSubWindows dictionary in the main window #
    SUBWINDOWID = "createengcallwindow"
    
    def __init__(self, parent=None):
        super(CreateEngCallWindow, self).__init__(parent)
        self.parent = parent
        self.loggedUser = parent.loggedUser
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowFlags(Qt.SubWindow | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)

        self.clientsList = clientscontainer.ClientsContainer()
        self.productsList = productscontainer.ProductsContainer()

        #############################
        #### WINDOW LAYOUT BUILD ####
        #############################
        boldFont = QFont()
        boldFont.setBold(True)

        #cliente
        clientLabel = MyQLabel("Cliente: ")
        self.clientComboBox = MyQFilterComboBox()

        firstLineLayout = QHBoxLayout()
        firstLineLayout.addWidget(clientLabel)
        firstLineLayout.addWidget(self.clientComboBox)
        
        #produto
        productLabel = MyQLabel("Produto: ")
        self.productComboBox = MyQFilterComboBox()

        secondLineLayout = QHBoxLayout()
        secondLineLayout.addWidget(productLabel)
        secondLineLayout.addWidget(self.productComboBox)                                     

        #dispositivo de teste
        deviceLabel = MyQLabel("Dispositivo: ")
        self.deviceField = MyQNumberLineEdit()

        thirdLineLayout = QHBoxLayout()
        thirdLineLayout.addWidget(deviceLabel)
        thirdLineLayout.addWidget(self.deviceField)
        thirdLineLayout.addStretch(1)
        
        #Breve descrição sobre o chamado
        actionTakenLabel = QLabel("Descrição do chamado: ")
        actionTakenLabel.setFont(boldFont)
        
        self.charCounter = QLabel("255")
        self.charCounter.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.charCounter.setStyleSheet('color: red')
        self.charCounter.setFont(boldFont)

        self.callDescription = QPlainTextEdit()
        self.callDescription.setMinimumWidth(300)
        self.callDescription.setMaximumHeight(100)

        self.textFormat = QTextCharFormat()
        self.textFormat.setFontCapitalization(QFont.AllUppercase)

        self.callDescription.setCurrentCharFormat(self.textFormat)
        
        fourthLineLayout = QHBoxLayout()
        fourthLineLayout.addWidget(actionTakenLabel)
        fourthLineLayout.addStretch(1)
        fourthLineLayout.addWidget(self.charCounter)

        # botoes

        createCallButton = QPushButton(" Criar Chamado ")
        createCallButton.setMinimumWidth(100)
        cancelButton = QPushButton(" Cancelar ")
        cancelButton.setMinimumWidth(100)

        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch(1)
        buttonLayout.addWidget(createCallButton)
        buttonLayout.addWidget(cancelButton)
        buttonLayout.addStretch(1)
        
        #######################
        #### WINDOW LAYOUT ####
        #######################
        
        windowLayout = QVBoxLayout()
        windowLayout.addLayout(firstLineLayout)
        windowLayout.addLayout(secondLineLayout)
        windowLayout.addLayout(thirdLineLayout)
        windowLayout.addLayout(fourthLineLayout)
        windowLayout.addWidget(self.callDescription)
        windowLayout.addLayout(buttonLayout)

        centralWidget = QWidget()
        centralWidget.setLayout(windowLayout)
        self.setWidget(centralWidget)
        self.setWindowIcon(QIcon(":/engineer_call.png"))
        self.setWindowTitle("Criar Chamado de Engenharia")

        # --> Event that counts the characteres #
        self.callDescription.textChanged.connect(self.calculateCharacters)
        self.clientComboBox.currentIndexChanged.connect(self.populateProductsComboBox)
        self.deviceField.editingFinished.connect(self.completeWithZeros)
        cancelButton.clicked.connect(self.close)
        createCallButton.clicked.connect(self.createEngineeringCall)

        ###################
        #### TAB ORDER ####
        ###################
        self.populateClientComboBox()
        self.callDescription.setFocus()


###############################################################################################################################################################################
    def createEngineeringCall(self):
        message = ""
        failed = False

        if self.clientComboBox.currentIndex() <= 0:
            failed = True
            message += "\t - Selecione o Cliente relacionado ao chamado\n"

        if self.productComboBox.currentIndex() <= 0:
            failed = True
            message += "\t - Selecione o Produto relacionado ao chamado\n"

        if not len(self.deviceField.text()):
            failed = True
            message += "\t - Insira o código do Dispositivo relacionado ao chamado\n"
        else:
            if not int(self.deviceField.text()):
                failed = True
                message += "\t - Insira o código do Dispositivo relacionado ao chamado\n"

        if not len(self.callDescription.toPlainText()):
            failed = True
            message += "\t - Insira uma breve descrição sobre o problema encontrado\n"
    
        
        if failed:
            message = "Falha ao criar Chamado:\n" + message
                
            messageBox = QMessageBox()
            messageBox.setText(message)
            messageBox.setWindowTitle("Erro!")
            messageBox.setIcon(QMessageBox.Critical)
            messageBox.setWindowIcon(QIcon(":/warning_icon.png"))
            messageBox.exec_()
            
            return
        
        callCreator = CallCreator(self.clientComboBox.currentData(),
                                  self.productComboBox.currentData(),
                                  self.deviceField.text(),
                                  self.callDescription.toPlainText(),
                                  self.loggedUser["login"])

        try:
            callCreator.createEngineerCall()
        except DatabaseConnectionError as error:
            place, cause = error.args
            message = "Falha em: " + place + "\nErro: " +cause
            messageBox = QMessageBox()
            messageBox.setText(message)
            messageBox.setWindowTitle("Erro!")
            messageBox.setIcon(QMessageBox.Critical)
            messageBox.setWindowIcon(QIcon(":/warning_icon.png"))
            messageBox.exec_()
            return
        except Exception as error:
            message = "\nErro: " +str(error)
            messageBox = QMessageBox()
            messageBox.setText(message)
            messageBox.setWindowTitle("Erro!")
            messageBox.setIcon(QMessageBox.Critical)
            messageBox.setWindowIcon(QIcon(":/warning_icon.png"))
            messageBox.exec_()
            return

        messageBox = QMessageBox()
        messageBox.setText("Chamado de Engenharia criado com sucesso!")
        messageBox.setWindowTitle("Sucesso!")
        messageBox.setIcon(QMessageBox.Information)
        messageBox.setWindowIcon(QIcon(":/information.png"))
        messageBox.exec_()

        self.close()

###############################################################################################################################################################################
    def completeWithZeros(self):
        device = self.deviceField.text()
        if len(device):
            self.deviceField.setText('{0:06d}'.format(int(device)))
        
###############################################################################################################################################################################


    def calculateCharacters(self):
        """
        This method is called when a key is pressed in the action taken description, decrementing its counter
        """

        # --> Line inserted because the uppercase is lost when the backspace is pressed #
        self.callDescription.setCurrentCharFormat(self.textFormat)
        
        textLength = len(self.callDescription.toPlainText())
        if textLength <= 255:
           self.charCounter.setText(str(255 - textLength))
        else:
            text = self.callDescription.toPlainText()
            self.callDescription.setPlainText(text[:255])
            cursor = self.callDescription.textCursor()
            cursor.setPosition(textLength - 1)
            self.callDescription.setTextCursor(cursor)



###############################################################################################################################################################################

    def populateClientComboBox(self):
        """
        This method loads all the active clients
        """        
        try:
            self.clientsList.loadActiveClients()
        except DatabaseConnectionError as error:
            message = "Falha em: " + place + "\nErro: " +cause
            messageBox = QMessageBox()
            messageBox.setText(message)
            messageBox.setWindowTitle("Erro!")
            messageBox.setIcon(QMessageBox.Critical)
            messageBox.setWindowIcon(QIcon(":/warning_icon.png"))
            messageBox.exec_()
            return

        model = QStandardItemModel()
        item = QStandardItem("")
        item.setData(-1, Qt.UserRole)
        model.setItem(0, 0, item)
        for row, client in enumerate(self.clientsList):
            item = QStandardItem(client.clientName)
            item.setData(client.clientId, Qt.UserRole)
            model.setItem((row+1), 0, item)

        self.clientComboBox.setModel(model)
        self.clientComboBox.setModelColumn(0)
        self.clientComboBox.setCurrentIndex(0)

###############################################################################################################################################################################

    def populateProductsComboBox(self, index):
        """
        This method is called when the client combobox change value.
        It will load all the client products.
        """
        clientId = self.clientComboBox.itemData(index)
        if index > -1:
            try:
                self.productsList.loadProductsFromClient(clientId, True)
            except DatabaseConnectionError as error:
                message = "Falha em: " + place + "\nErro: " +cause
                messageBox = QMessageBox()
                messageBox.setText(message)
                messageBox.setWindowTitle("Erro!")
                messageBox.setIcon(QMessageBox.Critical)
                messageBox.setWindowIcon(QIcon(":/warning_icon.png"))
                messageBox.exec_()
                return

            model = QStandardItemModel()
            item = QStandardItem("")
            item.setData(-1, Qt.UserRole)
            model.setItem(0, 0, item)
            
            for row, product in enumerate(self.productsList):
                item = QStandardItem(product.productName)
                item.setData(int(product.productId), Qt.UserRole)
                model.setItem((row+1), 0, item)

            self.productComboBox.setModel(model)
            self.productComboBox.setModelColumn(0)
            self.productComboBox.setCurrentIndex(0)
            
        else:
            self.productComboBox.clear()

###############################################################################################################################################################################
       
    def closeEvent(self, event):
        """
        This method remove its reference from its parent opened sub window list before being closed
        """
        del self.parent.openedSubWindows[self.SUBWINDOWID]
        self.close()

        
