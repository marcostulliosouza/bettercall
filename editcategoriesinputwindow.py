from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import qrc_resources
from magicDB import *
from myExceptions import *

import inputscontainer


class MyInputDialog(QDialog):
    """
    This class is responsible for creating a popup used to edit the categories
    """
    def __init__(self, parent=None, inputCat=None):
        super(MyInputDialog, self).__init__(parent)

        categoryLabel = QLabel("Categoria: ")

        self.editableCategory = QLineEdit()
        self.editableCategory.setText(inputCat.inputCatDesc)
        self.editableCategory.setMinimumWidth(210)

        buttonConfirm = QPushButton("Confirmar")
        buttonCancel = QPushButton("Cancelar")

        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch(1)
        buttonLayout.addWidget(buttonConfirm)
        buttonLayout.addWidget(buttonCancel)

        editCategoryLayout = QGridLayout()
        editCategoryLayout.addWidget(categoryLabel, 0, 0)
        editCategoryLayout.addWidget(self.editableCategory, 0, 1)
        editCategoryLayout.addLayout(buttonLayout, 1, 0, 1, 2)

        self.setLayout(editCategoryLayout)

        buttonCancel.clicked.connect(self.close)


class EditCategoriesInputWindow(QDialog):
    """
    This class is responsible for rendering the categories edit window modally.
    """

    def __init__(self, parent=None):
        super(EditCategoriesInputWindow, self).__init__(parent)
        self.parent = parent
        self.catList = inputscontainer.InputCategoryContainer()
        self.setAttribute(Qt.WA_DeleteOnClose)

        boldFont = QFont()
        boldFont.setBold(True)

        categoryLabel = QLabel("Categoria: ")
        categoryLabel.setFont(boldFont)
    

        self.categoriesComboBox = QComboBox()
        self.categoriesComboBox.setMinimumContentsLength(30)
        self.populateCategoriesComboBox()
        

        self.buttonInsert = QPushButton("Inserir")

        self.buttonEdit = QPushButton("Editar")
        self.buttonEdit.setDisabled(True)
        
        self.buttonCancel = QPushButton("Cancelar")

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.buttonInsert)
        buttonLayout.addWidget(self.buttonEdit)
        buttonLayout.addWidget(self.buttonCancel)
        

        editCategoriesWindowLayout = QGridLayout()
        editCategoriesWindowLayout.addWidget(categoryLabel, 0, 0)
        editCategoriesWindowLayout.addWidget(self.categoriesComboBox, 0, 1)
        editCategoriesWindowLayout.addLayout(buttonLayout, 1, 0, 1, 2)

        self.categoriesComboBox.currentIndexChanged.connect(self.enableEditButton)
        self.buttonCancel.clicked.connect(self.cancelEditCategory)
        self.buttonEdit.clicked.connect(self.editInputCategory)

        self.setLayout(editCategoriesWindowLayout)
        self.setWindowIcon(QIcon(":/input_categories.png"))
        self.setWindowTitle("Edição de Categorias de Insumos")


    def populateCategoriesComboBox(self):
        """
        This method is used to populate the input categories combobox
        """
        self.catList.loadInputCategories()
        
        self.categoriesComboBox.addItem("", -1)
        
        for row, category in enumerate(self.catList):
            self.categoriesComboBox.addItem(category.inputCatDesc, category.inputCatId)

    def editInputCategory(self):
        """
        This method is used to update the Category name
        """
        categoryId = self.categoriesComboBox.itemData(self.categoriesComboBox.currentIndex())

        inputCat = self.catList.inputCategoryFromId(categoryId)
        
        inputDialog = MyInputDialog(self, inputCat)
        inputDialog.exec_()
        
        
    
    
    def enableEditButton(self, index):
        """
        This method is invoked when a value is changed in the category combobox
        """
        catId = self.categoriesComboBox.itemData(self.categoriesComboBox.currentIndex())
        if catId > 0:
            self.buttonEdit.setDisabled(False)
        else:
            self.buttonEdit.setDisabled(True)
        
    def cancelEditCategory(self):
        self.done(1)
    
