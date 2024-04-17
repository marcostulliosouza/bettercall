import os
import configparser
from ftplib import FTP

from PyQt5.QtCore import (
    Qt,
    QSortFilterProxyModel,
    QDate,
    QThread,
    pyqtSignal
    )

from PyQt5.QtGui import (
    QIcon,
    QFont,
    QIntValidator,
    QStandardItemModel,
    QStandardItem,
    QCursor
    )

from PyQt5.QtWidgets import (
    QDialog,
    QLabel,
    QLineEdit,
    QLayout,
    QGridLayout,
    QHBoxLayout,
    QComboBox,
    QCompleter,
    QPushButton,
    QCheckBox,
    QDateEdit,
    QCalendarWidget,
    QFileDialog,
    QProgressBar,
    QMessageBox
    )

import qrc_resources
import clientscontainer
import invoicescontainer
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

        self.setMinimumWidth(117)


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
        self.setMinimumWidth(200)
        
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
    def __init__(self, text="", dependentField=None, parent=None):
        super(MyQCheckBox, self).__init__(text, parent)

        # --> appearance #
        boldFont = QFont()
        boldFont.setBold(True)
        self.setFont(boldFont)

        self.setMinimumWidth(10)

        # --> functionalities #
        self.textField = dependentField

        self.stateChanged.connect(self.textField.setEnabled)
        
        
        
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
        self.setMinimumDate(QDate.currentDate())

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
        filePath, viewType = QFileDialog.getOpenFileName(self, "Selecione a Nota Fiscal", path, "Arquivos PDF(*.pdf)")
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

    
###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################

class InvoiceUploadThread(QThread):
    """
    Thread responsible for uploading the file and creating its record in the
    database
    """
    updateBarValue = pyqtSignal(int)
    updateTextValue = pyqtSignal(str)
    updateStatusNormal = pyqtSignal(str)
    updateStatusWarning = pyqtSignal(str)
    updateThreadErrorCode = pyqtSignal(int)
    threadFinishedWell = pyqtSignal()

    def __init__(self):
        """
        At the instantiation of the Thread it gathers the path for the file server in the config.ini 
        """
        QThread.__init__(self)
        
        parser = configparser.SafeConfigParser()
        parser.read("dbconfig.ini")
        
        self.FTPPath = parser.get("ftp", "path")
        self.FTPUser = parser.get("ftp", "user")
        self.FTPPass = parser.get("ftp", "pass")
        
###############################################################################################################################################################################

    def setDataDict(self, dataDict):
        self.dataDict = dataDict

###############################################################################################################################################################################

    def run(self):
        """
        This method is responsible for translating and inserting the
        data from the invoice that is being uploaded
        """

        ##############################################################################################################
        # --> firstly builds up the destination file name. It will be composed by its client name and invoice number #
        ##############################################################################################################
        destinyName = self.dataDict["invoiceClientName"] + "_" + str(self.dataDict["invoiceNumber"]) + ".pdf"        
       
                

        #self.updateTextValue.emit("%d KBs de %d KBs concluídos" % (transfered, fsize))
        
        # --> Copy the file to its destination
        


        try:
            file = open(self.dataDict["invoiceFilePath"], "rb")
            ftp = FTP(self.FTPPath)
            ftp.login(self.FTPUser, self.FTPPass)
            ftp.cwd("nf")
            ftp.storbinary("STOR " + destinyName, file)

            file.close()
            ftp.quit()
        except Exception as e:
            self.updateThreadErrorCode.emit(2)
            self.quit()
            
        
        self.updateBarValue.emit(100.0)
        self.updateStatusNormal.emit("Arquivo transferido com sucesso. Inserindo no banco de dados suas informações.")

        # --> creates a new invoice object #
        newInvoice = invoicescontainer.Invoice(
                                               None,
                                               self.dataDict["invoiceNumber"],
                                               self.dataDict["invoiceClientId"],
                                               self.dataDict["invoiceClientName"],
                                               self.dataDict["invoiceDocSap"],
                                               "",
                                               self.dataDict["invoiceHasReturnDate"],
                                               self.dataDict["invoiceReturnDate"]
                                            )

        
        try:
            newInvoice.insertNewInvoice()
        except DatabaseConnectionError as error:
            # --> removes the uploaded file #
            os.remove(destiny)
            self.updateThreadErrorCode.emit(1)
                        
            place, cause = error.args

            message = "Falha em: " + place + "\nErro: " +cause
            
            messageBox = QMessageBox()
            messageBox.setText(message)
            messageBox.setWindowTitle("Erro!")
            messageBox.setIcon(QMessageBox.Critical)
            messageBox.setWindowIcon(QIcon(":/warning_icon.png"))
            messageBox.exec_()
            self.quit()
            
        
        except Exception as error:
            # --> removes the uploaded file #
            os.remove(destiny)
            self.updateThreadErrorCode.emit(2)
            self.quit()
            

        self.updateBarValue.emit(100)
        
###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################

class InvoiceUploadWindow(QDialog):
    """
    This class is responsible for rendering the receipt upload window
    """
    def __init__(self, parent=None):
        super(InvoiceUploadWindow, self).__init__(parent)
        self.parent = parent
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.clientsList = clientscontainer.ClientsContainer()
        self.uploadThread = InvoiceUploadThread()
        self.threadError = 0

        # --> invoice number #
        invoiceNumberLabel = MyQLabel("Número da Nota Fiscal: ")        
        self.invoiceNumberField = MyQNumberLineEdit()


        # --> invoice client #
        invoiceClientLabel = MyQLabel("Cliente:  ")
        
        self.invoiceClientComboBox = MyQFilterComboBox()
        self.populateInvoiceComboBox()

        # --> invoice Doc SAP #
        invoiceDocSAPLabel = MyQLabel("Número Doc. SAP: ")
        self.invoiceDocSAPField = MyQNumberLineEdit()

        # --> invoice return date #
        self.invoiceReturnDateField = MyQDateEdit()
        self.invoiceReturnDateField.setEnabled(False)

        # --> invoice with Return checkbox #
        self.invoiceHasReturnCheckBox = MyQCheckBox("com retorno em:", self.invoiceReturnDateField)

        # --> invoice file #
        invoiceFileLabel = MyQLabel("Nota Fiscal: ")
        self.invoiceFilePath = MyQFileLineEdit()
        
        self.invoiceFileButton = QPushButton(" Selecionar Arquivo ")
        self.invoiceFileButton.setCursor(QCursor(Qt.PointingHandCursor))

        # --> progress bar #   
    
        self.progressBar = QProgressBar()
        self.progressBar.setRange(0, 100)
        self.progressBar.setTextVisible(False)

        boldFont = QFont()
        #boltFont.setBold(True)
        
        self.progressLabel = QLabel(" ")
        self.progressLabel.setFont(QFont("Times",weight=QFont.Bold))
        self.progressLabel.setAlignment(Qt.AlignHCenter)

        # --> buttons #
        sendFileButton = MyQPushButton(" Enviar Arquivo ")
        sendFileButton.setCursor(QCursor(Qt.PointingHandCursor))
        
        cancelButton = MyQPushButton(" Cancelar ")
        cancelButton.setCursor(QCursor(Qt.PointingHandCursor))

        # --> checkbox date edit layout #
        checkboxDateFieldLayout = QHBoxLayout()
        checkboxDateFieldLayout.addWidget(self.invoiceHasReturnCheckBox)
        checkboxDateFieldLayout.addWidget(self.invoiceReturnDateField)
        checkboxDateFieldLayout.addStretch(1)

        # --> file field and button layout #

        fileFieldLayout = QHBoxLayout()
        fileFieldLayout.addWidget(self.invoiceFilePath)
        fileFieldLayout.addWidget(self.invoiceFileButton)
        
        # --> buttons Layout #
        buttonsLayout = QHBoxLayout()
        buttonsLayout.addStretch(1)
        buttonsLayout.addWidget(sendFileButton)
        buttonsLayout.addWidget(cancelButton)


        windowLayout = QGridLayout()
        windowLayout.addWidget(invoiceNumberLabel, 0, 0)
        windowLayout.addWidget(self.invoiceNumberField, 0, 1)
        windowLayout.addWidget(invoiceClientLabel, 0, 2)
        windowLayout.addWidget(self.invoiceClientComboBox, 0, 3)
        windowLayout.addWidget(invoiceDocSAPLabel, 1, 0)
        windowLayout.addWidget(self.invoiceDocSAPField, 1, 1)
        windowLayout.addLayout(checkboxDateFieldLayout, 1, 2, 1, 2)
        windowLayout.addWidget(invoiceFileLabel, 2, 0)
        windowLayout.addLayout(fileFieldLayout, 2, 1, 1, 3)
        windowLayout.addWidget(self.progressBar, 3, 0, 1, 4)
        windowLayout.addWidget(self.progressLabel, 4, 0, 1, 4)
        windowLayout.addLayout(buttonsLayout, 5, 0, 1, 4)
 
        self.setLayout(windowLayout)

        self.setWindowIcon(QIcon(":/invoice.png"))
        self.setWindowTitle("Envio de Nota Fiscal")
        
        # --> Line responsible for preventing window resize
        self.layout().setSizeConstraint(QLayout.SetFixedSize)

        #########################
        # --> SIGNAL CONNECTION #
        #########################
        
        self.invoiceFileButton.clicked.connect(self.fileSelection)
        cancelButton.clicked.connect(self.close)
        sendFileButton.clicked.connect(self.sendInvoice)

        # --> thread signals #
        self.uploadThread.updateTextValue.connect(self.updateUploadText)
        self.uploadThread.updateBarValue.connect(self.updateUploadBar)
        self.uploadThread.finished.connect(self.fileTransferFinished)
        self.uploadThread.updateStatusNormal.connect(self.setStatusMessageNormal)
        self.uploadThread.updateStatusWarning.connect(self.setStatusMessageWarning)
        self.uploadThread.updateThreadErrorCode.connect(self.setThreadError)
        
 ###############################################################################################################################################################################
       
    def sendInvoice(self):
        """
        This method verifies if all the requisites were filled before upload
        the invoice file.
        """

        # --> Firstly checks if all the fields were filled up #
        
        missingFields = []
        dataDict = {}
        if self.invoiceNumberField.text():
            dataDict["invoiceNumber"] = int(self.invoiceNumberField.text())
        else:
            missingFields.append("Número da Nota Fiscal")

        if self.invoiceClientComboBox.currentIndex() != 0:
            dataDict["invoiceClientId"] = self.invoiceClientComboBox.itemData(self.invoiceClientComboBox.currentIndex())
            dataDict["invoiceClientName"] = self.invoiceClientComboBox.itemText(self.invoiceClientComboBox.currentIndex())
        else:
            missingFields.append("Cliente")

        if self.invoiceDocSAPField.text():
            dataDict["invoiceDocSap"] = int(self.invoiceDocSAPField.text())
        else:
            missingFields.append("Número Doc. SAP") 

        if self.invoiceFilePath.text():
            dataDict["invoiceFilePath"] = self.invoiceFilePath.text()
        else:
            missingFields.append("Arquivo da Nota Fiscal a ser enviada")

        if self.invoiceHasReturnCheckBox.isChecked():
            dataDict["invoiceHasReturnDate"] = 1
        else:
            dataDict["invoiceHasReturnDate"] = 0

        dataDict["invoiceReturnDate"] = self.invoiceReturnDateField.text()

        if len(missingFields) > 0:
            fields = ",\n\t".join(missingFields)
            
            messageBox = QMessageBox()
            messageBox.setText("Os campos abaixo são de preenchimento obrigatório:\n\t"+fields)
            messageBox.setWindowTitle("Atenção!")
            messageBox.setIcon(QMessageBox.Warning)
            messageBox.setWindowIcon(QIcon(":/warning_icon.png"))
            messageBox.exec_()

            return

        # --> now checks if the file was already uploaded #
        invoiceUploadChecker = invoicescontainer.InvoiceChecker()

        try:
            if invoiceUploadChecker.checkInvoiceUpload(dataDict["invoiceNumber"], dataDict["invoiceClientId"]):
                messageBox = QMessageBox()
                messageBox.setText("Uma Nota Fiscal referente a este Cliente e com este Número já foi enviada.")
                messageBox.setWindowTitle("Atenção!")
                messageBox.setIcon(QMessageBox.Warning)
                messageBox.setWindowIcon(QIcon(":/warning_icon.png"))
                messageBox.exec_()
                return
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

        # --> Confirmation required #
        if self.threadError == 0:
            messageBox = QMessageBox()
            messageBox.setIcon(QMessageBox.Question)
            messageBox.setWindowIcon(QIcon(":/question.png"))
            messageBox.setWindowTitle("Confirmar Envio?")
            messageBox.setText("Deseja confirmar o envio desta nota fiscal?")
            messageBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            messageBox.button(QMessageBox.Yes).setText("Sim")
            messageBox.button(QMessageBox.No).setText("Não")
        
            messageBox.exec_()
        
            # --> If the Yes button was clicked #
            if messageBox.clickedButton() == messageBox.button(QMessageBox.No):
                return
            
        self.threadError = 0

        self.lockFields()
        self.setCursor(QCursor(Qt.WaitCursor))

        self.uploadThread.setDataDict(dataDict)

        self.uploadThread.start()
        
###############################################################################################################################################################################
                
    def setThreadError(self, value):
        """
        Slot created to update the thread finished error
        """
        self.threadError = value

###############################################################################################################################################################################

    def clearFields(self):
        """
        This method is used to clear the form fields
        """
        self.invoiceNumberField.setText("")

        self.invoiceClientComboBox.lineEdit().setText("")
        self.invoiceClientComboBox.setCurrentIndex(-1)
        self.invoiceClientComboBox.myCompleter.setCompletionPrefix("")
        self.invoiceClientComboBox.pFilterModel.setFilterFixedString("")
        
        self.invoiceDocSAPField.setText("")
        self.invoiceHasReturnCheckBox.setChecked(False)
        self.invoiceReturnDateField.setDate(QDate.currentDate())
        self.invoiceReturnDateField.setEnabled(False)
        self.invoiceFilePath.setText("")

###############################################################################################################################################################################

    def lockFields(self):
        """
        This method disables all the buttons and set all the lineedits to readonly
        """
        self.invoiceNumberField.setEnabled(False)
        self.invoiceClientComboBox.lineEdit().setEnabled(False)
        self.invoiceDocSAPField.setEnabled(False)
        self.invoiceHasReturnCheckBox.setEnabled(False)
        self.invoiceReturnDateField.setEnabled(False)
        self.invoiceFilePath.setEnabled(False)

###############################################################################################################################################################################
        

    def unlockFields(self):
        """
        This method unlocks all the field, allowing the user to interact with them
        """
        self.invoiceNumberField.setEnabled(True)
        self.invoiceClientComboBox.lineEdit().setEnabled(True)
        self.invoiceDocSAPField.setEnabled(True)
        self.invoiceHasReturnCheckBox.setEnabled(True)
        self.invoiceReturnDateField.setEnabled(True)
        self.invoiceFilePath.setEnabled(True)
        
###############################################################################################################################################################################
    
    def fileSelection(self):
        """
        This method is called when the button "Selecionar Arquivo" is pressed.
        It is used to open a File Dialog
        """
        path = os.path.join(os.path.join(os.environ['USERPROFILE']), "Desktop")
        filePath, viewType = QFileDialog.getOpenFileName(self, "Selecione a Nota Fiscal", path, "Arquivos PDF(*.pdf)")
        self.invoiceFilePath.setText(filePath)

###############################################################################################################################################################################

    def populateInvoiceComboBox(self):
        """
        This method loads all the active invoices
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

        self.invoiceClientComboBox.setModel(model)
        self.invoiceClientComboBox.setModelColumn(0)

        self.invoiceClientComboBox.setCurrentIndex(0)

###############################################################################################################################################################################
   
    def mousePressEvent(self, e):
        """
        Reimplementation of the mousepressevent.
        This events clear the qcombobox if no client is selected.
        """
        cursor = self.cursor()
        if cursor.shape() == Qt.WaitCursor:
            return
        
        text = self.invoiceClientComboBox.lineEdit().text()
        
        
        if self.invoiceClientComboBox.findText(text) <= 0:
            self.invoiceClientComboBox.myCompleter.setCompletionPrefix("")
            self.invoiceClientComboBox.pFilterModel.setFilterFixedString("")
            self.invoiceClientComboBox.lineEdit().setText("")
            self.invoiceClientComboBox.clearFocus()
            self.invoiceClientComboBox.setCurrentIndex(-1)

###############################################################################################################################################################################

    def updateUploadBar(self, value):
        """
        Slot created to update the uploadBar
        """
        self.progressBar.setValue(value)

###############################################################################################################################################################################

    def setThreadError(self, value):
        """
        Slot created to update the thread finished error
        """
        self.threadError = value
        
###############################################################################################################################################################################

    def updateUploadText(self, text):
        """
        Slot created to update the upload Text
        """
        self.progressLabel.setText(text)

###############################################################################################################################################################################

    def setStatusMessageWarning(self, message):
        self.progressLabel.setStyleSheet("QLabel {color: red; font-weight: bold}")
        self.progressLabel.setText(message)

###############################################################################################################################################################################

    def setStatusMessageNormal(self, message):
        self.progressLabel.setStyleSheet("QLabel {color: black; font-weight: bold}")
        self.progressLabel.setText(message)

###############################################################################################################################################################################

    def fileTransferFinished(self):
        self.unlockFields()
        self.setCursor(QCursor(Qt.ArrowCursor))
        if self.threadError == 0:
            self.setStatusMessageNormal("Arquivo enviado com sucesso!")
            self.parent.updateInvoicesTable()
            messageBox = QMessageBox()
            messageBox.setIcon(QMessageBox.Question)
            messageBox.setWindowIcon(QIcon(":/question.png"))
            messageBox.setWindowTitle("Nota Fiscal cadastrada com sucesso!")
            messageBox.setText("Nota Fiscal cadastrada com sucesso. Deseja cadastrar outra Nota Fiscal?")
            messageBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            messageBox.button(QMessageBox.Yes).setText("Sim")
            messageBox.button(QMessageBox.No).setText("Não")
        
            messageBox.exec_()
        
            # --> If the Yes button was clicked #
            if messageBox.clickedButton() == messageBox.button(QMessageBox.No):
                self.close()
            else:
                self.clearFields()
                self.progressBar.setValue(0)
                self.progressLabel.setText("")

        else:
            # --> Confirmation required #
            messageBox = QMessageBox()
            
            messageBox.setWindowTitle("Erro!")
            messageBox.setIcon(QMessageBox.Critical)
            messageBox.setWindowIcon(QIcon(":/warning_icon.png"))
            
            messageBox.setText("Falha no envio da Nota Fiscal. Tente novamente.\nSe o erro persistir contate o administrador do sistema.")
            
            messageBox.exec_()
        
            self.progressBar.setValue(0)
            self.setStatusMessageWarning("Falha ao enviar o arquivo.")



            
