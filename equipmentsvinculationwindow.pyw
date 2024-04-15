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
        QStandardItemModel,
        QStandardItem,
        QImage,
        QPalette,
        QPixmap,
        QBrush,
        QColor
    )

from PyQt5.QtWidgets import (
        QMdiSubWindow,
        QMessageBox,
        QLabel,
        QTableWidget,
        QTableWidgetItem,
        QPushButton,
        QLineEdit,
        QLayout,
        QHBoxLayout,
        QVBoxLayout,
        QGridLayout,
        QCompleter,
        QCheckBox,
        QWidget,
        QGroupBox,
        QListWidget,
        QListWidgetItem,
        QAbstractScrollArea,
        QHeaderView,
        QComboBox,
        QDialog
    )


import qrc_resources
from magicDB import *
from myExceptions import *

import selectdevicetoproductwindow
import clientscontainer
import productscontainer
import devicescontainer

__version__ = "2.0.0"

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

        self.setMinimumWidth(66)
        self.setFixedHeight(20)


###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################

class MyQCheckBox(QCheckBox):
    """
    This class reimplements the QCheckBox class
    """
    def __init__(self, text="", parent=None):
        super(MyQCheckBox, self).__init__(text, parent)

        # --> appearance #
        boldFont = QFont()
        boldFont.setBold(True)
        self.setFont(boldFont)
        self.setMinimumWidth(10)


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
        
        self.setFixedWidth(113)

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
        self.setMinimumSize(QSize(590, 280))
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
        deviceFunction = QTableWidgetItem("Função")
        
        # --> Set the Header Items #
        self.setHorizontalHeaderItem(0, deviceStatusIcon)
        self.setHorizontalHeaderItem(1, deviceDocStatusIcon)
        self.setHorizontalHeaderItem(2, deviceImageIcon)
        self.setHorizontalHeaderItem(3, deviceId)
        self.setHorizontalHeaderItem(4, deviceDescription)
        self.setHorizontalHeaderItem(5, deviceFunction)

        self.horizontalHeader().resizeSection(0, 30)
        self.horizontalHeader().resizeSection(1, 30)
        self.horizontalHeader().resizeSection(2, 30)
        self.horizontalHeader().resizeSection(3, 100)
        self.horizontalHeader().resizeSection(4, 250)
        self.horizontalHeader().resizeSection(5, 100)
    
        self.horizontalHeader().setStyleSheet(tableStylesheet)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)

###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################


class EquipmentsVinculationWindow(QMdiSubWindow):

    # --> Constant id, used for location inside the openedSubWindows dictionary in the main window #
    SUBWINDOWID = "equipmentsvinculationwindow"

    def __init__(self, parent=None):
        super(EquipmentsVinculationWindow, self).__init__(parent)
        self.parent = parent
        self.loggedUser = parent.loggedUser
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowFlags(Qt.SubWindow | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)

        self.activeClients = clientscontainer.ClientsContainer()
        self.productsFromClient = productscontainer.ProductsContainer()
        self.devicesFromProducts = devicescontainer.DevicesContainer()

        boldFont = QFont()
        boldFont.setBold(True)

        self.noTestBrush = QBrush()
        self.noTestBrush.setColor(QColor(130, 130, 130))
        
        self.hasTestBrush = QBrush()
        self.hasTestBrush.setColor(QColor(0, 0, 0))

        listPalette = QPalette()
        listPalette.setColor(QPalette.Highlight, listPalette.color(QPalette.Active, QPalette.Highlight))
        
        ####################################
        #### WINDOW LAYOUT CONSTRUCTION ####
        ####################################

        # --> Client combobox
        
        clientLabel = MyQLabel("Cliente: ")
        
        self.clientComboBox = QComboBox()
        self.clientComboBox.setMinimumWidth(198)
        
        self.populateClientComboBox()

        # --> Products List #
        
        self.productsList = QListWidget()
        self.productsList.setFixedSize(QSize(250, 293))

        groupLayout = QHBoxLayout()
        groupLayout.addWidget(self.productsList)

        productsGroupBox = QGroupBox("Produtos:")
        productsGroupBox.setFont(boldFont)
        productsGroupBox.setLayout(groupLayout)


        ##### --> BUILDING THE FIRST COLUMN LAYOUT #####
        clientLineLayout = QHBoxLayout()
        clientLineLayout.addWidget(clientLabel)
        clientLineLayout.addWidget(self.clientComboBox)
        clientLineLayout.addStretch(1)

        clientProductColumnLayout = QVBoxLayout()
        clientProductColumnLayout.addLayout(clientLineLayout)
        clientProductColumnLayout.addWidget(productsGroupBox)
        
        # --> Detailed list of devices from the product #

        self.hasTestCheckBox = MyQCheckBox("Com Teste")

        self.deactivateDeviceButton = QPushButton()
        self.deactivateDeviceButton.setIcon(QIcon(":/delete.png"))
        self.deactivateDeviceButton.setToolTip("Remover Produto")

        firstLineDetailedLayout = QHBoxLayout()
        firstLineDetailedLayout.addWidget(self.hasTestCheckBox)
        firstLineDetailedLayout.addStretch(1)
        firstLineDetailedLayout.addWidget(self.deactivateDeviceButton)
        

        self.addDeviceButton = MyQPushButton("Adicionar Dispositivo")
        self.removeDeviceButton = MyQPushButton("Remover Dispositivo")
        self.addDeviceButton.setEnabled(False)
        self.removeDeviceButton.setEnabled(False)
        

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.addDeviceButton)
        buttonLayout.addWidget(self.removeDeviceButton)
        buttonLayout.addStretch(1)

        self.vinculatedDevicesTable = MyQTableWidget()
        
        productDevicesLayout = QVBoxLayout()
        productDevicesLayout.addLayout(firstLineDetailedLayout)
        productDevicesLayout.addLayout(buttonLayout)
        productDevicesLayout.addWidget(self.vinculatedDevicesTable)
        productDevicesLayout.addStretch(1)

        self.productDetailGroupBox = QGroupBox()
        self.productDetailGroupBox.setLayout(productDevicesLayout)
        self.productDetailGroupBox.setEnabled(False)

        secondLineLayout = QHBoxLayout()
        secondLineLayout.addLayout(clientProductColumnLayout)
        secondLineLayout.addWidget(self.productDetailGroupBox)
        secondLineLayout.addStretch(1)

        
        cancelButton = MyQPushButton("Cancelar")

        lastRowButtonLayout = QHBoxLayout()
        lastRowButtonLayout.addStretch(1)
        lastRowButtonLayout.addWidget(cancelButton)
        lastRowButtonLayout.addStretch(1)

        windowLayout = QVBoxLayout()
        windowLayout.addLayout(secondLineLayout)
        windowLayout.addLayout(lastRowButtonLayout)

        # --> create the centralWidget of the QMdiSubWindow and set its layout #
        centralWidget = QWidget()
        centralWidget.setLayout(windowLayout)
        self.setWidget(centralWidget)

        self.setWindowFlags(Qt.Window | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
        self.setWindowTitle("Vinculação de Produtos e Equipamentos")
        self.setWindowIcon(QIcon(":/chain.png"))
        
        # --> Line responsible for preventing window resize
        #self.layout().setSizeConstraint(QLayout.SetFixedSize)

        #####################
        #### --> SIGNALS ####
        #####################
        
        self.clientComboBox.currentIndexChanged.connect(self.loadProductsFromClient)
        self.productsList.itemClicked.connect(self.fillProductAndDevicesInformation)
        cancelButton.clicked.connect(self.close)
        self.deactivateDeviceButton.clicked.connect(self.deactivateProduct)
        self.hasTestCheckBox.stateChanged.connect(self.updateProductHasTestStatus)
        self.addDeviceButton.clicked.connect(self.addDeviceToProduct)
        self.vinculatedDevicesTable.itemClicked.connect(self.enableRemoveButton)
        self.removeDeviceButton.clicked.connect(self.removeDeviceFromProduct)


###############################################################################################################################################################################

    def removeDeviceFromProduct(self):
        """
        This method is called when the button "remover dispositivo" is clicked. After confirmation it removes the vinculation between the device and the product
        """
        if not self.vinculatedDevicesTable.currentItem():
            return
        
        productId = self.productsList.currentItem().data(Qt.UserRole)
        deviceId = self.vinculatedDevicesTable.item(self.vinculatedDevicesTable.currentRow(), 3).data(Qt.UserRole)
        device = self.devicesFromProducts.deviceFromId(deviceId)

        messageBox = QMessageBox()
        messageBox.setIcon(QMessageBox.Question)
        messageBox.setWindowIcon(QIcon(":/question.png"))
        messageBox.setWindowTitle("Confirmar remoção de Vinculação do Dispositivo")
        messageBox.setText("Confirmar remoção da vinculação dispositivo \"" + self.vinculatedDevicesTable.currentItem().text() + "\" com o Produto \"" + self.productsList.currentItem().text() + "\"")
        messageBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        messageBox.button(QMessageBox.Yes).setText("Sim")
        messageBox.button(QMessageBox.No).setText("Não")
        
        messageBox.exec_()

        # --> If the Yes button was clicked #
        if messageBox.clickedButton() == messageBox.button(QMessageBox.No):
            return

        else:
            try:
                device.removeDeviceVinculationToProduct(productId)
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
        

###############################################################################################################################################################################


    def enableRemoveButton(self):
        """
        This method is used to enable the remove device button. It is called when a item in the vinculated
        devices table is clicked
        """
        self.removeDeviceButton.setEnabled(True)

###############################################################################################################################################################################

    def addDeviceToProduct(self):
        """
        This method is called when the button "Adicionar Dispositivo" is clicked
        """
        if not self.productsList.currentItem():
            return
        product = self.productsFromClient.productFromId(self.productsList.currentItem().data(Qt.UserRole))

        selectDeviceToProductWindow = selectdevicetoproductwindow.SelectDeviceToProductWindow(self, product)
        selectDeviceToProductWindow.exec_()


###############################################################################################################################################################################

    def updateProductHasTestStatus(self, prodHasTest):
        """
        This method is called when the checkbox is clicked, changing the product has test status in the database.
        """
        currentClient = self.clientComboBox.itemData(self.clientComboBox.currentIndex())
        if currentClient <= 1:
            return
        
        product = self.productsFromClient.productFromId(self.productsList.currentItem().data(Qt.UserRole))
        
        if not prodHasTest:
            status = 0
        else:
            status = 1

        try:
            product.updateHasTest(status)
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

        if status == 1:
            self.productsList.currentItem().setForeground(self.hasTestBrush)
        else:
            self.productsList.currentItem().setForeground(self.noTestBrush)

        
###############################################################################################################################################################################

    def deactivateProduct(self):
        """
        This method is called when the button with a trash can icon is clicked. After confirmation this method will deactivate
        the product and reload the product list
        """
        product = self.productsFromClient.productFromId(self.productsList.currentItem().data(Qt.UserRole))
        
        messageBox = QMessageBox()
        messageBox.setIcon(QMessageBox.Question)
        messageBox.setWindowIcon(QIcon(":/question.png"))
        messageBox.setWindowTitle("Confirmar remoção de Produto")
        messageBox.setText("Confirmar remoção do produto \"" + product.productName + "\" da lista de produtos deste cliente? Esta operação não poderá ser revertida.")
        messageBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        messageBox.button(QMessageBox.Yes).setText("Sim")
        messageBox.button(QMessageBox.No).setText("Não")
        
        messageBox.exec_()

        # --> If the Yes button was clicked #
        if messageBox.clickedButton() == messageBox.button(QMessageBox.No):
            return

        else:
            try:
                product.deactivateProduct()
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
        
            self.loadProductsFromClient()
            
            messageBox = QMessageBox()
            messageBox.setText("Produto removido com sucesso!")
            messageBox.setWindowTitle("Sucesso!")
            messageBox.setIcon(QMessageBox.Information)
            messageBox.setWindowIcon(QIcon(":/information.png"))
            messageBox.exec_()

###############################################################################################################################################################################
       

    def fillProductAndDevicesInformation(self, item):
        """
        This method is called when a item is selected in the product list. It will fill up the table containing the test devices
        and the checkbox that informs if the product has test or not
        """
        
        self.productDetailGroupBox.setEnabled(True)
        self.addDeviceButton.setEnabled(True)
        product = self.productsFromClient.productFromId(item.data(Qt.UserRole))
        if product.prodHasTest:
            self.hasTestCheckBox.setChecked(True)
        else:
            self.hasTestCheckBox.setChecked(False)

        self.updateDevicesTable()
    

###############################################################################################################################################################################

    def updateDevicesTable(self):
        """
        This method loads the invoices to the table using the data in the fields to filter the result
        """
        self.removeDeviceButton.setEnabled(False)
        product = self.productsFromClient.productFromId(self.productsList.currentItem().data(Qt.UserRole))
               
        try:
            self.devicesFromProducts.loadDevicesVinculatedToProduct(product.productId)
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

        
        self.vinculatedDevicesTable.clearContents()
        self.vinculatedDevicesTable.setRowCount(len(self.devicesFromProducts))
        
        # --> QFont That determinates the apearance of the text in the table #
        fontStyle = QFont()
        fontStyle.setBold(True)
        
        for row, device in enumerate(self.devicesFromProducts):

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

            self.vinculatedDevicesTable.setCellWidget(row, 0, deviceStatusIcon)

            if device.deviceDocSent == 1:
                deviceDocIcon.setPixmap(QIcon(":/doc_ok.png").pixmap(QSize(25,25)))
                deviceDocIcon.setToolTip("Documento de instalação enviado.")
            else:
                deviceDocIcon.setPixmap(QIcon(":/doc_nok.png").pixmap(QSize(25,25)))
                deviceDocIcon.setToolTip("Documento de instalação NÃO enviado!")

            self.vinculatedDevicesTable.setCellWidget(row, 1, deviceDocIcon)

            if device.deviceHasImage == 1 and device.deviceImageExtension:
                
                deviceImageButton = MyQDeviceImageButton(device.deviceId, device.deviceImageExtension, self)
                self.vinculatedDevicesTable.setCellWidget(row, 2, deviceImageButton)
          
            # --> Identificação do Dispositivo #
            item = QTableWidgetItem(str(device.deviceId).zfill(6))
            item.setData(Qt.UserRole, int(device.deviceId))
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.vinculatedDevicesTable.setItem(row, 3, item)

            # --> Descrição #
            item = QTableWidgetItem(device.deviceDescription)
            self.vinculatedDevicesTable.setItem(row, 4, item)

            # --> Função #
            item = QTableWidgetItem(device.deviceFunction)
            self.vinculatedDevicesTable.setItem(row, 5, item)
        

###############################################################################################################################################################################
 
    def loadProductsFromClient(self):
        """
        This method is called when a client is selected, loading all the products in the product list
        """
        self.addDeviceButton.setEnabled(False)
        currentClient = self.clientComboBox.itemData(self.clientComboBox.currentIndex())
        if currentClient <= 1:
            self.productsList.clear()
            self.hasTestCheckBox.setChecked(False)
            self.productDetailGroupBox.setEnabled(False)
            return

        
        self.productsList.clear()
        
        regularFont = QFont()
        regularFont.setBold(False)

        try:
            self.productsFromClient.loadProductsFromClient(currentClient, True)
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
        
        for product in self.productsFromClient:
            item = QListWidgetItem(product.productName)
            item.setData(Qt.UserRole, product.productId)
            item.setFont(regularFont)
            if product.prodHasTest == 1:
                item.setForeground(self.hasTestBrush)
            else:
                item.setForeground(self.noTestBrush)
            self.productsList.addItem(item)
        


###############################################################################################################################################################################
        

    def populateClientComboBox(self):
        """
        This method is called to load all the analyst active clients.
        """

        try:
            self.activeClients.loadClientsFromAnalyst(self.loggedUser["id"], True)
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


        self.clientComboBox.addItem("", -1)
        for row, client in enumerate(self.activeClients):
            self.clientComboBox.addItem(client.clientName, client.clientId)

        
###############################################################################################################################################################################


    def closeEvent(self, event):
        """
        This method remove its reference from its parent opened sub window list before being closed
        """
        del self.parent.openedSubWindows[self.SUBWINDOWID]
        self.close()
