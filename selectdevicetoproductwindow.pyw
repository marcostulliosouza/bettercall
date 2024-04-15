from configparser import SafeConfigParser
from ftplib import FTP
import tempfile
import os

from PyQt5.QtCore import (
        Qt,
        QSize
    )

from PyQt5.QtGui import (
        QFont,
        QIcon,
        QImage,
        QBrush,
        QColor,
        QPalette,
        QPixmap,
        QIntValidator
    )

from PyQt5.QtWidgets import (
        QDialog,
        QGroupBox,
        QLayout,
        QHBoxLayout,
        QVBoxLayout,
        QLabel,
        QLineEdit,
        QTableWidget,
        QTableWidgetItem,
        QHeaderView,
        QAbstractScrollArea,
        QPushButton,
        QComboBox
    )

import devicescontainer
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

        self.setMinimumWidth(80)


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

class MyQTableWidget(QTableWidget):
    """
    This class is used to create a personilized qtablewidget for the window
    """
    def __init__(self, parent=None):
        super(MyQTableWidget, self).__init__(parent)
        self.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.setAlternatingRowColors(True)
        self.setAutoFillBackground(True)
        self.setMinimumSize(QSize(590, 180))
        self.setEditTriggers(QTableWidget.NoEditTriggers)
        self.setSelectionBehavior(QTableWidget.SelectRows)
        self.setSelectionMode(QTableWidget.SingleSelection)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setHighlightSections(False)
        self.verticalHeader().setVisible(False)

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
        self.setColumnCount(6)

        deviceStatusIcon = QTableWidgetItem(" ")
        deviceDocStatusIcon = QTableWidgetItem(" ")
        deviceImageIcon = QTableWidgetItem(" ")
        deviceId = QTableWidgetItem("Identificação")
        deviceDescription = QTableWidgetItem("Descrição")
        deviceOwner = QTableWidgetItem("Proprietário")
        
        # --> Set the Header Items #
        self.setHorizontalHeaderItem(0, deviceStatusIcon)
        self.setHorizontalHeaderItem(1, deviceDocStatusIcon)
        self.setHorizontalHeaderItem(2, deviceImageIcon)
        self.setHorizontalHeaderItem(3, deviceId)
        self.setHorizontalHeaderItem(4, deviceDescription)
        self.setHorizontalHeaderItem(5, deviceOwner)

        self.horizontalHeader().resizeSection(0, 30)
        self.horizontalHeader().resizeSection(1, 30)
        self.horizontalHeader().resizeSection(2, 30)
        self.horizontalHeader().resizeSection(3, 100)
        self.horizontalHeader().resizeSection(4, 280)
        self.horizontalHeader().resizeSection(5, 100)
    
        self.horizontalHeader().setStyleSheet(tableStylesheet)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)

###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################


class SelectDeviceToProductWindow(QDialog):
    """
    This class is responsible for rendering the dialog that is used to select the devices
    related to a especific product.
    """
    def __init__(self, parent=None, product=None):
        super(SelectDeviceToProductWindow, self).__init__(parent)

        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setFixedSize(720, 330)
        self.parent = parent
        self.product = product
        self.devicesList = devicescontainer.DevicesContainer()

        self.isFiltering = False
        self.filteringFields = []

        
        ###############################
        ##### BUILD THE INTERFACE #####
        ###############################

        self.boldFont = QFont()
        self.boldFont.setBold(True)

        self.regularFont = QFont()
        self.regularFont.setBold(False)
        
        # --> ID #
        deviceIdLabel = MyQLabel("Identificação: ")
        self.deviceIdField = MyQNumberLineEdit()

        # --> Descricao #
        deviceDescriptionLabel = MyQLabel("Descrição: ")
        self.deviceDescriptionField = QLineEdit()
        self.deviceDescriptionField.setMinimumWidth(180)
        self.deviceDescriptionField.setMaxLength(40)
        self.deviceDescriptionField.setFont(self.regularFont)

        # --> Botões Filtro #
        clearFilterButton = MyQPushButton("Limpar")
        filterButton = MyQPushButton("Filtrar")
        
        filterGroupBox = QGroupBox("Filtro")
        filterGroupBox.setFont(self.boldFont)

        groupBoxLayout = QHBoxLayout()
        groupBoxLayout.addWidget(deviceIdLabel)
        groupBoxLayout.addWidget(self.deviceIdField)
        groupBoxLayout.addWidget(deviceDescriptionLabel)
        groupBoxLayout.addWidget(self.deviceDescriptionField)
        groupBoxLayout.addWidget(clearFilterButton)
        groupBoxLayout.addWidget(filterButton)
        groupBoxLayout.addStretch(1)

        filterGroupBox.setLayout(groupBoxLayout)

        # --> Tabela de dispositivos disponíveis #
        self.allowedDevicesTable = MyQTableWidget()
        
        # --> ComboBox contendo as funções possíveis do dispositivo #
        deviceFunctionLabel = MyQLabel("Função do Dispositivo neste Produto: ")

        self.deviceFunctionComboBox = QComboBox()
        self.deviceFunctionComboBox.setMinimumWidth(200)

        self.populateDeviceFunctionsComboBox()

        deviceFunctionFieldsLayout = QHBoxLayout()
        deviceFunctionFieldsLayout.addStretch(1)
        deviceFunctionFieldsLayout.addWidget(deviceFunctionLabel)
        deviceFunctionFieldsLayout.addWidget(self.deviceFunctionComboBox)

        # --> Botões #
        self.addDeviceToProductButton = MyQPushButton("Adicionar")
        self.addDeviceToProductButton.setEnabled(False)
        
        cancelButton = MyQPushButton("Cancelar")

        buttonsLayout = QHBoxLayout()
        buttonsLayout.addStretch(1)
        buttonsLayout.addWidget(self.addDeviceToProductButton)
        buttonsLayout.addWidget(cancelButton)
        buttonsLayout.addStretch(1)
        
        
        windowLayout = QVBoxLayout()
        windowLayout.addWidget(filterGroupBox)
        windowLayout.addWidget(self.allowedDevicesTable)
        windowLayout.addLayout(deviceFunctionFieldsLayout)
        windowLayout.addLayout(buttonsLayout)
        windowLayout.addStretch(1)

        self.setLayout(windowLayout)

        self.setWindowTitle("Adicionar Dispositivos ao Produto \"" + product.productName + "\"")
        # --> Line responsible for preventing window resize
        self.layout().setSizeConstraint(QLayout.SetFixedSize)

        self.updateDevicesTable()

        self.deviceDescriptionField.textChanged.connect(self.setUpperCaseDescription)
        clearFilterButton.clicked.connect(self.clearFilter)
        cancelButton.clicked.connect(self.close)
        filterButton.clicked.connect(self.filterTable)
        self.addDeviceToProductButton.clicked.connect(self.addDeviceToProduct)
        self.allowedDevicesTable.currentCellChanged.connect(self.verifiesIfEnableAddButtonTable)
        self.deviceFunctionComboBox.currentIndexChanged.connect(self.verifiesIfEnableAddButtonComboBox)

###############################################################################################################################################################################

    def verifiesIfEnableAddButtonComboBox(self, index):
        if index > 0:
            self.addDeviceToProductButton.setEnabled(True)
        else:
            self.addDeviceToProductButton.setEnabled(False)

###############################################################################################################################################################################

    def verifiesIfEnableAddButtonTable(self, currentRow, currentColumn, previousRow, previousColumn):
        """
        This method is called when a item is selected in the table. If there is a function selected to the device it enables the Add button
        """
        deviceFunction = self.deviceFunctionComboBox.itemData(self.deviceFunctionComboBox.currentIndex())
        
        if currentRow > -1 and deviceFunction > -1:
            self.addDeviceToProductButton.setEnabled(True)

###############################################################################################################################################################################

    def addDeviceToProduct(self):
        """
        This method is used to relate the device to the product and reloading the table
        """
        deviceId = self.allowedDevicesTable.item(self.allowedDevicesTable.currentRow(), 3).data(Qt.UserRole)
        deviceFunction = self.deviceFunctionComboBox.itemData(self.deviceFunctionComboBox.currentIndex())
        
        if deviceFunction < 0:
            return

        
        try:
            self.product.addDeviceToProduct(deviceId, deviceFunction)  
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
        
        self.updateDevicesTable()
        self.parent.updateDevicesTable()
        self.deviceFunctionComboBox.setCurrentIndex(0)
        self.addDeviceToProductButton.setEnabled(False)

###############################################################################################################################################################################

    def setUpperCaseDescription(self):
        """
        make the description text uppercase
        """
        self.deviceDescriptionField.setText(self.deviceDescriptionField.text().upper())


###############################################################################################################################################################################

    def clearFilter(self):
        """
        This method is called when the button "Limpar" is clicked, cleaning the filter fields
        """
        self.isFiltering = False
        self.filteringFields = []        

        self.deviceIdField.setText("")

        self.deviceDescriptionField.setText("")
                
        self.updateDevicesTable()

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

        self.updateDevicesTable()
        
###############################################################################################################################################################################

    def updateDevicesTable(self):
        """
        This method loads the invoices to the table using the data in the fields to filter the result
        """

        self.isFiltering = True
        self.filteringFields.append("(dis_cliente = '" + str(self.product.productClientId) + "' OR dis_cliente IS NULL)")
        self.filteringFields.append("(dis_id NOT IN (SELECT vdp_dispositivo FROM vinculacao_dispositivo_produto WHERE vdp_produto = '" + str(self.product.productId) + "'))")

                
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


        self.allowedDevicesTable.clearContents()
        self.allowedDevicesTable.setRowCount(len(self.devicesList))
        
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

            self.allowedDevicesTable.setCellWidget(row, 0, deviceStatusIcon)

            if device.deviceDocSent == 1:
                deviceDocIcon.setPixmap(QIcon(":/doc_ok.png").pixmap(QSize(25,25)))
                deviceDocIcon.setToolTip("Documento de instalação enviado.")
            else:
                deviceDocIcon.setPixmap(QIcon(":/doc_nok.png").pixmap(QSize(25,25)))
                deviceDocIcon.setToolTip("Documento de instalação NÃO enviado!")

            self.allowedDevicesTable.setCellWidget(row, 1, deviceDocIcon)

            if device.deviceHasImage == 1 and device.deviceImageExtension:
                
                deviceImageButton = MyQDeviceImageButton(device.deviceId, device.deviceImageExtension, self)
                self.allowedDevicesTable.setCellWidget(row, 2, deviceImageButton)
          
            # --> Identificação do Dispositivo #
            item = QTableWidgetItem(str(device.deviceId).zfill(6))
            item.setData(Qt.UserRole, int(device.deviceId))
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.allowedDevicesTable.setItem(row, 3, item)

            # --> Descrição #
            item = QTableWidgetItem(device.deviceDescription)
            self.allowedDevicesTable.setItem(row, 4, item)

            # --> Cliente #
            item = QTableWidgetItem(device.deviceClientName)
            self.allowedDevicesTable.setItem(row, 5, item)
    

###############################################################################################################################################################################

    def populateDeviceFunctionsComboBox(self):
        """
        This method is called to populate the combobox with all possible
        devices functions
        """
        try:
            functionList = self.devicesList.loadDevicesFunctions()
        except DatabaseConnectionError as error:
            message = "Falha em: " + place + "\nErro: " +cause
            messageBox = QMessageBox()
            messageBox.setText(message)
            messageBox.setWindowTitle("Erro!")
            messageBox.setIcon(QMessageBox.Critical)
            messageBox.setWindowIcon(QIcon(":/warning_icon.png"))
            messageBox.exec_()
            return


        self.deviceFunctionComboBox.addItem("", -1)
        
        for functionId, functionDescription in functionList:
            self.deviceFunctionComboBox.addItem(functionDescription, functionId)

###############################################################################################################################################################################
        
    def showEvent(self, event):
        ## --> Code created to move the device selection Dialog above the table ##
        xPos = (self.parent.parent.screenResolution['w'] - self.width()) / 2
        yPos = ((self.parent.parent.screenResolution['h'] + 300) - self.height()) / 2

        self.move(xPos, yPos)
        
###############################################################################################################################################################################

    def reject(self):
        self.done(0)      
