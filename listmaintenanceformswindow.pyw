from PyQt5.QtCore import (
    Qt,
    QSize
    )

from PyQt5.QtGui import (
    QFont,
    QPalette
    )

from PyQt5.QtWidgets import (
    QMdiSubWindow,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QHBoxLayout,    
    QAbstractScrollArea,
    QHeaderView,
    QWidget
    )

from myExceptions import *

import maintenanceformscontainer
import editmaintenanceformwindow
import createmaintenanceformwindow


__version__ = "2.0.0"

###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################

class MyQPushButton(QPushButton):
    """MyQLineEdit
    This class reimplements the QPushButton
    """
    def __init__(self, text="", parent=None):
        super(MyQPushButton, self).__init__(text, parent)

        regularFont = QFont()
        regularFont.setBold(False)
        self.setFont(regularFont)

        self.setCursor(Qt.PointingHandCursor)
        
        self.setFixedWidth(135)


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
        self.setMinimumSize(QSize(600, 300))
        self.setEditTriggers(QTableWidget.NoEditTriggers)
        self.setSelectionBehavior(QTableWidget.SelectRows)
        self.setSelectionMode(QTableWidget.SingleSelection)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setHighlightSections(False)

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

        # --> create theitems for the headers #
        self.setColumnCount(3)

        formDescription = QTableWidgetItem("Descrição")
        formLastModificationDate = QTableWidgetItem("Última Modificação")
        formModifier = QTableWidgetItem("Modificado Por")
        
        # --> Set the Header Items #
        self.setHorizontalHeaderItem(0, formDescription)
        self.setHorizontalHeaderItem(1, formLastModificationDate)
        self.setHorizontalHeaderItem(2, formModifier)


        self.horizontalHeader().resizeSection(0, 250)
        self.horizontalHeader().resizeSection(1, 150)
        self.horizontalHeader().resizeSection(2, 150)
    
        self.horizontalHeader().setStyleSheet(tableStylesheet)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)



###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################

class ListMaintenanceFormsWindow(QMdiSubWindow):
    """
    This class is responsible for rendering the "Listar Formularios de Manutenção" window
    as a MDI sub Window and for managing the data inside it
    """
    # --> constant id, used for location inside the openedSubWindows dictionary in the main window #
    SUBWINDOWID = "listmaintenanceformswindow"

    def __init__(self, parent=None):
        super(ListMaintenanceFormsWindow, self).__init__(parent)
        self.parent = parent
        self.loggedUser = parent.loggedUser
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowFlags(Qt.SubWindow | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)

        self.maintenanceFormsList = maintenanceformscontainer.MaintenanceFormsContainer()
        

        ######################
        #### LAYOUT BUILD ####
        ######################

        self.newFormButton = MyQPushButton("Cadastrar Formulário")
        self.editFormButton = MyQPushButton("Editar Formulário")
        self.editFormButton.setEnabled(False)
        self.copyFormButton = MyQPushButton("Criar Cópia de Formulário")
        self.copyFormButton.setEnabled(False)

        buttonsLayout = QHBoxLayout()
        buttonsLayout.addWidget(self.newFormButton)
        buttonsLayout.addWidget(self.editFormButton)
        buttonsLayout.addWidget(self.copyFormButton)
        buttonsLayout.addStretch(1)
        

        self.formsTable = MyQTableWidget()

        windowLayout = QVBoxLayout()
        windowLayout.addLayout(buttonsLayout)
        windowLayout.addWidget(self.formsTable)

        centralWidget = QWidget()
        centralWidget.setLayout(windowLayout)
        self.setWidget(centralWidget)
        #self.setWindowIcon(QIcon(":/scanner.png"))
        self.setWindowFlags(Qt.Window | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)

        self.setWindowTitle("Formulários de Manutenção")

        self.updateFormTable()

        ###########################
        #### SIGNALS AND SLOTS ####
        ###########################

        self.formsTable.itemDoubleClicked.connect(self.openEditMaintenanceFormWindow)
        self.formsTable.itemSelectionChanged.connect(self.enableButtonEditForm)
        self.editFormButton.clicked.connect(self.openEditMaintenanceFormWindow)
        self.newFormButton.clicked.connect(self.openCreateMaintenanceFormWindow)
        self.copyFormButton.clicked.connect(self.openCopyMaintenanceFormWindow)


###############################################################################################################################################################################

    def enableButtonEditForm(self):
        """
        This method is used to enable the button "Editar Formulário" if any form is selected
        """
        if len(self.formsTable.selectedItems()):
            self.editFormButton.setEnabled(True)
            self.copyFormButton.setEnabled(True)
        else:
            self.editFormButton.setEnabled(False)
            self.copyFormButton.setEnabled(False)


###############################################################################################################################################################################

    def currentRowMaintenanceForm(self):
        """
        This method returns the current selected row
        """
        row = self.formsTable.currentRow()
        if row > -1:
            item = self.formsTable.item(row, 0)
            key = item.data(Qt.UserRole)
            return self.maintenanceFormsList.maintenanceFormFromId(key)

        return None

###############################################################################################################################################################################
    def openCopyMaintenanceFormWindow(self):
        """
        This method is called when the button "Cadastrar Formulário" is clicked
        """
        maintenanceForm = self.currentRowMaintenanceForm()
        
        createMaintenanceFormWindow = createmaintenanceformwindow.CreateMaintenanceFormWindow(maintenanceForm, self)
        createMaintenanceFormWindow.setModal(True)

        createMaintenanceFormWindow.show()
          
        xPos = (self.parent.screenResolution['w'] - createMaintenanceFormWindow.width()) / 2
        yPos = (self.parent.screenResolution['h'] - createMaintenanceFormWindow.height()) / 2
            
        createMaintenanceFormWindow.move(xPos, yPos)
        createMaintenanceFormWindow.raise_()
        createMaintenanceFormWindow.activateWindow()

###############################################################################################################################################################################
    

    def openCreateMaintenanceFormWindow(self):
        """
        This method is called when the button "Cadastrar Formulário" is clicked
        """
        
        createMaintenanceFormWindow = createmaintenanceformwindow.CreateMaintenanceFormWindow(None, self)
        createMaintenanceFormWindow.setModal(True)

        createMaintenanceFormWindow.show()
          
        xPos = (self.parent.screenResolution['w'] - createMaintenanceFormWindow.width()) / 2
        yPos = (self.parent.screenResolution['h'] - createMaintenanceFormWindow.height()) / 2
            
        createMaintenanceFormWindow.move(xPos, yPos)
        createMaintenanceFormWindow.raise_()
        createMaintenanceFormWindow.activateWindow()

        

###############################################################################################################################################################################


    def openEditMaintenanceFormWindow(self):
        """
        This method is called when a form is double clicked or the button "Editar Formulário" is clicked
        """
        maintenanceForm = self.currentRowMaintenanceForm()
        
        editMaintenanceFormWindow = editmaintenanceformwindow.EditMaintenanceFormWindow(maintenanceForm, self)
        editMaintenanceFormWindow.setModal(True)

        editMaintenanceFormWindow.show()
          
        xPos = (self.parent.screenResolution['w'] - editMaintenanceFormWindow.width()) / 2
        yPos = (self.parent.screenResolution['h'] - editMaintenanceFormWindow.height()) / 2
            
        editMaintenanceFormWindow.move(xPos, yPos)
        editMaintenanceFormWindow.raise_()
        editMaintenanceFormWindow.activateWindow()
        

###############################################################################################################################################################################
    def updateFormTable(self):
        """
        This method loads the invoices to the table using the data in the fields to filter the result
        """
        self.editFormButton.setEnabled(False)
        try:
            self.maintenanceFormsList.loadMaintenanceForms()
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


        self.formsTable.clearContents()
        self.formsTable.setRowCount(len(self.maintenanceFormsList))
        
        # --> QFont That determinates the apearance of the text in the table #
        fontStyle = QFont()
        fontStyle.setBold(True)

        for row, maintenanceForm in enumerate(self.maintenanceFormsList):

           # --> Identificação do Dispositivo #
            item = QTableWidgetItem(maintenanceForm.formDescription)
            item.setData(Qt.UserRole, int(maintenanceForm.formId))
            self.formsTable.setItem(row, 0, item)

            # --> Descrição #
            item = QTableWidgetItem(maintenanceForm.formLastModification)
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.formsTable.setItem(row, 1, item)

            # --> Código SAP #
            item = QTableWidgetItem(str(maintenanceForm.formModifier))
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.formsTable.setItem(row, 2, item)

###############################################################################################################################################################################

    def closeEvent(self, event):
        """
        This method remove its reference from its parent opened sub window list before being closed
        """
        del self.parent.openedSubWindows[self.SUBWINDOWID]
        self.close()
