from shutil import copyfile
import os
import tempfile
from ftplib import FTP

from configparser import SafeConfigParser

from PyQt5.QtCore import (
        Qt
    )

from PyQt5.QtGui import (
        QFont,
        QIcon,
        QPixmap,
        QImage,
        QTextCharFormat,
        QIntValidator
    )

from PyQt5.QtWidgets import (
        QDialog,
        QLineEdit,
        QGroupBox,
        QPushButton,
        QLabel,
        QPlainTextEdit,
        QLayout,
        QHBoxLayout,
        QVBoxLayout,
        QGridLayout,
        QScrollArea,
        QMessageBox,
        QComboBox,
        QFileDialog,
        QTableWidget,
        QTableWidgetItem,
        QHeaderView,
        QAbstractScrollArea
    )

import qrc_resources
from magicDB import *
from devicescontainer import DeviceStatusContainer
import maintenanceformscontainer
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

        self.setMinimumWidth(100)
        self.setFixedHeight(20)

###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################

class MyQAnswerLabel(QLabel):
    """
    This class reimplements the qlabel class
    """
    def __init__(self, text="", parent=None):
        super(MyQAnswerLabel, self).__init__(text, parent)
        # --> define a bold Font #        
        boldFont = QFont()
        boldFont.setBold(False)
        self.setFont(boldFont)

        self.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.setMinimumWidth(80)

###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################

class MyQButton(QPushButton):
    """
    This class reimplements the QPushButton class
    """
    def __init__(self, text="", parent=None):
        super(MyQButton, self).__init__(text, parent)
        # --> define a bold Font #        
        boldFont = QFont()
        boldFont.setBold(False)
        self.setFont(boldFont)
        self.setFixedWidth(98)
        self.setCursor(Qt.PointingHandCursor)
       

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
        self.setMaximumHeight(100)
        self.setEditTriggers(QTableWidget.NoEditTriggers)
        self.setSelectionMode(QTableWidget.NoSelection)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setHighlightSections(False)

        
        # --> create theitems for the headers #
        self.setColumnCount(2)
       

        self.horizontalHeader().resizeSection(0, 300)
        
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.horizontalHeader().hide()



###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################


class DetailedDeviceWindow(QDialog):
    """
    This class is responsible for rendering the device window modally.
    This window will hold the edit function and the data show function.
    """
    
    def __init__(self, device=None, parent=None):
        super(DetailedDeviceWindow, self).__init__(parent)
        self.device = device
        self.loggedUser = parent.loggedUser
        self.parent = parent
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.editMode = 0

        self.device.loadAllDetailedData()

        #########################################
        #### --> WINDOW LAYOUT BUILDING CODE ####
        #########################################
        boldFont = QFont()
        boldFont.setBold(True)

        regularFont = QFont()
        regularFont.setBold(False)

        capitalFont = QFont()
        capitalFont.setBold(False)
        capitalFont.setCapitalization(QFont.AllUppercase)

        self.textFormat = QTextCharFormat()
        self.textFormat.setFontCapitalization(QFont.AllUppercase)

        # --> Validator that allows only integers #
        self.intValidator = QIntValidator()
        
        ##################################
        #### --> INFORMATION GROUPBOX ####
        ##################################

        #--> LABELS #
        deviceDescriptionLabel = MyQLabel("Descrição: ")
        deviceSAPCodeLabel = MyQLabel("Código SAP: ")
        deviceOwnerLabel = MyQLabel("Proprietário: ")
        deviceInvoiceLabel = MyQLabel("Nota Fiscal: ")
        deviceStatusLabel = MyQLabel("Status: ")
        deviceLifeCicleLabel = MyQLabel("Ciclo de Vida: ")
        deviceStoragePositionLabel = MyQLabel("Posição no Estoque: ")
        deviceCiclesDoneLabel = MyQLabel("Ciclos Executados: ")
        
        deviceObservationLabel = MyQLabel("Observações: ")
        deviceObservationLabel.setMinimumWidth(10)
        
        self.obsCharCounter = MyQLabel(str(1000 - len(self.device.deviceObservation)))
        self.obsCharCounter.setStyleSheet('color: red')
        self.obsCharCounter.setVisible(False)

        #--> DATA LABELS #
        self.deviceDescriptionDataLabel = MyQAnswerLabel(self.device.deviceDescription)
        self.deviceDescriptionDataLabel.setMinimumWidth(202)


        #--> SAP CODE #
        
        self.deviceSAPCodeDataLabel = MyQAnswerLabel(str(self.device.deviceSAPCode))

        self.deviceSAPCodeDataField = QLineEdit()
        self.deviceSAPCodeDataField.setFixedWidth(60)
        self.deviceSAPCodeDataField.setFont(capitalFont)

        #--> CLIENT #
        if self.device.deviceClientId > 0:
            self.deviceOwnerDataLabel = MyQAnswerLabel(self.device.deviceClientName)
            self.deviceInvoiceDataLabel = MyQAnswerLabel(str(self.device.deviceInvoiceNumber))
        else:
            self.deviceOwnerDataLabel = MyQAnswerLabel("HI-MIX")
            self.deviceInvoiceDataLabel = MyQAnswerLabel("")

        #--> STATUS #
        self.deviceStatusDataLabel = MyQAnswerLabel(self.device.deviceStatusDescription)
        
        self.deviceStatusComboBox = QComboBox()
        self.deviceStatusComboBox.setFixedWidth(100)
        self.deviceStatusComboBox.setFont(regularFont)

        self.populateDeviceStatusComboBox()
        
        #--> LIFE CICLE #
        self.deviceLifeCicleDataLabel = MyQAnswerLabel(str(self.device.deviceLifeCicle)) if self.device.deviceLifeCicle else MyQAnswerLabel("N/D")

        self.deviceLifeCicleDataField = QLineEdit()
        self.deviceLifeCicleDataField.setFixedWidth(60)
        self.deviceLifeCicleDataField.setFont(regularFont)
        self.deviceLifeCicleDataField.setValidator(self.intValidator)
        
        #--> STORAGE POSITION #
        self.deviceStoragePositionDataLabel = MyQAnswerLabel(self.device.deviceStoragePosition) if self.device.deviceStoragePosition else MyQAnswerLabel("N/D")

        self.deviceStoragePositionDataField = QLineEdit()
        self.deviceStoragePositionDataField.setFixedWidth(60)
        self.deviceStoragePositionDataField.setFont(capitalFont)
        self.deviceStoragePositionDataField.setMaxLength(5)

        self.deviceDoneCiclesDataLabel = MyQAnswerLabel(str(self.device.deviceRunnedCicles))
        

        #--> OBSERVATION #
        self.deviceObservationsDataLabel = MyQAnswerLabel(self.device.deviceObservation)
        self.deviceObservationsDataLabel.setStyleSheet("padding: 5 5 5 2")

        self.deviceObservationsDataField = QPlainTextEdit()
        self.deviceObservationsDataField.setCurrentCharFormat(self.textFormat)
        self.deviceObservationsDataField.setFont(regularFont)
        self.deviceObservationsDataField.setFixedWidth(518)
        self.deviceObservationsDataField.setFixedHeight(118)
        
        self.observationScrollArea = QScrollArea()
        self.observationScrollArea.setWidget(self.deviceObservationsDataLabel)
        self.observationScrollArea.ensureVisible(0, 0, 0, 0)
        self.observationScrollArea.setFixedHeight(120)

        #--> OBSERVATION CHARCOUNTER LAYOUT #
        observationLayout = QHBoxLayout()
        observationLayout.addWidget(deviceObservationLabel)
        observationLayout.addStretch(1)
        observationLayout.addWidget(self.obsCharCounter)
        

        #--> LAYOUT INFORMATION GROUPBOX #
        self.informationGBLayout = QGridLayout()
        self.informationGBLayout.addWidget(deviceDescriptionLabel, 0, 0)
        self.informationGBLayout.addWidget(self.deviceDescriptionDataLabel, 0, 1)
        self.informationGBLayout.addWidget(deviceSAPCodeLabel, 0, 2)
        self.informationGBLayout.addWidget(self.deviceSAPCodeDataLabel, 0, 3)

        self.informationGBLayout.addWidget(deviceOwnerLabel, 1, 0)
        self.informationGBLayout.addWidget(self.deviceOwnerDataLabel, 1, 1)
        if self.device.deviceClientId > 0:
            self.informationGBLayout.addWidget(deviceInvoiceLabel, 1, 2)
            self.informationGBLayout.addWidget(self.deviceInvoiceDataLabel, 1, 3)

        self.informationGBLayout.addWidget(deviceStatusLabel, 2, 0)
        self.informationGBLayout.addWidget(self.deviceStatusDataLabel, 2, 1)
        self.informationGBLayout.addWidget(deviceLifeCicleLabel, 2, 2)
        self.informationGBLayout.addWidget(self.deviceLifeCicleDataLabel, 2, 3)

        self.informationGBLayout.addWidget(deviceStoragePositionLabel, 3, 0)
        self.informationGBLayout.addWidget(self.deviceStoragePositionDataLabel, 3, 1)
        self.informationGBLayout.addWidget(deviceCiclesDoneLabel, 3, 2)
        self.informationGBLayout.addWidget(self.deviceDoneCiclesDataLabel, 3, 3)

        self.informationGBLayout.addLayout(observationLayout, 4, 0, 1, 4)
        self.informationGBLayout.addWidget(self.observationScrollArea, 5, 0, 1, 4)
      
        informationGroupBox = QGroupBox("Informações:")
        informationGroupBox.setFont(boldFont)
        informationGroupBox.setLayout(self.informationGBLayout)

        ##################################
        #### --> MAINTENANCE GROUPBOX ####
        ##################################

        #--> LABELS #
        deviceMaintenanceIntervalTypeLabel = MyQLabel("Tipo de Intervalo: ")
        deviceIntervalBetweenMaintenances = MyQLabel("Intervalo entre Manutenções: ")
        deviceMaintenanceForm = MyQLabel("Formulário de Manutenção: ")

        # --> DATA LABELS #
        if self.device.deviceInfoMaintenance:
            self.deviceMaintenanceIntervalTypeDataLabel = MyQAnswerLabel("DIAS CORRIDOS") if self.device.deviceMaintenanceIntervalType == "DIA" else MyQAnswerLabel("PLACAS TESTADAS")

            self.deviceBetweenMaintenanceIntervalDataLabel = MyQAnswerLabel(str(self.device.deviceMaintenanceDaysInterval)) if self.device.deviceMaintenanceIntervalType == "DIA" else MyQAnswerLabel(str(self.device.deviceMaintenanceBoardsInterval))       
            self.deviceBetweenMaintenanceIntervalDataLabel.setFixedWidth(60)
            self.deviceBetweenMaintenanceIntervalDataLabel.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        
            self.deviceSulfixInterval = MyQLabel(" DIAS CORRIDOS") if self.device.deviceMaintenanceIntervalType == "DIA" else MyQLabel(" PLACAS TESTADAS") 
            self.deviceSulfixInterval.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

            self.deviceMaintenanceFormDataLabel = MyQAnswerLabel(" ")

        else:
            self.deviceMaintenanceIntervalTypeDataLabel = MyQAnswerLabel("")

            self.deviceBetweenMaintenanceIntervalDataLabel = MyQAnswerLabel("")       
            self.deviceBetweenMaintenanceIntervalDataLabel.setFixedWidth(60)
            self.deviceBetweenMaintenanceIntervalDataLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
            self.deviceSulfixInterval = MyQLabel("") 
            self.deviceSulfixInterval.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.deviceMaintenanceFormDataLabel = MyQAnswerLabel(self.device.deviceMaintenanceFormDescription)

        self.maintenanceIntervalTypeComboBox = QComboBox()
        self.maintenanceIntervalTypeComboBox.setFont(regularFont)
        self.maintenanceIntervalTypeComboBox.setFixedWidth(150)
        self.maintenanceIntervalTypeComboBox.addItem("", "")
        self.maintenanceIntervalTypeComboBox.addItem("PLACAS TESTADAS", "PLACA")
        self.maintenanceIntervalTypeComboBox.addItem("DIAS CORRIDOS", "DIA")

        self.deviceBetweenMaintenanceIntervalDataField = QLineEdit()
        self.deviceBetweenMaintenanceIntervalDataField.setFixedWidth(60)
        self.deviceBetweenMaintenanceIntervalDataField.setFont(regularFont)
        self.deviceBetweenMaintenanceIntervalDataField.setValidator(self.intValidator)

        self.deviceMaintenanceFormsComboBox = QComboBox()
        self.deviceMaintenanceFormsComboBox.setFont(regularFont)
        self.deviceMaintenanceFormsComboBox.setFixedWidth(250)

        self.populateMaintenanceFormsComboBox()

        #--> LAYOUT BUILD MAINTENANCE GROUPBOX #
        self.maintenanceGBLayout = QGridLayout()
        self.maintenanceGBLayout.addWidget(deviceMaintenanceIntervalTypeLabel, 0, 0)
        self.maintenanceGBLayout.addWidget(self.deviceMaintenanceIntervalTypeDataLabel, 0, 1, 1, 2)
        self.maintenanceGBLayout.addWidget(deviceIntervalBetweenMaintenances, 1, 0)
        self.maintenanceGBLayout.addWidget(self.deviceBetweenMaintenanceIntervalDataLabel, 1, 1)
        self.maintenanceGBLayout.addWidget(self.deviceSulfixInterval, 1, 2)
        self.maintenanceGBLayout.addWidget(deviceMaintenanceForm, 2, 0)
        self.maintenanceGBLayout.addWidget(self.deviceMaintenanceFormDataLabel, 2, 1, 1, 2)
        
        self.maintenanceGroupBox = QGroupBox("Com Manutenção Preventiva:")
        self.maintenanceGroupBox.setCheckable(True)
        if self.device.deviceHasMaintenance:
            self.maintenanceGroupBox.setChecked(True)
        else:
            self.maintenanceGroupBox.setChecked(False)
            
        self.maintenanceGroupBox.setFont(boldFont)
        self.maintenanceGroupBox.setLayout(self.maintenanceGBLayout)

        ##########################################
        #### --> VINCULATED PRODUCTS GROUPBOX ####
        ##########################################

        vinculatedProductsGroupBox = QGroupBox("Produtos Vinculados:")
        vinculatedProductsGroupBox.setFont(boldFont)       
        
        self.device.loadVinculatedProducts()
        if len(self.device.vinculatedProductsList):
            self.vinculatedProductsTable = MyQTableWidget()
            self.populateVinculatedProductsTable()

            vinculatedProductsGBLayout = QHBoxLayout()
            vinculatedProductsGBLayout.addWidget(self.vinculatedProductsTable)
            
        else:
            noVinculatedProductsLabel = QLabel("Não há produtos vinculados a este dispositivo.")
            noVinculatedProductsLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            noVinculatedProductsLabel.setStyleSheet('color: red')
            noVinculatedProductsLabel.setFixedHeight(23)
            
            vinculatedProductsGBLayout = QHBoxLayout()
            vinculatedProductsGBLayout.addWidget(noVinculatedProductsLabel)
            

        vinculatedProductsGroupBox.setLayout(vinculatedProductsGBLayout)

        ############################
        #### --> FILES GROUPBOX ####
        ############################

        #--> IMAGE #
        
        imageGroupBox = QGroupBox("Imagem")
        imageGroupBox.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        
        self.sendImageButton = MyQButton(" Enviar ")
        self.seeImageButton = MyQButton(" Visualizar ")
        self.changeImageButton = MyQButton(" Alterar ")
       
        self.noImageMessage = QLabel("Imagem não enviada!")
        self.noImageMessage.setStyleSheet('color: red')
        self.noImageMessage.setFixedHeight(23)
        self.noImageMessage.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        

        if self.device.deviceHasImage and self.device.deviceImageExtension:
            self.seeImageButton.setVisible(True)
            self.noImageMessage.setVisible(False)
        else:
            self.seeImageButton.setVisible(False)
            self.noImageMessage.setVisible(True)

        self.sendImageButton.setVisible(False)
        self.changeImageButton.setVisible(False)

            
        imageGBLayout = QHBoxLayout()
        imageGBLayout.addStretch(1)
        imageGBLayout.addWidget(self.sendImageButton)
        imageGBLayout.addWidget(self.seeImageButton)
        imageGBLayout.addWidget(self.changeImageButton)
        imageGBLayout.addWidget(self.noImageMessage)
        imageGBLayout.addStretch(1)
        
        imageGroupBox.setLayout(imageGBLayout)

        #--> INSTALATION DOC #

        documentationGroupBox = QGroupBox("Doc. de Instalação")
        documentationGroupBox.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        
        self.sendDocButton = MyQButton(" Enviar ")
        self.downloadDocButton = MyQButton(" Salvar ")
        self.changeDocButton = MyQButton(" Alterar ")
        
        self.noDocMessage = QLabel("Documento não enviado!")
        self.noDocMessage.setStyleSheet('color: red')
        self.noDocMessage.setFixedHeight(23)
        self.noDocMessage.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        if self.device.deviceDocSent:
            self.downloadDocButton.setVisible(True)
            self.noDocMessage.setVisible(False)
        else:
            self.downloadDocButton.setVisible(False)
            self.noDocMessage.setVisible(True)

        self.sendDocButton.setVisible(False)
        self.changeDocButton.setVisible(False)

        docGBLayout = QHBoxLayout()
        docGBLayout.addStretch(1)
        docGBLayout.addWidget(self.sendDocButton)
        docGBLayout.addWidget(self.downloadDocButton)
        docGBLayout.addWidget(self.changeDocButton)
        docGBLayout.addWidget(self.noDocMessage)
        docGBLayout.addStretch(1)

        documentationGroupBox.setLayout(docGBLayout)

        #--> LAYOUT BUILD FILES GROUPBOX #

        filesGBLayout = QHBoxLayout()
        filesGBLayout.addWidget(imageGroupBox)
        filesGBLayout.addWidget(documentationGroupBox)
        
        filesGroupBox = QGroupBox("Arquivos:")
        filesGroupBox.setFont(boldFont)
        filesGroupBox.setLayout(filesGBLayout)

        ############################
        #### --> BUTTONS LAYOUT ####
        ############################
        
        self.editDeviceInfoButton = MyQButton(" Editar ")
        self.saveDeviceInfoButton = MyQButton(" Salvar ")
        self.cancelEditButton = MyQButton(" Cancelar ")
        self.closeWindowButton = MyQButton(" Fechar ")

        buttonsLayout = QHBoxLayout()
        buttonsLayout.addStretch(1)
        buttonsLayout.addWidget(self.editDeviceInfoButton)
        buttonsLayout.addWidget(self.saveDeviceInfoButton)
        buttonsLayout.addWidget(self.cancelEditButton)
        buttonsLayout.addWidget(self.closeWindowButton)
        buttonsLayout.addStretch(1)
        
        self.saveDeviceInfoButton.setVisible(False)
        self.cancelEditButton.setVisible(False)

        if self.loggedUser["category"] > 40:
            self.editDeviceInfoButton.setVisible(False)    

        #################################
        #### --> WINDOW LAYOUT BUILD ####
        #################################
            
        windowLayout = QVBoxLayout()
        windowLayout.addWidget(informationGroupBox)
        windowLayout.addWidget(self.maintenanceGroupBox)
        windowLayout.addWidget(vinculatedProductsGroupBox)
        windowLayout.addWidget(filesGroupBox)
        windowLayout.addLayout(buttonsLayout)

        self.setLayout(windowLayout)
        self.setWindowIcon(QIcon(":/scanner.png"))
        self.setWindowTitle("Dispositivo "+str(self.device.deviceId).zfill(6))
        self.layout().setSizeConstraint(QLayout.SetFixedSize)

        #####################
        #### --> SIGNALS ####
        #####################
        
        self.maintenanceGroupBox.clicked.connect(self.ignoresClickIfNotEdit)
        self.closeWindowButton.clicked.connect(self.close)
        self.editDeviceInfoButton.clicked.connect(self.changeBetweenViewAndEditMode)
        self.cancelEditButton.clicked.connect(self.changeBetweenViewAndEditMode)
        self.deviceObservationsDataField.textChanged.connect(self.calculateCharacters)
        self.maintenanceIntervalTypeComboBox.currentIndexChanged.connect(self.maintenanceIntervalChanged)

        self.seeImageButton.clicked.connect(self.displayDeviceImage)
        self.changeImageButton.clicked.connect(self.sendOrChangeDeviceImage)
        self.sendImageButton.clicked.connect(self.sendOrChangeDeviceImage)

        self.changeDocButton.clicked.connect(self.sendOrChangeDeviceDoc)
        self.sendDocButton.clicked.connect(self.sendOrChangeDeviceDoc)
        self.downloadDocButton.clicked.connect(self.saveDeviceDoc)

        self.saveDeviceInfoButton.clicked.connect(self.saveChangedDeviceInfo)


###############################################################################################################################################################################


    def populateVinculatedProductsTable(self):
        """
            Method used to load all the vinculated products to the table
        """
        self.vinculatedProductsTable.setRowCount(len(self.device.vinculatedProductsList))

        
        for row, (productName, deviceFunction) in enumerate(self.device.vinculatedProductsList):

            # --> Descrição do Produto #
            item = QTableWidgetItem(productName)
            self.vinculatedProductsTable.setItem(row, 0, item)

            # --> Função do Dispositivo #
            item = QTableWidgetItem(deviceFunction)
            self.vinculatedProductsTable.setItem(row, 1, item)
            
        


###############################################################################################################################################################################

    def saveChangedDeviceInfo(self):
        #--> IF DEVICE STATUS IS BEING CHANGED TO ACTIVE#
        message = ""
        failed = 0

    
        
        if self.deviceStatusComboBox.currentData() == 2:
            
            if not self.device.deviceHasImage:
                failed = 1
                message += "\t- Imagem do dispositivo não enviada\n"

            if not self.device.deviceDocSent:
                failed = 1
                message += "\t- Documento de instalação do dispositivo não enviado"
    

            if failed:
                message = "Falha ao ativar dispositivo:\n" + message
                
                messageBox = QMessageBox()
                messageBox.setText(message)
                messageBox.setWindowTitle("Erro!")
                messageBox.setIcon(QMessageBox.Critical)
                messageBox.setWindowIcon(QIcon(":/warning_icon.png"))
                messageBox.exec_()
                
                return

        if self.maintenanceGroupBox.isChecked():
            if not self.maintenanceIntervalTypeComboBox.currentData():
                failed = 1
                message += "\t - Selecione o tipo de intervalo de manutenção preventiva\n"

            if not len(self.deviceBetweenMaintenanceIntervalDataField.text()):
                failed = 1
                message += "\t - Informe um intervalo entre manutenções preventivas\n"
            elif not int(self.deviceBetweenMaintenanceIntervalDataField.text()):
                failed = 1
                message += "\t - Intervalo entre manutenções preventivas INVÁLIDO\n"
        
            if not self.deviceMaintenanceFormsComboBox.currentData():
                failed = 1
                message += "\t - Selecione um formulário de manutenção.\n"
            
            if failed:
                message = "Falha ao atualizar Dispositivo:\n" + message
                
                messageBox = QMessageBox()
                messageBox.setText(message)
                messageBox.setWindowTitle("Erro!")
                messageBox.setIcon(QMessageBox.Critical)
                messageBox.setWindowIcon(QIcon(":/warning_icon.png"))
                messageBox.exec_()

                self.deviceStatusComboBox.setCurrentIndex(self.deviceStatusComboBox.findData(self.device.deviceStatusId, Qt.UserRole))

                return

        if self.device.deviceStatusId == 3:
            status = str(3)
        else:
            status = str(self.deviceStatusComboBox.currentData())

        data = {
            "status" : "'" + status + "'",
            "SAPCode" : "'" + self.deviceSAPCodeDataField.text() + "'",
            "lifecicle" : ("'" + self.deviceLifeCicleDataField.text() + "'" if len(self.deviceLifeCicleDataField.text()) else "'N/D'"),
            "storage" : ("'" + self.deviceStoragePositionDataField.text() + "'" if len(self.deviceStoragePositionDataField.text()) else "NULL"),
            "observation" : "'" + self.deviceObservationsDataField.toPlainText() + "'",
            "hasMaintenance" : self.maintenanceGroupBox.isChecked(),
            "maintenanceType" : self.maintenanceIntervalTypeComboBox.currentData(),
            "maintenanceInterval" : ("'" + self.deviceBetweenMaintenanceIntervalDataField.text() + "'" if len(self.deviceBetweenMaintenanceIntervalDataField.text()) else "'0'"),
            "maintenanceForm" : "'" + str(self.deviceMaintenanceFormsComboBox.currentData()) + "'"
        }

        try:
            self.device.updateDeviceInformation(data)
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
        except Exception as error:
            message = "\nErro: " +str(error)
            messageBox = QMessageBox()
            messageBox.setText(message)
            messageBox.setWindowTitle("Erro!")
            messageBox.setIcon(QMessageBox.Critical)
            messageBox.setWindowIcon(QIcon(":/warning_icon.png"))
            messageBox.exec_()
            return

        self.parent.updateDevicesTable()
        self.device.loadAllDetailedData()

        self.changeBetweenViewAndEditMode()
        
        messageBox = QMessageBox()
        messageBox.setText("Informações do Dispositivo atualizadas com sucesso!")
        messageBox.setIcon(QMessageBox.Information)
        messageBox.setWindowTitle("Atenção!")
        messageBox.setWindowIcon(QIcon(":/scanner.png"))
        messageBox.exec_()
        
###############################################################################################################################################################################


    def sendOrChangeDeviceImage(self):
        path = os.path.join(os.path.join(os.environ['USERPROFILE']), "Desktop")
        filePath, viewType = QFileDialog.getOpenFileName(self, "Selecione a Imagem do Dispositivo", path, "Arquivos de Imagem ( *.jpg *.png)")

        if len(filePath):        
            try:
                self.device.saveOrUpdateDeviceImage(filePath)
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
            except Exception as error:
                place, cause = error.args
                message = "Falha em: " + place + "\nErro: " +cause
                messageBox = QMessageBox()
                messageBox.setText(message)
                messageBox.setWindowTitle("Erro!")
                messageBox.setIcon(QMessageBox.Critical)
                messageBox.setWindowIcon(QIcon(":/warning_icon.png"))
                messageBox.exec_()
                return


            self.parent.updateDevicesTable()
            self.sendImageButton.setVisible(False)
            self.seeImageButton.setVisible(True)
            self.changeImageButton.setVisible(True)
            self.noImageMessage.setVisible(False)

            messageBox = QMessageBox()
            messageBox.setText("Imagem do Dispositivo enviada com sucesso.")
            messageBox.setIcon(QMessageBox.Information)
            messageBox.setWindowTitle("Atenção!")
            messageBox.setWindowIcon(QIcon(":/scanner.png"))
            messageBox.exec_()


###############################################################################################################################################################################

    def sendOrChangeDeviceDoc(self):
        path = os.path.join(os.path.join(os.environ['USERPROFILE']), "Desktop")
        filePath, viewType = QFileDialog.getOpenFileName(self, "Selecione o Documento de Instalação do Dispositivo", path, "Arquivos PDF(*.pdf)")

        if len(filePath):        
            try:
                self.device.saveOrUpdateDeviceDoc(filePath)
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
            except Exception as error:
                place, cause = error.args
                message = "Falha em: " + place + "\nErro: " +cause
                messageBox = QMessageBox()
                messageBox.setText(message)
                messageBox.setWindowTitle("Erro!")
                messageBox.setIcon(QMessageBox.Critical)
                messageBox.setWindowIcon(QIcon(":/warning_icon.png"))
                messageBox.exec_()
                return


            self.parent.updateDevicesTable()
            self.sendDocButton.setVisible(False)
            self.downloadDocButton.setVisible(True)
            self.changeDocButton.setVisible(True)
            self.noDocMessage.setVisible(False)

            messageBox = QMessageBox()
            messageBox.setText("Documento de Instalação do Dispositivo enviado com sucesso.")
            messageBox.setIcon(QMessageBox.Information)
            messageBox.setWindowTitle("Atenção!")
            messageBox.setWindowIcon(QIcon(":/scanner.png"))
            messageBox.exec_()           
        

###############################################################################################################################################################################

    def saveDeviceDoc(self):
        """
        This method is used to download the jig instalation file
        """

        parser = SafeConfigParser()
        parser.read("dbconfig.ini")

        FTPPath = parser.get("ftp", "path")
        FTPUser = parser.get("ftp", "user")
        FTPPass = parser.get("ftp", "pass")
        self.fileName = str(self.device.deviceId).zfill(6) + ".pdf"
                
        messageBox = QMessageBox()
        messageBox.setIcon(QMessageBox.Question)
        messageBox.setWindowIcon(QIcon(":/question.png"))
        messageBox.setWindowTitle("Download do Documento de Instalação")
        messageBox.setText("Salvar o Documento de Instalação do Dispositivo \"" + str(self.device.deviceId).zfill(6) + "\" em sua área\nde trabalho?")
        messageBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        messageBox.button(QMessageBox.Yes).setText("Sim")
        messageBox.button(QMessageBox.No).setText("Não")
        
        messageBox.exec_()
        # --> If the Yes button was clicked #
        if messageBox.clickedButton() == messageBox.button(QMessageBox.No):
            return
        
##################################################################################

        desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        destinationFilePath = desktop + "\\" + str(self.device.deviceId).zfill(6) + ".pdf"

############################################################################
        
        try:
            ftp = FTP(FTPPath)
            ftp.login(FTPUser, FTPPass)
            ftp.cwd("doc")
            ftp.retrbinary("RETR " + self.fileName, open(destinationFilePath, "wb").write)
            ftp.quit()            
           
        except Exception as e:
            messageBox = QMessageBox()
            messageBox.setText("Falha ao efetuar o download do arquivo.\n" + str(e))
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

    def maintenanceIntervalChanged(self, index):
        if index > 0:
            if self.maintenanceIntervalTypeComboBox.currentData(Qt.UserRole) == "DIA":
                self.deviceSulfixInterval.setText(" DIAS CORRIDOS")
            else:
                self.deviceSulfixInterval.setText(" PLACAS TESTADAS")
        else:
            self.deviceSulfixInterval.setText("")

###############################################################################################################################################################################


    def populateMaintenanceFormsComboBox(self):
        maintenanceFormsList = maintenanceformscontainer.MaintenanceFormsContainer()

        try:
            maintenanceFormsList.loadMaintenanceForms()
        except DatabaseConnectionError as error:
            message = "Falha em: " + place + "\nErro: " +cause
            messageBox = QMessageBox()
            messageBox.setText(message)
            messageBox.setWindowTitle("Erro!")
            messageBox.setIcon(QMessageBox.Critical)
            messageBox.setWindowIcon(QIcon(":/warning_icon.png"))
            messageBox.exec_()
            return

        self.deviceMaintenanceFormsComboBox.addItem("", "")
        for maintenanceForm in maintenanceFormsList:
            self.deviceMaintenanceFormsComboBox.addItem(maintenanceForm.formDescription, maintenanceForm.formId)
  

###############################################################################################################################################################################

    def populateDeviceStatusComboBox(self):
        """
        This method is responsible for loading all the device status in the filter combobox
        """

        deviceStatusList = DeviceStatusContainer()

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


        for deviceStatus in deviceStatusList:
            if deviceStatus.deviceStatusId < 3:
                self.deviceStatusComboBox.addItem(deviceStatus.deviceStatusDescription, deviceStatus.deviceStatusId)

###############################################################################################################################################################################
           

    def calculateCharacters(self):
        """
        This method is called when a key is pressed in the action taken description, decrementing its counter
        """

        # --> Line inserted because the uppercase is lost when the backspace is pressed #
        self.deviceObservationsDataField.setCurrentCharFormat(self.textFormat)
        
        textLength = len(self.deviceObservationsDataField.toPlainText())
        if textLength <= 1000:
           self.obsCharCounter.setText(str(1000 - textLength))
        else:
            text = self.deviceObservationsDataField.toPlainText()
            self.deviceObservationsDataField.setPlainText(text[:1000])
            cursor = self.deviceObservationsDataField.textCursor()
            cursor.setPosition(textLength - 1)
            self.deviceObservationsDataField.setTextCursor(cursor)

        
###############################################################################################################################################################################
        
    def changeBetweenViewAndEditMode(self):
        """
        This method is called to switch the window mode between view and edit modes.
        """
        if self.editMode:
            self.editMode = 0

            #--> SAP CODE #
            self.deviceSAPCodeDataLabel.setText(self.device.deviceSAPCode)
            self.deviceSAPCodeLayoutItem = self.informationGBLayout.replaceWidget(self.deviceSAPCodeDataField, self.deviceSAPCodeDataLabel)
            self.deviceSAPCodeDataField = self.deviceSAPCodeLayoutItem.widget()
            self.deviceSAPCodeDataField.setVisible(False)
            self.deviceSAPCodeDataLabel.setVisible(True)
            
            
            #--> DEVICE STATUS #
            if self.device.deviceStatusId < 3:
                self.deviceStatusDataLabel.setText(self.device.deviceStatusDescription)
                self.deviceStatusLayoutItem = self.informationGBLayout.replaceWidget(self.deviceStatusComboBox, self.deviceStatusDataLabel)
                self.deviceStatusComboBox = self.deviceStatusLayoutItem.widget()
                self.deviceStatusComboBox.setVisible(False)
                self.deviceStatusDataLabel.setVisible(True)
            
            #--> LIFE CICLE #
            if self.device.deviceLifeCicle:
                self.deviceLifeCicleDataLabel.setText(str(self.device.deviceLifeCicle))
            else:
                self.deviceLifeCicleDataLabel.setText("N/D")
            self.deviceLifeCicleLayoutItem = self.informationGBLayout.replaceWidget(self.deviceLifeCicleDataField, self.deviceLifeCicleDataLabel)
            self.deviceLifeCicleDataField = self.deviceLifeCicleLayoutItem.widget()
            self.deviceLifeCicleDataField.setVisible(False)
            self.deviceLifeCicleDataLabel.setVisible(True)

            #--> STORAGE POSITION #
            self.deviceStoragePositionDataLabel.setText(self.device.deviceStoragePosition)
            self.deviceStoragePositionLayoutItem = self.informationGBLayout.replaceWidget(self.deviceStoragePositionDataField, self.deviceStoragePositionDataLabel)
            self.deviceStoragePositionDataField = self.deviceStoragePositionLayoutItem.widget()
            self.deviceStoragePositionDataField.setVisible(False)
            self.deviceStoragePositionDataLabel.setVisible(True)

            #-->OBSERVATION#
            self.obsCharCounter.setText(str(1000 - len(self.deviceObservationsDataLabel.text())))
            self.obsCharCounter.setVisible(False)
            self.deviceObservationsDataField = self.observationScrollArea.takeWidget()
            self.observationScrollArea.setWidget(self.deviceObservationsDataLabel)
            self.deviceObservationsDataLabel.setText(self.device.deviceObservation)
            
            #####################
            #### MAINTENANCE ####
            #####################

            if self.device.deviceInfoMaintenance:
                if self.device.deviceMaintenanceIntervalType == "DIA":
                    self.deviceMaintenanceIntervalTypeDataLabel.setText("DIAS CORRIDOS")
                    self.deviceSulfixInterval.setText(" DIAS CORRIDOS")
                    self.deviceBetweenMaintenanceIntervalDataLabel.setText(str(self.device.deviceMaintenanceDaysInterval))
                else:
                    self.deviceMaintenanceIntervalTypeDataLabel.setText("PLACAS TESTADAS")
                    self.deviceSulfixInterval.setText(" PLACAS TESTADAS")
                    self.deviceBetweenMaintenanceIntervalDataLabel.setText(str(self.device.deviceMaintenanceBoardsInterval))

                

            
            #--> INTERVAL TYPE #
            self.maintenanceIntervalTypeLayoutItem = self.maintenanceGBLayout.replaceWidget(self.maintenanceIntervalTypeComboBox, self.deviceMaintenanceIntervalTypeDataLabel)
            self.maintenanceIntervalTypeComboBox = self.maintenanceIntervalTypeLayoutItem.widget()
            self.maintenanceIntervalTypeComboBox.setVisible(False)
            self.deviceMaintenanceIntervalTypeDataLabel.setVisible(True)

            #--> INTERVAL VALUE#
            self.betweenMaintenanceIntervalLayoutItem = self.maintenanceGBLayout.replaceWidget(self.deviceBetweenMaintenanceIntervalDataField, self.deviceBetweenMaintenanceIntervalDataLabel)
            self.deviceBetweenMaintenanceIntervalDataField = self.betweenMaintenanceIntervalLayoutItem.widget()
            self.deviceBetweenMaintenanceIntervalDataLabel.setVisible(True)
            self.deviceBetweenMaintenanceIntervalDataField.setVisible(False)
            
            # --> INTERVAL LABEL #
            if self.device.deviceMaintenanceIntervalType:
                if self.device.deviceMaintenanceIntervalType == "DIA":
                    self.deviceSulfixInterval.setText(" DIAS CORRIDOS")
                else:
                    self.deviceSulfixInterval.setText(" PLACAS TESTADAS")
            else:
                self.deviceSulfixInterval.setText("")


            # --> MAINTENANCE FORM #
            self.deviceMaintenanceFormDataLabel.setText(self.device.deviceMaintenanceFormDescription)
            self.deviceMaintenanceFormLayoutItem = self.maintenanceGBLayout.replaceWidget(self.deviceMaintenanceFormsComboBox, self.deviceMaintenanceFormDataLabel)
            self.deviceMaintenanceFormsComboBox = self.deviceMaintenanceFormLayoutItem.widget()
            self.deviceMaintenanceFormsComboBox.setVisible(False)
            self.deviceMaintenanceFormDataLabel.setVisible(True)
            
            #-->IMAGE#            
            if self.device.deviceHasImage and self.device.deviceImageExtension:
                self.seeImageButton.setVisible(True)
                self.changeImageButton.setVisible(False)                
            else:
                self.sendImageButton.setVisible(False)
                self.noImageMessage.setVisible(True)

            #-->DOCUMENTATION#
            if self.device.deviceDocSent:
                self.downloadDocButton.setVisible(True)
                self.changeDocButton.setVisible(False)
            else:
                self.sendDocButton.setVisible(False)
                self.noDocMessage.setVisible(True)
                
            
            #-->BUTTONS#
            self.editDeviceInfoButton.setVisible(True)
            self.saveDeviceInfoButton.setVisible(False)
            self.cancelEditButton.setVisible(False)
            self.closeWindowButton.setVisible(True)
        else:
            self.editMode = 1

            #--> SAP CODE #
            self.deviceSAPCodeLayoutItem = self.informationGBLayout.replaceWidget(self.deviceSAPCodeDataLabel, self.deviceSAPCodeDataField)
            self.deviceSAPCodeDataLabel = self.deviceSAPCodeLayoutItem.widget()
            self.deviceSAPCodeDataField.setText(self.device.deviceSAPCode)
            self.deviceSAPCodeDataField.setVisible(True)
            self.deviceSAPCodeDataLabel.setVisible(False)

            #--> DEVICE STATUS #
            if self.device.deviceStatusId < 3:
                self.deviceStatusLayoutItem = self.informationGBLayout.replaceWidget(self.deviceStatusDataLabel, self.deviceStatusComboBox)
                self.deviceStatusDataLabel = self.deviceStatusLayoutItem.widget()
                self.deviceStatusComboBox.setVisible(True)
                self.deviceLifeCicleDataLabel.setVisible(False)
                self.deviceStatusComboBox.setCurrentIndex(self.deviceStatusComboBox.findData(self.device.deviceStatusId, Qt.UserRole))
             
            #--> LIFE CICLE #
            self.deviceLifeCicleLayoutItem = self.informationGBLayout.replaceWidget(self.deviceLifeCicleDataLabel, self.deviceLifeCicleDataField)
            self.deviceLifeCicleDataLabel = self.deviceLifeCicleLayoutItem.widget()
            if self.device.deviceLifeCicle:
                self.deviceLifeCicleDataField.setText(str(self.device.deviceLifeCicle))
            self.deviceLifeCicleDataField.setVisible(True)
            self.deviceLifeCicleDataLabel.setVisible(False)

            #-->STORAGE POSITION#
            self.deviceStoragePositionLayoutItem = self.informationGBLayout.replaceWidget(self.deviceStoragePositionDataLabel, self.deviceStoragePositionDataField)
            self.deviceStoragePositionDataLabel = self.deviceStoragePositionLayoutItem.widget()
            if self.device.deviceStoragePosition:
                self.deviceStoragePositionDataField.setText(self.device.deviceStoragePosition)
            self.deviceStoragePositionDataField.setVisible(True)
            self.deviceStoragePositionDataLabel.setVisible(False)

            #-->OBSERVATION#
            self.obsCharCounter.setVisible(True)
            self.deviceObservationsDataLabel = self.observationScrollArea.takeWidget()
            self.observationScrollArea.setWidget(self.deviceObservationsDataField)
            self.deviceObservationsDataField.setPlainText(self.deviceObservationsDataLabel.text())
            self.obsCharCounter.setText(str(1000 - len(self.deviceObservationsDataLabel.text())))
        

            #####################
            #### MAINTENANCE ####
            #####################
            
            #--> INTERVAL TYPE #
            self.maintenanceIntervalTypeLayoutItem = self.maintenanceGBLayout.replaceWidget(self.deviceMaintenanceIntervalTypeDataLabel, self.maintenanceIntervalTypeComboBox)
            self.deviceMaintenanceIntervalTypeDataLabel = self.maintenanceIntervalTypeLayoutItem.widget()
            self.maintenanceIntervalTypeComboBox.setVisible(True)
            self.deviceMaintenanceIntervalTypeDataLabel.setVisible(False)
            
            if self.device.deviceInfoMaintenance:
                self.maintenanceIntervalTypeComboBox.setCurrentIndex(self.maintenanceIntervalTypeComboBox.findData(self.device.deviceMaintenanceIntervalType, Qt.UserRole))
            else:
                self.maintenanceIntervalTypeComboBox.setCurrentIndex(0)

            #--> INTERVAL SIZE #
            self.betweenMaintenanceIntervalLayoutItem = self.maintenanceGBLayout.replaceWidget(self.deviceBetweenMaintenanceIntervalDataLabel, self.deviceBetweenMaintenanceIntervalDataField)
            self.deviceBetweenMaintenanceIntervalDataLabel = self.betweenMaintenanceIntervalLayoutItem.widget()
            self.deviceBetweenMaintenanceIntervalDataLabel.setVisible(False)
            self.deviceBetweenMaintenanceIntervalDataField.setVisible(True)
            self.deviceBetweenMaintenanceIntervalDataField.setText(self.deviceBetweenMaintenanceIntervalDataLabel.text())
                

            # --> MAINTENANCE FORM #
            self.deviceMaintenanceFormLayoutItem = self.maintenanceGBLayout.replaceWidget(self.deviceMaintenanceFormDataLabel, self.deviceMaintenanceFormsComboBox)
            self.deviceMaintenanceFormDataLabel = self.deviceMaintenanceFormLayoutItem.widget()
            self.deviceMaintenanceFormDataLabel.setVisible(False)
            self.deviceMaintenanceFormsComboBox.setVisible(True)
            self.deviceMaintenanceFormsComboBox.setCurrentIndex(self.deviceMaintenanceFormsComboBox.findData(self.device.deviceMaintenanceFormId, Qt.UserRole))
            
           
            #-->IMAGE#
            self.noImageMessage.setVisible(False)
            if self.device.deviceHasImage and self.device.deviceImageExtension:
                self.seeImageButton.setVisible(True)
                self.changeImageButton.setVisible(True)                
            else:
                self.sendImageButton.setVisible(True)

            #-->DOCUMENTATION#
            self.noDocMessage.setVisible(False)
            if self.device.deviceDocSent:
                self.downloadDocButton.setVisible(True)
                self.changeDocButton.setVisible(True)
            else:
                self.sendDocButton.setVisible(True)
            
            #-->BUTTONS#
            self.editDeviceInfoButton.setVisible(False)
            self.saveDeviceInfoButton.setVisible(True)
            self.cancelEditButton.setVisible(True)
            self.closeWindowButton.setVisible(False)

            self.deviceObservationsDataField.setFocus()
            self.deviceObservationsDataField.clearFocus()
        
###############################################################################################################################################################################

    
    def displayDeviceImage(self):
        """
        This method overrides the click event, implementing the invoice download
        """
        
        deviceImageDialog = MyQDeviceImageDialog(self.device.deviceId, self.device.deviceImageExtension)
        deviceImageDialog.exec_()
         
###############################################################################################################################################################################


    def ignoresClickIfNotEdit(self, checked):
        if not self.editMode:
            if not checked:
                self.maintenanceGroupBox.setChecked(True)
            else:
                self.maintenanceGroupBox.setChecked(False)
        
