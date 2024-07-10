import sys


from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from myExceptions import *

__version__ = "1.0.0"

import inputscontainer

class ListInputsWindow(QMdiSubWindow):
    """
    This class is responsible for rendering the "Listar Chamados" window
    as a MDI sub Window and for managing the data inside it
    """
    #constant id, used for location inside the openedSubWindows dictionary in the
    #main window
    SUBWINDOWID = "listinputswindow"
    
    def __init__(self, parent=None):
        super(ListInputsWindow, self).__init__(parent)
        self.parent = parent
        #self.loggedUser = parent.loggedUser
        self.setAttribute(Qt.WA_DeleteOnClose)
        
        #build the "Lista Insumos" window

        #Button New Input
        self.newInputButton = QPushButton(" Novo Insumo ")

        self.editInputButton = QPushButton(" Editar Insumo ")
        self.editInputButton.setEnabled(False)

        
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.newInputButton)
        button_layout.addWidget(self.editInputButton)
        button_layout.addStretch(1)

        boldFont = QFont()
        boldFont.setBold(True)

        regularFont = QFont()
        regularFont.setBold(False)

        filterGroupBox = QGroupBox("Filtro")
        filterGroupBox.setFont(boldFont)
        

        #Description
        descriptionLabel = QLabel("Descrição:")
        descriptionLabel.setFixedWidth(110)
        descriptionLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        self.filterDescriptionField = QLineEdit()
        self.filterDescriptionField.setFixedWidth(190)
        self.filterDescriptionField.setFont(regularFont)

        #Position
        positionLabel = QLabel("Posição: ")
        positionLabel.setFixedWidth(110)
        positionLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.filterPositionField = QLineEdit()
        self.filterPositionField.setFixedWidth(190)
        self.filterPositionField.setFont(regularFont)

        #Category
        categoryLabel = QLabel("Categoria: ")
        categoryLabel.setFixedWidth(110)
        categoryLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.categoryComboBox = QComboBox()
        self.categoryComboBox.setMinimumContentsLength(23)

        #Com saldo
        self.quantityCheckBox = QCheckBox("Insumos Sem Saldo")
        self.quantityCheckBox.setMinimumWidth(200)

        #Part Number
        partNumberLabel = QLabel("Part Number:")
        partNumberLabel.setFixedWidth(110)
        partNumberLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.filterPNField = QLineEdit()
        self.filterPNField.setFixedWidth(190)
        self.filterPNField.setFont(regularFont)

        # SAP
        sapLabel = QLabel("SAP: ")
        sapLabel.setFixedWidth(110)
        sapLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.filterSapField = QLineEdit()
        self.filterSapField.setFixedWidth(190)
        self.filterSapField.setFont(regularFont)
        
                
        clearFilterButton = QPushButton(" Limpar ")
        clearFilterButton.setMinimumWidth(98)
        clearFilterButton.setFont(regularFont)
        
        filterButton = QPushButton(" Filtrar ")
        filterButton.setMinimumWidth(98)
        filterButton.setFont(regularFont)


        firstRowFilterLayout = QHBoxLayout()
        firstRowFilterLayout.addWidget(descriptionLabel)
        firstRowFilterLayout.addWidget(self.filterDescriptionField)
        firstRowFilterLayout.addWidget(positionLabel)
        firstRowFilterLayout.addWidget(self.filterPositionField)
        firstRowFilterLayout.addWidget(categoryLabel)
        firstRowFilterLayout.addWidget(self.categoryComboBox)
        firstRowFilterLayout.addSpacing(50)
        firstRowFilterLayout.addWidget(self.quantityCheckBox)
        firstRowFilterLayout.addStretch(1)

        secondRowFilterLayout = QHBoxLayout()
        secondRowFilterLayout.addWidget(partNumberLabel)
        secondRowFilterLayout.addWidget(self.filterPNField)
        secondRowFilterLayout.addWidget(sapLabel)
        secondRowFilterLayout.addWidget(self.filterSapField)
        secondRowFilterLayout.addStretch(1)
        secondRowFilterLayout.addWidget(clearFilterButton)
        secondRowFilterLayout.addWidget(filterButton)


        filterLayout = QVBoxLayout()
        filterLayout.addLayout(firstRowFilterLayout)
        filterLayout.addLayout(secondRowFilterLayout)
                
        filterGroupBox.setLayout(filterLayout)

        #######################################################
        #####Table having all the inputs of the inventory #####
        #######################################################
        self.inventoryTable = QTableWidget()
        self.inventoryTable.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.inventoryTable.setAlternatingRowColors(True)
        self.inventoryTable.setAutoFillBackground(True)
        self.inventoryTable.setMinimumSize(QSize(1300, 330))
        self.inventoryTable.setEditTriggers(QTableWidget.NoEditTriggers)
        self.inventoryTable.setSelectionBehavior(QTableWidget.SelectRows)
        self.inventoryTable.setSelectionMode(QTableWidget.SingleSelection)
        self.inventoryTable.horizontalHeader().setStretchLastSection(True)
        self.inventoryTable.horizontalHeader().setHighlightSections(False)

        stylesheet = "::section{ " \
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
        
       
        
        #Create the Items for the headers
        self.inventoryTable.setColumnCount(7)

        position = QTableWidgetItem("Posição")
        position.setSizeHint(QSize(100, 0))

        sap = QTableWidgetItem("SAP")
        sap.setSizeHint(QSize(100, 0))

        description = QTableWidgetItem("Descrição do Insumo")
        description.setSizeHint(QSize(450, 0))
        
        category = QTableWidgetItem("Categoria")
        category.setSizeHint(QSize(155, 0))
        
        partNumber = QTableWidgetItem("Part Number")
        partNumber.setSizeHint(QSize(155, 0))
        
        minQuantity = QTableWidgetItem("Quantidade Mínima")
        minQuantity.setSizeHint(QSize(155, 0))
        
        quantity = QTableWidgetItem("Quantidade Atual")
    
        

        
        #set the Header Items
        self.inventoryTable.setHorizontalHeaderItem(0, position)
        self.inventoryTable.setHorizontalHeaderItem(1, sap)
        self.inventoryTable.setHorizontalHeaderItem(2, description)
        self.inventoryTable.setHorizontalHeaderItem(3, category)
        self.inventoryTable.setHorizontalHeaderItem(4, partNumber)
        self.inventoryTable.setHorizontalHeaderItem(5, minQuantity)
        self.inventoryTable.setHorizontalHeaderItem(6, quantity)


        
        self.inventoryTable.horizontalHeader().setStyleSheet(stylesheet)
        self.inventoryTable.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        
        #build the listCalls Subwindow
        
        layout = QVBoxLayout()
        layout.addLayout(button_layout)
        layout.addWidget(filterGroupBox)
        layout.addWidget(self.inventoryTable)
        layout.addStretch(1)

        #create the centralWidget of the QMdiSubWindow and set its layout
        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setWidget(centralWidget)       


        #load the subwindow data
        self.inventoryTable.resizeColumnsToContents()

        #creates a periodic event that will uplode the calls screen
        
        self.setWindowIcon(QIcon(":/inventory.png"))
        # self.updateSubWindowTitle()



    def verifyIfUserAnsweringCall(self):
        """
        This method verifies if there is any call being answered by the user, preventing him from
        opening another calls, opening directly the call that is being answered by the user
        """
        call = self.callsList.verifyAnyCallBeingAnswered(self.loggedUser['id'])
        if (call is not None) and (not self.userAnsweringCall):
            self.userAnsweringCall = True
            callWindow = callwindow.CallWindow(call, self)
            callWindow.setModal(True)

            callWindow.show()
            
            xPos = (self.parent.screenResolution['w'] - callWindow.width()) / 2
            yPos = (self.parent.screenResolution['h'] - callWindow.height()) / 2
            
            callWindow.move(xPos, yPos)
            callWindow.raise_()
            callWindow.activateWindow()
            
            
        
    def openAnswerCallWindow(self):
        """
        This method is called when a call is double clicked or the button "answer call" is clicked
        """
        call = self.currentRowCall()
        
        if not call.isLockedCall():
            callWindow = callwindow.CallWindow(call, self)
            callWindow.setModal(True)

            callWindow.show()
            
            xPos = (self.parent.screenResolution['w'] - callWindow.width()) / 2
            yPos = (self.parent.screenResolution['h'] - callWindow.height()) / 2
            
            callWindow.move(xPos, yPos)
            callWindow.raise_()
            callWindow.activateWindow()
            
        else:
            messageBox = QMessageBox()
            messageBox.setIcon(QMessageBox.Warning)
            messageBox.setWindowIcon(QIcon(":/warning_icon2.png"))
            messageBox.setWindowTitle("Atenção!")
            messageBox.setText("Este chamado está sendo visualizado por outro colaborador.")
            messageBox.exec_()

        
        
    def enableButtonAnswerCall(self):
        """
        This method is used to enable the button "Answer Call" if any call is selected
        """
        if len(self.openedCallsTable.selectedItems()):
            self.answerCallButton.setEnabled(True)
        else:
            self.answerCallButton.setEnabled(False)
        
        
    def updateOpenedCallsTable(self):
        """
        This method updates the table that has the opened calls
        """
        self.callsList.loadCalls()

        self.openedCallsTable.clearContents()
        self.openedCallsTable.setRowCount(len(self.callsList))
        self.updateSubWindowTitle()
        self.verifyIfUserAnsweringCall()
        self.updateIndicators()


        #QFont That determinates the apearance of the text in the table
        fontStyle = QFont()
        fontStyle.setBold(True)

        for row, call in enumerate(self.callsList):
            #Icone
            iconLabel = QLabel()



            if call.insidePlan:
                iconLabel.setPixmap(QIcon(":/red_icon.png").pixmap(QSize(30,30)))
                iconLabel.setToolTip("Produto está contido no plano de produção.")
            else:
                iconLabel.setPixmap(QIcon(":/yellow_icon.png").pixmap(QSize(30,30)))
                iconLabel.setToolTip("Produto NÃO está contido no plano de produção.")

            self.openedCallsTable.setCellWidget(row, 0, iconLabel)


            #Duração Total
            item = QTableWidgetItem(call.formatedTotalDuration)
            item.setData(Qt.UserRole, int(call.callId))
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            item.setFont(fontStyle)
            if call.totalDuration and call.totalDuration > 30:
                item.setForeground(Qt.red)
            elif call.totalDuration and call.totalDuration < 0:
                item.setForeground(Qt.blue)

            self.openedCallsTable.setItem(row, 1, item)

            #Duração Atendimento
            if call.status != "Aberto":
                item = QTableWidgetItem(call.formatedAnswerDuration)
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                item.setFont(fontStyle)
                if call.answerDuration and call.answerDuration > 30:
                    item.setForeground(Qt.red)
                self.openedCallsTable.setItem(row, 2, item)

            #Aberto por
            item = QTableWidgetItem(call.creator)
            self.openedCallsTable.setItem(row, 3, item)

            #Tipo de Chamado
            item = QTableWidgetItem(call.callType)
            self.openedCallsTable.setItem(row, 4, item)

            #Cliente
            item = QTableWidgetItem(call.client)
            self.openedCallsTable.setItem(row, 5, item)

            #Produto
            item = QTableWidgetItem(call.product)
            item.setSizeHint(QSize(100, 0))
            self.openedCallsTable.setItem(row, 6, item)

            #Status
            item = QTableWidgetItem(call.status)
            self.openedCallsTable.setItem(row, 7, item)

            #Suporte Responsável
            item = QTableWidgetItem(call.support)
            item.setSizeHint(QSize(160, 0))
            self.openedCallsTable.setItem(row, 8, item)

            #Descrição do Chamado
            item = QTableWidgetItem(call.description)
            self.openedCallsTable.setItem(row, 9, item)

        

    def updateSubWindowTitle(self):
        """
        This method is used to update the window title with the total number of opened calls
        """
        if len(self.callsList) != 1:
            self.setWindowTitle("Controle de Estoque - %d Insumos Listados" % len(self.callsList))
        else:
            self.setWindowTitle("Controle de Estoque - 1 Insumo Listado")



   
    def closeEvent(self, event):
        """
        This method remove its reference from its parent opened sub window list before being closed
        """
        del self.parent.openedSubWindows[self.SUBWINDOWID]
        self.close()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    listinputswindow = ListInputsWindow()
    listinputswindow.show()
    app.exec_()
