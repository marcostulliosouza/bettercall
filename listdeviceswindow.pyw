from configparser import SafeConfigParser
from ftplib import FTP
import tempfile
import os

from PyQt5.QtCore import (
    Qt,
    QSortFilterProxyModel,
    QSize
    )

from PyQt5.QtGui import (
    QFont,
    QIcon,
    QIntValidator,
    QPixmap,
    QImage,
    QStandardItemModel,
    QStandardItem,
    QPalette
    )

from PyQt5.QtWidgets import (
    QMdiSubWindow,
    QWidget,
    QPushButton,
    QLayout,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QGroupBox,
    QCheckBox,
    QComboBox,
    QCompleter,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QAbstractScrollArea,
    QDialog,
    QMessageBox
    )


import deviceregisterwindow
import detaileddevicewindow
import invoicescontainer
import clientscontainer
import devicescontainer

from myExceptions import *


__version__ = "2.0.0"


###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################
class MyQDeviceImageDialog(QDialog):
    def __init__(self, deviceId=None, deviceImageExtension=None, parent=None):
        super(MyQDeviceImageDialog, self).__init__(parent)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setAttribute(Qt.WA_DeleteOnClose)
        parser = SafeConfigParser()
        parser.read("dbconfig.ini")
        FTPPath = parser.get("ftp", "path")
        FTPUser = parser.get("ftp", "user")
        FTPPass = parser.get("ftp", "pass")
        
        fileName = str(deviceId) + "." + deviceImageExtension

        self.tempFile = tempfile.NamedTemporaryFile(delete=False)

        #filePath = destinyPath + "/dis/" + fileName

        ftp = FTP(FTPPath)
        ftp.login(FTPUser, FTPPass)
        ftp.cwd("dis")
        ftp.retrbinary("RETR " + fileName, self.tempFile.write)
        ftp.quit()

        self.tempFile.close()

        deviceImage = QImage(self.tempFile.name)

        imageLabel = QLabel()
        if deviceImage.width() > 800:
            imageLabel.setPixmap(QPixmap.fromImage(deviceImage.scaledToWidth(800)))
        else:
            imageLabel.setPixmap(QPixmap.fromImage(deviceImage))

        layout = QVBoxLayout()
        layout.addWidget(imageLabel)

        self.setLayout(layout)
        self.setWindowTitle("Dispositivo "+str(deviceId).zfill(6))

        
    def closeEvent(self, event):
        os.remove(self.tempFile.name)



###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################


class MyQDeviceImageButton(QPushButton):
    def __init__(self, deviceId=None, deviceImageExtension=None, parent=None):
        super(MyQDeviceImageButton, self).__init__(parent)
        self.deviceId = deviceId
        self.deviceImageExtension = deviceImageExtension
        
        self.setCursor(Qt.PointingHandCursor)
        self.setIcon(QIcon(":/cam.png"))
        self.setIconSize(QSize(25, 25))

        self.clicked.connect(self.displayDeviceImage)

###############################################################################################################################################################################


    def displayDeviceImage(self):
        """
        This method overrides the click event, implementing the invoice download
        """
        
        deviceImageDialog = MyQDeviceImageDialog(self.deviceId, self.deviceImageExtension)
        deviceImageDialog.exec_()
         

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


class MyQLineEdit(QLineEdit):
    """
    This class reimplements qlineedit class
    """
    def __init__(self, parent=None):
        super(MyQLineEdit, self).__init__(parent)

        regularFont = QFont()
        regularFont.setBold(False)
        regularFont.setCapitalization(QFont.AllUppercase)
        
        self.setFont(regularFont)
        self.setFixedWidth(100)

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

class MyQCheckBox(QCheckBox):
    """
    This class reimplements the QCheckBox class
    """
    def __init__(self, text="", dependentFields=[], parent=None):
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
                self.stateChanged.connect(self.enableDisableFields)

###############################################################################################################################################################################

    def enableDisableFields(self, state):
        """
        This method enables and disable the fields related to the checkbbox
        """
        for field in self.dependentFields:
            field.lineEdit().setEnabled(state)
            if not state:
                field.clearSearchFilter()
        

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

class MyQPushButton(QPushButton):
    """MyQLineEdit
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

class MyQTableWidget(QTableWidget):
    """
    This class is used to create a personilized qtablewidget for the window
    """
    def __init__(self, parent=None):
        super(MyQTableWidget, self).__init__(parent)
        self.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.setAlternatingRowColors(True)
        self.setAutoFillBackground(True)
        self.setMinimumSize(QSize(853, 300))
        self.setEditTriggers(QTableWidget.NoEditTriggers)
        self.setSelectionBehavior(QTableWidget.SelectRows)
        self.setSelectionMode(QTableWidget.SingleSelection)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setHighlightSections(False)

        tablePalette = QPalette()
        tablePalette.setColor(QPalette.Inactive, QPalette.Highlight, tablePalette.color(QPalette.Active, QPalette.Highlight))
        tablePalette.setColor(QPalette.Inactive, QPalette.HighlightedText, tablePalette.color(QPalette.Active, QPalette.HighlightedText))
        self.setPalette(tablePalette)

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
        self.setColumnCount(9)

        deviceStatusIcon = QTableWidgetItem(" ")
        deviceDocStatusIcon = QTableWidgetItem(" ")
        deviceImageIcon = QTableWidgetItem(" ")
        deviceId = QTableWidgetItem("Identificação")
        deviceDescription = QTableWidgetItem("Descrição")
        deviceSAPCode = QTableWidgetItem("Código SAP")
        deviceClient = QTableWidgetItem("Proprietário")
        deviceInInvoice = QTableWidgetItem("NF de Entrada")
        deviceOutInvoice = QTableWidgetItem("NF de Saída")
        
        # --> Set the Header Items #
        self.setHorizontalHeaderItem(0, deviceStatusIcon)
        self.setHorizontalHeaderItem(1, deviceDocStatusIcon)
        self.setHorizontalHeaderItem(2, deviceImageIcon)
        self.setHorizontalHeaderItem(3, deviceId)
        self.setHorizontalHeaderItem(4, deviceDescription)
        self.setHorizontalHeaderItem(5, deviceSAPCode)
        self.setHorizontalHeaderItem(6, deviceClient)
        self.setHorizontalHeaderItem(7, deviceInInvoice)
        self.setHorizontalHeaderItem(8, deviceOutInvoice)

        self.horizontalHeader().resizeSection(0, 30)
        self.horizontalHeader().resizeSection(1, 30)
        self.horizontalHeader().resizeSection(2, 30)
        self.horizontalHeader().resizeSection(3, 100)
        self.horizontalHeader().resizeSection(4, 280)
        self.horizontalHeader().resizeSection(5, 100)
        self.horizontalHeader().resizeSection(6, 150)
        self.horizontalHeader().resizeSection(7, 100)
        self.horizontalHeader().resizeSection(8, 100)
    
        self.horizontalHeader().setStyleSheet(tableStylesheet)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)

###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################

class ListDevicesWindow(QMdiSubWindow):
    """
    This class is responsible for rendering the "Listar Notas Fiscais" window
    as a MDI sub Window and for managing the data inside it
    """
    #constant id, used for location inside the openedSubWindows dictionary in the
    #main window
    SUBWINDOWID = "listdeviceswindow"

    def __init__(self, parent=None):
        super(ListDevicesWindow, self).__init__(parent)
        self.loggedUser = parent.loggedUser
        self.parent = parent
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.clientsList = clientscontainer.ClientsContainer()
        self.invoicesList = invoicescontainer.InvoicesContainer()
        self.devicesList = devicescontainer.DevicesContainer()

        self.isFiltering = False
        self.filteringFields = []

        ###############################
        #### --> LAYOUT DEFINITION ####
        ###############################

        # --> Creating the fonts used in this window #

        boldFont = QFont()
        boldFont.setBold(True)

        regularFont = QFont()
        regularFont.setBold(False)
        
        deviceRegisterButton = MyQPushButton("Cadastrar Dispositivo")
        deviceRegisterButton.setFixedWidth(130)

        self.viewDeviceButton = MyQPushButton("Ver Dispositivo")
        self.viewDeviceButton.setDisabled(True)

        ####################################
        # --> FILTER GROUPBOX AND ELEMENTS #
        ####################################
        filterGroupBox = QGroupBox("Filtro")
        filterGroupBox.setFont(boldFont)

        # --> ID #
        deviceIdLabel = MyQLabel("Identificação: ")
        self.deviceIdField = MyQNumberLineEdit()

        # --> Descricao #
        deviceDescriptionLabel = MyQLabel("Descrição: ")
        self.deviceDescriptionField = QLineEdit()
        self.deviceDescriptionField.setMinimumWidth(273)
        self.deviceDescriptionField.setMaxLength(40)
        self.deviceDescriptionField.setFont(regularFont)


        # --> Propriedade do cliente #
        self.clientComboBox = MyQFilterComboBox()

        self.populateClientComboBox()

        invoiceLabel = MyQLabel("Nota Fiscal: ")
        self.invoiceComboBox = MyQFilterComboBox()
        self.invoiceComboBox.setFixedWidth(100)
        
        self.clientPropertyCheckBox = MyQCheckBox("Propriedade do Cliente: ", [self.clientComboBox, self.invoiceComboBox])
        self.clientPropertyCheckBox.setChecked(True)

        # --> Código SAP #
        deviceSAPCodeLabel = MyQLabel("Código SAP: ")
        self.deviceSAPCodeField = MyQLineEdit()


        # --> Status do Dispositivo #
        deviceStatusLabel = MyQLabel("Status: ")
        self.deviceStatusComboBox = QComboBox()
        self.deviceStatusComboBox.setFixedWidth(100)
        self.deviceStatusComboBox.setFont(regularFont)

        self.populateDeviceStatusComboBox()

        # --> Propriedade da Hi-Mix #
        self.himixPropertyCheckBox = MyQCheckBox("Propriedade da Hi-Mix")
        self.himixPropertyCheckBox.setChecked(True)

        # --> Botoes #
        filterButton = MyQPushButton(" Filtrar ")
        clearFilterButton = MyQPushButton(" Limpar ")


        # --> Tabela de Dispositivos
        self.devicesTable = MyQTableWidget()

        # --> Layout dos botões de Cadastro e visualização de dispositivo #
        rowButtonLayout = QHBoxLayout()
        rowButtonLayout.addWidget(deviceRegisterButton)
        rowButtonLayout.addWidget(self.viewDeviceButton)
        rowButtonLayout.addStretch(1)

        # --> First Row Filter Layout #
        firstRowFilterLayout = QHBoxLayout()
        firstRowFilterLayout.addWidget(deviceIdLabel)
        firstRowFilterLayout.addWidget(self.deviceIdField)
        firstRowFilterLayout.addWidget(deviceDescriptionLabel)
        firstRowFilterLayout.addWidget(self.deviceDescriptionField)
        firstRowFilterLayout.addWidget(deviceSAPCodeLabel)
        firstRowFilterLayout.addWidget(self.deviceSAPCodeField)
        

        # --> Second Row Filter Layout #
        secondRowFilterLayout = QHBoxLayout()
        secondRowFilterLayout.addWidget(deviceStatusLabel)
        secondRowFilterLayout.addWidget(self.deviceStatusComboBox)
        secondRowFilterLayout.addSpacing(52)
        secondRowFilterLayout.addWidget(self.clientPropertyCheckBox)
        secondRowFilterLayout.addWidget(self.clientComboBox)
        secondRowFilterLayout.addWidget(invoiceLabel)
        secondRowFilterLayout.addWidget(self.invoiceComboBox)
        secondRowFilterLayout.addStretch(1)

        # --> Third Row Filter Layout #
        thirdRowFilterLayout = QHBoxLayout()
        thirdRowFilterLayout.addSpacing(277)
        thirdRowFilterLayout.addWidget(self.himixPropertyCheckBox)
        thirdRowFilterLayout.addStretch(1)
        thirdRowFilterLayout.addWidget(clearFilterButton)
        thirdRowFilterLayout.addWidget(filterButton)
        
        
        # --> building the filter layout #
        filterLayout = QVBoxLayout()
        filterLayout.addLayout(firstRowFilterLayout)
        filterLayout.addLayout(secondRowFilterLayout)
        filterLayout.addLayout(thirdRowFilterLayout)
        filterGroupBox.setLayout(filterLayout)
        
        
        windowLayout = QVBoxLayout()
        windowLayout.addLayout(rowButtonLayout)
        windowLayout.addWidget(filterGroupBox)
        windowLayout.addWidget(self.devicesTable)

       
        centralWidget = QWidget()
        centralWidget.setLayout(windowLayout)
        self.setWidget(centralWidget)
        self.setWindowIcon(QIcon(":/scanner.png"))
        self.setWindowFlags(Qt.Window | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)


        self.updateDevicesTable()

        ###########################
        #### SIGNALS AND SLOTS ####
        ###########################
        
        deviceRegisterButton.clicked.connect(self.openDeviceRegisterWindow)
        filterButton.clicked.connect(self.filterTable)
        clearFilterButton.clicked.connect(self.clearFilter)
        self.clientPropertyCheckBox.toggled.connect(self.clientPropertyCheckboxChecker)
        self.himixPropertyCheckBox.toggled.connect(self.himixPropertyCheckboxChecker)
        self.clientComboBox.currentIndexChanged.connect(self.populateInvoicesComboBox)
        self.devicesTable.itemDoubleClicked.connect(self.openDetailedDeviceWindow)

        self.viewDeviceButton.clicked.connect(self.openDetailedDeviceWindow)
        self.devicesTable.itemSelectionChanged.connect(self.activateViewDeviceButton)

###############################################################################################################################################################################

    def activateViewDeviceButton(self):
        row = self.devicesTable.currentRow()
        if row > -1:
            self.viewDeviceButton.setEnabled(True)
        else:
            self.viewDeviceButton.setEnabled(False)


###############################################################################################################################################################################

    def openDetailedDeviceWindow(self):
        """
        This method is called when a device is double clicked or the button "Ver Dispositivo" is clicked
        """
        device = self.currentRowDevice()
        
        detailedDeviceWindow = detaileddevicewindow.DetailedDeviceWindow(device, self)
        detailedDeviceWindow.setModal(True)

        detailedDeviceWindow.show()
          
        xPos = (self.parent.screenResolution['w'] - detailedDeviceWindow.width()) / 2
        yPos = (self.parent.screenResolution['h'] - detailedDeviceWindow.height()) / 2
            
        detailedDeviceWindow.move(xPos, yPos)
        detailedDeviceWindow.raise_()
        detailedDeviceWindow.activateWindow()

###############################################################################################################################################################################

    def currentRowDevice(self):
        """
        This method returns the current selected row
        """
        row = self.devicesTable.currentRow()
        if row > -1:
            item = self.devicesTable.item(row, 3)
            key = item.data(Qt.UserRole)
            return self.devicesList.deviceFromId(key)

        return None

###############################################################################################################################################################################
       
    def clearFilter(self):
        """
        This method is called when the button "Limpar" is clicked, cleaning the filter fields
        """
        self.isFiltering = False
        self.filteringFields = []        

        self.deviceIdField.setText("")

        self.deviceDescriptionField.setText("")
        
        self.deviceSAPCodeField.setText("")

        self.deviceStatusComboBox.setCurrentIndex(0)
        self.clientPropertyCheckBox.setChecked(True)
        self.himixPropertyCheckBox.setChecked(True)

        self.clientComboBox.clearSearchFilter()
        

        self.invoiceComboBox.clearSearchFilter()
        
        
        self.updateDevicesTable()     

###############################################################################################################################################################################
        
    def clientPropertyCheckboxChecker(self, wasChecked):
        """
        This method is called when any of the checkbox in the filter is clicked
        don't allowing both to be unchecked
        """
        if not wasChecked:
            if not self.himixPropertyCheckBox.isChecked():
                self.clientPropertyCheckBox.setChecked(True)
            else:
                self.clientComboBox.setDisabled(True)
                self.invoiceComboBox.setDisabled(True)
        else:
            self.clientComboBox.setDisabled(False)
            self.invoiceComboBox.setDisabled(False)

###############################################################################################################################################################################
    
    def himixPropertyCheckboxChecker(self, wasChecked):
        """
        This method is called when any of the checkbox in the filter is clicked
        don't allowing both to be unchecked
        """
        if not wasChecked:
            if not self.clientPropertyCheckBox.isChecked():
                self.himixPropertyCheckBox.setChecked(True)

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

###############################################################################################################################################################################
    
    def filterTable(self):
        """
        This method is called when the button "Filtrar" is clicked, creating the fields list
        that will be passed to the updateDevicesTable
        """
        self.filteringFields = []

        if  self.deviceIdField.text():
            self.filteringFields.append("LPAD(dis_id, 6, '0') LIKE '%" + self.deviceIdField.text() + "%'")

        if self.deviceDescriptionField.text():
            self.filteringFields.append("dis_descricao LIKE '%" + self.deviceDescriptionField.text() + "%'")
        
        if self.deviceSAPCodeField.text():
            self.filteringFields.append("dis_codigo_sap LIKE '%" + self.deviceSAPCodeField.text() + "%'")
    
        if self.deviceStatusComboBox.currentIndex() > 0:
            self.filteringFields.append("dis_status = '" + str(self.deviceStatusComboBox.itemData(self.deviceStatusComboBox.currentIndex())) + "'")

        ownerListAux = []
        if self.clientPropertyCheckBox.isChecked():
            if self.clientComboBox.currentIndex() <= 0:
                ownerListAux.append("dis_cliente IS NOT NULL")
            else:
                ownerListAux.append("dis_cliente = '" + str(self.clientComboBox.itemData(self.clientComboBox.currentIndex())) + "'")

            if self.invoiceComboBox.currentIndex() > 0:
                self.filteringFields.append("ese_nota_fiscal_entrada = '" + str(self.invoiceComboBox.itemData(self.invoiceComboBox.currentIndex())) + "'")
                
                
        if self.himixPropertyCheckBox.isChecked():
            ownerListAux.append("dis_cliente IS NULL")


        self.filteringFields.append("(" + " OR ".join(ownerListAux) + ")")

        
        
        if len(self.filteringFields):
            self.isFiltering = True
        else:
            self.isFiltering = False

       
        self.updateDevicesTable()

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

    def updateDevicesTable(self):
        """
        This method loads the invoices to the table using the data in the fields to filter the result
        """
        try:
            self.devicesList.loadDevices(self.isFiltering, self.filteringFields)
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


        self.devicesTable.clearContents()
        self.devicesTable.setRowCount(len(self.devicesList))
        self.updateSubWindowTitle()

        # --> QFont That determinates the apearance of the text in the table #
        fontStyle = QFont()
        fontStyle.setBold(True)

        for row, device in enumerate(self.devicesList):

            # --> Icone #
            deviceStatusIcon = QLabel()
            deviceDocIcon = QLabel()
            deviceHasImageIcon = QLabel()
            
            if device.deviceStatusId == 1:
                deviceStatusIcon.setPixmap(QIcon(":/red_icon.png").pixmap(QSize(30,30)))
                deviceStatusIcon.setToolTip("BLOQUEADO")
            elif device.deviceStatusId == 2:
                deviceStatusIcon.setPixmap(QIcon(":/green_icon.png").pixmap(QSize(30,30)))
                deviceStatusIcon.setToolTip("ATIVO")
            else:
                deviceStatusIcon.setPixmap(QIcon(":/yellow_icon.png").pixmap(QSize(30,30)))
                deviceStatusIcon.setToolTip("INATIVO")

            self.devicesTable.setCellWidget(row, 0, deviceStatusIcon)

            if device.deviceDocSent == 1:
                deviceDocIcon.setPixmap(QIcon(":/doc_ok.png").pixmap(QSize(25,25)))
                deviceDocIcon.setToolTip("Documento de instalação enviado.")
            else:
                deviceDocIcon.setPixmap(QIcon(":/doc_nok.png").pixmap(QSize(25,25)))
                deviceDocIcon.setToolTip("Documento de instalação NÃO enviado!")

            self.devicesTable.setCellWidget(row, 1, deviceDocIcon)

            if device.deviceHasImage == 1 and device.deviceImageExtension:
                
                deviceImageButton = MyQDeviceImageButton(device.deviceId, device.deviceImageExtension, self)
                self.devicesTable.setCellWidget(row, 2, deviceImageButton)
          
            # --> Identificação do Dispositivo #
            item = QTableWidgetItem(str(device.deviceId).zfill(6))
            item.setData(Qt.UserRole, int(device.deviceId))
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.devicesTable.setItem(row, 3, item)

            # --> Descrição #
            item = QTableWidgetItem(device.deviceDescription)
            self.devicesTable.setItem(row, 4, item)

            # --> Código SAP #
            item = QTableWidgetItem(str(device.deviceSAPCode))
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.devicesTable.setItem(row, 5, item)

            # --> Cliente #
            item = QTableWidgetItem(device.deviceClientName)
            self.devicesTable.setItem(row, 6, item)
    
            # --> Nota Fiscal de Entrada#
            if device.deviceInvoiceNumber:
                item = QTableWidgetItem(str(device.deviceInvoiceNumber))
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.devicesTable.setItem(row, 7, item)

             # --> Nota Fiscal de Saida#
            if device.deviceOutInvoiceNumber:
                item = QTableWidgetItem(str(device.deviceOutInvoiceNumber))
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.devicesTable.setItem(row, 8, item)
                
###############################################################################################################################################################################

    def populateDeviceStatusComboBox(self):
        """
        This method is responsible for loading all the device status in the filter combobox
        """

        deviceStatusList = devicescontainer.DeviceStatusContainer()

        try:
            deviceStatusList.loadDeviceStatus()
        except DatabaseConnectionError as error:
            message = "Falha em: " + place + "\nErro: " +cause
            messageBox = QMessageBox()
            messageBox.setText(message)
            messageBox.setWindowTitle("Erro!")
            messageBox.setIcon(QMessageBox.Critical)
            messageBox.setWindowIcon(QIcon(":/warning_icon.png"))
            messageBox.exec_()
            return


        self.deviceStatusComboBox.addItem("TODOS", 0)

        for deviceStatus in deviceStatusList:
            self.deviceStatusComboBox.addItem(deviceStatus.deviceStatusDescription, deviceStatus.deviceStatusId)
       
###############################################################################################################################################################################


    def updateSubWindowTitle(self):
        """
        This method is used to update the window title with the total number of opened calls
        """
        if len(self.devicesList) != 1:
            self.setWindowTitle("Listagem de Equipamentos - %d Dispositivos" % len(self.devicesList))
        else:
            self.setWindowTitle("Listagem de Equipamentos - 1 Dispositivo")
        

###############################################################################################################################################################################

    def openDeviceRegisterWindow(self):
        """
        This method is responsible for displaying the device record dialog window
        """
        deviceRegisterWindow = deviceregisterwindow.DeviceRegisterWindow(self)
        deviceRegisterWindow.setModal(True)

        deviceRegisterWindow.show()
          
        xPos = (self.parent.screenResolution['w'] - deviceRegisterWindow.width()) / 2
        yPos = (self.parent.screenResolution['h'] - deviceRegisterWindow.height()) / 2
            
        deviceRegisterWindow.move(xPos, yPos)
        deviceRegisterWindow.raise_()
        deviceRegisterWindow.activateWindow()

###############################################################################################################################################################################
       
    def closeEvent(self, event):
        """
        This method remove its reference from its parent opened sub window list before being closed
        """
        del self.parent.openedSubWindows[self.SUBWINDOWID]
        self.close()
