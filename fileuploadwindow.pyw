import sys
import time
import os
import configparser

from PyQt5.QtCore import (
        Qt,
        QDate,
        QThread,
        pyqtSignal
    )

from PyQt5.QtGui import (
        QIcon,
        QFont,
        QCursor
    )

from PyQt5.QtWidgets import (
        QApplication,
        QMdiSubWindow,
        QDialog,
        QGridLayout,
        QLabel,
        QDateEdit,
        QCalendarWidget,
        QLineEdit,
        QPushButton,
        QFileDialog,
        QLayout,
        QVBoxLayout,
        QHBoxLayout,
        QProgressBar,
        QMessageBox,
        QWidget
    )

import qrc_resources
from magicDB import *
from myExceptions import *

import prodfilescontainer


__version__ = "2.0.0"

###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################

class FileLineEdit(QLineEdit):
    """
    This class was created to replace the mousePressEvent
    """
    def __init__(self):
        super(FileLineEdit, self).__init__()

###############################################################################################################################################################################

    def mousePressEvent(self, event):
        path = os.path.join(os.path.join(os.environ['USERPROFILE']), "Desktop")
        filePath, viewType = QFileDialog.getOpenFileName(self, "Selecione o Plano de Produção", "",
                                                         "Planilha do Excel(*.xlsx)")
        self.setText(filePath)


###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################


class ProdFileUploadThread(QThread):
    """
    Thread responsible for translating the production file into data to be inserted to the database
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
        self.prodFileList = prodfilescontainer.ProdFileOpContainer()

        parser = configparser.SafeConfigParser()
        parser.read("dbconfig.ini")
        self.destinyPath = parser.get("fserver_connection", "path")
        self.destinyPath = self.destinyPath + "/op/"

###############################################################################################################################################################################

    def setPath(self, filePath):
        self.sourcePath = filePath

###############################################################################################################################################################################

    def setDate(self, date):
        self.date = date


###############################################################################################################################################################################
        
    def run(self):
        """
        This method is responsible for translating and inserting the
        production data into the database and creates all the calls related to
        that production
        """

        #########################################################################################################################
        # --> firstly builds up the destination file name. It will be composed by its date, folloing the format "YYYYMMDD.xlsx" #
        #########################################################################################################################
        splitDate =  self.date.split("/")

        destinyName = splitDate[2] + splitDate[1] + splitDate[0] + ".xlsx"        
        destiny = self.destinyPath + destinyName

        # --> Calculates the size of the file that will be transfered #
        statinfo = os.stat(self.sourcePath)
        
        fsize = statinfo.st_size / 1024
        transfered = 0

        self.updateTextValue.emit("%d KBs de %d KBs concluídos" % (transfered, fsize))


        # --> Copy the file to its destination
        with open(self.sourcePath, "rb") as src, open(destiny, "wb") as dst:
            while 1:
                copy_buffer = src.read(1024)
                if not copy_buffer:
                    break
                transfered += len(copy_buffer)/1024
                dst.write(copy_buffer)
                percentage = (transfered / fsize) * 33.0
                self.updateBarValue.emit(percentage)
                self.updateTextValue.emit("%d KBs de %d KBs concluídos" % (transfered, fsize))

        self.updateStatusNormal.emit("Arquivo transferido com sucesso. Iniciando leitura.")
        



        # --> starts the file translator
        self.fileTranslator = prodfilescontainer.ProdFileTranslator(destiny)

    
        if not self.fileTranslator.loadWorksheet():
            self.updateThreadErrorCode.emit(3)
            self.exit(3)


        # --> Read all the data from the production file #
        parsedDataList = self.fileTranslator.parseData()
       
        
        
        self.updateStatusNormal.emit("Leitura efetuada com sucesso. Inserindo dados ao banco.")
        # --> Create the file op container, responsible for managing the data form and to the database #
        self.prodFileList.setDate(self.date)
        try:
            self.prodFileList.populateContainer(parsedDataList)
        except DatabaseConnectionError as error:
            place, cause = error.args

            message = "Falha em: " + place + "\nErro: " +cause
            
            messageBox = QMessageBox()
            messageBox.setText(message)
            messageBox.setWindowTitle("Erro!")
            messageBox.setIcon(QMessageBox.Critical)
            messageBox.setWindowIcon(QIcon(":/warning_icon.png"))
            messageBox.exec_()
            self.exit(5)
            return
        
        for i in range(33, 67):
            self.updateBarValue.emit(i)

    
        ##############################################################################
        # --> From here all the data must be correct to be inserted into the databse #
        ##############################################################################
        try:
            self.prodFileList.flushToDatabase()
        except DatabaseConnectionError as error:
            place, cause = error.args

            message = "Falha em: " + place + "\nErro: " +cause
            
            messageBox = QMessageBox()
            messageBox.setText(message)
            messageBox.setWindowTitle("Erro!")
            messageBox.setIcon(QMessageBox.Critical)
            messageBox.setWindowIcon(QIcon(":/warning_icon.png"))
            messageBox.exec_()
            self.exit(6)
            return
        
        self.updateStatusNormal.emit("Criando chamados automáticos.")

        try:        
            self.prodFileList.createCalls()
        except DatabaseConnectionError as error:
            place, cause = error.args

            message = "Falha em: " + place + "\nErro: " +cause
            
            messageBox = QMessageBox()
            messageBox.setText(message)
            messageBox.setWindowTitle("Erro!")
            messageBox.setIcon(QMessageBox.Critical)
            messageBox.setWindowIcon(QIcon(":/warning_icon.png"))
            messageBox.exec_()
            self.exit(6)
            return
        
        for i in range(67, 101):
            self.updateBarValue.emit(i)
        self.threadFinishedWell.emit()
        

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

        self.setMinimumWidth(98)
        self.setFont(regularFont)
        self.setCursor(QCursor(Qt.PointingHandCursor))

###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################

class MyQDateEdit(QDateEdit):
    """
    This class reimplements the qpushbutton class
    """
    def __init__(self, parent=None):
        super(MyQDateEdit, self).__init__(parent)

        self.setDate(QDate.currentDate().addDays(1))
        self.setFixedWidth(120)
        self.setCalendarPopup(True)
        self.setDisplayFormat("dd/MM/yyyy")
        self.calendarWidget().setHorizontalHeaderFormat(QCalendarWidget.NoHorizontalHeader)
        self.calendarWidget().setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        stylesheet = "QCalendarWidget QWidget#qt_calendar_navigationbar :hover{"\
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

        self.setStyleSheet(stylesheet)
        self.setFocusPolicy(Qt.NoFocus)

###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################
            

class ProductionPlanUploadWindow(QMdiSubWindow):

    # --> Constant id, used for location inside the openedSubWindows dictionary in the main window #
    SUBWINDOWID = "prodplanuploadwindow"
    
    def __init__(self, parent=None):
        super(ProductionPlanUploadWindow, self).__init__(parent)
        self.parent = parent        
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowFlags(Qt.SubWindow | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
        self.setFixedSize(600, 200)
        self.uploadThread = ProdFileUploadThread()
        self.threadSuccess = False
        self.threadError = 0

        # --> Creates the interface for the file upload #
        boldFont = QFont()
        boldFont.setBold(True)

        #########################################
        ####### --> DATE LABEL AND FIELD ########
        #########################################
        dateProductionLabel = QLabel("Data do Plano de Produção: ")
        dateProductionLabel.setFont(boldFont)

        self.dateProductionField = MyQDateEdit()
        
        #####################################
        ###### --> FILE SELECTOR FIELD#######
        #####################################

        productionFileLabel = QLabel("Plano de Produção: ")
        productionFileLabel.setFont(boldFont)

        self.productionFilePath = FileLineEdit()
        self.productionFilePath.setFocusPolicy(Qt.NoFocus)
        
        buttonSelectFile = QPushButton(" Selecionar Arquivo ")
        buttonSelectFile.setCursor(QCursor(Qt.PointingHandCursor))

        fieldsLayout = QGridLayout()
        fieldsLayout.addWidget(dateProductionLabel, 0, 0)
        fieldsLayout.addWidget(self.dateProductionField, 0, 1, 1, 2)
        fieldsLayout.addWidget(productionFileLabel, 1, 0)
        fieldsLayout.addWidget(self.productionFilePath, 1, 1)
        fieldsLayout.addWidget(buttonSelectFile, 1, 2)

        #######################################
        ######### --> PROGRESS BAR ############
        #######################################

        self.progressBar = QProgressBar()
        self.progressBar.setRange(0, 100)
        self.progressBar.setTextVisible(False)

        self.progressLabel = QLabel(" ")
        self.progressLabel.setFont(boldFont)
        self.progressLabel.setAlignment(Qt.AlignHCenter)

        #####################################
        ######### --> BUTTONS BAR ###########
        #####################################
        self.uploadStatusLabel = QLabel(" ")
        self.uploadStatusLabel.setAlignment(Qt.AlignHCenter)

        self.sendFileButton = MyQPushButton(" Enviar Arquivo ")
        self.cancelButton = MyQPushButton(" Cancelar ")
        
        labelLayout = QHBoxLayout()
        labelLayout.addStretch(1)
        labelLayout.addWidget(self.uploadStatusLabel)
        labelLayout.addStretch(1)

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.sendFileButton)
        buttonLayout.addWidget(self.cancelButton)
        buttonLayout.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        
        # --> Construct the fileupload window layout #
        windowLayout = QVBoxLayout()
        windowLayout.addLayout(fieldsLayout)
        windowLayout.addWidget(self.progressBar)
        windowLayout.addWidget(self.progressLabel)
        windowLayout.addWidget(self.uploadStatusLabel)
        windowLayout.addLayout(buttonLayout)
        windowLayout.addStretch(1)
        
        # --> Create a central widget for the QMdiSubWindow #
        centralWidget = QWidget()
        centralWidget.setLayout(windowLayout)
        self.setWidget(centralWidget)
        

        # --> Connecting all the signals #
        buttonSelectFile.clicked.connect(self.fileSelection)
        self.sendFileButton.clicked.connect(self.sendFile)
        self.cancelButton.clicked.connect(self.cancelUpload)
    
        # --> Thread signals #
        self.uploadThread.updateBarValue.connect(self.updateUploadBar)
        self.uploadThread.updateTextValue.connect(self.updateUploadText)
        self.uploadThread.updateStatusWarning.connect(self.setStatusMessageWarning)
        self.uploadThread.updateStatusNormal.connect(self.setStatusMessageNormal)
        self.uploadThread.finished.connect(self.fileTransferFinished)
        self.uploadThread.updateThreadErrorCode.connect(self.setThreadError)
        self.uploadThread.threadFinishedWell.connect(self.threadFinishedWell)


        self.setWindowIcon(QIcon(":/prod_plan_2.png"))
        self.setWindowTitle("Envio de Plano de Produção")
        
        # --> Line responsible for preventing window resize
        #self.layout().setSizeConstraint(QLayout.SetFixedSize)

###############################################################################################################################################################################


    def fileSelection(self):
        """
        This method is called when the button "Selecionar Arquivo" is pressed.
        It is used to open a File Dialog
        """
        filePath, viewType = QFileDialog.getOpenFileName(self, "Selecione o Plano de Produção", "",
                                                         "Planilha do Excel(*.xlsx)")
        self.productionFilePath.setText(filePath)

###############################################################################################################################################################################

    def setStatusMessage(self, message, warningMsg=False):
        """
        This method sets the status message. if the warningMsg is true the message will be
        colored in red
        """
        self.uploadStatusLabel.setText(message)
        
        if warningMsg:
            self.uploadStatusLabel.setStyleSheet("QLabel {color: red; font-weight: bold}")
        else:
            self.uploadStatusLabel.setStyleSheet("QLabel {color: black; font-weight: normal}")

###############################################################################################################################################################################

    def threadFinishedWell(self):
        self.threadSuccess = True

###############################################################################################################################################################################
        
    def setStatusMessageWarning(self, message):
        self.uploadStatusLabel.setStyleSheet("QLabel {color: red; font-weight: bold}")
        self.uploadStatusLabel.setText(message)

###############################################################################################################################################################################

    def setStatusMessageNormal(self, message):
        self.uploadStatusLabel.setStyleSheet("QLabel {color: black; font-weight: bold}")
        self.uploadStatusLabel.setText(message)

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
        
    def fileTransferFinished(self):
        if self.threadSuccess:
            messageBox = QMessageBox()
            messageBox.setText("Envio do Plano de Produção realizado com sucesso.")
            messageBox.setIcon(QMessageBox.Information)
            messageBox.setWindowTitle("Atenção!")
            messageBox.setWindowIcon(QIcon(":/prod_plan_icon.png"))
            messageBox.exec_()
            self.parent.setStatusBarMessage(" ")
            self.close()           
        else:
            self.uploadStatusLabel.setStyleSheet("QLabel {color: red; font-weight: bold}")
            if self.threadError == 1:
                self.uploadStatusLabel.setText("Uma falha ocorreu durante o envio do plano de produção para o servidor.")
            elif self.threadError == 2:
                self.uploadStatusLabel.setText("Envio do Plano de Produção cancelado pelo usuário.")
            elif self.threadError == 3:
                self.uploadStatusLabel.setText("Falha ao tentar interpretar os dados do plano de produção.")
            elif self.threadError == 4:
                self.uploadStatusLabel.setText("Falha ao tentar traduzir o plano de produção.")
            elif self.threadError == 5:
                self.uploadStatusLabel.setText("Falha ao tentar gerar os dados para inserção do plano de produção.")
            else:
                self.uploadStatusLabel.setText("Uma falha ocorreu no envio do plano de produção.")
            self.sendFileButton.setEnabled(True)


###############################################################################################################################################################################

    def sendFile(self):
        """
        This method is called when the button "Enviar Arquivo" is pressed.
        It will send the file to its final destination and retrieve the data needed to insert
        into the database
        """
        prodFileChecker = prodfilescontainer.ProdFileOpChecker()
        
        splitDate =  self.dateProductionField.text().split("/")
        prodDate = splitDate[2] + "-" + splitDate[1] + "-" + splitDate[0]

        if prodFileChecker.checkProductionUpload(prodDate):
            messageBox = QMessageBox()
            messageBox.setText("Arquivo do Plano de Produção referente a esta data já enviado.")
            messageBox.setWindowTitle("Atenção!")
            messageBox.setIcon(QMessageBox.Warning)
            messageBox.setWindowIcon(QIcon(":/warning_icon.png"))
            messageBox.exec_()
            return 
              
        if self.productionFilePath.text():
            self.sendFileButton.setEnabled(False)
            self.uploadThread.setPath(self.productionFilePath.text())
            self.uploadThread.setDate(self.dateProductionField.text())
            self.uploadThread.start()
        else:
            messageBox = QMessageBox()
            messageBox.setText("Selecione o Plano de Produção!")
            messageBox.setWindowTitle("Atenção!")
            messageBox.setIcon(QMessageBox.Information)
            messageBox.setWindowIcon(QIcon(":/information.png"))
            messageBox.exec_()

        
###############################################################################################################################################################################
               
    def cancelUpload(self):
        """
        This method is used to cancel the file upload. If the upload thread is running it will be canceled,
        else it will close the subwindow
        """
        if self.uploadThread.isRunning():
            messageBox = QMessageBox()
            messageBox.setIcon(QMessageBox.Question)
            messageBox.setWindowIcon(QIcon(":/question.png"))
            messageBox.setWindowTitle("Cancelar Upload?")
            messageBox.setText("Deseja cancelar o envio do Plano de Produção?")
            messageBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            messageBox.button(QMessageBox.Yes).setText("Sim")
            messageBox.button(QMessageBox.No).setText("Não")
            
            messageBox.exec_()
            
            # --> If the Yes button was clicked
            if messageBox.clickedButton() == messageBox.button(QMessageBox.Yes):
                self.threadError = 2
                self.uploadThread.exit(2)
        else:
            self.close()

###############################################################################################################################################################################


    def closeEvent(self, event):
        """
        This method remove its reference from its parent opened sub window list before being closed
        """
        del self.parent.openedSubWindows[self.SUBWINDOWID]
        self.close()

      
