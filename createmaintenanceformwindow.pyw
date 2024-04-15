from PyQt5.QtCore import (
    Qt,
    QSize,
    QEvent
    )

from PyQt5.QtGui import (
    QFont,
    QCursor,
    QTextCharFormat,
    QIcon
    )

from PyQt5.QtWidgets import (
    QWidget,
    QScrollArea,
    QPlainTextEdit,
    QDialog,
    QLabel,
    QPushButton,
    QLayout,
    QHBoxLayout,
    QGridLayout,
    QVBoxLayout,
    QMessageBox,
    QGroupBox,
    QLineEdit,
    QFrame,
    QSizePolicy
    )
from time import sleep
import qrc_resources
import maintenanceformscontainer

from myExceptions import *

__version__ = "2.0.0"

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

        self.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.setMinimumWidth(80)

###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################

class MyQPushButton(QPushButton):
    """
    This class reimplements the qpushbutton class
    """
    def __init__(self, text="", parent=None):
        super(MyQPushButton, self).__init__(text, parent)

        self.setFixedWidth(100)
        self.setCursor(QCursor(Qt.PointingHandCursor))


###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################

class MyQDeletePushButton(QPushButton):
    """
    This class reimplements the qpushbutton class
    """
    def __init__(self, text="", parent=None, itemsLayout=None, windowPointer=None):
        super(MyQDeletePushButton, self).__init__(text, parent)

        self.parent = parent
        self.itemsLayout = itemsLayout
        self.windowPointer = windowPointer

        self.setFixedWidth(35)
        self.setIcon(QIcon(":/delete.png"))
        self.setCursor(QCursor(Qt.PointingHandCursor))

        self.clicked.connect(self.deleteFormItem)

    def deleteFormItem(self):
        self.itemsLayout.itemAt(self.parent.itemPosition).widget().deleteLater()
        self.itemsLayout.itemAt(self.parent.itemPosition).widget().setParent(None)

        for i in range(self.parent.itemPosition, self.itemsLayout.count()):
            self.itemsLayout.itemAt(i).widget().itemPosition = i
        #elf.itemsLayout.removeItem(item)
        self.windowPointer.reloadSizeButton.animateClick(10)
        
        
        if self.itemsLayout.count():
            # --> disable button from the first frame
            self.itemsLayout.itemAt(0).widget().layout().itemAt(2).widget().setEnabled(False)

            # --> disable button from the last frame
            self.itemsLayout.itemAt((self.itemsLayout.count() - 1)).widget().layout().itemAt(3).widget().setEnabled(False)

###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################

class MyQEditPushButton(QPushButton):
    """
    This class reimplements the qpushbutton class
    """
    def __init__(self, text="", parent=None, dialogPointer=None):
        super(MyQEditPushButton, self).__init__(text, parent)

        self.parent = parent
        self.dialogWindow = dialogPointer

        self.setFixedWidth(35)
        self.setIcon(QIcon(":/edit.png"))
        self.setCursor(QCursor(Qt.PointingHandCursor))

        self.clicked.connect(self.editFormItem)

    def editFormItem(self):
        #print(self.parent.itemPosition)
        text = self.parent.layout().itemAt(0).widget().text()
        self.dialogWindow.newItemField.setPlainText(text)
        self.dialogWindow.calculateCharacters()

        self.dialogWindow.addNewItemButton.setVisible(False)
        self.dialogWindow.changeItemButton.setVisible(True)
        self.dialogWindow.cancelItemChangeButton.setVisible(True)

        self.dialogWindow.editingItemPosition = self.parent.itemPosition
        

###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################

class MyQUpPushButton(QPushButton):
    """
    This class reimplements the qpushbutton class
    """
    def __init__(self, text="", parent=None, itemsLayout=None):
        super(MyQUpPushButton, self).__init__(text, parent)
        self.parent = parent
        self.itemsLayout = itemsLayout

        self.setFixedWidth(35)
        self.setIcon(QIcon(":/up.png"))
        self.setCursor(QCursor(Qt.PointingHandCursor))

        self.clicked.connect(self.moveItemUp)

    def moveItemUp(self):
        actualPosition = self.parent.itemPosition
        nextPosition = self.parent.itemPosition - 1

        self.itemsLayout.itemAt(nextPosition).widget().itemPosition = actualPosition

        self.itemsLayout.removeWidget(self.parent)
        self.itemsLayout.insertWidget(nextPosition, self.parent)
        self.parent.itemPosition = nextPosition

        # --> set enabled the button up
        self.parent.layout().itemAt(3).widget().setEnabled(True)

        # --> set enabled the next down button
        self.itemsLayout.itemAt(actualPosition).widget().layout().itemAt(2).widget().setEnabled(True)    

        # --> disable button from the first frame
        self.itemsLayout.itemAt(0).widget().layout().itemAt(2).widget().setEnabled(False)

        # --> disable button from the last frame
        self.itemsLayout.itemAt((self.itemsLayout.count() - 1)).widget().layout().itemAt(3).widget().setEnabled(False)


###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################

class MyQDownPushButton(QPushButton):
    """
    This class reimplements the qpushbutton class
    """
    def __init__(self, text="", parent=None, itemsLayout=None):
        super(MyQDownPushButton, self).__init__(text, parent)
        self.parent = parent
        self.itemsLayout = itemsLayout

        self.setFixedWidth(35)
        self.setIcon(QIcon(":/down.png"))
        self.setCursor(QCursor(Qt.PointingHandCursor))

        self.clicked.connect(self.moveItemDown)

    def moveItemDown(self):
        actualPosition = self.parent.itemPosition
        nextPosition = self.parent.itemPosition + 1

       
        self.itemsLayout.itemAt(nextPosition).widget().itemPosition = actualPosition

        self.itemsLayout.removeWidget(self.parent)
        self.itemsLayout.insertWidget(nextPosition, self.parent)
        self.parent.itemPosition = nextPosition

        # --> set enabled the button up
        self.parent.layout().itemAt(2).widget().setEnabled(True)

        # --> set enabled the next down button
        self.itemsLayout.itemAt(actualPosition).widget().layout().itemAt(3).widget().setEnabled(True)    

        # --> disable button from the first frame
        self.itemsLayout.itemAt(0).widget().layout().itemAt(2).widget().setEnabled(False)

        # --> disable button from the last frame
        self.itemsLayout.itemAt((self.itemsLayout.count() - 1)).widget().layout().itemAt(3).widget().setEnabled(False)
        
        

###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################


class MyQLineEdit(QLineEdit):
    """
    This class reimplements qlineedit class
    """
    def __init__(self, parent=None):
        super(MyQLineEdit, self).__init__(parent)

        regularFont = QFont()
        regularFont.setBold(False)
        regularFont.setCapitalization(QFont.AllUppercase)
        
        self.setFont(regularFont)
        self.setFixedWidth(100)

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
    
    def enterEvent(self, event):
        self.setFrameStyle(QFrame.Panel | QFrame.Sunken)

    def leaveEvent(self, event):
        self.setFrameStyle(QFrame.Panel | QFrame.Raised)


###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################


class CreateMaintenanceFormWindow(QDialog):
    """
    This class is responsible for rendering the call window modally.
    If the call is being answered by another user it only will load just the 
    """
    
    def __init__(self, maintenanceForm=None, parent=None):
        super(CreateMaintenanceFormWindow, self).__init__(parent)
        self.parent = parent
        self.editingItemPosition = -1

        self.maintenanceForm = maintenanceForm

        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setFixedSize(QSize(655, 475))

        # --> Groupbox Title #
        boldFont = QFont()
        boldFont.setBold(True)
   

        ######################
        #### LAYOUT BUILD ####
        ######################

        formDescriptionLabel = MyQLabel("Descrição: ")

        self.formDescriptionField = MyQLineEdit()
        self.formDescriptionField.setMinimumWidth(540)

       
        newItemLabel = MyQLabel("Novo Item: ")
        newItemLabelLayout = QVBoxLayout()
        newItemLabelLayout.addWidget(newItemLabel)
        newItemLabelLayout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        
        
        self.newItemField = QPlainTextEdit()
        self.newItemField.setFixedSize(QSize(435, 75))
        self.textFormat = QTextCharFormat()
        self.textFormat.setFontCapitalization(QFont.AllUppercase)
        self.newItemField.setCurrentCharFormat(self.textFormat)

        self.addNewItemButton = MyQPushButton(" Adicionar ")
        
        self.changeItemButton = MyQPushButton(" Alterar ")
        self.changeItemButton.setVisible(False)

        self.cancelItemChangeButton = MyQPushButton(" Cancelar ")
        self.cancelItemChangeButton.setVisible(False)

        
        self.charCounter = QLabel("255")
        self.charCounter.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.charCounter.setStyleSheet('color: red')
        self.charCounter.setFont(boldFont)

        
        addNewItemButtonLayout = QVBoxLayout()
        addNewItemButtonLayout.addWidget(self.addNewItemButton)
        addNewItemButtonLayout.addWidget(self.changeItemButton)
        addNewItemButtonLayout.addWidget(self.cancelItemChangeButton)
        addNewItemButtonLayout.addStretch(1)
        addNewItemButtonLayout.addWidget(self.charCounter)
        
        #--> Form Items Groupbox
        formItemsGroupBox = QGroupBox("Items do Formulário: ")
        formItemsGroupBox.setFont(boldFont)
        formItemsGroupBox.setMinimumHeight(310)
       

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
        
        formItemsGroupBox.setLayout(formItemsGBLayout)
        
        #--> Buttons
        self.saveButton = MyQPushButton(" Salvar ")
        self.cancelButton = MyQPushButton(" Cancelar ")

        self.reloadSizeButton = MyQPushButton("Resize")

        self.firstLineLayout = QHBoxLayout()
        self.firstLineLayout.addWidget(formDescriptionLabel)
        self.firstLineLayout.addWidget(self.formDescriptionField)

        self.secondLineLayout = QHBoxLayout()
        self.secondLineLayout.addLayout(newItemLabelLayout)
        self.secondLineLayout.addWidget(self.newItemField)
        self.secondLineLayout.addLayout(addNewItemButtonLayout)

        self.buttonsLayout = QHBoxLayout()
        self.buttonsLayout.addStretch(1)
        self.buttonsLayout.addWidget(self.saveButton)
        self.buttonsLayout.addWidget(self.cancelButton)
        self.buttonsLayout.addStretch(1)
        
        self.windowLayout = QVBoxLayout()
        self.windowLayout.addLayout(self.firstLineLayout)
        self.windowLayout.addLayout(self.secondLineLayout)
        self.windowLayout.addWidget(formItemsGroupBox)
        self.windowLayout.addLayout(self.buttonsLayout)
        
        self.setLayout(self.windowLayout)

        if not maintenanceForm:
            self.setWindowTitle("Cadastro de Novo Formulário")
        else:
            self.setWindowTitle("Criar Cópia de Formulário")
            self.loadFormData()
        
       
        ###########################
        #### SIGNALS AND SLOTS ####
        ###########################
        self.cancelButton.clicked.connect(self.close)
        self.newItemField.textChanged.connect(self.calculateCharacters)
        self.changeItemButton.clicked.connect(self.changeItemText)
        self.cancelItemChangeButton.clicked.connect(self.cancelItemEdition)
        self.addNewItemButton.clicked.connect(self.addNewItemToList)
        self.saveButton.clicked.connect(self.saveForm)
        self.reloadSizeButton.clicked.connect(self.reloadItemLayoutSize)


###############################################################################################################################################################################

    def loadFormData(self):
        self.formDescriptionField.setText(self.maintenanceForm.formDescription)
        self.maintenanceForm.formItemsList.loadItemsFromMaintenanceForm()

        for item in self.maintenanceForm.formItemsList:
            self.insertItemToList(item.itemDescription)            

###############################################################################################################################################################################

    def insertItemToList(self, text):

        boldFont = QFont()
        boldFont.setBold(False)

        formItemFrame = MyQFrame(None, self.formItemsListLayout.count())
                
        formItemLayout = QHBoxLayout()

        itemDescription = QLabel(text.upper())
        itemDescription.setFixedSize(QSize(390, 65))
        itemDescription.setWordWrap(True)
        itemDescription.setFont(boldFont)

        # --> Up Button            
        moveUpButton = MyQUpPushButton(text="", parent=formItemFrame, itemsLayout=self.formItemsListLayout)

                    
        # --> Down Button
        moveDownButton = MyQDownPushButton(text="", parent=formItemFrame, itemsLayout=self.formItemsListLayout)
        #moveDownButton.setEnabled(False)

        # --> Edit Button
        editItemButton = MyQEditPushButton(text="", parent=formItemFrame, dialogPointer=self)

        removeItemButton = MyQDeletePushButton(text="", parent=formItemFrame, itemsLayout=self.formItemsListLayout, windowPointer=self)
                  
        formItemLayout.addWidget(itemDescription)
        formItemLayout.addStretch(1)
        formItemLayout.addWidget(moveUpButton)
        formItemLayout.addWidget(moveDownButton)
        formItemLayout.addWidget(editItemButton)
        formItemLayout.addWidget(removeItemButton)

        formItemFrame.setLayout(formItemLayout)

        if self.formItemsListLayout.count():
            # --> enable button from the last frame
            self.formItemsListLayout.itemAt((self.formItemsListLayout.count() - 1)).widget().layout().itemAt(3).widget().setEnabled(True)
        
        self.formItemsListLayout.insertWidget(self.formItemsListLayout.count() , formItemFrame)

        if self.formItemsListLayout.count():
            # --> disable button from the first frame
            self.formItemsListLayout.itemAt(0).widget().layout().itemAt(2).widget().setEnabled(False)
            # --> disable button from the last frame
            self.formItemsListLayout.itemAt((self.formItemsListLayout.count() - 1)).widget().layout().itemAt(3).widget().setEnabled(False)

        self.scrollArea.widget().resize(self.scrollArea.widget().sizeHint().width(), self.formItemsListLayout.count()*93)
        
        self.reloadSizeButton.animateClick(10)
        

###############################################################################################################################################################################

    def saveForm(self):
        """
        This method is used to update the maintenance form
        """
        if not len(self.formDescriptionField.text()):
            messageBox = QMessageBox()
            messageBox.setText("É necessária uma descrição para o formulário.")
            messageBox.setWindowTitle("Erro!")
            messageBox.setIcon(QMessageBox.Critical)
            messageBox.setWindowIcon(QIcon(":/warning_icon.png"))
            messageBox.exec_()
            return
        
        if not self.formItemsListLayout.count():
            messageBox = QMessageBox()
            messageBox.setText("Não há itens cadastrados no formulário.")
            messageBox.setWindowTitle("Erro!")
            messageBox.setIcon(QMessageBox.Critical)
            messageBox.setWindowIcon(QIcon(":/warning_icon.png"))
            messageBox.exec_()
            return
        
        messageBox = QMessageBox()
        messageBox.setIcon(QMessageBox.Question)
        messageBox.setWindowIcon(QIcon(":/question.png"))
        messageBox.setWindowTitle("Cadastrar Formulário?")
        messageBox.setText("Deseja cadastrar este formulário?")
        messageBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        
        messageBox.button(QMessageBox.Yes).setText("Sim")
        messageBox.button(QMessageBox.Yes).setCursor(QCursor(Qt.PointingHandCursor))
        
        messageBox.button(QMessageBox.No).setText("Não")
        messageBox.button(QMessageBox.No).setCursor(QCursor(Qt.PointingHandCursor))
        
        messageBox.exec_()
        
        # --> If the Yes button was clicked #
        if messageBox.clickedButton() == messageBox.button(QMessageBox.No):
            return


        insertList = []
        for i in range(0, self.formItemsListLayout.count()):
            if not self.formItemsListLayout.itemAt(i).widget().itemId:
                insertList.append(
                    (self.formItemsListLayout.itemAt(i).widget().layout().itemAt(0).widget().text(),
                     self.formItemsListLayout.itemAt(i).widget().itemPosition)
                )
       
        # --> Try to create the new form
        try:
            self.maintenanceForm = maintenanceformscontainer.MaintenanceForm()
            self.maintenanceForm.insertNewForm(self.formDescriptionField.text(), self.parent.loggedUser["id"], insertList)
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


        messageBox = QMessageBox()
        messageBox.setText("Formulário cadastrado com sucesso.")
        messageBox.setWindowTitle("Sucesso!")
        messageBox.setIcon(QMessageBox.Information)
        messageBox.setWindowIcon(QIcon(":/information.png"))
        messageBox.exec_()

        self.parent.updateFormTable()

        self.close()
###############################################################################################################################################################################
    
    def reloadItemLayoutSize(self):
        self.scrollArea.widget().resize(self.scrollArea.widget().sizeHint())


###############################################################################################################################################################################

    def addNewItemToList(self):

        if len(self.newItemField.toPlainText()) == 0:
            return
        
        boldFont = QFont()
        boldFont.setBold(False)

        formItemFrame = MyQFrame(None, self.formItemsListLayout.count())
                
        formItemLayout = QHBoxLayout()

        itemDescription = QLabel(self.newItemField.toPlainText().upper())
        itemDescription.setFixedSize(QSize(390, 65))
        itemDescription.setWordWrap(True)
        itemDescription.setFont(boldFont)

        # --> Up Button            
        moveUpButton = MyQUpPushButton(text="", parent=formItemFrame, itemsLayout=self.formItemsListLayout)

                    
        # --> Down Button
        moveDownButton = MyQDownPushButton(text="", parent=formItemFrame, itemsLayout=self.formItemsListLayout)
        #moveDownButton.setEnabled(False)

        # --> Edit Button
        editItemButton = MyQEditPushButton(text="", parent=formItemFrame, dialogPointer=self)

        removeItemButton = MyQDeletePushButton(text="", parent=formItemFrame, itemsLayout=self.formItemsListLayout, windowPointer=self)
                  
        formItemLayout.addWidget(itemDescription)
        formItemLayout.addStretch(1)
        formItemLayout.addWidget(moveUpButton)
        formItemLayout.addWidget(moveDownButton)
        formItemLayout.addWidget(editItemButton)
        formItemLayout.addWidget(removeItemButton)

        formItemFrame.setLayout(formItemLayout)

        if self.formItemsListLayout.count():
            # --> enable button from the last frame
            self.formItemsListLayout.itemAt((self.formItemsListLayout.count() - 1)).widget().layout().itemAt(3).widget().setEnabled(True)
        
        self.formItemsListLayout.insertWidget(self.formItemsListLayout.count() , formItemFrame)

        if self.formItemsListLayout.count():
            # --> disable button from the first frame
            self.formItemsListLayout.itemAt(0).widget().layout().itemAt(2).widget().setEnabled(False)
            # --> disable button from the last frame
            self.formItemsListLayout.itemAt((self.formItemsListLayout.count() - 1)).widget().layout().itemAt(3).widget().setEnabled(False)

        self.scrollArea.widget().resize(self.scrollArea.widget().sizeHint().width(), self.formItemsListLayout.count()*93)
        
        self.reloadSizeButton.animateClick(10)

        self.newItemField.setPlainText("")
       


###############################################################################################################################################################################


    def cancelItemEdition(self):
        self.addNewItemButton.setVisible(True)
        
        self.changeItemButton.setVisible(False)

        self.cancelItemChangeButton.setVisible(False)

        self.newItemField.setPlainText("")
        

###############################################################################################################################################################################

    def changeItemText(self):
        frame = self.formItemsListLayout.itemAt(self.editingItemPosition).widget()
        frame.layout().itemAt(0).widget().setText(self.newItemField.toPlainText().upper())

        self.addNewItemButton.setVisible(True)
        self.changeItemButton.setVisible(False)
        self.cancelItemChangeButton.setVisible(False)
        
        self.newItemField.setPlainText("")
        self.calculateCharacters()
        self.editingItemPosition = -1

        self.reloadSizeButton.animateClick(10)  
            
###############################################################################################################################################################################


    def calculateCharacters(self):
        """
        This method is called when a key is pressed in the action taken description, decrementing its counter
        """

        # --> Line inserted because the uppercase is lost when the backspace is pressed #
        self.newItemField.setCurrentCharFormat(self.textFormat)
        
        textLength = len(self.newItemField.toPlainText())
        if textLength <= 255:
           self.charCounter.setText(str(255 - textLength))
        else:
            text = self.newItemField.toPlainText()
            self.newItemField.setPlainText(text[:255])
            cursor = self.newItemField.textCursor()
            cursor.setPosition(255)
            self.newItemField.setTextCursor(cursor)
    
            
               
            















            
