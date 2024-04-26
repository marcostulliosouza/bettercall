from PyQt5.QtCore import (
    Qt,
    QTimer
    )

from PyQt5.QtGui import (
    QIcon,
    QFont,
    QColor,
    QCursor
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
    QLayout,
    QMessageBox
    )

import qrc_resources
from magicDB import *
from myExceptions import *
import closecallwindow
import selectuserwindow

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

        self.setHidden(True)
        self.setMinimumWidth(120)
        self.setCursor(QCursor(Qt.PointingHandCursor))

###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################

class MyQDataLabel(QLabel):
    """
    This class reimplements the QLabel class
    """
    def __init__(self, text="", parent=None):
        super(MyQDataLabel, self).__init__(text, parent)

        regularFont = QFont()
        regularFont.setBold(False)

        self.setFont(regularFont)
        
###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################


class CallWindow(QDialog):
    """
    This class is responsible for rendering the call window modally.
    If the call is being answered by another user it only will load just the 
    """
    
    def __init__(self, call=None, parent=None):
        super(CallWindow, self).__init__(parent)
        self.call = call
        self.parent = parent
        self.loggedUser = parent.loggedUser
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setMinimumWidth(450)
        
        self.updateInterfaceTimer = QTimer()

        self.exitStatus = 0
        
        # --> Duration #
        durationLabel = QLabel("Duração:")
        self.lcdDisplay = QLCDNumber(self)
        self.lcdDisplay.setSegmentStyle(QLCDNumber.Filled)
        self.lcdDisplay.setMinimumWidth(380)
        self.lcdDisplay.setMinimumHeight(100)
        self.lcdDisplay.setMaximumHeight(100)
        self.updateClock()       
        
        
        # --> Buttons #
        self.addHelpButton = MyQPushButton(" Adicionar Ajudante ")
        
        self.answerCallButton = MyQPushButton(" Atender Chamado ")
        self.answerCallButton.setHidden(False)
        
        self.finishCallButton = MyQPushButton(" Finalizar Chamado ")
        
        self.transferCallButton = MyQPushButton(" Transferir Chamado ")
        
        self.giveupCallButton = MyQPushButton(" Desistir do Chamado ")
        
        # --> Groupbox containing the call information #
        groupBoxTitleFont = QFont()
        groupBoxTitleFont.setBold(True)

        # --> Call Data elements #
        callInfoFont = QFont()
        callInfoFont.setBold(False)

        # --> Create the label and field for the responsible for the call #

        callSupportGroupBox = QGroupBox("Colaborador Responsável:")
        callSupportGroupBox.setFont(groupBoxTitleFont)

        callSupportData = MyQDataLabel(self.call.support)
       
        callSupportLayout = QHBoxLayout()
        callSupportLayout.addStretch(1)
        callSupportLayout.addWidget(callSupportData)
        callSupportLayout.addStretch(1)
        callSupportGroupBox.setLayout(callSupportLayout)
        

        buttonLayout = QHBoxLayout()
        buttonLayout.setAlignment(Qt.AlignHCenter)
        buttonLayout.addWidget(self.addHelpButton)
        buttonLayout.addStretch(1)
        buttonLayout.addWidget(self.answerCallButton)
        buttonLayout.addWidget(self.finishCallButton)
        buttonLayout.addStretch(1)
        buttonLayout.addWidget(self.transferCallButton)

        buttonLayout2 = QHBoxLayout()
        buttonLayout2.setAlignment(Qt.AlignHCenter)
        buttonLayout2.addStretch(1)
        buttonLayout2.addWidget(self.giveupCallButton)
        buttonLayout2.addStretch(1)

        

        callInfoGroupBox = QGroupBox("Informações sobre o Chamado:")
        callInfoGroupBox.setFont(groupBoxTitleFont)

        # --> Created By #
        createdByLabel = QLabel("Criado por:")
        self.createdByData = MyQDataLabel(self.call.creator)
        
        # --> Call type #
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

        # --> Local #
        self.localLabel = QLabel("Local:")
        self.localData = MyQDataLabel(self.call.location)

        # --> Call Description #
        callDescriptionLabel = QLabel("Descrição do Chamado:")


        self.callDescriptionData = QPlainTextEdit(self.call.description)
        self.callDescriptionData.setFont(callInfoFont)
        self.callDescriptionData.setReadOnly(True)
        self.callDescriptionData.setMaximumHeight(80)

                
        # --> Create the groupbox layout #
        callInfoFrameLayout = QGridLayout()
        callInfoFrameLayout.addWidget(createdByLabel, 0, 0)
        callInfoFrameLayout.addWidget(self.createdByData, 0, 1)
        callInfoFrameLayout.addWidget(callTypeLabel, 1, 0)
        callInfoFrameLayout.addWidget(self.callTypeData, 1, 1)
        callInfoFrameLayout.addWidget(callClientLabel, 2, 0)
        callInfoFrameLayout.addWidget(self.callClientData, 2, 1)
        callInfoFrameLayout.addWidget(callProductLabel, 3, 0)
        callInfoFrameLayout.addWidget(self.callProductData, 3, 1)

        # --> If the type is "Install Jiga" we wont have the device id #
        if self.call.typeId > 1:
            callInfoFrameLayout.addWidget(self.dtLabel, 4, 0)
            callInfoFrameLayout.addWidget(self.dtData, 4, 1)
            callInfoFrameLayout.addWidget(self.localLabel, 5, 0)
            callInfoFrameLayout.addWidget(self.localData, 5, 1)
            callInfoFrameLayout.addWidget(callDescriptionLabel, 6, 0, 1, 2)
            callInfoFrameLayout.addWidget(self.callDescriptionData, 7, 0, 1, 2)
        else:
            callInfoFrameLayout.addWidget(callDescriptionLabel, 6, 0, 1, 2)
            callInfoFrameLayout.addWidget(self.callDescriptionData, 7, 0, 1, 2)

        callInfoGroupBox.setLayout(callInfoFrameLayout)


        # --> Helper Part #
        self.callHelpersGroupBox = QGroupBox("Colaborador Ajudante:")
        self.callHelpersGroupBox.setFont(groupBoxTitleFont)

        self.callHelpersData = QLabel()
        self.callHelpersData.setFont(callInfoFont)

        callHelpersFrameLayout = QVBoxLayout()
        callHelpersFrameLayout.addWidget(self.callHelpersData)

        self.callHelpersGroupBox.setLayout(callHelpersFrameLayout)
        self.callHelpersGroupBox.setHidden(True)

     
        # --> Build the layout #
        layout = QVBoxLayout()
        layout.addWidget(self.lcdDisplay)

        # --> If the call is being answered by someone #
        if self.call.statusId > 1:
            # --> And is not the user watching the call #
            if self.call.supportId != self.loggedUser['id']:
                layout.addWidget(callSupportGroupBox)
            # --> Else, if the user is responsible #
            else:
                self.switchInterfaceState()
                layout.addLayout(buttonLayout)
                layout.addLayout(buttonLayout2)
        else:
            layout.addLayout(buttonLayout)
            layout.addLayout(buttonLayout2)
            
        layout.addWidget(callInfoGroupBox)
        
        layout.addWidget(self.callHelpersGroupBox)
        

        # --> Set the window layout and complements #
        self.setLayout(layout)
        self.layout().setSizeConstraint(QLayout.SetFixedSize)

        # --> Connecting the signals to the slots #
        self.addHelpButton.clicked.connect(self.addHelperCall)
        self.answerCallButton.clicked.connect(self.answerCall)
        self.finishCallButton.clicked.connect(self.close)
        self.transferCallButton.clicked.connect(self.transferCall)
        self.giveupCallButton.clicked.connect(self.giveupCall)

        # --> Start interface update timer #
        self.updateInterfaceTimer.timeout.connect(self.updateCallWindowUI)
        self.updateInterfaceTimer.start(30000)
        self.updateCallWindowUI()

        self.setWindowIcon(QIcon(":/call.png"))
        self.setWindowTitle("Atender Chamado")

        # --> Line responsible for preventing window resize
        self.layout().setSizeConstraint(QLayout.SetFixedSize)


###############################################################################################################################################################################

    def answerCall(self):
        """
        This method is used to ask the user if he wants to quit the application
        """
        messageBox = QMessageBox()
        messageBox.setIcon(QMessageBox.Question)
        messageBox.setWindowIcon(QIcon(":/question.png"))
        messageBox.setWindowTitle("Atender Chamado?")
        messageBox.setText("Iniciar o atendimento deste chamado?")
        messageBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        
        messageBox.button(QMessageBox.Yes).setText("Sim")
        messageBox.button(QMessageBox.Yes).setCursor(QCursor(Qt.PointingHandCursor))
        
        messageBox.button(QMessageBox.No).setText("Não")
        messageBox.button(QMessageBox.No).setCursor(QCursor(Qt.PointingHandCursor))
        
        messageBox.exec_()
        
        # --> If the Yes button was clicked #
        if messageBox.clickedButton() == messageBox.button(QMessageBox.Yes):

            # --> Try to set the call as being answered
            try:
                self.call.setCallAsBeingAnswered(self.loggedUser["id"])
            except DatabaseConnectionError as error:
                message = "Falha em: " + place + "\nErro: " +cause
                messageBox = QMessageBox()
                messageBox.setText(message)
                messageBox.setWindowTitle("Erro!")
                messageBox.setIcon(QMessageBox.Critical)
                messageBox.setWindowIcon(QIcon(":/warning_icon.png"))
                messageBox.exec_()
                return

            # --> After that update the call object with the new information
            try:
                self.call.updateCallData()
            except DatabaseConnectionError as error:
                message = "Falha em: " + place + "\nErro: " +cause
                messageBox = QMessageBox()
                messageBox.setText(message)
                messageBox.setWindowTitle("Erro!")
                messageBox.setIcon(QMessageBox.Critical)
                messageBox.setWindowIcon(QIcon(":/warning_icon.png"))
                messageBox.exec_()
                return
            
            self.switchInterfaceState()
            self.updateCallWindowUI()
            self.parent.userAnsweringCall = True
            self.parent.updateOpenedCallsTable()


###############################################################################################################################################################################


    def giveupCall(self):
        """
        This method is used when the user wants to give up from a call that he started to answer
        """
        messageBox = QMessageBox()
        messageBox.setIcon(QMessageBox.Question)
        messageBox.setWindowIcon(QIcon(":/question.png"))
        messageBox.setWindowTitle("Desistir de Chamado?")
        messageBox.setText("Deseja desistir de atender este chamado?")
        messageBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        
        messageBox.button(QMessageBox.Yes).setText("Sim")
        messageBox.button(QMessageBox.Yes).setCursor(QCursor(Qt.PointingHandCursor))
        
        messageBox.button(QMessageBox.No).setText("Não")
        messageBox.button(QMessageBox.No).setCursor(QCursor(Qt.PointingHandCursor))
        
        messageBox.exec_()
        
        # --> If the Yes button was clicked #
        if messageBox.clickedButton() == messageBox.button(QMessageBox.Yes):
            try:
                self.call.giveUpFromCall(self.loggedUser["id"])
            except DatabaseConnectionError as error:
                message = "Falha em: " + place + "\nErro: " +cause
                messageBox = QMessageBox()
                messageBox.setText(message)
                messageBox.setWindowTitle("Erro!")
                messageBox.setIcon(QMessageBox.Critical)
                messageBox.setWindowIcon(QIcon(":/warning_icon.png"))
                messageBox.exec_()
                return

            try:
                self.call.updateCallData()
            except DatabaseConnectionError as error:
                message = "Falha em: " + place + "\nErro: " +cause
                messageBox = QMessageBox()
                messageBox.setText(message)
                messageBox.setWindowTitle("Erro!")
                messageBox.setIcon(QMessageBox.Critical)
                messageBox.setWindowIcon(QIcon(":/warning_icon.png"))
                messageBox.exec_()
                return
            self.close()
        

###############################################################################################################################################################################


    def switchInterfaceState(self):
        """
        This method inserts the responsible for the call
        """
        if self.call.statusId > 1:
            self.answerCallButton.setHidden(True)
            self.finishCallButton.setHidden(False)
            self.addHelpButton.setHidden(False)
            self.transferCallButton.setHidden(False)
            self.giveupCallButton.setHidden(False)
                     

###############################################################################################################################################################################
   
    
    def addHelperCall(self):
        """
        This method is called when the button "Adicionar ajudante" is clicked
        """
        title = "Adicionar Ajudante"
        icon = "add_helper"
        confirmation = True
        confirmationMessage = "Adicionar este usuário como ajudante?"
        mode = selectuserwindow.AllCallHelpersMode
        helperUserWindow = selectuserwindow.SelectUserWindow(self, title, icon, confirmation, confirmationMessage, mode, self.call.callId)
        helperUserWindow.exec_()

        selectedId = helperUserWindow.result()
        if  selectedId > 0:
            try:
                isHelping = self.call.isHelping(selectedId)
            except DatabaseConnectionError as error:
                message = "Falha em: " + place + "\nErro: " +cause
                messageBox = QMessageBox()
                messageBox.setText(message)
                messageBox.setWindowTitle("Erro!")
                messageBox.setIcon(QMessageBox.Critical)
                messageBox.setWindowIcon(QIcon(":/warning_icon.png"))
                messageBox.exec_()
                return
            
            if not isHelping:
                try:
                    self.call.addHelper(selectedId)
                except DatabaseConnectionError as error:
                    message = "Falha em: " + place + "\nErro: " +cause
                    messageBox = QMessageBox()
                    messageBox.setText(message)
                    messageBox.setWindowTitle("Erro!")
                    messageBox.setIcon(QMessageBox.Critical)
                    messageBox.setWindowIcon(QIcon(":/warning_icon.png"))
                    messageBox.exec_()
                    return
                self.updateCallWindowUI()
                
            else:
                messageBox = QMessageBox()
                messageBox.setText("Usuário selecionado já está ajudando neste chamado.")
                messageBox.setWindowTitle("Atenção!")
                messageBox.setIcon(QMessageBox.Warning)
                messageBox.setWindowIcon(QIcon(":/warning_icon.png"))
                messageBox.exec_()
                return
        
        
###############################################################################################################################################################################
        
        
    
    def transferCall(self):
        """
        This method is called when the button "Transferir Chamado" is clicked
        """
        title = "Transferir Chamado"
        icon = "switch_user"
        confirmation = True
        confirmationMessage = "Transferir o chamado para este usuário?"
        mode = selectuserwindow.UsersTransferCallMode
        transferUserWindow = selectuserwindow.SelectUserWindow(self, title, icon, confirmation, confirmationMessage, mode)
        transferUserWindow.exec_()
        selectedId = transferUserWindow.result()
        if selectedId > 0:
            try:
                self.call.transferCallFromTo(self.loggedUser["id"], selectedId)
            except DatabaseConnectionError as error:
                message = "Falha em: " + place + "\nErro: " +cause
                messageBox = QMessageBox()
                messageBox.setText(message)
                messageBox.setWindowTitle("Erro!")
                messageBox.setIcon(QMessageBox.Critical)
                messageBox.setWindowIcon(QIcon(":/warning_icon.png"))
                messageBox.exec_()
                return

            try:
                self.call.updateCallData()
            except DatabaseConnectionError as error:
                message = "Falha em: " + place + "\nErro: " +cause
                messageBox = QMessageBox()
                messageBox.setText(message)
                messageBox.setWindowTitle("Erro!")
                messageBox.setIcon(QMessageBox.Critical)
                messageBox.setWindowIcon(QIcon(":/warning_icon.png"))
                messageBox.exec_()
                return

            self.close()
            

###############################################################################################################################################################################
        
    
    def updateCallWindowUI(self):
        """
        This method is called periodically when the call window is oppened, updating
        the clock and the Helpers list
        """
        self.updateClock()
        try:
            hasHelpers, helpersList = self.call.hasHelpers()
        except DatabaseConnectionError as error:
            message = "Falha em: " + place + "\nErro: " +cause
        
            messageBox = QMessageBox()
            messageBox.setText(message)
            messageBox.setWindowTitle("Erro!")
            messageBox.setIcon(QMessageBox.Critical)
            messageBox.setWindowIcon(QIcon(":/warning_icon.png"))
            messageBox.exec_()
            return


        if hasHelpers:
            self.callHelpersData.setText("\n".join(helpersList))
            self.callHelpersGroupBox.setHidden(False)
            
            
###############################################################################################################################################################################
            

    def updateClock(self):
        """
        This method displays the call duration. If the call is late or in advance the display's palette will be changed
        to fits the status color
        """
        try:
            self.call.updateDuration()
            
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

        if self.call.statusId == 1: #Aberto
            duration = self.call.totalDuration
            formatedDuration = self.call.formatedTotalDuration
        else:
            duration = self.call.answerDuration
            formatedDuration = self.call.formatedAnswerDuration
            
        if duration > 30:
            lcdPalette = self.lcdDisplay.palette()
            lcdPalette.setColor(lcdPalette.WindowText, QColor(255, 0, 0))
            self.lcdDisplay.setPalette(lcdPalette)
        elif duration < 0:
            lcdPalette = self.lcdDisplay.palette()
            lcdPalette.setColor(lcdPalette.WindowText, QColor(20, 20, 255))
            self.lcdDisplay.setPalette(lcdPalette)
        else:
            lcdPalette = self.lcdDisplay.palette()
            lcdPalette.setColor(lcdPalette.WindowText, QColor(0, 0, 0))
            self.lcdDisplay.setPalette(lcdPalette)

        
        self.lcdDisplay.setDigitCount(len(formatedDuration))
        self.lcdDisplay.display(formatedDuration)


###############################################################################################################################################################################


    def showEvent(self, event):
        """
        This method is called when a call at the call table is double clicked.
        It locks the call, preventing it for being answered twice at the same time.
        """
        if self.call.statusId == 1:
            try:
                self.call.lockCall(True)
                
            except DatabaseConnectionError as error:
                place, cause = error.args

                message = "Falha em: " + place + "\nErro: " +cause
        
                messageBox = QMessageBox()
                messageBox.setText(message)
                messageBox.setWindowTitle("Erro!")
                messageBox.setIcon(QMessageBox.Critical)
                messageBox.setWindowIcon(QIcon(":/warning_icon.png"))
                messageBox.exec_()
                self.exitStatus = 1
                self.close()
                return

    ###############################################################################################################################################################################

    def reject(self):
        """
        This methods replace the slot reject, executing the triggering the Close
        Event
        """
        self.close()

    ###############################################################################################################################################################################

    def closeEvent(self, event):
        """
        This method is a substitute for the closeEvent SLOT
        It checks if the call need to be answered before close or not
        """
        # --> if the detailed call window is not closed by an error #
        if self.exitStatus == 0:

            # --> if the user that opened the detailed call is not the responsible for this call #
            if self.call.statusId == 1:
                try:
                    self.call.lockCall(False)

                except DatabaseConnectionError as error:
                    place, cause = error.args

                    message = "Falha em: " + place + "\nErro: " + cause

                    messageBox = QMessageBox()
                    messageBox.setText(message)
                    messageBox.setWindowTitle("Erro!")
                    messageBox.setIcon(QMessageBox.Critical)
                    messageBox.setWindowIcon(QIcon(":/warning_icon.png"))
                    messageBox.exec_()
                    return

            else:
                if self.call.supportId == self.loggedUser['id']:
                    closeCallWindow = closecallwindow.CloseCallWindow(self.call, self)
                    self.parent.updateOpenedCallsTable()
                    closeCallWindow.exec_()
                    if closeCallWindow.result() == 0:
                        event.ignore()
                    else:
                        self.parent.userAnsweringCall = False

        self.parent.updateOpenedCallsTable()

                
