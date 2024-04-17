from PyQt5.QtCore import (
        Qt,
        QSize
    )

from PyQt5.QtGui import (
        QFont,
        QIcon,
        QBrush,
        QColor,
        QPalette,
        QCursor
    )

from PyQt5.QtWidgets import (
        QMdiSubWindow,
        QDialog,
        QLabel,
        QPushButton,
        QLineEdit,
        QLayout,
        QHBoxLayout,
        QVBoxLayout,
        QGridLayout,
        QWidget,
        QGroupBox,
        QListWidget,
        QListWidgetItem,
        QComboBox
    )

import qrc_resources
from magicDB import *
from myExceptions import *

import userscontainer
import clientscontainer

__version__ = "2.0.0"

###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################

class MyQPushButton(QPushButton):
    """
    This class reimplements the qpushbutton class
    """
    def __init__(self, icon=None, parent=None):
        super(MyQPushButton, self).__init__("", parent)

        self.setFixedSize(50, 50)
        self.setDisabled(True)
        self.setFocusPolicy(Qt.NoFocus)
        self.setCursor(QCursor(Qt.PointingHandCursor))

        if icon:
            self.setIcon(icon)


###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################


class ClientResponsibleWindow(QMdiSubWindow):

    # --> Constant id, used for location inside the openedSubWindows dictionary in the main window #
    SUBWINDOWID = "clientresponsiblewindow"

    def __init__(self, parent=None):
        super(ClientResponsibleWindow, self).__init__(parent)
        self.parent = parent        
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowFlags(Qt.SubWindow | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
        self.analystsList = userscontainer.UsersContainer()
        self.undefinedClients = clientscontainer.ClientsContainer()
        self.definedClients = clientscontainer.ClientsContainer()

        ###################################
        # --> Firstly build the interface #
        ###################################

        boldFont = QFont()
        boldFont.setBold(True)

        listPalette = QPalette()
        listPalette.setColor(QPalette.Inactive, QPalette.Highlight, listPalette.color(QPalette.Active, QPalette.Highlight))
        listPalette.setColor(QPalette.Inactive, QPalette.HighlightedText, listPalette.color(QPalette.Active, QPalette.HighlightedText))
        self.setPalette(listPalette)
        
        # --> Analist List #
        selectAnalystLabel = QLabel("Analista Responsável: ")
        selectAnalystLabel.setFont(boldFont)

        self.analystsComboBox = QComboBox()
        self.analystsComboBox.setMinimumWidth(200)

        self.populateAnalystsList()


        # --> Undefined clients List #
        undefinedClientGroupBox = QGroupBox("Clientes Disponíveis")
        undefinedClientGroupBox.setFont(boldFont)

        groupLayout = QGridLayout()
        
        self.undefinedClientsList = QListWidget()
        self.undefinedClientsList.setFixedSize(QSize(200, 350))
        self.undefinedClientsList.setPalette(listPalette)

        groupLayout.addWidget(self.undefinedClientsList)
        undefinedClientGroupBox.setLayout(groupLayout)

        # --> Buttons for the lists #
        self.selectButton = MyQPushButton(QIcon(":/right.png"))
        self.unselectButton = MyQPushButton(QIcon(":/left.png"))
        self.lockUnlockButton = MyQPushButton(QIcon(":/lock.png"))
        
        buttonsLayout = QVBoxLayout()
        buttonsLayout.addWidget(self.selectButton)
        buttonsLayout.addWidget(self.unselectButton)
        buttonsLayout.addWidget(self.lockUnlockButton)
        buttonsLayout.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

        # --> Defined clients List #
        selectedClientGroupBox = QGroupBox("Clientes Selecionados")
        selectedClientGroupBox.setFont(boldFont)

        groupLayout = QGridLayout()
        
        self.definedClientsList = QListWidget()
        self.definedClientsList.setFixedSize(QSize(200, 350))
        self.definedClientsList.setPalette(listPalette)

        groupLayout.addWidget(self.definedClientsList)
        selectedClientGroupBox.setLayout(groupLayout)

        # --> Close Button #
        self.closeButton = QPushButton("Fechar")
        self.closeButton.setFixedWidth(98)
        self.closeButton.setCursor(QCursor(Qt.PointingHandCursor))
        
  
        # --> Horizontal Layout First Row #
        analystLayout = QHBoxLayout()
        analystLayout.setAlignment(Qt.AlignLeft)
        analystLayout.addWidget(selectAnalystLabel)
        analystLayout.addWidget(self.analystsComboBox)
        analystLayout.addStretch(1)

        # --> Horizontal Layout Second Row #
        listsLayout = QHBoxLayout()
        listsLayout.addWidget(undefinedClientGroupBox)
        listsLayout.addLayout(buttonsLayout)
        listsLayout.addWidget(selectedClientGroupBox)

        # --> Horizontal Layout Third Row #
        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch(1)
        buttonLayout.addWidget(self.closeButton)
        buttonLayout.addStretch(1)

        # --> Vertical Layout #
        windowLayout = QVBoxLayout()
        windowLayout.addLayout(analystLayout)
        windowLayout.addLayout(listsLayout)
        windowLayout.addLayout(buttonLayout)


        # --> create the centralWidget of the QMdiSubWindow and set its layout #
        centralWidget = QWidget()
        centralWidget.setLayout(windowLayout)
        self.setWidget(centralWidget)     

        self.populateUndefinedClientList()


        # --> SIGNALS #
        self.selectButton.clicked.connect(self.selectClient)
        self.unselectButton.clicked.connect(self.unselectClient)
        
        self.lockUnlockButton.clicked.connect(self.lockOrUnlockClient)

        self.undefinedClientsList.itemClicked.connect(self.undefinedListClickVerification)
        self.definedClientsList.itemClicked.connect(self.definedListClickVerification)
        
        self.analystsComboBox.currentIndexChanged.connect(self.checkIfEnablesButton)
        self.closeButton.clicked.connect(self.closeWindow)

        self.setWindowTitle("Clientes e Analistas Responsáveis")
        self.setWindowIcon(QIcon(":/client.png"))

        # --> Line responsible for preventing window resize
        self.layout().setSizeConstraint(QLayout.SetFixedSize)
        
###############################################################################################################################################################################

    def closeWindow(self):
        self.close()
    

###############################################################################################################################################################################

    def undefinedListClickVerification(self, item):
        """
        This slot is called when the undefined clients list is clicked
        """
        self.lockUnlockButton.setDisabled(False)
        self.definedClientsList.setCurrentRow(-1)
        # --> PADLOCK CODE VERIFICATION #
        key = item.data(Qt.UserRole)
        client = self.undefinedClients.clientFromId(key)
        if client.clientActive:
            self.lockUnlockButton.setIcon(QIcon(":/lock.png"))
        else:
            self.lockUnlockButton.setIcon(QIcon(":/unlock.png"))
        
        currentAnalyst = self.analystsComboBox.itemData(self.analystsComboBox.currentIndex())
        if currentAnalyst < 0:
            return
        
        self.definedClientsList.setCurrentRow(-1)
        self.unselectButton.setDisabled(True)
        self.selectButton.setDisabled(False)

        
###############################################################################################################################################################################

    def definedListClickVerification(self, item):
        """
        This slot is called when the defined clients list is clicked
        """
        self.lockUnlockButton.setDisabled(False)
        self.undefinedClientsList.setCurrentRow(-1)
        # --> if no analyst was selected ignore
        currentAnalyst = self.analystsComboBox.itemData(self.analystsComboBox.currentIndex())
        if currentAnalyst < 0:
            return
                
        self.undefinedClientsList.setCurrentRow(-1)
        self.selectButton.setDisabled(True)
        self.unselectButton.setDisabled(False)

        # --> PADLOCK CODE VERIFICATION #
        key = item.data(Qt.UserRole)
        client = self.definedClients.clientFromId(key)
        if client.clientActive:
            self.lockUnlockButton.setIcon(QIcon(":/lock.png"))
        else:
            self.lockUnlockButton.setIcon(QIcon(":/unlock.png"))

###############################################################################################################################################################################

    def lockOrUnlockClient(self):
        lockedBrush = QBrush()
        lockedBrush.setColor(QColor(130, 130, 130))
        
        unlockedBrush = QBrush()
        unlockedBrush.setColor(QColor(0, 0, 0))
        
        rowUndefinedClient = self.undefinedClientsList.currentRow()
        rowDefinedClient = self.definedClientsList.currentRow()

        if rowUndefinedClient > -1 or rowDefinedClient > -1:
            if rowUndefinedClient > -1:
                item = self.undefinedClientsList.item(rowUndefinedClient)
                key = item.data(Qt.UserRole)
                client = self.undefinedClients.clientFromId(key)
            else:
                item = self.definedClientsList.item(rowDefinedClient)
                key = item.data(Qt.UserRole)
                client = self.definedClients.clientFromId(key)
            
            if client.clientActive:
                self.lockUnlockButton.setIcon(QIcon(":/unlock.png"))
                item.setForeground(lockedBrush)
                try:
                    client.setActive(False)

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

            else:
                self.lockUnlockButton.setIcon(QIcon(":/lock.png"))
                item.setForeground(unlockedBrush)
                try:
                    client.setActive(True)

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
            

###############################################################################################################################################################################

    def checkIfEnablesButton(self):
        """
        This slot is called when the analyst is changed
        """
        currentAnalyst = self.analystsComboBox.itemData(self.analystsComboBox.currentIndex())
        if currentAnalyst < 0:
            self.definedClientsList.clear()
            self.selectButton.setDisabled(True)
            self.unselectButton.setDisabled(True)
            return

        self.populateUndefinedClientList()
        self.populateDefinedClientList(currentAnalyst)

        undefinedClientRow = self.undefinedClientsList.currentRow()
        definedClientRow = self.definedClientsList.currentRow()
        
        if undefinedClientRow > -1:
            self.selectButton.setDisabled(False)
            self.unselectButton.setDisabled(True)
            self.lockUnlockButton.setDisabled(False)
            self.definedClientsList.setCurrentRow(-1)

            item = self.undefinedClientsList.item(undefinedClientRow)
            key = item.data(Qt.UserRole)
            client = self.undefinedClients.clientFromId(key)
            if client.clientActive:
                self.lockUnlockButton.setIcon(QIcon(":/lock.png"))
            else:
                self.lockUnlockButton.setIcon(QIcon(":/unlock.png"))  

            
        elif definedClientRow > -1:
            self.selectButton.setDisabled(True)
            self.unselectButton.setDisabled(False)
            self.lockUnlockButton.setDisabled(False)
            self.undefinedClientsList.setCurrentRow(-1)
            
            item = self.definedClientsList.item(definedClientRow)
            key = item.data(Qt.UserRole)
            client = self.definedClients.clientFromId(key)
            if client.clientActive:
                self.lockUnlockButton.setIcon(QIcon(":/lock.png"))
            else:
                self.lockUnlockButton.setIcon(QIcon(":/unlock.png"))  
            
        else:
            self.selectButton.setDisabled(True)
            self.unselectButton.setDisabled(True)
            self.lockUnlockButton.setDisabled(True)


###############################################################################################################################################################################

    def unselectClient(self):
        row = self.definedClientsList.currentRow()
        if row > -1:
            item = self.definedClientsList.takeItem(row)
            key = item.data(Qt.UserRole)
            client = self.definedClients.clientFromId(key)

            try:
                client.unsetAnalyst()
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
            
            self.undefinedClients.add(client)
            self.undefinedClientsList.addItem(item)
            self.undefinedClientsList.sortItems()

            # --> interface management #
            self.definedClientsList.setCurrentRow(-1)
            self.undefinedClientsList.setCurrentRow(-1)
            self.unselectButton.clearFocus()
            self.selectButton.clearFocus()
            self.unselectButton.setDisabled(True)
            self.lockUnlockButton.setDisabled(True)

###############################################################################################################################################################################

    def selectClient(self):
        currentAnalyst = self.analystsComboBox.itemData(self.analystsComboBox.currentIndex())
                
        row = self.undefinedClientsList.currentRow()
        if row > -1:
                        
            item = self.undefinedClientsList.takeItem(row)
            key = item.data(Qt.UserRole)
            client = self.undefinedClients.clientFromId(key)

            try:
                client.setAnalyst(currentAnalyst)
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
            
            self.definedClients.add(client)
            
            self.undefinedClients.removeClient(key, client)

            self.definedClientsList.addItem(item)
            self.definedClientsList.sortItems()

            
            # --> interface management #
            self.undefinedClientsList.setCurrentRow(-1)
            self.definedClientsList.setCurrentRow(-1)
            self.selectButton.clearFocus()
            self.unselectButton.clearFocus()
            self.selectButton.setDisabled(True)
            self.lockUnlockButton.setDisabled(True)

           
###############################################################################################################################################################################


    def populateDefinedClientList(self, analystId):
        """
        This method is used to load the list of clients from a specific analyst       
        """
        lockedBrush = QBrush()
        lockedBrush.setColor(QColor(130, 130, 130))
        
        unlockedBrush = QBrush()
        unlockedBrush.setColor(QColor(0, 0, 0))
        
        self.definedClientsList.clear()
        
        regularFont = QFont()
        regularFont.setBold(False)

        try:
            self.definedClients.loadClientsFromAnalyst(analystId)
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

        for client in self.definedClients:
            item = QListWidgetItem(client.clientName)
            item.setData(Qt.UserRole, client.clientId)
            item.setFont(regularFont)
            if client.clientActive == 1:
                item.setForeground(unlockedBrush)
            else:
                item.setForeground(lockedBrush)
            self.definedClientsList.addItem(item)
        
        
###############################################################################################################################################################################

    def populateUndefinedClientList(self):
        """
        This method is used to load the list of clients without analyst       
        """

        lockedBrush = QBrush()
        lockedBrush.setColor(QColor(130, 130, 130))
        
        unlockedBrush = QBrush()
        unlockedBrush.setColor(QColor(0, 0, 0))

        self.undefinedClientsList.clear()
        
        regularFont = QFont()
        regularFont.setBold(False)

        try:
            self.undefinedClients.loadClientsWithoutAnalyst()
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

        for client in self.undefinedClients:
            item = QListWidgetItem(client.clientName)
            item.setData(Qt.UserRole, client.clientId)
            item.setFont(regularFont)
            if client.clientActive == 1:
                item.setForeground(unlockedBrush)
            else:
                item.setForeground(lockedBrush)
            self.undefinedClientsList.addItem(item)
            

###############################################################################################################################################################################

    def populateAnalystsList(self):
        try:
            self.analystsList.loadAnalystsUsers()
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

        self.analystsComboBox.addItem("", -1)
        
        for row, user in enumerate(self.analystsList):
            self.analystsComboBox.addItem(user.userName, user.userId)
        
###############################################################################################################################################################################


    def closeEvent(self, event):
        """
        This method remove its reference from its parent opened sub window list before being closed
        """
        del self.parent.openedSubWindows[self.SUBWINDOWID]
        self.close()
