import os

from PyQt5.QtCore import (
    Qt,
    QSortFilterProxyModel
    )

from PyQt5.QtGui import (
    QFont,
    QIcon,
    QTextCharFormat,
    QStandardItemModel,
    QStandardItem,
    QIntValidator
    )

from PyQt5.QtWidgets import (
    QDialog,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLineEdit,
    QSpinBox,
    QCheckBox,
    QComboBox,
    QCompleter,
    QPushButton,
    QFileDialog,
    QPlainTextEdit,
    QLayout,
    QMessageBox
    )


import qrc_resources
import clientscontainer
import invoicescontainer
import devicescontainer
from magicDB import *
from myExceptions import *



__version__ = "2.0.0"

###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################


class MyQNumberLineEdit(QLineEdit):
    """
    This class reimplements qlineedit class
    """
    def __init__(self, parent=None):
        super(MyQNumberLineEdit, self).__init__(parent)
        
        # --> Validator that allows only integers #
        validator = QIntValidator()
        self.setValidator(validator)

        self.setFixedWidth(100)
        

###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################

class MyQLabel(QLabel):
    """
    This class reimplements the qlabel class
    """
    def __init__(self, text="", parent=None):
        super(MyQLabel, self).__init__(text, parent)
        # --> define a bold Font #        
        boldFont = QFont()
        boldFont.setBold(True)
        self.setFont(boldFont)

        self.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.setMinimumWidth(10)


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
        self.lineEdit().setEnabled(False)
        
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

class MyQCheckBox(QCheckBox):
    """
    This class reimplements the QCheckBox class
    """
    def __init__(self, text="", dependentFields=None, parent=None):
        super(MyQCheckBox, self).__init__(text, parent)

        # --> appearance #
        boldFont = QFont()
        boldFont.setBold(True)
        self.setFont(boldFont)
        self.dependentFields = dependentFields

        self.setMinimumWidth(10)

        # --> functionalities #
        if dependentFields:
            for field in dependentFields:
                self.stateChanged.connect(field.lineEdit().setEnabled)

        
###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################


class MyQFileLineEdit(QLineEdit):
    """
    This class was created to replace the mousePressEvent
    """
    def __init__(self):
        super(MyQFileLineEdit, self).__init__()

###############################################################################################################################################################################
    
    def mousePressEvent(self, event):
        path = os.path.join(os.path.join(os.environ['USERPROFILE']), "Desktop")
        filePath, viewType = QFileDialog.getOpenFileName(self, "Selecione a Imagem do Dispositivo", path, "Arquivos de Imagem ( *.jpg *.png)")
        self.setText(filePath)


###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################


class MyQPushButton(QPushButton):
    """
    This class reimplements the QPushButton
    """
    def __init__(self, text="", parent=None):
        super(MyQPushButton, self).__init__(text, parent)
        
        self.setFixedWidth(103)
        self.setCursor(Qt.PointingHandCursor)

    

###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################

class DeviceRegisterWindow(QDialog):
    """
    This class is responsible for rendering the receipt upload window
    """
    def __init__(self, parent=None):
        super(DeviceRegisterWindow, self).__init__(parent)
        self.parent = parent
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setAttribute(Qt.WA_DeleteOnClose)
        
        self.clientsList = clientscontainer.ClientsContainer()
        self.invoicesList = invoicescontainer.InvoicesContainer()

        #######################
        # --> INTERFACE BUILD #
        #######################

        # --> descrição #
        descriptionLabel = MyQLabel("Descrição: ")
        self.descriptionField = QLineEdit()
        self.descriptionField.setMinimumWidth(273)
        self.descriptionField.setMaxLength(40)

        # --> quantidade #
        quantityLabel = MyQLabel("Quantidade: ")
        quantityLabel.setMinimumWidth(80)
        self.quantityField = QSpinBox()
        self.quantityField.setMinimum(1)
        self.quantityField.setMinimumWidth(40)
        #self.quantityField.setReadOnly(True)
        self.quantityField.setFocusPolicy(Qt.NoFocus)
        
        # --> codigo SAP #
        sapCodeLabel = MyQLabel("Código SAP: ")
        sapCodeLabel.setMinimumWidth(80)
        self.sapCodeField = QLineEdit()
        self.sapCodeField.setFixedWidth(80)
        
        # --> NF #
        invoiceLabel = MyQLabel("Nota Fiscal: ")
        invoiceLabel.setMinimumWidth(80)

        self.invoiceComboBox = MyQFilterComboBox()
        self.invoiceComboBox.setFixedWidth(80)
        self.invoiceComboBox.lineEdit().setEnabled(False)


        # --> Cliente #
        self.clientComboBox = MyQFilterComboBox()
        self.clientComboBox.lineEdit().setEnabled(False)
       
        # --> CheckBox cliente e nota fiscal #
        self.clientCheckBox = MyQCheckBox("Propriedade do Cliente: ", [self.clientComboBox, self.invoiceComboBox])
       
        # --> Imagem #
        imageLabel = MyQLabel("Imagem do Dispositivo: ")
        self.deviceImagePath = MyQFileLineEdit()
        self.deviceImageButton = MyQPushButton(" Selecionar Arquivo ")

        # --> Com manutenção preventiva #
        self.maintenanceCheckBox = MyQCheckBox("Com Manutenção Preventiva")

        # --> Observações #
        observationsLabel = MyQLabel("Observações: ")
        self.observationsField = QPlainTextEdit()
        self.observationsField.setFixedHeight(120)

        self.textFormat = QTextCharFormat()
        self.textFormat.setFontCapitalization(QFont.AllUppercase)

        self.observationsField.setCurrentCharFormat(self.textFormat)

        
        self.charCounter = MyQLabel("1000")
        self.charCounter.setStyleSheet('color: red')
        
        # --> Botoes #

        registerButton = MyQPushButton(" Cadastrar ")
        cancelButton = MyQPushButton(" Cancelar ")

        # --> first row fields layout #
        firstRowLayout = QHBoxLayout()
        firstRowLayout.addWidget(descriptionLabel)
        firstRowLayout.addWidget(self.descriptionField)
        firstRowLayout.addSpacing(15)
        firstRowLayout.addWidget(sapCodeLabel)
        firstRowLayout.addWidget(self.sapCodeField)
        firstRowLayout.addSpacing(15)
        firstRowLayout.addWidget(quantityLabel)
        firstRowLayout.addWidget(self.quantityField)
        firstRowLayout.addStretch(1)


        # --> second row fields layout #
        secondRowLayout = QHBoxLayout()
        secondRowLayout.addWidget(self.clientCheckBox)
        secondRowLayout.addWidget(self.clientComboBox)
        secondRowLayout.addSpacing(15)
        secondRowLayout.addWidget(invoiceLabel)
        secondRowLayout.addWidget(self.invoiceComboBox)
        secondRowLayout.addStretch(1)

        # --> third row Fields Layout #
        thirdRowLayout = QHBoxLayout()
        thirdRowLayout.addWidget(imageLabel)
        thirdRowLayout.addWidget(self.deviceImagePath)
        thirdRowLayout.addWidget(self.deviceImageButton)

        # --> fourth row Fields Layout #
        fourthRowLayout = QHBoxLayout()
        fourthRowLayout.addWidget(self.maintenanceCheckBox)
        fourthRowLayout.addStretch(1)

        # --> fifth row Fields Layout #
        fifthRowLayout = QHBoxLayout()
        fifthRowLayout.addWidget(observationsLabel)
        fifthRowLayout.addStretch(1)
        fifthRowLayout.addWidget(self.charCounter)

        # --> sixth row Fields Layout #
        sixthRowLayout = QHBoxLayout()
        sixthRowLayout.addStretch(1)
        sixthRowLayout.addWidget(registerButton)
        sixthRowLayout.addWidget(cancelButton)
        sixthRowLayout.addStretch(1)
        
        

        # --> Build the window Layout #
        windowLayout = QVBoxLayout()
        windowLayout.addLayout(firstRowLayout)
        windowLayout.addLayout(secondRowLayout)
        windowLayout.addLayout(fourthRowLayout)
        windowLayout.addLayout(fifthRowLayout)
        windowLayout.addWidget(self.observationsField)
        windowLayout.addLayout(thirdRowLayout)
        windowLayout.addLayout(sixthRowLayout)
        self.setLayout(windowLayout)


        self.setWindowIcon(QIcon(":/scanner.png"))
        self.setWindowTitle("Cadastro de Novo Dispositivo")
        self.layout().setSizeConstraint(QLayout.SetFixedSize)

        #####################
        #### --> SIGNALS ####
        #####################

        self.observationsField.textChanged.connect(self.changeCharCounter)
        self.clientComboBox.currentIndexChanged.connect(self.populateInvoicesComboBox)
        self.clientCheckBox.stateChanged.connect(self.checkClientsInvoicesComboBox)
        self.descriptionField.textChanged.connect(self.setUpperCaseDescription)
        self.deviceImageButton.clicked.connect(self.imageFileDialog)

        registerButton.clicked.connect(self.registerDevice)
        cancelButton.clicked.connect(self.close)

###############################################################################################################################################################################

    def imageFileDialog(self):
        path = os.path.join(os.path.join(os.environ['USERPROFILE']), "Desktop")
        filePath, viewType = QFileDialog.getOpenFileName(self, "Selecione a Imagem do Dispositivo", path, "Arquivos de Imagem ( *.jpg *.png)")
        self.deviceImagePath.setText(filePath)

###############################################################################################################################################################################


    def fieldsValidator(self):
        """
        Verifies all the mandatory fields of the form, returning True if everything is ok
        """
        missingFields = []

        if len(self.descriptionField.text()) == 0:
            missingFields.append("Descrição")

        if len(self.sapCodeField.text()) == 0 and self.clientCheckBox.isChecked():
            missingFields.append("Código SAP")

        if self.clientCheckBox.isChecked():
            if self.clientComboBox.currentIndex() <= 0:
                missingFields.append("Cliente")

            if self.invoiceComboBox.currentIndex() <= 0:
                missingFields.append("Nota Fiscal")

        
        if len(missingFields) > 0:
            fields = ",\n\t".join(missingFields)
            
            messageBox = QMessageBox()
            messageBox.setText("Os campos abaixo são de preenchimento obrigatório:\n\t"+fields)
            messageBox.setWindowTitle("Atenção!")
            messageBox.setIcon(QMessageBox.Warning)
            messageBox.setWindowIcon(QIcon(":/warning_icon.png"))
            messageBox.exec_()

            return False

        else:
            messageBox = QMessageBox()
            messageBox.setIcon(QMessageBox.Question)
            messageBox.setWindowIcon(QIcon(":/question.png"))
            messageBox.setWindowTitle("Cadastro de Novo Dispositivo")
            messageBox.setText("Confirmar cadastro do dispositivo?")
            messageBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            messageBox.button(QMessageBox.Yes).setText("Sim")
            messageBox.button(QMessageBox.No).setText("Não")
        
            messageBox.exec_()
        
            # --> If the Yes button was clicked #
            if messageBox.clickedButton() == messageBox.button(QMessageBox.No):
                return False
            
            return True

###############################################################################################################################################################################
        
    def registerDevice(self):
        """
        This method is called when the button 'Cadastrar' is clicked.
        It verifies if the fields are filled up and then insert the data into the
        database using the class devicescontainer.DevicesRecorder
        """
        if not self.fieldsValidator():
            return


        ########################################
        #### --> create the data dictionary ####
        ########################################
        
        deviceData = {}

        deviceData["quantity"] = self.quantityField.value()
        deviceData["description"] = self.descriptionField.text()
        deviceData["SAPCode"] = self.sapCodeField.text()
        deviceData["clientProperty"] = self.clientCheckBox.isChecked()
        if self.clientCheckBox.isChecked():
            deviceData["client"] = self.clientComboBox.itemData(self.clientComboBox.currentIndex())
            deviceData["invoice"] = self.invoiceComboBox.itemData(self.invoiceComboBox.currentIndex())
        else:
            deviceData["client"] = 0
            deviceData["invoice"] = 0

        deviceData["observation"] = self.observationsField.toPlainText().upper()
        deviceData["image"] = self.deviceImagePath.text()
        deviceData["maintenance"] = self.maintenanceCheckBox.isChecked()

        ####################################################################
        # --> try to flush the data to the database, creating a new device #
        ####################################################################

        deviceRecorder = devicescontainer.DevicesRecorder(deviceData)

        try:
            deviceRecorder.registerDevice()
                         
        except Exception as error:
            cause = "Erro: {0}".format(error.args)
            message = cause + "\nTente novamente. Se o erro persistir contate o administrador do sistema"
                    
            messageBox = QMessageBox()
            messageBox.setText(message)
            messageBox.setWindowTitle("Erro!")
            messageBox.setIcon(QMessageBox.Critical)
            messageBox.setWindowIcon(QIcon(":/warning_icon.png"))
            messageBox.exec_()
            self.parent.close()
            return

        # update the table of the parent window
        if self.parent.SUBWINDOWID == "listdeviceswindow":
            self.parent.updateDevicesTable()
        
        if self.clientCheckBox.isChecked():
            messageBox = QMessageBox()
            messageBox.setIcon(QMessageBox.Question)
            messageBox.setWindowIcon(QIcon(":/question.png"))
            messageBox.setWindowTitle("Sucesso!")
            messageBox.setText("Dispositivo(s) cadastrado(s) com sucesso.\nCadastrar outro dispositivo nesta nota fiscal?")
            messageBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            messageBox.button(QMessageBox.Yes).setText("Sim")
            messageBox.button(QMessageBox.No).setText("Não")
                
            messageBox.exec_()
                
            # --> If the Yes button was clicked #
            if messageBox.clickedButton() == messageBox.button(QMessageBox.No):
                self.resetFields()
            else:
                self.resetFields(True)
        else:
            messageBox = QMessageBox()
            messageBox.setIcon(QMessageBox.Information)
            messageBox.setWindowIcon(QIcon(":/warning_icon.png"))
            messageBox.setWindowTitle("Sucesso!")
            messageBox.setText("Dispositivo(s) cadastrado(s) com sucesso.")
                    
            messageBox.exec_()
        
            
            self.resetFields(True)

###############################################################################################################################################################################
        
    def resetFields(self, keepClient=False):
        """
        This method is called after the device record. It resets the form fields
        """
        #description
        self.descriptionField.setText("")
        #SAP Code
        self.sapCodeField.setText("")
        #quantity
        self.quantityField.setValue(1)

        #observation
        self.observationsField.setPlainText("")

        #image
        self.deviceImagePath.setText("")

        #maintenance
        self.maintenanceCheckBox.setChecked(False)

        if not keepClient:
            self.clientCheckBox.setChecked(False)
        
        
###############################################################################################################################################################################

    
    def setUpperCaseDescription(self):
        """
        make the description text uppercase
        """
        self.descriptionField.setText(self.descriptionField.text().upper())
        
###############################################################################################################################################################################

    def checkClientsInvoicesComboBox(self, state):
        if state == 0:
            self.clientComboBox.myCompleter.setCompletionPrefix("")
            self.clientComboBox.pFilterModel.setFilterFixedString("")
            self.clientComboBox.lineEdit().setText("")
            self.clientComboBox.clear()

            self.invoiceComboBox.myCompleter.setCompletionPrefix("")
            self.invoiceComboBox.pFilterModel.setFilterFixedString("")
            self.invoiceComboBox.lineEdit().setText("")
            self.invoiceComboBox.clear()
        else:
            self.populateClientComboBox()
        
###############################################################################################################################################################################

    def changeCharCounter(self):
        # --> Line inserted because the uppercase is lost when the backspace is pressed #
        self.observationsField.setCurrentCharFormat(self.textFormat)
        
        textLength = len(self.observationsField.toPlainText())
        if textLength <= 1000:
           self.charCounter.setText(str(1000 - textLength))
        else:
            text = self.observationsField.toPlainText()
            self.observationsField.setPlainText(text[:1000])
            cursor = self.observationsField.textCursor()
            cursor.setPosition(1000)
            self.observationsField.setTextCursor(cursor)

###############################################################################################################################################################################


    def mousePressEvent(self, e):
        """
        Reimplementation of the mousepressevent.
        This events clear the qcombobox if no client is selected.
        """
        cursor = self.cursor()
        if cursor.shape() == Qt.WaitCursor:
            return
        
        # --> check if any invoice was selected #
        
        text = self.invoiceComboBox.lineEdit().text()
        
        if self.invoiceComboBox.findText(text) <= 0:
            self.invoiceComboBox.myCompleter.setCompletionPrefix("")
            self.invoiceComboBox.pFilterModel.setFilterFixedString("")
            self.invoiceComboBox.lineEdit().setText("")
            self.invoiceComboBox.clearFocus()
            self.invoiceComboBox.setCurrentIndex(-1)


        # --> check if any client was selected

        text = self.clientComboBox.lineEdit().text()
        
        if self.clientComboBox.findText(text) <= 0:
            self.clientComboBox.myCompleter.setCompletionPrefix("")
            self.clientComboBox.pFilterModel.setFilterFixedString("")
            self.clientComboBox.lineEdit().setText("")
            self.clientComboBox.clearFocus()
            self.clientComboBox.setCurrentIndex(-1)

            self.invoiceComboBox.myCompleter.setCompletionPrefix("")
            self.invoiceComboBox.pFilterModel.setFilterFixedString("")
            self.invoiceComboBox.lineEdit().setText("")
            self.invoiceComboBox.clearFocus()
            self.invoiceComboBox.setCurrentIndex(-1)

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

    def populateInvoicesComboBox(self, index):
        """
        This method is called when the client combobox change value.
        It will load all the client invoices.
        """
        clientId = self.clientComboBox.itemData(index)
        if index > -1:
            condition = ["nof_cliente = '" + str(clientId) + "'"] 
            
            try:
                self.invoicesList.loadInvoices(True, condition)
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
            
            for row, invoice in enumerate(self.invoicesList):
                item = QStandardItem(invoice.invoiceNumber)
                item.setData(int(invoice.invoiceId), Qt.UserRole)
                model.setItem((row+1), 0, item)

            self.invoiceComboBox.setModel(model)
            self.invoiceComboBox.setModelColumn(0)
            self.invoiceComboBox.setCurrentIndex(0)
            
        else:
            self.invoiceComboBox.clear()
        
