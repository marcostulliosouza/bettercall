from PyQt5.QtCore import (
    Qt,
    QSortFilterProxyModel
    )

from PyQt5.QtGui import (
    QIcon,
    QFont,
    QIntValidator,
    QBrush,
    QColor,
    QStandardItemModel,
    QStandardItem
    )

from PyQt5.QtWidgets import (
    QDialog,
    QLabel,
    QLineEdit,
    QWidget,
    QTableWidget,
    QTableWidgetItem,
    QCheckBox,
    QHeaderView,
    QAbstractScrollArea,
    QAbstractItemView,
    QComboBox,
    QPushButton,
    QCompleter,
    QHBoxLayout,
    QVBoxLayout,
    QLayout,
    QMessageBox
    )

import qrc_resources
import invoicescontainer
import clientscontainer
import devicescontainer
from magicDB import *
from myExceptions import *

__version__ = "2.0.0"


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

        self.setMinimumWidth(113)

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
        
        # --> Validator that allows only integers #
        validator = QIntValidator()
        self.setValidator(validator)

        self.setFixedWidth(100)
        
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
        self.setFocusPolicy(Qt.ClickFocus)
        self.setEditable(True)
        self.myCompleter = QCompleter(self)
        self.setMinimumWidth(177)
        
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

class MyQTableWidget(QTableWidget):
    """
    This class is used to create a personilized qtablewidget for the window
    """
    def __init__(self, parent=None):
        super(MyQTableWidget, self).__init__(parent)
        self.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.setAlternatingRowColors(True)
        self.setAutoFillBackground(True)
        self.setEditTriggers(QTableWidget.NoEditTriggers)
        self.setSelectionBehavior(QTableWidget.SelectRows)
        self.setSelectionMode(QAbstractItemView.NoSelection)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.horizontalHeader().setStretchLastSection(True)
        self.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.horizontalHeader().setHighlightSections(False)

        tableStylesheet = "::section{ " \
                     "           font: bold; " \
                     "           color: white; " \
                     "           border: 1px solid black; " \
                     "           height: 20px; " \
                     "           background-color: qlineargradient( " \
                     "                      x1:0, " \
                     "                      y1:0, " \
                     "                      x2:0, " \
                     "                      y2:1, " \
                     "                      stop:0 #4C4C4C, " \
                     "                      stop: 0.12 #595959, " \
                     "                      stop: 0.25 #666666, " \
                     "                      stop: 0.39 #474747, " \
                     "                      stop: 0.5 #2C2C2C, " \
                     "                      stop: 0.51 #000000, " \
                     "                      stop: 0.60 #111111, " \
                     "                      stop: 0.76 #2B2B2B, " \
                     "                      stop: 0.91 #1C1C1C, " \
                     "                      stop: 1 #131313);} "

        # --> create theitems for the headers #
        self.setColumnCount(4)

        checkboxField = QTableWidgetItem(" ")
        equipmentId = QTableWidgetItem("Identificação")
        deviceDescription = QTableWidgetItem("Descrição")
        deviceSAPCode = QTableWidgetItem("Código SAP")
        
        
        # --> Set the Header Items #
        self.setHorizontalHeaderItem(0, checkboxField)
        self.setHorizontalHeaderItem(1, equipmentId)
        self.setHorizontalHeaderItem(2, deviceDescription)
        self.setHorizontalHeaderItem(3, deviceSAPCode)
        

        self.horizontalHeader().resizeSection(0, 19)
        self.horizontalHeader().resizeSection(1, 100)
        self.horizontalHeader().resizeSection(2, 280)
        self.horizontalHeader().resizeSection(3, 100)
        
        self.horizontalHeader().setStyleSheet(tableStylesheet)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)

###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################

class MyQPushButton(QPushButton):
    """
    This class reimplements the QPushButton
    """
    def __init__(self, text="", parent=None):
        super(MyQPushButton, self).__init__(text, parent)

        regularFont = QFont()
        regularFont.setBold(False)
        self.setFont(regularFont)

        self.setCursor(Qt.PointingHandCursor)
        
        self.setFixedWidth(103)
        
###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################


class ReturnEquipmentsWindow(QDialog):
    """
    This class is responsible for rendering the return equipment window modally.
    It can receive a Invoice number or a device number and its type, loading
    the client data and all devices related to the invoice that contains the
    device
    """
    
    def __init__(self, invoiceId=None, deviceId=None, deviceType=None, parent=None):
        super(ReturnEquipmentsWindow, self).__init__(parent)
        self.parent = parent

        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.clientsList = clientscontainer.ClientsContainer()
        self.invoicesList = invoicescontainer.InvoicesContainer()
        self.devicesList = devicescontainer.DevicesContainer()

        self.tableCheckedIndexes = set()

        # --> Brushes used to set de selection and unselection of an item in the table #
        self.selectedBrush = QBrush(QColor(51, 153, 255, 100), Qt.SolidPattern)
        self.alreadySentBrush = QBrush(QColor(66, 255, 100, 100), Qt.SolidPattern)
        self.noBrush = QBrush()


        ###############################
        #### --> FIELDS DEFINITION ####
        ###############################

        # --> Cliente #
        clientLabel = MyQLabel("Cliente: ")
        clientLabel.setMinimumWidth(60)
        self.clientComboBox = MyQFilterComboBox()
        self.populateClientComboBox()
        
        # --> Nota Fiscal de Entrada #
        invoiceInLabel = MyQLabel("Nota Fiscal de Entrada: ")
        invoiceInLabel.setMinimumWidth(200)
        self.invoiceComboBox = MyQFilterComboBox()
        self.invoiceComboBox.setFixedWidth(100)

        firstRowFieldsLayout = QHBoxLayout()
        firstRowFieldsLayout.addWidget(clientLabel)
        firstRowFieldsLayout.addWidget(self.clientComboBox)
        firstRowFieldsLayout.addWidget(invoiceInLabel)
        firstRowFieldsLayout.addWidget(self.invoiceComboBox)

        # --> Tabela de Equipamentos #
        self.invoiceEquipmentsTable = MyQTableWidget()


        # --> Número da Nota Fiscal de Saída #
        invoiceOutLabel = MyQLabel("Número da Nota Fiscal de Saída: ")
        self.invoiceOutField = MyQNumberLineEdit()
        
        lastRowFieldsLayout = QHBoxLayout()
        lastRowFieldsLayout.addWidget(invoiceOutLabel)
        lastRowFieldsLayout.addWidget(self.invoiceOutField)

        # --> Botões #

        returnButton = MyQPushButton("Devolver")
        cancelButton = MyQPushButton("Cancelar")

        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch(1)
        buttonLayout.addWidget(returnButton)
        buttonLayout.addWidget(cancelButton)
        buttonLayout.addStretch(1)

        #################################
        #### --> WINDOW LAYOUT BUILD ####
        #################################
        windowLayout = QVBoxLayout()
        windowLayout.addLayout(firstRowFieldsLayout)
        windowLayout.addWidget(self.invoiceEquipmentsTable)
        windowLayout.addLayout(lastRowFieldsLayout)
        windowLayout.addLayout(buttonLayout)
        windowLayout.addStretch(1)
        

        self.setLayout(windowLayout)
        self.setWindowIcon(QIcon(":/send_equipment.png"))
        self.setWindowTitle("Devolver Equipamentos")
        self.layout().setSizeConstraint(QLayout.SetFixedSize)

        ###############################
        #### --> SIGNALS AND SLOTS ####
        ###############################
        
        self.clientComboBox.currentIndexChanged.connect(self.populateInvoicesComboBox)
        self.invoiceComboBox.currentIndexChanged.connect(self.populateInvoiceEquipmentsTable)
        self.invoiceEquipmentsTable.itemClicked.connect(self.toggleTableItem)
        returnButton.clicked.connect(self.returnEquipments)
        cancelButton.clicked.connect(self.close)

#####################################################################################################################################

    def returnEquipments(self):
        """
        This method is called to return the equipments to its owners.
        This method will be divided in 3 parts being the first one for devices, the second one for measurement equipments and
        the third one will be for the computers
        """
        devsIdList = []
        devsString = ""

        if not len(self.tableCheckedIndexes):
            messageBox = QMessageBox()
            messageBox.setText("Selecione os dispositivos que serão retornados ao Cliente.")
            messageBox.setWindowTitle("Atenção!")
            messageBox.setIcon(QMessageBox.Warning)
            messageBox.setWindowIcon(QIcon(":/warning_icon.png"))
            messageBox.exec_()

            return

        
        try:
            invoiceOutNumber = int(self.invoiceOutField.text())
        except ValueError:
            messageBox = QMessageBox()
            messageBox.setText("É necessario informar o número da Nota Fiscal de Saída.")
            messageBox.setWindowTitle("Atenção!")
            messageBox.setIcon(QMessageBox.Warning)
            messageBox.setWindowIcon(QIcon(":/warning_icon.png"))
            messageBox.exec_()

            return
        
    

        for tableRow in self.tableCheckedIndexes:
            equipmentId = self.invoiceEquipmentsTable.item(tableRow, 1).data(Qt.UserRole)
            device = self.devicesList.deviceFromId(equipmentId)
            devsIdList.append(device.deviceId)
            devsString += "\nDispositivo: " + str(device.deviceId).zfill(6)

        ##############
        messageBox = QMessageBox()
        messageBox.setIcon(QMessageBox.Question)
        messageBox.setWindowIcon(QIcon(":/question.png"))
        messageBox.setWindowTitle("Confirmar retorno de Equipamentos")
        messageBox.setText("Confirmar devolução dos Equipamentos abaixo?" + devsString)
        messageBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        messageBox.button(QMessageBox.Yes).setText("Sim")
        messageBox.button(QMessageBox.No).setText("Não")
        
        messageBox.exec_()
        
        # --> If the Yes button was clicked #
        if messageBox.clickedButton() == messageBox.button(QMessageBox.No):
            return

        else:
            try:
                self.devicesList.returnDevices(devsIdList, invoiceOutNumber)
            except DatabaseConnectionError as error:
                place, cause = error.args

                message = "Falha em: " + place + "\nErro: " +cause
            
                messageBox = QMessageBox()
                messageBox.setText(message)
                messageBox.setWindowTitle("Erro!")
                messageBox.setIcon(QMessageBox.Critical)
                messageBox.setWindowIcon(QIcon(":/warning_icon.png"))
                messageBox.exec_()
                self.parent.close()
                return
        
            self.populateInvoiceEquipmentsTable()
            
            messageBox = QMessageBox()
            messageBox.setText("Retorno de Equipamentos executado com sucesso!")
            messageBox.setWindowTitle("Sucesso!")
            messageBox.setIcon(QMessageBox.Information)
            messageBox.setWindowIcon(QIcon(":/information.png"))
            messageBox.exec_()

#####################################################################################################################################

    def toggleTableItem(self, tableItem):

        equipmentId = self.invoiceEquipmentsTable.item(tableItem.row(), 1).data(Qt.UserRole)
        device = self.devicesList.deviceFromId(equipmentId)
        if device.deviceStatusId != 3:

            if tableItem.row() in self.tableCheckedIndexes:
                self.tableCheckedIndexes.remove(tableItem.row())
                brush = self.noBrush
                self.invoiceEquipmentsTable.item(tableItem.row(), 0).setCheckState(Qt.Unchecked)

            else:
                self.tableCheckedIndexes.add(tableItem.row())
                brush = self.selectedBrush
                self.invoiceEquipmentsTable.item(tableItem.row(), 0).setCheckState(Qt.Checked)

            
            self.invoiceEquipmentsTable.item(tableItem.row(), 0).setBackground(brush)
            self.invoiceEquipmentsTable.item(tableItem.row(), 1).setBackground(brush)
            self.invoiceEquipmentsTable.item(tableItem.row(), 2).setBackground(brush)
            self.invoiceEquipmentsTable.item(tableItem.row(), 3).setBackground(brush)
    
        
#####################################################################################################################################

    def populateInvoiceEquipmentsTable(self):
        """
        This method loads the devices related to the invoice to the table
        """
        self.tableCheckedIndexes.clear()
        
        filterFields = []
        filterFields.append("dis_cliente = '" + str(self.clientComboBox.itemData(self.clientComboBox.currentIndex())) + "'")
        filterFields.append("ese_nota_fiscal_entrada = '" + str(self.invoiceComboBox.itemData(self.invoiceComboBox.currentIndex())) + "'")
        
        
        try:
            self.devicesList.loadDevices(True, filterFields)
        except DatabaseConnectionError as error:
            place, cause = error.args

            message = "Falha em: " + place + "\nErro: " +cause
        
            messageBox = QMessageBox()
            messageBox.setText(message)
            messageBox.setWindowTitle("Erro!")
            messageBox.setIcon(QMessageBox.Critical)
            messageBox.setWindowIcon(QIcon(":/warning_icon.png"))
            messageBox.exec_()
            self.parent.close()
            return


        self.invoiceEquipmentsTable.clearContents()
        self.invoiceEquipmentsTable.setRowCount(len(self.devicesList))
        
        # --> QFont That determinates the apearance of the text in the table #
        fontStyle = QFont()
        fontStyle.setBold(True)

        
        for row, device in enumerate(self.devicesList):

            # --> Coluna do Checkbox #
            if device.deviceStatusId != 3:
                item = QTableWidgetItem()
                item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                item.setCheckState(Qt.Unchecked)
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            else:
                item = QTableWidgetItem()
                item.setBackground(self.alreadySentBrush)

            self.invoiceEquipmentsTable.setItem(row, 0, item)    
          
            # --> Identificação do Dispositivo #
            item = QTableWidgetItem(str(device.deviceId).zfill(6))
            item.setData(Qt.UserRole, device.deviceId)
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            if device.deviceStatusId == 3:
                    item.setFlags(Qt.NoItemFlags)
                    item.setBackground(self.alreadySentBrush)
            self.invoiceEquipmentsTable.setItem(row, 1, item)

            # --> Descrição #
            item = QTableWidgetItem(device.deviceDescription)
            if device.deviceStatusId == 3:
                    item.setFlags(Qt.NoItemFlags)
                    item.setBackground(self.alreadySentBrush)
            self.invoiceEquipmentsTable.setItem(row, 2, item)

            # --> Código SAP #
            item = QTableWidgetItem(str(device.deviceSAPCode))
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            if device.deviceStatusId == 3:
                    item.setFlags(Qt.NoItemFlags)
                    item.setBackground(self.alreadySentBrush)
            self.invoiceEquipmentsTable.setItem(row, 3, item)

     
#####################################################################################################################################
        
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
        
#####################################################################################################################################

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

