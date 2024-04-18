from PyQt5.QtCore import (
    Qt,
    QSettings
    )

from PyQt5.QtGui import (
    QIcon,
    QCursor,
    QFont
    )

from PyQt5.QtWidgets import (
    QDialog,
    QLabel,
    QLineEdit,
    QCheckBox,
    QHBoxLayout,
    QPushButton,
    QGridLayout,
    QLayout,
    QMessageBox
    )

import qrc_resources
from magicDB import *
from myExceptions import *

__version__ = "2.0.0"


###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################


class LoginWindow(QDialog):
    """
    This class is responsible for rendering the login window modally.
    If the login doesn't happen, being cancelled by pressing Cancel or closing
    the windown, the application will terminate
    """
    
    def __init__(self, callback, parent=None):
        super(LoginWindow, self).__init__(parent)

        # --> object that holds the persistent login data #
        self.settings = QSettings()
        
        self.parent = parent
        self.callback = callback

        boldFont = QFont()
        boldFont.setBold(True)

        
        # --> Login Label and Field #
        loginLabel = QLabel("&Usuário:")
        loginLabel.setFont(boldFont)
        
        self.loginField = QLineEdit()
        self.loginField.setMinimumSize(300, 0)
        loginLabel.setBuddy(self.loginField)
        if self.settings.value("login/saveData", type=bool):
            self.loginField.setText(self.settings.value("login/username"))

        # --> Password Label and Field #
        passLabel = QLabel("&Senha:")
        passLabel.setFont(boldFont)
        
        self.passField = QLineEdit()
        self.passField.setEchoMode(QLineEdit.Password)
        passLabel.setBuddy(self.passField)
        if self.settings.value("login/saveData", type=bool):
            self.passField.setText(self.settings.value("login/password"))

        # --> Save user checkbox #
        self.saveUserDataCheckBox = QCheckBox("Guardar informações do usuário")
        if self.settings.value("login/saveData", type=bool):
            self.saveUserDataCheckBox.setChecked(True)

        # --> Buttons #
        

        loginButton = QPushButton("Entrar")
        loginButton.setCursor(QCursor(Qt.PointingHandCursor))

        cancelButton = QPushButton("Cancelar")
        cancelButton.setCursor(QCursor(Qt.PointingHandCursor))
        
        buttonsLayout = QHBoxLayout()
        buttonsLayout.addStretch(1)    
        buttonsLayout.addWidget(loginButton)
        buttonsLayout.addWidget(cancelButton)
        buttonsLayout.addStretch(1)
        
        # --> build the layout #
        layout = QGridLayout()
        layout.addWidget(loginLabel, 0, 0)
        layout.addWidget(self.loginField, 0, 1)
        
        layout.addWidget(passLabel, 1, 0)
        layout.addWidget(self.passField, 1, 1)

        layout.addWidget(self.saveUserDataCheckBox, 2, 0, 1, 2)

        layout.addLayout(buttonsLayout, 3, 0, 1, 2)
        
        self.setLayout(layout)
        self.layout().setSizeConstraint(QLayout.SetFixedSize)

        # --> connecting the buttons to its respectives SLOTS #
        loginButton.clicked.connect(self.tryLogin)
        cancelButton.clicked.connect(self.cancelLogin)
        self.rejected.connect(self.cancelLogin)

        self.setWindowIcon(QIcon(":/login_icon.png"))
        self.setWindowTitle("Autenticação de Usuário")

###############################################################################################################################################################################

    def tryLogin(self):
        """
        This method tries execute the Login verifying if the user related with
        the login and password exists. If the query returns a row that means that
        the user exists
        """
        myDBConnection = DBConnection()
               
        try:
            if len(self.loginField.text()) == 0: 
                raise EmptyFieldsError("Login", "O campo 'Usuário' é de preenchimento obrigatório.")
            if len(self.passField.text()) == 0:
                raise EmptyFieldsError("Senha", "O campo 'Senha' é de preenchimento obrigatório.")
            
            fields = [
                "col_nome",
                "col_login",
                "col_id",
                "col_categoria"
                ]
            
            tables = [
                ("colaboradores", "", "")
                ]

            where = [
                "(col_ativo = 1 OR col_categoria = 1)",
                "col_login = '" + self.loginField.text() + "'",
                "col_senha = MD5('" + self.passField.text() + "')"
                ]

            querySuccess, queryResult = myDBConnection.selectQuery(fields, tables, where)

            if not querySuccess:
                raise DatabaseConnectionError
            
            if querySuccess and len(queryResult) < 1:
                raise LoginFailedError

        # --> if there is any empty field #
        except EmptyFieldsError as error:
            field, message = error.args
            if field == "Login":
                fieldtoFocus = self.loginField
            elif field == "Senha":
                fieldtoFocus = self.passField
                
            messageBox = QMessageBox()
            messageBox.setText(message)
            messageBox.setWindowTitle("Atenção!")
            messageBox.setIcon(QMessageBox.Warning)
            messageBox.setWindowIcon(QIcon(":/warning_icon.png"))
            messageBox.exec_()
            fieldtoFocus.setFocus()
            return
        
        # --> if there is no user with inserted data #
        except LoginFailedError:
            messageBox = QMessageBox()
            messageBox.setText("Falha ao efetuar o Login. \nUsuário ou Senha incorretos.")
            messageBox.setWindowTitle("Atenção!")
            messageBox.setIcon(QMessageBox.Warning)
            messageBox.setWindowIcon(QIcon(":/warning_icon.png"))
            messageBox.exec_()
            return

        # --> if failed to connect to the database #
        except DatabaseConnectionError:
            messageBox = QMessageBox()
            messageBox.setText("Falha ao tentar consultar o banco de dados.")
            messageBox.setWindowTitle("Atenção!")
            messageBox.setIcon(QMessageBox.Warning)
            messageBox.setWindowIcon(QIcon(":/warning_icon.png"))
            messageBox.exec_()
            return


        self.parent.updateUserData(queryResult[0])
        self.parent.logged = True


        # --> code responsible for saving the last user and password logged in the system #
        self.settings.setValue("login/saveData", self.saveUserDataCheckBox.isChecked())
        if self.saveUserDataCheckBox.isChecked():
            self.settings.setValue("login/username", self.loginField.text())
            self.settings.setValue("login/password", self.passField.text())
        QDialog.accept(self)

###############################################################################################################################################################################

    def cancelLogin(self):
        """
        This method is called whether the Login Dialog is closed or
        the Cancel button is pressed
        """
        self.callback()
        
