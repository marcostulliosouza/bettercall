from PyQt5.QtCore import (
    Qt,
    QTimer,
    QSize,
    QEvent
    )

from PyQt5.QtGui import (
    QFont,
    QIcon,
    QColor,
    QCursor,
    QTextCharFormat
    )

from PyQt5.QtWidgets import (
    QDialog,
    QLabel,
    QLCDNumber,
    QPushButton,
    QGroupBox,
    QLayout,
    QHBoxLayout,
    QPlainTextEdit,
    QGridLayout,
    QVBoxLayout,
    QMessageBox,
    QSplitter,
    QWidget,
    QScrollArea,
    QFrame,
    QButtonGroup,
    QRadioButton
    )

import qrc_resources
from magicDB import *
from myExceptions import *

import maintenanceformscontainer
import maintenancelogscontainer


__version__ = "2.0.0"

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

class MyQLabel(QLabel):
    """
    This class reimplements the qlabel class
    """
    def __init__(self, text="", parent=None):
        super(MyQLabel, self).__init__(text, parent)
        boldFont = QFont()
        boldFont.setBold(True)

        self.setFixedWidth(120)
        self.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.setFont(boldFont)

###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################

class MyQDeviceInfoLabel(QLabel):
    """
    This class reimplements the qlabel class
    """
    def __init__(self, text="", parent=None):
        super(MyQDeviceInfoLabel, self).__init__(text, parent)
        regularFont = QFont()
        regularFont.setBold(False)

        self.setFixedWidth(200)
        self.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.setWordWrap(True)
        self.setFont(regularFont)

###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################

class MyQFrame(QFrame):
    """
    This class reimplements qframe class
    """
    def __init__(self, itemId=None, itemPosition=None, parent=None):
        super(MyQFrame, self).__init__(parent)
        self.itemId = itemId
        self.itemPosition = itemPosition
        
        self.setFrameStyle(QFrame.Panel | QFrame.Raised)
    


###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################

class MyQButtonGroup(QButtonGroup):
    """
    This class reimplements the QButtonGroup class
    """
    def __init__(self, itemId=None, parent=None):
        super(MyQButtonGroup, self).__init__(parent)
        self.itemId = itemId
        self.parent = parent
        
        self.setExclusive(True)

        self.buttonClicked.connect(self.verifyEndMaintenanceButton)

    def verifyEndMaintenanceButton(self, button):
        self.parent.formItemsAnswered[self.itemId] = self.checkedId()

        if len(self.parent.formItemsAnswered) == len(self.parent.maintenanceForm):
            self.parent.finishMaintenanceButton.setEnabled(True)
    
###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################

class MyQPlainTextEdit(QPlainTextEdit):
    """
    This class reimplements the QPlainTextEdit class
    """
    def __init__(self, parent=None):
        super(MyQPlainTextEdit, self).__init__(parent)
        self.textFormat = QTextCharFormat()
        self.textFormat.setFontCapitalization(QFont.AllUppercase)

        regularFont = QFont()
        regularFont.setBold(False)

        self.setCurrentCharFormat(self.textFormat)
        self.setFixedSize(QSize(300, 80))
        self.setFont(regularFont)

        self.textChanged.connect(self.calculateCharacters)

    def calculateCharacters(self):
        self.setCurrentCharFormat(self.textFormat)
        
        textLength = len(self.toPlainText())
        if textLength > 255:
            text = self.toPlainText()
            self.setPlainText(text[:255])
            cursor = self.textCursor()
            cursor.setPosition(255)
            self.setTextCursor(cursor)


###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################


class DeviceMaintenanceWindow(QDialog):
    """
    This class is responsible for rendering the maintenance window modally.
    It doesn't allow to open another window for the user if the user didn't finish the last maintenance
    """
    
    def __init__(self, device=None, maintenanceLogId=None, parent=None):
        super(DeviceMaintenanceWindow, self).__init__(parent)
        self.device = device
        self.device.loadAllDetailedData()
        
        self.parent = parent
        self.loggedUser = parent.loggedUser

        self.formItemsAnswered = {}
        self.maintenanceLog = maintenancelogscontainer.MaintenanceLog(maintenanceLogId)
        self.loadMaintenanceLogData()

        self.maintenanceForm = maintenanceformscontainer.MaintenanceFormItemsContainer(self.device.deviceMaintenanceFormId)
        self.maintenanceForm.loadItemsFromMaintenanceForm()
        
        
        self.loggedUser = parent.loggedUser
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setMinimumWidth(1200)
        
        
        
        self.updateInterfaceTimer = QTimer()

        boldFont = QFont()
        boldFont.setBold(True)

        regularFont = QFont()
        regularFont.setBold(False)


        # --> Duration #
        self.lcdDisplay = QLCDNumber(self)
        self.lcdDisplay.setSegmentStyle(QLCDNumber.Filled)
        self.lcdDisplay.setFixedSize(350, 100)
        
        self.updateClock()

        # --> Device Info #

        deviceDescriptionLabel = MyQLabel("Descrição: ")
        deviceDescriptionDataLabel = MyQDeviceInfoLabel(self.device.deviceDescription)
        

        deviceOwnerLabel = MyQLabel("Proprietário: ")
        deviceOwnerDataLabel = MyQDeviceInfoLabel(self.device.deviceClientName)

        deviceLifeCicleLable = MyQLabel("Vida Útil: ")
        deviceLifeCicleDataLabel = MyQDeviceInfoLabel(str(self.device.deviceLifeCicle))

        deviceCyclesLabel = MyQLabel("Ciclos Totais Executados: ")
        deviceCyclesDataLabel = MyQDeviceInfoLabel(str(self.device.deviceRunnedCicles))
       
        deviceInfoGBLayout = QGridLayout()
        deviceInfoGBLayout.addWidget(deviceDescriptionLabel, 0, 0)
        deviceInfoGBLayout.addWidget(deviceDescriptionDataLabel, 0, 1)
        deviceInfoGBLayout.addWidget(deviceOwnerLabel, 1, 0)
        deviceInfoGBLayout.addWidget(deviceOwnerDataLabel, 1, 1)
        deviceInfoGBLayout.addWidget(deviceLifeCicleLable, 2, 0)
        deviceInfoGBLayout.addWidget(deviceLifeCicleDataLabel, 2, 1)
        deviceInfoGBLayout.addWidget(deviceCyclesLabel, 3, 0)
        deviceInfoGBLayout.addWidget(deviceCyclesDataLabel, 3, 1)
        
        
        deviceInfoGroupBox = QGroupBox("Informações sobre o dispositivo:")
        deviceInfoGroupBox.setFont(boldFont)
        deviceInfoGroupBox.setLayout(deviceInfoGBLayout)

        # --> Maintenance Observation #
        self.textFormat = QTextCharFormat()
        self.textFormat.setFontCapitalization(QFont.AllUppercase)
                                              
        maintenanceObservationLabel = MyQLabel("Observação sobre a manutenção: ")
        maintenanceObservationLabel.setFixedWidth(300)
        
        self.maintenanceObservationField = QPlainTextEdit()
        self.maintenanceObservationField.setFixedSize(QSize(350, 143))
        self.maintenanceObservationField.setEnabled(False)
        self.maintenanceObservationField.setCurrentCharFormat(self.textFormat)

        

        # --> Left Side Window Layout #
        leftSideWindowLayout = QVBoxLayout()
        leftSideWindowLayout.addSpacing(6)
        leftSideWindowLayout.addWidget(self.lcdDisplay)
        leftSideWindowLayout.addWidget(deviceInfoGroupBox)
        leftSideWindowLayout.addWidget(maintenanceObservationLabel)
        leftSideWindowLayout.addWidget(self.maintenanceObservationField)
        leftSideWindowLayout.addStretch(1)


        # --> Maintenance Form Groupbox #
        self.maintenanceFormGroupBox = QGroupBox("Formulário de Manutenção:")
        self.maintenanceFormGroupBox.setFont(boldFont)
        self.maintenanceFormGroupBox.setMinimumHeight(400)
        self.maintenanceFormGroupBox.setEnabled(False)


        #--> Widget that holds a QVboxLayout to put scrollbars
        self.formItemsList = QWidget()
        
        self.formItemsListLayout = QVBoxLayout()
        self.formItemsList.setLayout(self.formItemsListLayout)

        #--> ScrollArea
        self.scrollArea = QScrollArea()
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidget(self.formItemsList)

        formItemsGBLayout = QHBoxLayout()
        formItemsGBLayout.addWidget(self.scrollArea)

        self.maintenanceFormGroupBox.setLayout(formItemsGBLayout)
        
        
        # --> Right Side Window Layout #
        rightSideWindowLayout = QVBoxLayout()
        rightSideWindowLayout.addWidget(self.maintenanceFormGroupBox)

        # --> Layout for the LCD Display, device info and maintenance form #
        infoAndDataLayout = QHBoxLayout()
        infoAndDataLayout.addLayout(leftSideWindowLayout)
        infoAndDataLayout.addLayout(rightSideWindowLayout)

        # --> Buttons #

        self.beginMaintenanceButton = MyQPushButton(" Iniciar ")
        self.cancelButton = MyQPushButton(" Cancelar ")
        self.finishMaintenanceButton = MyQPushButton(" Finalizar ")
        self.finishMaintenanceButton.setEnabled(False)

        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch(1)
        buttonLayout.addWidget(self.beginMaintenanceButton)
        buttonLayout.addWidget(self.finishMaintenanceButton)
        buttonLayout.addWidget(self.cancelButton)
        buttonLayout.addStretch(1)


        windowLayout = QVBoxLayout()
        windowLayout.addLayout(infoAndDataLayout)
        windowLayout.addLayout(buttonLayout)

        self.setLayout(windowLayout)
        self.setWindowIcon(QIcon(":/maintenance.png"))
        self.setWindowTitle("Manutenção Preventiva - Dispositivo {:06d}".format(self.device.deviceId))

        self.listMaintenanceFormItems()

        # --> Start interface update timer #
        self.updateInterfaceTimer.timeout.connect(self.updateMaintenanceWindowUI)
        self.updateInterfaceTimer.start(55000)
        self.updateMaintenanceWindowUI()
        self.installEventFilter(self)

        ###########################
        #### SIGNALS AND SLOTS ####
        ###########################

        self.cancelButton.clicked.connect(self.close)
        self.beginMaintenanceButton.clicked.connect(self.beginMaintenance)
        self.finishMaintenanceButton.clicked.connect(self.endMaintenance)


###############################################################################################################################################################################
    def endMaintenance(self):
        """
        This method is used to finish the maintenance. 
        """

        messageBox = QMessageBox()
        messageBox.setIcon(QMessageBox.Question)
        messageBox.setWindowIcon(QIcon(":/question.png"))
        messageBox.setWindowTitle("Finalizar Manutenção?")
        messageBox.setText("Deseja finalizar esta manutenção preventiva?")
        messageBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        
        messageBox.button(QMessageBox.Yes).setText("Sim")
        messageBox.button(QMessageBox.Yes).setCursor(QCursor(Qt.PointingHandCursor))
        
        messageBox.button(QMessageBox.No).setText("Não")
        messageBox.button(QMessageBox.No).setCursor(QCursor(Qt.PointingHandCursor))
        
        messageBox.exec_()
        
        # --> If the Yes button was clicked #
        if messageBox.clickedButton() == messageBox.button(QMessageBox.No):
            return

        
        itemAnswerList = []
        maintenanceInformation = {}
        
        for i in range(0, self.formItemsListLayout.count()):
            itemFrame = self.formItemsListLayout.itemAt(i).widget()
            itemId = itemFrame.itemId
            itemAnswerSituation = itemFrame.layout().itemAt(1).widget().group().checkedId()
            itemAnswerObservation = itemFrame.layout().itemAt(3).widget().toPlainText()
            itemAnswerList.append((itemId, self.maintenanceLog.maintenanceLogId, itemAnswerSituation, itemAnswerObservation))


        
        maintenanceInformation["observation"] = self.maintenanceObservationField.toPlainText()
        maintenanceInformation["deviceInfoMaintenance"] = self.device.deviceInfoMaintenance


        try:
            self.maintenanceLog.endMaintenance(maintenanceInformation, itemAnswerList)
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

        messageBox = QMessageBox()
        messageBox.setText("Manutenção finalizada com sucesso!")
        messageBox.setWindowTitle("Sucesso!")
        messageBox.setIcon(QMessageBox.Information)
        messageBox.setWindowIcon(QIcon(":/maintenance.png"))
        messageBox.exec_()

        self.parent.updateMaintenancesTable()
        self.maintenanceLog.maintenanceLogStatusId = 2 
                
        self.close()


###############################################################################################################################################################################

    def updateMaintenanceWindowUI(self):
        self.updateClock()
        if not self.maintenanceLog.maintenanceLogId:
            self.beginMaintenanceButton.setEnabled(True)
            self.cancelButton.setEnabled(True)
            self.finishMaintenanceButton.setVisible(False)
        else:
            self.maintenanceFormGroupBox.setEnabled(True)
            self.beginMaintenanceButton.setVisible(False)
            self.cancelButton.setVisible(False)
            self.finishMaintenanceButton.setVisible(True)
            self.maintenanceObservationField.setEnabled(True)
            

###############################################################################################################################################################################
    def eventFilter(self, source, event):
        if event.type() == QEvent.KeyPress:
            if source is self and event.key() == Qt.Key_Escape:
                return True
        return super(DeviceMaintenanceWindow, self).eventFilter(source, event)
                



###############################################################################################################################################################################

    def loadMaintenanceLogData(self):
        """
        This method updates the maintenance log object
        """
        self.maintenanceLog.maintenanceLogDevice = self.device.deviceId
        self.maintenanceLog.maintenanceLogType = self.device.deviceMaintenanceIntervalType
        self.maintenanceLog.maintenanceLogLastMaintenance = self.device.deviceLastMaintenance if (self.device.deviceLastMaintenance != "NUNCA") else self.device.deviceRegisterDate
        self.maintenanceLog.maintenanceLogIntervalType = self.device.deviceMaintenanceIntervalType
        
        self.maintenanceLog.maintenanceLogDaysInterval = self.device.deviceMaintenanceDaysInterval
        
        self.maintenanceLog.maintenanceLogBoardsInterval = self.device.deviceMaintenanceBoardsInterval
        
        self.maintenanceLog.maintenanceLogBoardsRunned = self.device.deviceBoardsRunned
        self.maintenanceLog.maintenanceLogTotalBoardsRunned = self.device.deviceRunnedCicles
                                              
        self.maintenanceLog.maintenanceLogUser = self.loggedUser["id"]
                                              
        self.maintenanceLog.maintenanceLogStatusId = 1
    
###############################################################################################################################################################################

    def updateClock(self):
        if not self.maintenanceLog.maintenanceLogId:
            lcdPalette = self.lcdDisplay.palette()
            lcdPalette.setColor(lcdPalette.WindowText, QColor(0, 0, 0))
            self.lcdDisplay.setPalette(lcdPalette)
            self.lcdDisplay.setDigitCount(5)
            self.lcdDisplay.display("00:00")
        else:
            try:
                duration = self.maintenanceLog.maintenanceDuration()
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

            lcdPalette = self.lcdDisplay.palette()
            lcdPalette.setColor(lcdPalette.WindowText, QColor(0, 0, 0))
            self.lcdDisplay.setPalette(lcdPalette)
            self.lcdDisplay.setDigitCount(5)
            self.lcdDisplay.display("%02d:%02d" % ((int(duration)//60), (int(duration)%60)))
        

###############################################################################################################################################################################
    def beginMaintenance(self):
        messageBox = QMessageBox()
        messageBox.setIcon(QMessageBox.Question)
        messageBox.setWindowIcon(QIcon(":/question.png"))
        messageBox.setWindowTitle("Iniciar Manutenção?")
        messageBox.setText("Deseja iniciar a manutenção preventiva deste dispositivo?")
        messageBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        
        messageBox.button(QMessageBox.Yes).setText("Sim")
        messageBox.button(QMessageBox.Yes).setCursor(QCursor(Qt.PointingHandCursor))
        
        messageBox.button(QMessageBox.No).setText("Não")
        messageBox.button(QMessageBox.No).setCursor(QCursor(Qt.PointingHandCursor))
        
        messageBox.exec_()
        
        # --> If the Yes button was clicked #
        if messageBox.clickedButton() == messageBox.button(QMessageBox.No):
            return

        try:
            self.maintenanceLog.startMaintenance()
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

        self.updateMaintenanceWindowUI()

        

###############################################################################################################################################################################

    
    def listMaintenanceFormItems(self):
        # --> Form Items #
        formItemFont = QFont()
        formItemFont.setBold(False)

        for formItem in self.maintenanceForm:
            formItemFrame = MyQFrame(formItem.itemId, formItem.itemPosition)
            
            # --> Item Description #
            itemDescription = QLabel(formItem.itemDescription)
            itemDescription.setFixedSize(QSize(338, 85))
            itemDescription.setWordWrap(True)
            itemDescription.setFont(formItemFont)
            itemDescription.setStyleSheet("border: 1px solid gray; padding: 0 5 0 5")

            # --> Item Answer #
            itemRadioButtonGroup = MyQButtonGroup(formItem.itemId, self)
            
            itemOK = QRadioButton("OK ")
            itemNOK = QRadioButton("NOK")

            itemRadioButtonGroup.addButton(itemOK)
            itemRadioButtonGroup.setId(itemOK, 1)
            
            itemRadioButtonGroup.addButton(itemNOK)
            itemRadioButtonGroup.setId(itemNOK, 0)

            # --> Observation #
            itemObservation = MyQPlainTextEdit()

            # --> Item Layout #        
            formItemLayout = QHBoxLayout()
            formItemLayout.addWidget(itemDescription)
            formItemLayout.addWidget(itemOK)
            formItemLayout.addWidget(itemNOK)
            formItemLayout.addWidget(itemObservation)

            formItemFrame.setLayout(formItemLayout)

            self.formItemsListLayout.insertWidget(formItem.itemPosition, formItemFrame)
            self.scrollArea.widget().resize(self.scrollArea.widget().sizeHint())

            

    def closeEvent(self, event):
        if self.maintenanceLog.maintenanceLogId and self.maintenanceLog.maintenanceLogStatusId == 1:
            event.ignore()
        


            
