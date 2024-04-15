import time
from datetime import datetime

from PyQt5.QtCore import (
        Qt,
        QSize
    )

from PyQt5.QtGui import (
        QFont,
        QIcon
    )

from PyQt5.QtWidgets import (
        QDialog,
        QGroupBox,
        QLabel,
        QPlainTextEdit,
        QLayout,
        QLineEdit,
        QGridLayout,
        QVBoxLayout,
        QHBoxLayout,
        QDateTimeEdit,
        QPushButton,
        QMessageBox
    )

import qrc_resources
from magicDB import *
from myExceptions import *


__version__ = "2.0.0"



###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################

class MyQDataLabel(QLabel):
    """
    This class reimplements the qpushbutton class
    """
    def __init__(self, text="", parent=None):
        super(MyQDataLabel, self).__init__(text, parent)

        regularFont = QFont()
        regularFont.setBold(False)

        self.setFont(regularFont)

###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################

class MyQDateLineEdit(QLineEdit):
    """
    This class reimplements the qlineedit class
    """
    def __init__(self, text="", parent=None):
        super(MyQDateLineEdit, self).__init__(text, parent)

        regularFont = QFont()
        regularFont.setBold(False)

        self.setFont(regularFont)

        self.setFixedWidth(110)
        
        self.setInputMask("00/00/0000 00:00")


###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################
class MyQButton(QPushButton):
    """
    This class reimplements the Qpushbutton for the edit button for users that has the permition
    """
    def __init__(self, text="", parent=None):
        super(MyQButton, self).__init__(text, parent)
    
        self.setIconSize(QSize(10,10))
        self.setFixedSize(16, 16)

###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################


class DetailedCallReportWindow(QDialog):
    """
    This class is responsible for rendering the call window modally.
    If the call is being answered by another user it only will show the
    informations about the call
    """
    
    def __init__(self, call=None, parent=None):
        super(DetailedCallReportWindow, self).__init__(parent)
        self.call = call
        self.parent = parent
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.editBeginning = 0
        self.editEnd = 0
        
        
        ########################################
        #### --> WINDOW LAYOUT CODE SESSION ####
        ########################################
        boldFont = QFont()
        boldFont.setBold(True)

        regularFont = QFont()
        regularFont.setBold(False)
        
        #######################
        #### --> CALL INFO ####
        #######################

        callInfoGroupBox = QGroupBox("Informações sobre o Chamado:")
        callInfoGroupBox.setFont(boldFont)
        
        
        # --> Call Status #
        statusLabel = QLabel("Status do Chamado: ")
        statusLabel.setMinimumWidth(200)
        self.statusData = MyQDataLabel(self.call.status)
       
        # --> Created By #
        createdByLabel = QLabel("Criado por:")
        self.createdByData = MyQDataLabel(self.call.creator)
         
        # --> Call Type #
        callTypeLabel = QLabel("Tipo de Chamado:")
        self.callTypeData = MyQDataLabel(self.call.callType)
       
        # --> Client #
        callClientLabel = QLabel("Cliente:")
        self.callClientData = MyQDataLabel(self.call.client)
       
        # --> Product #
        callProductLabel = QLabel("Produto:")
        self.callProductData = MyQDataLabel(self.call.product)
       
        # --> DT #
        self.dtLabel = QLabel("Dispositivo de Teste:")
        self.dtData = MyQDataLabel("DT-" + self.call.device)
        
        # --> Call Description #
        callDescriptionLabel = QLabel("Descrição do Chamado:")

        self.callDescriptionData = QPlainTextEdit(self.call.description)
        self.callDescriptionData.setFont(regularFont)
        self.callDescriptionData.setReadOnly(True)
        self.callDescriptionData.setMaximumHeight(80)
    
        callInfoFrameLayout = QGridLayout()

        callInfoFrameLayout.addWidget(statusLabel, 0, 0)
        callInfoFrameLayout.addWidget(self.statusData, 0, 1)
        callInfoFrameLayout.addWidget(createdByLabel, 1, 0)
        callInfoFrameLayout.addWidget(self.createdByData, 1, 1)
        callInfoFrameLayout.addWidget(callTypeLabel, 2, 0)
        callInfoFrameLayout.addWidget(self.callTypeData, 2, 1)
        callInfoFrameLayout.addWidget(callClientLabel, 3, 0)
        callInfoFrameLayout.addWidget(self.callClientData, 3, 1)
        callInfoFrameLayout.addWidget(callProductLabel, 4, 0)
        callInfoFrameLayout.addWidget(self.callProductData, 4, 1)

        # -->If the type is "Install Jiga" we wont have the device id #
        if self.call.typeId > 1:
            callInfoFrameLayout.addWidget(self.dtLabel, 5, 0)
            callInfoFrameLayout.addWidget(self.dtData, 5, 1)
            callInfoFrameLayout.addWidget(callDescriptionLabel, 6, 0, 1, 2)
            callInfoFrameLayout.addWidget(self.callDescriptionData, 7, 0, 1, 2)
        else:
            callInfoFrameLayout.addWidget(callDescriptionLabel, 5, 0, 1, 2)
            callInfoFrameLayout.addWidget(self.callDescriptionData, 6, 0, 1, 2)
        

        callInfoGroupBox.setLayout(callInfoFrameLayout)

        ######################################
        #### --> RESPONSIBLE FOR THE CALL ####
        ######################################
        
        callSupportGroupBox = QGroupBox("Informações sobre o Atendimento:")
        callSupportGroupBox.setFont(boldFont)
        callSupportGroupBox.setHidden(True)


        callSupportFrameLayout = QGridLayout()
        
        
        # --> If status of the call is "Em Atendimento" #
        if self.call.statusId == 2:
            callSupportGroupBox.setHidden(False)
        
            callSupportLabel = QLabel("Responsável: ")
            callSupportLabel.setMinimumWidth(200)
        
            callSupportData = MyQDataLabel(str(self.call.support))
            
            callBeginingAnsweringDateLabel = QLabel("Início do Atendimento: ")
            callBeginingAnsweringDateData = MyQDataLabel(str(self.call.formatedAnsweringDate))
            
            callWaitTimeLabel = QLabel("Tempo de Espera: ")

            minutesWaited = self.calculateDateDifference(self.call.formatedOpeningDate, self.call.formatedAnsweringDate)
            if minutesWaited < 0:
                formatedMinutesWaited = "-%02d:%02d" % (abs(minutesWaited)//60, abs(minutesWaited)%60)
            else:
                formatedMinutesWaited = "%02d:%02d" % (minutesWaited//60, minutesWaited%60)
                
            callWaitTimeData = MyQDataLabel(formatedMinutesWaited)
            
            callSupportFrameLayout.addWidget(callSupportLabel, 0, 0)
            callSupportFrameLayout.addWidget(callSupportData, 0, 1)
            callSupportFrameLayout.addWidget(callBeginingAnsweringDateLabel, 1, 0)
            callSupportFrameLayout.addWidget(callBeginingAnsweringDateData, 1, 1)
            callSupportFrameLayout.addWidget(callWaitTimeLabel, 2, 0)
            callSupportFrameLayout.addWidget(callWaitTimeData, 2, 1)
            
        # --> Else if the call status is "Encerrado" #
            
        elif self.call.statusId == 3:
            callSupportGroupBox.setHidden(False)
            
            callSupportLabel = QLabel("Responsável: ")
            callSupportLabel.setMinimumWidth(200)
        
            callSupportData = MyQDataLabel(str(self.call.support))
            
            callBeginningAnsweringDateLabel = QLabel("Início do Atendimento: ")


            #############################################
            # IF HAS PERMISSION INSERTS THE ICON 'EDIT' #
            #############################################
            if self.parent.loggedUser["category"] <= 10:
                self.callBeginningAnsweringDateDataField = MyQDataLabel(self.call.formatedAnsweringDate)
                self.callBeginningAnsweringDateDataEditButton = MyQButton()
                self.callBeginningAnsweringDateDataEditButton.setIcon(QIcon(":/edit.png"))

                self.callBeginningAnsweringDateDataSaveButton = MyQButton()
                self.callBeginningAnsweringDateDataSaveButton.setIcon(QIcon(":/save.png"))
                self.callBeginningAnsweringDateDataSaveButton.setVisible(False)

                self.callBeginningAnsweringDateDataCancelButton = MyQButton()
                self.callBeginningAnsweringDateDataCancelButton.setIcon(QIcon(":/cancel.png"))
                self.callBeginningAnsweringDateDataCancelButton.setVisible(False)
            

                self.callBeginningAnsweringDateData = QHBoxLayout()
                self.callBeginningAnsweringDateData.addWidget(self.callBeginningAnsweringDateDataField)
                self.callBeginningAnsweringDateData.addStretch(1)
                self.callBeginningAnsweringDateData.addWidget(self.callBeginningAnsweringDateDataSaveButton)
                self.callBeginningAnsweringDateData.addWidget(self.callBeginningAnsweringDateDataCancelButton)
                self.callBeginningAnsweringDateData.addWidget(self.callBeginningAnsweringDateDataEditButton)
                

                ## EDIT FIELD ##

                self.callBeginningDateTimeEdit = MyQDateLineEdit(self.call.formatedAnsweringDate)
                self.callBeginningDateTimeEdit.setVisible(False)

                
            else:
                self.callBeginningAnsweringDateData = MyQDataLabel(self.call.formatedAnsweringDate)
            


            callEndAnsweringDateLabel = QLabel("Fim do Atendimento: ")

            # IF HAS PERMISSION INSERTS THE ICON 'EDIT'
            if self.parent.loggedUser["category"] <= 10:
                self.callEndAnsweringDateDataField = MyQDataLabel(self.call.formatedEndDate)
                self.callEndAnsweringDateDataEditButton = MyQButton()
                self.callEndAnsweringDateDataEditButton.setIcon(QIcon(":/edit.png"))

                self.callEndAnsweringDateDataSaveButton = MyQButton()
                self.callEndAnsweringDateDataSaveButton.setIcon(QIcon(":/save.png"))
                self.callEndAnsweringDateDataSaveButton.setVisible(False)

                self.callEndAnsweringDateDataCancelButton = MyQButton()
                self.callEndAnsweringDateDataCancelButton.setIcon(QIcon(":/cancel.png"))
                self.callEndAnsweringDateDataCancelButton.setVisible(False)
            


                self.callEndAnsweringDateData = QHBoxLayout()
                self.callEndAnsweringDateData.addWidget(self.callEndAnsweringDateDataField)
                self.callEndAnsweringDateData.addStretch(1)
                self.callEndAnsweringDateData.addWidget(self.callEndAnsweringDateDataSaveButton)
                self.callEndAnsweringDateData.addWidget(self.callEndAnsweringDateDataCancelButton)
                self.callEndAnsweringDateData.addWidget(self.callEndAnsweringDateDataEditButton)

                ## EDIT FIELD ##

                self.callEndDateTimeEdit = MyQDateLineEdit(self.call.formatedEndDate)
                self.callEndDateTimeEdit.setVisible(False)

            else:
                self.callEndAnsweringDateData = MyQDataLabel(self.call.formatedEndDate)
            
            callWaitTimeLabel = QLabel("Tempo de Espera: ")

            minutesWaited = self.calculateDateDifference(self.call.formatedOpeningDate, self.call.formatedAnsweringDate)
            if minutesWaited < 0:
                formatedMinutesWaited = "-%02d:%02d" % (abs(minutesWaited)//60, abs(minutesWaited)%60)
            else:
                formatedMinutesWaited = "%02d:%02d" % (minutesWaited//60, minutesWaited%60)
                
            self.callWaitTimeData = MyQDataLabel(formatedMinutesWaited)
            
            callAnswerTimeLabel = QLabel("Tempo de Atendimento: ")
            minutesAnswering = self.calculateDateDifference(self.call.formatedAnsweringDate, self.call.formatedEndDate)
            if minutesAnswering < 0:
                formatedMinutesAnswering = "-%02d:%02d" % (abs(minutesAnswering)//60, abs(minutesAnswering)%60)
            else:
                formatedMinutesAnswering = "%02d:%02d" % (minutesAnswering//60, minutesAnswering%60)

            self.callAnswerTimeData = MyQDataLabel(self.call.formatedAnswerDuration)
            
            try:
                callDetractor, callActionTaken = self.call.getActionTaken()
            except DatabaseConnectionError as error:
                place, cause = error.args

                message = "Falha em: " + place + "\nErro: " +cause
            
                messageBox = QMessageBox()
                messageBox.setText(message)
                messageBox.setWindowTitle("Erro!")
                messageBox.setIcon(QMessageBox.Critical)
                messageBox.setWindowIcon(QIcon(":/warning_icon.png"))
                messageBox.exec_()
                self.close()
                return

            callDetractorLabel = QLabel("Detrator: ")
            callDetractorData = MyQDataLabel(callDetractor)
            
            callActionTakenLabel = QLabel("Ação Realizada:")
            callActionTakenData = QPlainTextEdit(callActionTaken)
            callActionTakenData.setFont(regularFont)
            callActionTakenData.setReadOnly(True)
            callActionTakenData.setMaximumHeight(80)

            
                
        
            callSupportFrameLayout.addWidget(callSupportLabel, 0, 0)
            callSupportFrameLayout.addWidget(callSupportData, 0, 1)
            callSupportFrameLayout.addWidget(callBeginningAnsweringDateLabel, 1, 0)

            if self.parent.loggedUser["category"] <= 10:
                callSupportFrameLayout.addLayout(self.callBeginningAnsweringDateData, 1, 1)

                ##############################
                #### EDIT BUTTONS SIGNALS ####
                ##############################
                
                self.callBeginningAnsweringDateDataEditButton.clicked.connect(self.editBeginningAnsweringDateTime)
                self.callBeginningAnsweringDateDataSaveButton.clicked.connect(self.saveBeginningAnsweringDateTime)
                self.callBeginningAnsweringDateDataCancelButton.clicked.connect(self.cancelBeginningAnsweringDateTimeEdit)
                
            else:
                callSupportFrameLayout.addWidget(self.callBeginningAnsweringDateData, 1, 1)
                
            callSupportFrameLayout.addWidget(callEndAnsweringDateLabel, 2, 0)

            if self.parent.loggedUser["category"] <= 10:
                callSupportFrameLayout.addLayout(self.callEndAnsweringDateData, 2, 1)

                ##############################
                #### EDIT BUTTONS SIGNALS ####
                ##############################
                
                self.callEndAnsweringDateDataEditButton.clicked.connect(self.editEndAnsweringDateTime)
                self.callEndAnsweringDateDataSaveButton.clicked.connect(self.saveEndAnsweringDateTime)
                self.callEndAnsweringDateDataCancelButton.clicked.connect(self.cancelEndAnsweringDateTimeEdit)
                
            else:
                callSupportFrameLayout.addWidget(self.callEndAnsweringDateData, 2, 1)
            
            callSupportFrameLayout.addWidget(callWaitTimeLabel, 3, 0)
            callSupportFrameLayout.addWidget(self.callWaitTimeData, 3, 1)
            callSupportFrameLayout.addWidget(callAnswerTimeLabel, 4, 0)
            callSupportFrameLayout.addWidget(self.callAnswerTimeData, 4, 1)
            callSupportFrameLayout.addWidget(callDetractorLabel, 5, 0)
            callSupportFrameLayout.addWidget(callDetractorData, 5, 1)
            callSupportFrameLayout.addWidget(callActionTakenLabel, 6, 0)
            callSupportFrameLayout.addWidget(callActionTakenData, 7, 0, 1, 2)


        callSupportGroupBox.setLayout(callSupportFrameLayout)
        

        ###########################
        #### --> HELPERS INFO #####
        ###########################

        # --> Helper Part #
        self.callHelpersGroupBox = QGroupBox("Colaborador Ajudante:")
        self.callHelpersGroupBox.setFont(boldFont)

        self.callHelpersData = QLabel()
        self.callHelpersData.setFont(regularFont)

        callHelpersFrameLayout = QVBoxLayout()
        callHelpersFrameLayout.addWidget(self.callHelpersData)

        self.callHelpersGroupBox.setLayout(callHelpersFrameLayout)
        self.callHelpersGroupBox.setHidden(True)
        self.fillUpHelpers()


        ##########################
        #### --> LAYOUT BUILD ####
        ##########################
        

        windowLayout = QVBoxLayout()
        windowLayout.addWidget(callInfoGroupBox)
        windowLayout.addWidget(callSupportGroupBox)
        windowLayout.addWidget(self.callHelpersGroupBox)
        windowLayout.addStretch(1)

        self.setLayout(windowLayout)

        self.setWindowIcon(QIcon(":/detailed_call_report.png"))
        self.setFixedWidth(500)

        splitDate = self.call.formatedOpeningDate.split(" ")
        self.setWindowTitle("Chamado aberto em: "+ splitDate[0] +" às "+splitDate[1])

        # --> Line responsible for preventing window resize
        self.layout().setSizeConstraint(QLayout.SetFixedSize)


###############################################################################################################################################################################


    def saveEndAnsweringDateTime(self):
        try:
            endDate = datetime.strptime(self.callEndDateTimeEdit.text(), "%d/%m/%Y %H:%M")
            beginningDate = datetime.strptime(self.callBeginningDateTimeEdit.text(), "%d/%m/%Y %H:%M")
        except ValueError:
            message = "Data de Término do Chamado Inválida!"
            messageBox = QMessageBox()
            messageBox.setText(message)
            messageBox.setWindowTitle("Erro!")
            messageBox.setIcon(QMessageBox.Critical)
            messageBox.setWindowIcon(QIcon(":/warning_icon.png"))
            messageBox.exec_()
            return

        if endDate < beginningDate:
            message = "Data de TÉRMINO do atendimento deve ser maior que a data de INÍCIO do atendimento!"
            messageBox = QMessageBox()
            messageBox.setText(message)
            messageBox.setWindowTitle("Erro!")
            messageBox.setIcon(QMessageBox.Critical)
            messageBox.setWindowIcon(QIcon(":/warning_icon.png"))
            messageBox.exec_()
            return

        self.saveNewDateTimesAndReloadInterface(
            datetime.strptime(self.callBeginningDateTimeEdit.text(), "%d/%m/%Y %H:%M").strftime("%Y-%m-%d %H:%M:%S"),
            endDate.strftime("%Y-%m-%d %H:%M:%S")            
            )

        layoutItem = self.callEndAnsweringDateData.replaceWidget(self.callEndDateTimeEdit, self.callEndAnsweringDateDataField)
        self.callEndDateTimeEdit = layoutItem.widget()
        self.callEndAnsweringDateDataField.setVisible(True)
        self.callEndDateTimeEdit.setVisible(False)

        self.callEndAnsweringDateDataEditButton.setVisible(True)
        self.callEndAnsweringDateDataSaveButton.setVisible(False)
        self.callEndAnsweringDateDataCancelButton.setVisible(False)

        message = "Data e hora de TÉRMINO do chamado atualizada com sucesso!"
        messageBox = QMessageBox()
        messageBox.setText(message)
        messageBox.setWindowTitle("Sucesso!")
        messageBox.setIcon(QMessageBox.Warning)
        messageBox.setWindowIcon(QIcon(":/warning_icon.png"))
        messageBox.exec_()
        

###############################################################################################################################################################################

    def cancelEndAnsweringDateTimeEdit(self):
        layoutItem = self.callEndAnsweringDateData.replaceWidget(self.callEndDateTimeEdit, self.callEndAnsweringDateDataField)
        self.callEndDateTimeEdit = layoutItem.widget()
        self.callEndAnsweringDateDataField.setVisible(True)
        self.callEndDateTimeEdit.setVisible(False)

        self.callEndAnsweringDateDataEditButton.setVisible(True)
        self.callEndAnsweringDateDataSaveButton.setVisible(False)
        self.callEndAnsweringDateDataCancelButton.setVisible(False)




###############################################################################################################################################################################

    def editEndAnsweringDateTime(self):
        self.callEndDateTimeEdit.setText(self.callEndAnsweringDateDataField.text())
        layoutItem = self.callEndAnsweringDateData.replaceWidget(self.callEndAnsweringDateDataField, self.callEndDateTimeEdit)
        self.callEndAnsweringDateDataField = layoutItem.widget()
        self.callEndAnsweringDateDataField.setVisible(False)
        self.callEndDateTimeEdit.setVisible(True)

        self.callEndAnsweringDateDataEditButton.setVisible(False)
        self.callEndAnsweringDateDataSaveButton.setVisible(True)
        self.callEndAnsweringDateDataCancelButton.setVisible(True)

###############################################################################################################################################################################


    def saveBeginningAnsweringDateTime(self):
        try:
            endDate = datetime.strptime(self.callEndDateTimeEdit.text(), "%d/%m/%Y %H:%M")
            beginningDate = datetime.strptime(self.callBeginningDateTimeEdit.text(), "%d/%m/%Y %H:%M")
        except ValueError:
            message = "Data de Início do Chamado Inválida!"
            messageBox = QMessageBox()
            messageBox.setText(message)
            messageBox.setWindowTitle("Erro!")
            messageBox.setIcon(QMessageBox.Critical)
            messageBox.setWindowIcon(QIcon(":/warning_icon.png"))
            messageBox.exec_()
            return

        if endDate < beginningDate:
            message = "Data de INÍCIO do atendimento deve ser menor que a data de TÉRMINO do atendimento!"
            messageBox = QMessageBox()
            messageBox.setText(message)
            messageBox.setWindowTitle("Erro!")
            messageBox.setIcon(QMessageBox.Critical)
            messageBox.setWindowIcon(QIcon(":/warning_icon.png"))
            messageBox.exec_()
            return

        self.saveNewDateTimesAndReloadInterface(
            beginningDate.strftime("%Y-%m-%d %H:%M:%S"),
            datetime.strptime(self.callEndDateTimeEdit.text(), "%d/%m/%Y %H:%M").strftime("%Y-%m-%d %H:%M:%S")
            )

        layoutItem = self.callBeginningAnsweringDateData.replaceWidget(self.callBeginningDateTimeEdit, self.callBeginningAnsweringDateDataField)
        self.callBeginningDateTimeEdit = layoutItem.widget()
        self.callBeginningAnsweringDateDataField.setVisible(True)
        self.callBeginningDateTimeEdit.setVisible(False)

        self.callBeginningAnsweringDateDataEditButton.setVisible(True)
        self.callBeginningAnsweringDateDataSaveButton.setVisible(False)
        self.callBeginningAnsweringDateDataCancelButton.setVisible(False)

        message = "Data e hora de INÍCIO DE ATENDIMENTO do chamado atualizada com sucesso!"
        messageBox = QMessageBox()
        messageBox.setText(message)
        messageBox.setWindowTitle("Sucesso!")
        messageBox.setIcon(QMessageBox.Warning)
        messageBox.setWindowIcon(QIcon(":/warning_icon.png"))
        messageBox.exec_()

###############################################################################################################################################################################

    def cancelBeginningAnsweringDateTimeEdit(self):
        layoutItem = self.callBeginningAnsweringDateData.replaceWidget(self.callBeginningDateTimeEdit, self.callBeginningAnsweringDateDataField)
        self.callBeginningDateTimeEdit = layoutItem.widget()
        self.callBeginningAnsweringDateDataField.setVisible(True)
        self.callBeginningDateTimeEdit.setVisible(False)

        self.callBeginningAnsweringDateDataEditButton.setVisible(True)
        self.callBeginningAnsweringDateDataSaveButton.setVisible(False)
        self.callBeginningAnsweringDateDataCancelButton.setVisible(False)
        

###############################################################################################################################################################################

    def editBeginningAnsweringDateTime(self):
        self.callBeginningDateTimeEdit.setText(self.callBeginningAnsweringDateDataField.text())
        layoutItem = self.callBeginningAnsweringDateData.replaceWidget(self.callBeginningAnsweringDateDataField, self.callBeginningDateTimeEdit)
        self.callBeginningAnsweringDateDataField = layoutItem.widget()
        self.callBeginningAnsweringDateDataField.setVisible(False)
        self.callBeginningDateTimeEdit.setVisible(True)

        self.callBeginningAnsweringDateDataEditButton.setVisible(False)
        self.callBeginningAnsweringDateDataSaveButton.setVisible(True)
        self.callBeginningAnsweringDateDataCancelButton.setVisible(True)
        


###############################################################################################################################################################################

    def calculateDateDifference(self, firstDate, secondDate):
        """
        This method receives 2 dates and return its difference in minutes
        """
        dateFormat = "%d/%m/%Y %H:%M"
        date1 = datetime.strptime(str(firstDate), dateFormat)
        date2 = datetime.strptime(str(secondDate), dateFormat)

        date1Timestamp = time.mktime(date1.timetuple())
        date2Timestamp = time.mktime(date2.timetuple())

        return (int(date2Timestamp) // 60) - (int(date1Timestamp) // 60) 


###############################################################################################################################################################################


    def fillUpHelpers(self):
        """
        This method is used to verify if there is any helper in the call.
        If there is any helper show it in the report
        """

        hasHelpers, helpersList = self.call.hasHelpers()
        if hasHelpers:
            self.callHelpersData.setText("\n".join(helpersList))
            self.callHelpersGroupBox.setHidden(False)


###############################################################################################################################################################################

    def saveNewDateTimesAndReloadInterface(self, beginningDate, endDate):
        try:
            self.call.changeCallDateTimes(beginningDate, endDate)
        except DatabaseConnectionError as error:
            place, cause = error.args

            message = "Falha em: " + place + "\nErro: " +cause
                
            messageBox = QMessageBox()
            messageBox.setText(message)
            messageBox.setWindowTitle("Erro!")
            messageBox.setIcon(QMessageBox.Critical)
            messageBox.setWindowIcon(QIcon(":/warning_icon.png"))
            messageBox.exec_()
            self.close()
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

        self.parent.updateCallsTable()
        self.call.updateDuration()
        

        minutesWaited = self.calculateDateDifference(self.call.formatedOpeningDate, self.call.formatedAnsweringDate)
        if minutesWaited < 0:
            formatedMinutesWaited = "-%02d:%02d" % (abs(minutesWaited)//60, abs(minutesWaited)%60)
        else:
            formatedMinutesWaited = "%02d:%02d" % (minutesWaited//60, minutesWaited%60)
                
        self.callWaitTimeData.setText(formatedMinutesWaited)
        self.callBeginningAnsweringDateDataField.setText(self.call.formatedAnsweringDate)
            
        minutesAnswering = self.calculateDateDifference(self.call.formatedAnsweringDate, self.call.formatedEndDate)
        if minutesAnswering < 0:
            formatedMinutesAnswering = "-%02d:%02d" % (abs(minutesAnswering)//60, abs(minutesAnswering)%60)
        else:
            formatedMinutesAnswering = "%02d:%02d" % (minutesAnswering//60, minutesAnswering%60)

        self.callAnswerTimeData.setText(formatedMinutesAnswering)
        self.callEndAnsweringDateDataField.setText(self.call.formatedEndDate)

        
        
        
