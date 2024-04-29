from configparser import SafeConfigParser
from ftplib import FTP
import tempfile
import os

from PyQt5.QtCore import (
        Qt,
        QDate,
        QSize,
        QSortFilterProxyModel
    )

from PyQt5.QtGui import (
        QFont,
        QIcon,
        QPalette,
        QIntValidator,
        QImage,
        QPixmap,
        QStandardItemModel,
        QStandardItem,
        QCursor
    )

from PyQt5.QtWidgets import (
        QMdiSubWindow,
        QGroupBox,
        QLabel,
        QDateEdit,
        QCalendarWidget,
        QLineEdit,
        QComboBox,
        QSpacerItem,
        QCheckBox,
        QPushButton,
        QLayout,
        QHBoxLayout,
        QVBoxLayout,
        QTableWidget,
        QAbstractScrollArea,
        QTableWidgetItem,
        QHeaderView,
        QWidget,
        QFileDialog,
        QMessageBox,
        QCompleter,
        QDialog
    )

from myExceptions import *
import clientscontainer
import productscontainer
import devicescontainer
import devicemaintenancewindow

import maintenancelogscontainer

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
        boldFont = QFont()
        boldFont.setBold(True)

        self.setFixedWidth(120)
        self.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.setFont(boldFont)

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


    """
    Adicionado a funcionalidade de selecionar itens de uma listbox com o teclado e enter;
    """
    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Enter, Qt.Key_Return):
            text = self.currentText()
            index = self.findText(text)
            if index != -1:
                self.setCurrentIndex(index)
            return
        elif event.key() == Qt.Key_Up:
            if self.currentIndex() > 0:
                self.setCurrentIndex(self.currentIndex() - 1)
        elif event.key() == Qt.Key_Down:
            if self.currentIndex() < self.count() - 1:
                self.setCurrentIndex(self.currentIndex() + 1)
        else:
            super(MyQFilterComboBox, self).keyPressEvent(event)

    def setTextIfCompleterIsClicked(self, text):
        if text:
            index = self.findText(text)
            if index != -1:
                self.setCurrentIndex(index)
    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            self.setCurrentIndex(max(0, self.currentIndex() - 1))
        else:
            self.setCurrentIndex(min(self.count() - 1, self.currentIndex() + 1))

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
class MyQDateEdit(QDateEdit):
    """
    This class reimplements the qdateedit class
    """
    def __init__(self, date=None, parent=None):
        super(MyQDateEdit, self).__init__(parent)

        calendarStylesheet = "QCalendarWidget QWidget#qt_calendar_navigationbar :hover{"\
                     "          font-weight: bold;" \
                     "          color: white;}" \
                     "QCalendarWidget QWidget#qt_calendar_navigationbar{"\
                     "          font-weight: bold;" \
                     "          color: white;" \
                     "          background-color: qlineargradient( " \
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
                     "                      stop: 1 #131313);}" \
                     "QCalendarWidget QWidget{"\
                     "          font-weight: bold;" \
                     "          selection-background-color: qlineargradient( " \
                     "                      x1:0, " \
                     "                      y1:0, " \
                     "                      x2:0, " \
                     "                      y2:1, " \
                     "                      stop:0 #7C7C7C, " \
                     "                      stop: 0.12 #898989, " \
                     "                      stop: 0.25 #999999, " \
                     "                      stop: 0.39 #777777, " \
                     "                      stop: 0.5 #5C5C5C, " \
                     "                      stop: 0.51 #333333, " \
                     "                      stop: 0.60 #444444, " \
                     "                      stop: 0.76 #5B5B5B, " \
                     "                      stop: 0.91 #4C4C4C, " \
                     "                      stop: 1 #434343);}"

        self.setCalendarPopup(True)
        self.setDisplayFormat("dd/MM/yyyy")
        self.calendarWidget().setHorizontalHeaderFormat(QCalendarWidget.NoHorizontalHeader)
        self.calendarWidget().setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.setStyleSheet(calendarStylesheet)
        self.setFocusPolicy(Qt.NoFocus)

        if date:
            self.setDate(date)


###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################

class MyQPushButton(QPushButton):
    """
    This class reimplements the qpushbutton class
    """
    def __init__(self, text="", parent=None):
        super(MyQPushButton, self).__init__(text, parent)

        regularFont = QFont()
        regularFont.setBold(False)

        self.setMinimumWidth(99)
        self.setFont(regularFont)
        self.setCursor(QCursor(Qt.PointingHandCursor))


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
        self.setSelectionMode(QTableWidget.SingleSelection)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.horizontalHeader().setStretchLastSection(True)
        self.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.horizontalHeader().setHighlightSections(False)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.setMinimumSize(QSize(870, 400))
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

        self.horizontalHeader().setStyleSheet(tableStylesheet)

        # --> Create the Items for the headers #
        self.setColumnCount(7)

        maintenanceStatusIcon = QTableWidgetItem(" ")
        deviceImageIcon = QTableWidgetItem(" ")
        
        deviceId = QTableWidgetItem("Identificação")
        deviceDescription = QTableWidgetItem("Descrição")
        client = QTableWidgetItem("Cliente")
        lastMaintenance = QTableWidgetItem("Última Manutenção")
        nextMaintenance = QTableWidgetItem("Próxima Manutenção")

        # --> Set the Header Items #
        self.setHorizontalHeaderItem(0, maintenanceStatusIcon)
        self.setHorizontalHeaderItem(1, deviceImageIcon)
        self.setHorizontalHeaderItem(2, deviceId)
        self.setHorizontalHeaderItem(3, deviceDescription)
        self.setHorizontalHeaderItem(4, client)
        self.setHorizontalHeaderItem(5, lastMaintenance)
        self.setHorizontalHeaderItem(6, nextMaintenance)

        self.horizontalHeader().resizeSection(0, 30)
        self.horizontalHeader().resizeSection(1, 30)
        self.horizontalHeader().resizeSection(2, 100)
        self.horizontalHeader().resizeSection(3, 300)
        self.horizontalHeader().resizeSection(4, 130)
        self.horizontalHeader().resizeSection(5, 150)
        self.horizontalHeader().resizeSection(6, 150)


###############################################################################################################################################################################
###############################################################################################################################################################################

###############################################################################################################################################################################

class ListMaintenancesWindow(QMdiSubWindow):
    """
    This class is responsible for rendering the "Listar Chamados" window
    as a MDI sub Window and for managing the data inside it
    """
    # --> Constant id, used for location inside the openedSubWindows dictionary in the main window #
    SUBWINDOWID = "listmaintenanceswindow"
    
    def __init__(self, parent=None):
        super(ListMaintenancesWindow, self).__init__(parent)
        self.parent = parent
        self.loggedUser = parent.loggedUser
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowFlags(Qt.SubWindow | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)

        self.clientsList = clientscontainer.ClientsContainer()
        self.productsList = productscontainer.ProductsContainer()

        self.devicesList = devicescontainer.DevicesContainer()

        self.maintenanceLogsList = maintenancelogscontainer.MaintenanceLogsContainer()

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
        self.deviceDescriptionField = MyQLineEdit()
        self.deviceDescriptionField.setMinimumWidth(243)
        self.deviceDescriptionField.setMaxLength(40)
        self.deviceDescriptionField.setFont(regularFont)

        # --> Data Ultima Manutenção #

        openingDatetime = MyQLabel("Última Manutenção: ")
                        
        self.fromDateField = MyQDateEdit(QDate.currentDate().addYears(-1))
        
        untilLabel = QLabel(" até ")
        untilLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        untilLabel.setMinimumWidth(30)

        self.untilDateField = MyQDateEdit(QDate.currentDate())

        # --> Por dias Corridos #
        self.passedDaysCheckBox = MyQCheckBox("Por dias corridos")
        self.passedDaysCheckBox.setMinimumWidth(285)
        self.passedDaysCheckBox.setChecked(True)

        # --> Propriedade do cliente #
        self.clientComboBox = MyQFilterComboBox()
        self.populateClientComboBox()

        # --> Product Combobox #
        productLabel = MyQLabel("Produto: ")
        self.productComboBox = MyQFilterComboBox()
        self.productComboBox.setMinimumWidth(204)


        self.clientPropertyCheckBox = MyQCheckBox("Propriedade do Cliente: ", [self.clientComboBox, self.productComboBox])
        self.clientPropertyCheckBox.setChecked(True)

        # --> Por placas testadas #
        self.testedBoardsCheckBox = MyQCheckBox("Por placas testadas")
        self.testedBoardsCheckBox.setMinimumWidth(285)
        self.testedBoardsCheckBox.setChecked(True)

        # --> Propriedade da Hi-Mix #
        self.himixPropertyCheckBox = MyQCheckBox("Propriedade da Hi-Mix")
        self.himixPropertyCheckBox.setChecked(True)

        # --> Botoes #
        filterButton = MyQPushButton(" Filtrar ")
        clearFilterButton = MyQPushButton(" Limpar ")

        # --> First Row Filter Layout #
        firstRowFilterLayout = QHBoxLayout()
        firstRowFilterLayout.addWidget(deviceIdLabel)
        firstRowFilterLayout.addWidget(self.deviceIdField)
        firstRowFilterLayout.addWidget(deviceDescriptionLabel)
        firstRowFilterLayout.addWidget(self.deviceDescriptionField)
        firstRowFilterLayout.addWidget(openingDatetime)
        firstRowFilterLayout.addWidget(self.fromDateField)
        firstRowFilterLayout.addWidget(untilLabel)
        firstRowFilterLayout.addWidget(self.untilDateField)

        # --> Second Row Filter Layout #
        secondRowFilterLayout = QHBoxLayout()
        secondRowFilterLayout.addWidget(self.passedDaysCheckBox)
        secondRowFilterLayout.addWidget(self.clientPropertyCheckBox)
        secondRowFilterLayout.addWidget(self.clientComboBox)
        secondRowFilterLayout.addWidget(productLabel)
        secondRowFilterLayout.addWidget(self.productComboBox)

        # --> Third Row Filter Layout #
        thirdRowFilterLayout = QHBoxLayout()
        thirdRowFilterLayout.addWidget(self.testedBoardsCheckBox)
        thirdRowFilterLayout.addWidget(self.himixPropertyCheckBox)
        thirdRowFilterLayout.addStretch(1)
        thirdRowFilterLayout.addWidget(filterButton)
        thirdRowFilterLayout.addWidget(clearFilterButton)

        # --> building the filter layout #
        filterLayout = QVBoxLayout()
        filterLayout.addLayout(firstRowFilterLayout)
        filterLayout.addLayout(secondRowFilterLayout)
        filterLayout.addLayout(thirdRowFilterLayout)
        filterGroupBox.setLayout(filterLayout)
        

        # --> Tabela de Manutenções #
        self.maintenancesTable = MyQTableWidget()


        # --> Define the window layout #
        windowLayout = QVBoxLayout()
        #windowLayout.addLayout(rowButtonLayout)
        windowLayout.addWidget(filterGroupBox)
        windowLayout.addWidget(self.maintenancesTable)

       
        centralWidget = QWidget()
        centralWidget.setLayout(windowLayout)
        self.setWidget(centralWidget)
        self.setWindowIcon(QIcon(":/maintenance.png"))
        self.setWindowFlags(Qt.Window | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)

        self.updateMaintenancesTable()

        ###########################
        #### SIGNALS AND SLOTS ####
        ###########################
        
        self.clientComboBox.currentIndexChanged.connect(self.populateProductsComboBox)
        filterButton.clicked.connect(self.filterTable)
        clearFilterButton.clicked.connect(self.clearFilter)
        self.clientPropertyCheckBox.toggled.connect(self.clientPropertyCheckboxChecker)
        self.himixPropertyCheckBox.toggled.connect(self.himixPropertyCheckboxChecker)
        self.passedDaysCheckBox.toggled.connect(self.passedDaysCheckboxChecker)
        self.testedBoardsCheckBox.toggled.connect(self.testedBoardsCheckboxChecker)
        self.maintenancesTable.itemDoubleClicked.connect(self.opendeviceMaintenanceWindow)

###############################################################################################################################################################################
        
        
    def opendeviceMaintenanceWindow(self):
        """
        This method is called when a maintenance is double clicked or the button "abrir manutenção" is clicked
        """
        device = self.currentRowMaintenance()
        #-->
        deviceMaintenanceWindow = devicemaintenancewindow.DeviceMaintenanceWindow(device, None, self)
        deviceMaintenanceWindow.setModal(True)

        deviceMaintenanceWindow.show()
          
        xPos = (self.parent.screenResolution['w'] - deviceMaintenanceWindow.width()) / 2
        yPos = (self.parent.screenResolution['h'] - deviceMaintenanceWindow.height()) / 2
            
        deviceMaintenanceWindow.move(xPos, yPos)
        deviceMaintenanceWindow.raise_()
        deviceMaintenanceWindow.activateWindow()

        
###############################################################################################################################################################################

    
    def currentRowMaintenance(self):
        """
        This method returns the current selected row
        """
        row = self.maintenancesTable.currentRow()
        if row > -1:
            item = self.maintenancesTable.item(row, 2)
            key = item.data(Qt.UserRole)
            return self.devicesList.deviceFromId(key)

        return None

###############################################################################################################################################################################
    def passedDaysCheckboxChecker(self, wasChecked):
        """
        This method is used when  the "Por dias Corridos" checkbox is toggled. It doesn't allow
        to uncheck both "Por dias corridos" e "por placas testadas" checkbox
        """
        if not wasChecked:
            if not self.testedBoardsCheckBox.isChecked():
                self.passedDaysCheckBox.setChecked(True)
                
###############################################################################################################################################################################
    def testedBoardsCheckboxChecker(self, wasChecked):
        """
        This method is used when  the "Por dias Corridos" checkbox is toggled. It doesn't allow
        to uncheck both "Por dias corridos" e "por placas testadas" checkbox
        """
        if not wasChecked:
            if not self.passedDaysCheckBox.isChecked():
                self.testedBoardsCheckBox.setChecked(True)

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
                self.productComboBox.setDisabled(True)
        else:
            self.clientComboBox.setDisabled(False)
            self.productComboBox.setDisabled(False)

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

    def verifyIfUserDoingMaintenance(self):
        """
        This method verifies if a maintenance is being done by the logged user.
        If it happens is because the program was closed before finish the maintenance
        """
        try:
            deviceId, maintenanceId = self.maintenanceLogsList.verifyAnyOpenedMaintenance(self.loggedUser['id'])
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

        if maintenanceId:
            device = self.devicesList.deviceFromId(deviceId)

            deviceMaintenanceWindow = devicemaintenancewindow.DeviceMaintenanceWindow(device, maintenanceId, self)
            deviceMaintenanceWindow.setModal(True)

            deviceMaintenanceWindow.show()
              
            xPos = (self.parent.screenResolution['w'] - deviceMaintenanceWindow.width()) / 2
            yPos = (self.parent.screenResolution['h'] - deviceMaintenanceWindow.height()) / 2
                
            deviceMaintenanceWindow.move(xPos, yPos)
            deviceMaintenanceWindow.raise_()
            deviceMaintenanceWindow.activateWindow()

        
###############################################################################################################################################################################


    def clearFilter(self):
        """
        This method is called when the button "Limpar" is clicked, cleaning the filter fields
        """
        self.isFiltering = False
        self.filteringFields = []        
        
        self.fromDateField.setDate(QDate(2017, 10, 20))
        self.untilDateField.setDate(QDate.currentDate())
        
        self.deviceIdField.setText("")
        self.deviceDescriptionField.setText("")

        self.clientComboBox.setCurrentIndex(0)
        self.productComboBox.setCurrentIndex(0)

        self.passedDaysCheckBox.setChecked(True)
        self.testedBoardsCheckBox.setChecked(True)

        self.himixPropertyCheckBox.setChecked(True)
        self.clientPropertyCheckBox.setChecked(True)

        self.updateMaintenancesTable()

###############################################################################################################################################################################
    
    def filterTable(self):
        """
        This method is called when the button "Filtrar" is clicked, creating the fields list
        that will be passed to the updateMaintenancesTable
        """
        self.filteringFields = []

        if  self.deviceIdField.text():
            self.filteringFields.append("LPAD(dis_id, 6, '0') LIKE '%" + self.deviceIdField.text() + "%'")

        if self.deviceDescriptionField.text():
            self.filteringFields.append("dis_descricao LIKE '%" + self.deviceDescriptionField.text() + "%'")
        
        fromDate = self.fromDateField.text().split("/")
        untilDate = self.untilDateField.text().split("/")

        self.filteringFields.append(
            "(( DATE(dim_data_ultima_manutencao) >= DATE('" + fromDate[2] + "-" + fromDate[1] + "-" + fromDate[0] + "')" \
            " AND DATE(dim_data_ultima_manutencao) <= DATE('" + untilDate[2] + "-" + untilDate[1] + "-" + untilDate[0] + "')) OR dim_data_ultima_manutencao IS NULL)")
        
    
        ownerListAux = []

        if self.himixPropertyCheckBox.isChecked():
            ownerListAux.append("dis_cliente IS NULL")
        
        if self.clientPropertyCheckBox.isChecked():
            if self.clientComboBox.currentIndex() <= 0:
                ownerListAux.append("dis_cliente IS NOT NULL")
            else:
                ownerListAux.append("dis_cliente = '" + str(self.clientComboBox.itemData(self.clientComboBox.currentIndex())) + "'")

        self.filteringFields.append("(" + " OR ".join(ownerListAux) + ")")
        
        if self.productComboBox.currentIndex() > 0:
            self.filteringFields.append("vdp_produto = '" + str(self.productComboBox.itemData(self.productComboBox.currentIndex())) + "'")

        maintenanceTypeAux = []
        if self.passedDaysCheckBox.isChecked():
            maintenanceTypeAux.append("dim_tipo_intervalo = 'DIA'")

        if self.testedBoardsCheckBox.isChecked():
            maintenanceTypeAux.append("dim_tipo_intervalo = 'PLACA'")

        self.filteringFields.append("(" + " OR ".join(maintenanceTypeAux) + ")")       
        
        #print(self.filteringFields)
        
        if len(self.filteringFields):
            self.isFiltering = True
        else:
            self.isFiltering = False

       
        self.updateMaintenancesTable()

###############################################################################################################################################################################

    def updateMaintenancesTable(self):
        """
        This method loads the maintenances to the table using the data in the fields to filter the result
        """
        try:
            self.devicesList.loadDevicesForMaintenance(self.isFiltering, self.filteringFields)
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

        self.maintenancesTable.clearContents()
        self.maintenancesTable.setRowCount(len(self.devicesList))
        self.verifyIfUserDoingMaintenance()
        self.updateSubWindowTitle()

        # --> QFont That determinates the apearance of the text in the table #
        fontStyle = QFont()
        fontStyle.setBold(True)

        self.devicesList.maintenanceSort()

        for row, device in enumerate(self.devicesList):

            # --> Icone #
            deviceMaintenanceStatusIcon = QLabel()
            deviceHasImageIcon = QLabel()

            if device.devicePercentageMaintenance <= 70:
                deviceMaintenanceStatusIcon.setPixmap(QIcon(":/green_icon.png").pixmap(QSize(30,30)))

            elif device.devicePercentageMaintenance <= 90:
                deviceMaintenanceStatusIcon.setPixmap(QIcon(":/yellow_icon.png").pixmap(QSize(30,30)))

            else:
                deviceMaintenanceStatusIcon.setPixmap(QIcon(":/red_icon.png").pixmap(QSize(30,30)))

            deviceMaintenanceStatusIcon.setToolTip(str(device.devicePercentageMaintenance).replace(".", ",") + " %")


            self.maintenancesTable.setCellWidget(row, 0, deviceMaintenanceStatusIcon)

            if device.deviceHasImage == 1 and device.deviceImageExtension:

                deviceImageButton = MyQDeviceImageButton(device.deviceId, device.deviceImageExtension, self)
                self.maintenancesTable.setCellWidget(row, 1, deviceImageButton)

            # --> Identificação do Dispositivo #
            item = QTableWidgetItem(str(device.deviceId).zfill(6))
            item.setData(Qt.UserRole, int(device.deviceId))
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.maintenancesTable.setItem(row, 2, item)

            # --> Descrição #
            item = QTableWidgetItem(device.deviceDescription)
            self.maintenancesTable.setItem(row, 3, item)

            # --> Cliente #
            item = QTableWidgetItem(device.deviceClientName)
            self.maintenancesTable.setItem(row, 4, item)

            # --> Última Manutenção
            item = QTableWidgetItem(device.deviceLastMaintenance)
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.maintenancesTable.setItem(row, 5, item)

            # --> Última Manutenção
            item = QTableWidgetItem(device.deviceNextMaintenance)
            self.maintenancesTable.setItem(row, 6, item)

    
###############################################################################################################################################################################


    def updateSubWindowTitle(self):
        """
        This method is used to update the window title with the total number of opened calls
        """
        if len(self.devicesList) != 1:
            self.setWindowTitle("Listagem de Manutenções - %d Dispositivos" % len(self.devicesList))
        else:
            self.setWindowTitle("Listagem de Manutenções - 1 Dispositivo")            

###############################################################################################################################################################################
       
    def closeEvent(self, event):
        """
        This method remove its reference from its parent opened sub window list before being closed
        """
        del self.parent.openedSubWindows[self.SUBWINDOWID]
        self.close()

