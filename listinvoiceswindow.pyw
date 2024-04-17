import urllib.request
import configparser
import os
from ftplib import FTP

from PyQt5.QtCore import (
    Qt,
    QSize,
    QDate,
    QSortFilterProxyModel
    )

from PyQt5.QtGui import (
    QFont,
    QIcon,
    QIntValidator,
    QPalette,
    QStandardItemModel,
    QStandardItem,
    QBrush,
    QColor,
    QCursor
    )

from PyQt5.QtWidgets import (
    QMdiSubWindow,
    QWidget,
    QVBoxLayout,
    QGroupBox,
    QLabel,
    QLineEdit,
    QLayout,
    QVBoxLayout,
    QHBoxLayout,
    QDateEdit,
    QCalendarWidget,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QAbstractScrollArea,
    QHeaderView,
    QCheckBox,
    QComboBox,
    QCompleter,
    QMessageBox
    )

from myExceptions import *
import invoiceuploadwindow
import invoicescontainer
import clientscontainer

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

        self.setFixedWidth(113)
        

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

        self.setFixedWidth(200)


###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################


class MyQDownloadButton(QPushButton):
    def __init__(self, invoiceNumber=None, invoiceClientName=None, parent=None):
        super(MyQDownloadButton, self).__init__(parent)
        
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.fileName = invoiceClientName + "_" + str(invoiceNumber) + ".pdf"
        
        self.setIcon(QIcon(":/download.png"))

        self.clicked.connect(self.downloadInvoiceFile)

###############################################################################################################################################################################

    def downloadInvoiceFile(self):
        """
        This method overrides the click event, implementing the invoice download
        """

        parser = configparser.SafeConfigParser()
        parser.read("dbconfig.ini")
        
        FTPPath = parser.get("ftp", "path")
        FTPUser = parser.get("ftp", "user")
        FTPPass = parser.get("ftp", "pass")
        

        
        
        messageBox = QMessageBox()
        messageBox.setIcon(QMessageBox.Question)
        messageBox.setWindowIcon(QIcon(":/question.png"))
        messageBox.setWindowTitle("Download de Nota Fiscal")
        messageBox.setText("Salvar a nota fiscal \"" + self.fileName + "\" em sua área\nde trabalho?")
        messageBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        messageBox.button(QMessageBox.Yes).setText("Sim")
        messageBox.button(QMessageBox.No).setText("Não")
        
        messageBox.exec_()
        
        # --> If the Yes button was clicked #
        if messageBox.clickedButton() == messageBox.button(QMessageBox.No):
            return
        
        # --> Builds the path for the destination file #
        desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        destinationFilePath = desktop + "\\" + self.fileName


        try:
            ftp = FTP(FTPPath)
            ftp.login(FTPUser, FTPPass)
            ftp.cwd("nf")
            ftp.retrbinary("RETR " + self.fileName, open(destinationFilePath, "wb").write)
            ftp.quit()            
           
        except Exception as e:
            messageBox = QMessageBox()
            messageBox.setText("Falha ao efetuar o download da nota fiscal.\n" + str(e))
            messageBox.setWindowTitle("Erro!")
            messageBox.setIcon(QMessageBox.Critical)
            messageBox.setWindowIcon(QIcon(":/warning_icon.png"))
            messageBox.exec_()
            return


       
        messageBox = QMessageBox()
        messageBox.setIcon(QMessageBox.Information)
        messageBox.setWindowIcon(QIcon(":/warning_icon.png"))
        messageBox.setWindowTitle("Sucesso!")
        messageBox.setText("Download efetuado com sucesso.")
                
        messageBox.exec_()
         
            


###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################

class MyQDateEdit(QDateEdit):
    """
    This class reimplements the QDateEdit class
    """
    def __init__(self, parent=None):
        super(MyQDateEdit, self).__init__(parent)
        
        self.setFixedWidth(81)
        self.setCalendarPopup(True)
        self.setDisplayFormat("dd/MM/yyyy")
        self.calendarWidget().setHorizontalHeaderFormat(QCalendarWidget.NoHorizontalHeader)
        self.calendarWidget().setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.setFocusPolicy(Qt.NoFocus)
        
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

        self.setStyleSheet(calendarStylesheet)
        self.setMaximumDate(QDate.currentDate())

###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################
       

class MyQFilterComboBox(QComboBox):
    """
    This class extends the QcomboBox, adding a text filter
    """
    def __init__(self, parent=None):
        super(MyQFilterComboBox, self).__init__(parent)
        regularFont = QFont()
        regularFont.setBold(False)
        self.setFont(regularFont)
        
        # --> self configuration #
        self.setFocusPolicy(Qt.StrongFocus)
        self.setEditable(True)
        self.myCompleter = QCompleter(self)
        self.setFixedWidth(200)
        
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

class MyQTableWidget(QTableWidget):
    """
    This class is used to create a personilized qtablewidget for the window
    """
    def __init__(self, parent=None):
        super(MyQTableWidget, self).__init__(parent)
        self.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.setAlternatingRowColors(True)
        self.setAutoFillBackground(True)
        self.setMinimumSize(QSize(665, 300))
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

        # --> create the items for the headers #
        self.setColumnCount(6)

        receiptNumber = QTableWidgetItem(" Número da Nota ")
        receiptClient = QTableWidgetItem("Cliente")
        receiptDocSAP = QTableWidgetItem(" Número Doc. SAP ")
        receiptCreationDate = QTableWidgetItem(" Data de Cadastro ")
        receiptReturnDate = QTableWidgetItem(" Data de Retorno ")
        receiptDownload = QTableWidgetItem(" ")
        
        # --> Set the Header Items #
        self.setHorizontalHeaderItem(0, receiptNumber)
        self.setHorizontalHeaderItem(1, receiptClient)
        self.setHorizontalHeaderItem(2, receiptDocSAP)
        self.setHorizontalHeaderItem(3, receiptCreationDate)
        self.setHorizontalHeaderItem(4, receiptReturnDate)
        self.setHorizontalHeaderItem(5, receiptDownload)

        self.horizontalHeader().resizeSection(0, 112)
        self.horizontalHeader().resizeSection(1, 120)
        self.horizontalHeader().resizeSection(2, 117)
        self.horizontalHeader().resizeSection(3, 112)
        self.horizontalHeader().resizeSection(4, 112)
        self.horizontalHeader().resizeSection(5, 50)

        self.horizontalHeader().setStyleSheet(tableStylesheet)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)

###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################


class ListInvoicesWindow(QMdiSubWindow):
    """
    This class is responsible for rendering the "Listar Notas Fiscais" window
    as a MDI sub Window and for managing the data inside it
    """
    #constant id, used for location inside the openedSubWindows dictionary in the
    #main window
    SUBWINDOWID = "listinvoiceswindow"

    def __init__(self, parent=None):
        super(ListInvoicesWindow, self).__init__(parent)
        self.parent = parent
        self.loggedUser = parent.loggedUser
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.clientsList = clientscontainer.ClientsContainer()
        self.invoicesList = invoicescontainer.InvoicesContainer()
     

        self.isFiltering = False
        self.filteringFields = [] 

        ##################################################
        # --> BUILDING THE "LISTAR NOTAS FISCAIS" WINDOW #
        ##################################################

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

        # --> Numero #    
        numberFilterLabel = MyQLabel("Número: ")
        self.numberFilterField = MyQNumberLineEdit()

        # --> Data de Cadastro #
        sendingDateLabel = MyQLabel("Data de Cadastro: ")
        self.fromDateField = MyQDateEdit()
        self.fromDateField.setDate(QDate.currentDate().addMonths(-1))
        
        untilLabel = MyQLabel(" até ")
        untilLabel.setMinimumWidth(26)

        self.untilDateField = MyQDateEdit()
        self.untilDateField.setDate(QDate.currentDate())
        

        # --> Doc. SAP Number #
        docSAPFilterLabel = MyQLabel("Doc. SAP: ")
        self.docSAPFilterField = MyQNumberLineEdit()
       
        # --> Client #
        clientFilterLabel = MyQLabel("Cliente: ")
        self.clientFilterComboBox = MyQFilterComboBox()
        self.populateInvoiceComboBox()

        # --> Return Date #
        self.hasReturnDateCheckBox = QCheckBox("Com Data de Retorno")

        # --> Buttons #
        sendInvoiceButton = QPushButton(" Enviar Nota Fiscal ")                
        sendInvoiceButton.setFont(regularFont)
        sendInvoiceButton.setCursor(QCursor(Qt.PointingHandCursor))

        clearFilterButton = QPushButton(" Limpar ")
        clearFilterButton.setMinimumWidth(98)
        clearFilterButton.setFont(regularFont)
        clearFilterButton.setCursor(QCursor(Qt.PointingHandCursor))
        
        filterButton = QPushButton(" Filtrar ")
        filterButton.setMinimumWidth(98)
        filterButton.setFont(regularFont)
        filterButton.setCursor(QCursor(Qt.PointingHandCursor))

        # --> Table of files #
        self.invoicesTable = MyQTableWidget()
        
        
        # --> First Row Filter Layout #
        firstRowFilterLayout = QHBoxLayout()
        firstRowFilterLayout.addWidget(numberFilterLabel)
        firstRowFilterLayout.addWidget(self.numberFilterField)
        firstRowFilterLayout.addWidget(clientFilterLabel)
        firstRowFilterLayout.addWidget(self.clientFilterComboBox)
        firstRowFilterLayout.addStretch(1)

        # --> Second Row Filter Layout #
        secondRowFilterLayout = QHBoxLayout()
        secondRowFilterLayout.addWidget(docSAPFilterLabel)
        secondRowFilterLayout.addWidget(self.docSAPFilterField)
        secondRowFilterLayout.addWidget(sendingDateLabel)
        secondRowFilterLayout.addWidget(self.fromDateField)
        secondRowFilterLayout.addWidget(untilLabel)
        secondRowFilterLayout.addWidget(self.untilDateField)
        secondRowFilterLayout.addStretch(1)

        # --> Third Row Filter Layout #
        thirdRowFilterLayout = QHBoxLayout()
        thirdRowFilterLayout.addWidget(self.hasReturnDateCheckBox)
        thirdRowFilterLayout.addStretch(1)
        thirdRowFilterLayout.addWidget(clearFilterButton)
        thirdRowFilterLayout.addWidget(filterButton)

        thirdRowFilterLayout.insertSpacing(0, 58)
        

        # --> building the filter layout #
        filterLayout = QVBoxLayout()
        filterLayout.addLayout(firstRowFilterLayout)
        filterLayout.addLayout(secondRowFilterLayout)
        filterLayout.addLayout(thirdRowFilterLayout)
        filterGroupBox.setLayout(filterLayout)

        # --> building the "send receipt" button layout
        sendInvoiceButtonLayout = QHBoxLayout()
        sendInvoiceButtonLayout.addWidget(sendInvoiceButton)
        sendInvoiceButtonLayout.addStretch(1)


        # --> build the subwindow layout #
        layout = QVBoxLayout()
        layout.addLayout(sendInvoiceButtonLayout)
        layout.addWidget(filterGroupBox)
        layout.addWidget(self.invoicesTable)
        layout.addStretch(1)
        
        
        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setWidget(centralWidget)
        self.setWindowIcon(QIcon(":/invoices2.png"))
        self.setWindowFlags(Qt.Window | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
        
        # --> Line responsible for preventing window resize
        #self.layout().setSizeConstraint(QLayout.SetFixedSize)

        self.updateInvoicesTable()
        
        # --> Connecting the signals #

        sendInvoiceButton.clicked.connect(self.openInvoiceUploadWindow)
        clearFilterButton.clicked.connect(self.clearFilter)
        filterButton.clicked.connect(self.filterTable)

###############################################################################################################################################################################

    def filterTable(self):
        """
        This method is called when the button "Filtrar" is clicked, creating the fields list
        that will be passed to the updateCallsTable
        """
        self.filteringFields = []

        fromDate = self.fromDateField.text().split("/")
        untilDate = self.untilDateField.text().split("/")

        self.filteringFields.append("DATE(nof_data_hora_cadastro) >= DATE('" + fromDate[2] + "-" + fromDate[1] + "-" + fromDate[0] + "')")
        self.filteringFields.append("DATE(nof_data_hora_cadastro) <= DATE('" + untilDate[2] + "-" + untilDate[1] + "-" + untilDate[0] + "')")

        if self.numberFilterField.text():
            self.filteringFields.append("nof_numero LIKE '%" + self.numberFilterField.text() + "%'")

        if self.clientFilterComboBox.currentIndex() > 0:
            self.filteringFields.append("nof_cliente = '" +str(self.clientFilterComboBox.itemData(self.clientFilterComboBox.currentIndex()))+ "'")

        if self.docSAPFilterField.text():
            self.filteringFields.append("nof_doc_sap LIKE '%" + self.docSAPFilterField.text() + "%'")

        
        if self.hasReturnDateCheckBox.isChecked():
            self.filteringFields.append("nof_com_retorno = '1'")


        if len(self.filteringFields):
            self.isFiltering = True
        else:
            self.isFiltering = False
    
        self.updateInvoicesTable()
       

###############################################################################################################################################################################

    def updateInvoicesTable(self):
        """
        This method loads the invoices to the table using its filter
        """
        try:
            self.invoicesList.loadInvoices(self.isFiltering, self.filteringFields)
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


        self.invoicesTable.clearContents()
        self.invoicesTable.setRowCount(len(self.invoicesList))
        self.updateSubWindowTitle()

        # --> QFont That determinates the apearance of the text in the table #
        fontStyle = QFont()
        fontStyle.setBold(True)

        
      
        greenBrush = QBrush(QColor(66, 255, 100, 100), Qt.SolidPattern)
        yellowBrush = QBrush(QColor(244, 241, 66, 100), Qt.SolidPattern)
        redBrush = QBrush(QColor(255, 66, 66, 100), Qt.SolidPattern)
        noBrush = QBrush()
        
        for row, invoice in enumerate(self.invoicesList):
            if invoice.invoiceHasReturn:
                if invoice.remainingDays >= 7:
                    brush = greenBrush
                elif invoice.remainingDays >= 0:
                    brush = yellowBrush
                else:
                    brush = redBrush
            else:
                brush = noBrush
            
            
            # --> Invice Number #
            item = QTableWidgetItem(str(invoice.invoiceNumber))
            item.setData(Qt.UserRole, int(invoice.invoiceId))
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            item.setBackground(brush)

            self.invoicesTable.setItem(row, 0, item)

            # --> Client #
            item = QTableWidgetItem(invoice.invoiceClientName)
            item.setBackground(brush)

            self.invoicesTable.setItem(row, 1, item)

            # --> Invoice Doc SAP Number #
            item = QTableWidgetItem(invoice.invoiceDocSAP)
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            item.setBackground(brush)

            self.invoicesTable.setItem(row, 2, item)

            # --> Invoice Upload Date #
            item = QTableWidgetItem(invoice.invoiceRecordDate)
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            item.setBackground(brush)

            self.invoicesTable.setItem(row, 3, item)

            # --> Invoice Return Date #
            if invoice.invoiceHasReturn:
                item = QTableWidgetItem(invoice.invoiceReturnDate)
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                item.setBackground(brush)

                self.invoicesTable.setItem(row, 4, item)


            item = QTableWidgetItem()
            item.setBackground(brush)
            self.invoicesTable.setItem(row, 5, item)

            downloadButton = MyQDownloadButton(invoice.invoiceNumber, invoice.invoiceClientName)
            self.invoicesTable.setCellWidget(row, 5, downloadButton)
            
###############################################################################################################################################################################

    def updateSubWindowTitle(self):
        """
        This method is used to update the window title with the total number of opened calls
        """
        if len(self.invoicesList) != 1:
            self.setWindowTitle("Listagem de Notas Fiscais - %d Arquivos" % len(self.invoicesList))
        else:
            self.setWindowTitle("Listagem de Notas Fiscais - 1 Arquivo")

###############################################################################################################################################################################

    def clearFilter(self):
        """
        This method is called when the button "Limpar" is clicked, cleaning the filter fields
        """
        self.isFiltering = False
        self.filteringFields = []        
        
        self.fromDateField.setDate(QDate.currentDate().addMonths(-1))
        self.untilDateField.setDate(QDate.currentDate())
        
        self.numberFilterField.setText("")
        self.docSAPFilterField.setText("")

        self.clientFilterComboBox.lineEdit().setText("")
        self.clientFilterComboBox.setCurrentIndex(-1)
        self.clientFilterComboBox.myCompleter.setCompletionPrefix("")
        self.clientFilterComboBox.pFilterModel.setFilterFixedString("")
        
        self.hasReturnDateCheckBox.setChecked(False)

        self.updateInvoicesTable()
        

###############################################################################################################################################################################

    def populateInvoiceComboBox(self):
        """
        This method loads all the active clients
        """        
        try:
            self.clientsList.loadActiveClients()
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

        model = QStandardItemModel()
        item = QStandardItem("")
        item.setData(-1, Qt.UserRole)
        model.setItem(0, 0, item)
        for row, client in enumerate(self.clientsList):
            item = QStandardItem(client.clientName)
            item.setData(client.clientId, Qt.UserRole)
            model.setItem((row+1), 0, item)

        self.clientFilterComboBox.setModel(model)
        self.clientFilterComboBox.setModelColumn(0)

        self.clientFilterComboBox.setCurrentIndex(0)

###############################################################################################################################################################################

    def openInvoiceUploadWindow(self):
        """
        This method opens the dialog responsible for uploading the receipts
        """
        invoiceUploadWindow = invoiceuploadwindow.InvoiceUploadWindow(self)
        invoiceUploadWindow.setModal(True)

        invoiceUploadWindow.show()
          
        xPos = (self.parent.screenResolution['w'] - invoiceUploadWindow.width()) / 2
        yPos = (self.parent.screenResolution['h'] - invoiceUploadWindow.height()) / 2
            
        invoiceUploadWindow.move(xPos, yPos)
        invoiceUploadWindow.raise_()
        invoiceUploadWindow.activateWindow()
        
###############################################################################################################################################################################
        
    def closeEvent(self, event):
        """
        This method remove its reference from its parent opened sub window list before being closed
        """
        del self.parent.openedSubWindows[self.SUBWINDOWID]
        self.close()
