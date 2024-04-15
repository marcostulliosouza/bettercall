from PyQt5.QtCore import (
        Qt
    )

from PyQt5.QtGui import (
        QFont,
        QIcon,
        QCursor
    )

from PyQt5.QtWidgets import (
        QDialog,
        QLabel,
        QComboBox,
        QPushButton,
        QHBoxLayout,
        QGridLayout,
        QMessageBox
    )

import userscontainer
from myExceptions import *

__version__ = "2.0.0"

AllActiveUsersMode = 0
AllActiveUsersButMeMode = 1
AllCallHelpersMode = 2
UsersTransferCallMode = 3


###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################


class SelectUserWindow(QDialog):
    """
    This class is responsible for rendering the user selection window.
    It inherit the usercontainer class, responsible for selecting the list of
    users based in the context they need to be selected
    """
    def __init__(self, parent=None, title=None, icon=None, confirmation=False, message=None, mode=AllActiveUsersMode, callId=None):
        super(SelectUserWindow, self).__init__(parent)
        
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setFixedSize(300, 100)

        self.mode = mode
        self.parent = parent
        self.loggedUser = parent.loggedUser
        self.confirmation = confirmation
        self.confirmationMessage = message
        self.mode = mode
        self.callId = callId

        self.usersList = userscontainer.UsersContainer()
        ###################################
        # --> Firstly build the interface #
        ###################################

        
        boldFont = QFont()
        boldFont.setBold(True)
        
        # --> Detractor #
        selectUserLabel = QLabel("Usuário: ")
        selectUserLabel.setFont(boldFont)
        selectUserLabel.setFixedWidth(50)

        self.userComboBox = QComboBox()
        self.populateUserComboBox()

        # --> Buttons #
        self.confirmSelectUserButton = QPushButton(" Confirmar ")
        self.confirmSelectUserButton.setCursor(QCursor(Qt.PointingHandCursor))
        
        self.cancelSelectUserButton = QPushButton(" Cancelar ")
        self.cancelSelectUserButton.setCursor(QCursor(Qt.PointingHandCursor))

        # --> Buttons layout #
        buttonsLayout = QHBoxLayout()
        buttonsLayout.addStretch(1)
        buttonsLayout.addWidget(self.confirmSelectUserButton)
        buttonsLayout.addWidget(self.cancelSelectUserButton)

        # --> Builds the window layout #
        layout = QGridLayout()
        layout.addWidget(selectUserLabel, 0, 0)
        layout.addWidget(self.userComboBox, 0, 1)
        layout.addLayout(buttonsLayout, 1, 0, 1, 2)

        self.setLayout(layout)

        # --> Connecting the signals #
        self.confirmSelectUserButton.clicked.connect(self.confirmSelectedUser)
        self.cancelSelectUserButton.clicked.connect(self.cancelSelectUser)

        
        if title is not None:
            self.setWindowTitle(title)

        if icon is not None:
            self.setWindowIcon(QIcon(":/" +icon+ ".png"))
            

###############################################################################################################################################################################

    def populateUserComboBox(self):
        """
        This method is used to load the users in the user container that can answer a call
        """
        try:
            if self.mode == AllActiveUsersMode:
                self.usersList.loadAllActiveUsers()
                
            elif self.mode == AllActiveUsersButMeMode:
                self.usersList.loadAllActiveUsers(self.loggedUser["id"])

            elif self.mode == AllCallHelpersMode:
                self.usersList.loadCallHelpers(self.callId, self.loggedUser["id"])

            elif self.mode == UsersTransferCallMode:
                self.usersList.loadTransferCallUsers(self.loggedUser["id"])

        except DatabaseConnectionError as error:
            place, cause = error.args

            message = "Falha em: " + place + "\nErro: " +cause
            
            messageBox = QMessageBox()
            messageBox.setText(message)
            messageBox.setWindowTitle("Erro!")
            messageBox.setIcon(QMessageBox.Critical)
            messageBox.setWindowIcon(QIcon(":/warning_icon.png"))
            messageBox.exec_()
            self.done(0)
            return
        
        
        self.userComboBox.addItem("", -1)
        
        for row, user in enumerate(self.usersList):
            self.userComboBox.addItem(user.userName, user.userId)


###############################################################################################################################################################################
   
    def confirmSelectedUser(self):
        """
        This method is called when the button "Confirmar" is clicked.
        It returns the selected user if there is any user selected, or raise an exception
        asking to the user to select an user
        """
        try:
            if self.userComboBox.itemData(self.userComboBox.currentIndex()) < 0:
                raise EmptyFieldsError("Usuário", "Selecione um usuário.")
            
        except EmptyFieldsError as error:
            field, message = error.args
            messageBox = QMessageBox()
            messageBox.setText(message)
            messageBox.setWindowTitle("Atenção!")
            messageBox.setIcon(QMessageBox.Warning)
            messageBox.setWindowIcon(QIcon(":/warning_icon.png"))
            messageBox.exec_()
            return
        # --> If the confirmation option is True #
        if self.confirmation:
            messageBox = QMessageBox()
            messageBox.setIcon(QMessageBox.Question)
            messageBox.setWindowIcon(QIcon(":/question.png"))
            messageBox.setWindowTitle(" ")
            messageBox.setText(self.confirmationMessage)
            messageBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            messageBox.button(QMessageBox.Yes).setText("Sim")
            messageBox.button(QMessageBox.No).setText("Não")
            
            messageBox.exec_()
            
            # --> If the Yes button was clicked #
            if messageBox.clickedButton() == messageBox.button(QMessageBox.Yes):
                self.done(self.userComboBox.itemData(self.userComboBox.currentIndex()))
            else:
                return

        else:
            self.done(self.userComboBox.itemData(self.userComboBox.currentIndex()))


###############################################################################################################################################################################

    def cancelSelectUser(self):
        """
        This method is called when the button "Cancelar" is clicked.
        It returns 0, signating to the parent dialog that it was closed without selection
        """
        self.done(0)


###############################################################################################################################################################################

    def reject(self):
        self.done(0)
    
