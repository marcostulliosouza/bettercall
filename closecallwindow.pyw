from PyQt5.QtCore import (
        Qt
    )

from PyQt5.QtGui import (
        QFont,
        QColor,
        QTextCharFormat,
        QIcon,
        QCursor
    )

from PyQt5.QtWidgets import (
        QDialog,
        QLabel,
        QComboBox,
        QPlainTextEdit,
        QPushButton,
        QLayout,
        QHBoxLayout,
        QGridLayout,
        QMessageBox
    )

import detractorscontainer
import qrc_resources
from magicDB import *
from myExceptions import *


__version__ = "2.0.0"


###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################


class CloseCallWindow(QDialog):
    """
    This class is responsible for rendering the login window modally.
    If the login doesn't happen, being cancelled by pressing Cancel or closing
    the windown, the application will terminate
    """
    STATUS_ANSWERED = 1
    STATUS_CANCEL = 0

    def __init__(self, call=None, parent=None):
        super(CloseCallWindow, self).__init__(parent)
        self.call = call
        self.parent = parent
        self.loggedUser = parent.loggedUser
        self.detList = detractorscontainer.DetractorContainer()
        
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        

        # --> Firstly build the interface #
        boldFont = QFont()
        boldFont.setBold(True)
        
        # --> Detractor #
        detractorLabel = QLabel("Detrator: ")
        detractorLabel.setFont(boldFont)
        detractorLabel.setFixedWidth(100)

        self.detractorComboBox = QComboBox()
        self.populateDetractorComboBox()

        # --> Actions Taken and char counter #
        actionTakenLabel = QLabel("Ação Realizada: ")
        actionTakenLabel.setFont(boldFont)

        self.charCounter = QLabel("1000")
        self.charCounter.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.charCounter.setStyleSheet('color: red')
        self.charCounter.setFont(boldFont)

        self.actionTakenDescription = QPlainTextEdit()
        self.actionTakenDescription.setMinimumWidth(300)
        self.actionTakenDescription.setMaximumHeight(80)

        self.textFormat = QTextCharFormat()
        self.textFormat.setFontCapitalization(QFont.AllUppercase)

        self.actionTakenDescription.setCurrentCharFormat(self.textFormat)

        

        # --> Buttons #
        self.confirmCloseCallButton = QPushButton(" Finalizar Chamado ")
        self.confirmCloseCallButton.setCursor(QCursor(Qt.PointingHandCursor))
        
        self.cancelCloseCallButton = QPushButton(" Cancelar ")
        self.cancelCloseCallButton.setCursor(QCursor(Qt.PointingHandCursor))

        # --> Buttons layout #
        buttonsLayout = QHBoxLayout()
        buttonsLayout.addStretch(1)
        buttonsLayout.addWidget(self.confirmCloseCallButton)
        buttonsLayout.addWidget(self.cancelCloseCallButton)
        

        # --> Builds the window layout #
        layout = QGridLayout()
        layout.addWidget(detractorLabel, 0, 0)
        layout.addWidget(self.detractorComboBox, 0, 1)
        layout.addWidget(actionTakenLabel, 1, 0)
        layout.addWidget(self.charCounter, 1, 1)
        layout.addWidget(self.actionTakenDescription, 2, 0, 1, 2)
        layout.addLayout(buttonsLayout, 3, 0, 1, 2)
        
        self.setLayout(layout)

        # --> Connecting the signals #
        self.confirmCloseCallButton.clicked.connect(self.confirmEndCall)
        self.cancelCloseCallButton.clicked.connect(self.cancelEndCall)
        # --> Event that counts the characteres #
        self.actionTakenDescription.textChanged.connect(self.calculateCharacters)
        
    

        self.setWindowIcon(QIcon(":/close_call.png"))
        self.setWindowTitle("Finalizar Chamado")

        # --> Line responsible for preventing window resize
        self.layout().setSizeConstraint(QLayout.SetFixedSize)


###############################################################################################################################################################################


    def populateDetractorComboBox(self):
        """
        This method is used to populate the combobox containing all the detractors
        """
        boldFont = QFont()
        boldFont.setBold(True)

        try:
            self.detList.loadDetractors(self.call.typeId)
        except DatabaseConnectionError as error:
            message = "Falha em: " + place + "\nErro: " +cause
            messageBox = QMessageBox()
            messageBox.setText(message)
            messageBox.setWindowTitle("Erro!")
            messageBox.setIcon(QMessageBox.Critical)
            messageBox.setWindowIcon(QIcon(":/warning_icon.png"))
            messageBox.exec_()
            return

        
        self.detractorComboBox.addItem("", -1)
        
        for row, detractor in enumerate(self.detList):
            self.detractorComboBox.addItem(detractor.detDescription, detractor.detId)
            if int(detractor.detIndicator) == 0:
                self.detractorComboBox.setItemData((row+1), QColor("#CCCCCC"), Qt.BackgroundRole)
            else:
                self.detractorComboBox.setItemData((row+1), boldFont, Qt.FontRole)

###############################################################################################################################################################################


    def calculateCharacters(self):
        """
        This method is called when a key is pressed in the action taken description, decrementing its counter
        """

        # --> Line inserted because the uppercase is lost when the backspace is pressed #
        self.actionTakenDescription.setCurrentCharFormat(self.textFormat)
        
        textLength = len(self.actionTakenDescription.toPlainText())
        if textLength <= 1000:
           self.charCounter.setText(str(1000 - textLength))
        else:
            text = self.actionTakenDescription.toPlainText()
            self.actionTakenDescription.setPlainText(text[:1000])
            cursor = self.actionTakenDescription.textCursor()
            cursor.setPosition(textLength - 1)
            self.actionTakenDescription.setTextCursor(cursor)

        
###############################################################################################################################################################################

    
    def confirmEndCall(self):
        """
        This method is called when the button "End Call" is pressed
        """
        
        # --> Firstly verifies if the fields are filled up #
        try:
            if self.detractorComboBox.currentIndex() < 0:
                raise EmptyFieldsError("Detrator", "Selecione um detrator.")

            if self.actionTakenDescription.document().characterCount() <= 1:
                raise EmptyFieldsError("Ação Realizada", "Descreva a ação realizada durante o chamado.")

        except EmptyFieldsError as error:
            field, message = error.args
            messageBox = QMessageBox()
            messageBox.setText(message)
            messageBox.setWindowTitle("Atenção!")
            messageBox.setIcon(QMessageBox.Warning)
            messageBox.setWindowIcon(QIcon(":/warning_icon.png"))
            messageBox.exec_()
            return

        # -->after that asks to the user for confirmation #
        messageBox = QMessageBox()
        messageBox.setIcon(QMessageBox.Question)
        messageBox.setWindowIcon(QIcon(":/question.png"))
        messageBox.setWindowTitle("Finalizar Chamado?")
        messageBox.setText("Finalizar este chamado?")
        messageBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        messageBox.button(QMessageBox.Yes).setText("Sim")
        messageBox.button(QMessageBox.No).setText("Não")
        
        messageBox.exec_()
        
        # --> If the Yes button was clicked #
        if messageBox.clickedButton() == messageBox.button(QMessageBox.Yes):
           

            actionTaken = self.actionTakenDescription.document().toPlainText()
            detractorId = self.detractorComboBox.itemData(self.detractorComboBox.currentIndex())

            try:
                self.call.closeCall(detractorId, actionTaken)
            except EmptyFieldsError as error:
                field, message = error.args
                messageBox = QMessageBox()
                messageBox.setText(message)
                messageBox.setWindowTitle("Atenção!")
                messageBox.setIcon(QMessageBox.Warning)
                messageBox.setWindowIcon(QIcon(":/warning_icon.png"))
                messageBox.exec_()
                return

            self.done(self.STATUS_ANSWERED)
 
###############################################################################################################################################################################

    
    def cancelEndCall(self):
        """
        This method is called when the user press the button "Cancel"
        """
        self.done(self.STATUS_CANCEL)

###############################################################################################################################################################################
    

    def reject(self):
        self.done(self.STATUS_CANCEL)

   
