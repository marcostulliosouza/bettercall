"""
    SISTEMA BETTER CALL TEST
    v2.0.0 - Desenvolvimento do módulo de controle de dispositivos, entrada e saida de dispositivos,
             cadastro de notas fiscais e controle das manutenções preventivas. Também foi reescrito todo
             o código para padronização e utilização melhor do conceito de OO.
    
    v1.6.1 - Correção de um problema na transferência de chamados. Adicionado a função de atualizar os
             parâmetros do objeto Call após transferir o chamado.


    v1.6.0 - Tela de controle de Analistas e Clientes relacionados
             Criação de função que permite execução de multiplas queries com uma unica
             transação.
             Conserto de calculo dos indicadores que arredondava para baixo ao invés de arredondar
             apenas.
             Conserto do tamanho das colunas do relatorio dos chamados

    v1.5.3 - Pequenas correções no codigo 


    v1.5.0 - Revisão de todo o código, criando rowback de todas as operações de alteração
             de dados do banco em caso de falha

    
    v1.0.0 - Primeira versão do sistema. Inclui funcionalidade de atendimento dos chamados
             abertos atraves da interface web, disponivel em chamados.visum.com.br
             Funcionalidade de envio de arquivos do plano de produção, com geração dos chamados
             de instalação de Jigas de teste e gravação.
"""

import sys
import ctypes
from datetime import datetime, timedelta
from time import sleep

from PyQt5.QtCore import (
    QTimer,
    Qt,
    QSettings,
    QCoreApplication
    )

from PyQt5.QtGui import (
    QIcon,
    QCursor
    )

from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QMdiArea,
    QAction,
    QMessageBox
    )

import qrc_resources
import loginwindow
import listcallswindow
import fileuploadwindow
import callsreportwindow
import prodfilescontainer
import listinputswindow
import editcategoriesinputwindow
import indicatorsearchwindow


#2018
import clientresponsiblewindow
import listinvoiceswindow
import listdeviceswindow
import returnequipmentswindow
import receiveequipmentswindow
import equipmentsvinculationwindow

#2019
import listmaintenanceswindow
import listmaintenanceformswindow
import createengcallwindow


from myExceptions import *

# bit of code to show the icon in the taskbar
myappid = u'bettercalltest'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

__version__ = "2.0.0"

QCoreApplication.setOrganizationName("Hi-mix")
QCoreApplication.setOrganizationDomain("himix.com")
QCoreApplication.setApplicationName("Better Call Test")

###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################



class MyQLabel(QLabel):
    """
    This class was created to reimplement the mousepressevent
    """
    def __init__(self, parent=None):
        super(MyQLabel, self).__init__()
        self.parent = parent

###############################################################################################################################################################################

    def mousePressEvent(self, event):
        if self.text() == "PLANO DE PRODUÇÃO NÃO ENVIADO!":
            self.parent.sendProdFileSubWindow()


###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################


class MainWindow(QMainWindow):
    """
    This class is responsible for creating the main window of
    the Calltest system
    """

    # --> time in miliseconds after rendering the mainwindow to show the Login Dialog #
    TIME_BEFORE_BEGIN = 500

    # --> skips Login Dialog #
    CODING_MODE = 0

    screenResolution = {}
    openedSubWindows = {}

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

    # --> production plan upload checker #
        self.productionChecker = prodfilescontainer.ProdFileOpChecker()

    # --> create a Multiple Document Interface(MDI) #
        self.MDI = QMdiArea(self)
        self.setCentralWidget(self.MDI)
        self.logged = False
        self.loggedUser = {}
        self.prodPlanTimer = QTimer()

    # --> status bar configuration #
        self.statusLabel = MyQLabel(self)
        self.statusLabel.setAlignment(Qt.AlignLeft)
        self.statusLabel.setText(" ")

        self.userBarLabel = QLabel()
        self.userBarLabel.setText(" ")
        self.userBarLabel.setScaledContents(True)

    # --> status bar creation #
        status = self.statusBar()
        status.addWidget(self.statusLabel, 1)
        status.addPermanentWidget(self.userBarLabel)
        status.setSizeGripEnabled(False)

    

    # --> set the window title bar #
        self.setWindowTitle(f"Better Call Test - {__version__}c")

    # --> set the window to maximized mode #
        self.setWindowState(Qt.WindowMaximized)

    # --> wait until everything is loaded #
        if not self.logged:
            if not self.CODING_MODE:
                QTimer.singleShot(self.TIME_BEFORE_BEGIN, self.login)

       

###############################################################################################################################################################################

    def createUserActions(self):
        """
        This method creates all the menu and toolbar actions
        """
        # --> Iniciar->Definir Analista Responsável #
        self.start_clientsAndResponsiblesAction = QAction("&Analistas e Clientes", self)
        self.start_clientsAndResponsiblesAction.setShortcut("Ctrl+A")
        self.start_clientsAndResponsiblesAction.setIcon(QIcon("images/client.png"))
        self.start_clientsAndResponsiblesAction.setToolTip("Vincular Clientes aos Analistas")
        self.start_clientsAndResponsiblesAction.setStatusTip("Vincular Clientes aos Analistas")
        self.start_clientsAndResponsiblesAction.triggered.connect(self.showClientResponsibleSubWindow)
        
        
        # --> Iniciar->Sair action #
        self.start_quitAction = QAction("&Sair", self)
        self.start_quitAction.setIcon(QIcon(":/quit2.png"))
        self.start_quitAction.setShortcut("Ctrl+Q")
        self.start_quitAction.setToolTip("Sair do programa")
        self.start_quitAction.setStatusTip("Sair do programa")
        self.start_quitAction.triggered.connect(self.askBeforeTerminate)

        # --> Chamados->Listar Chamados #
        self.calls_listCallsAction = QAction("Listar &Chamados", self)
        self.calls_listCallsAction.setIcon(QIcon(":/calls.png"))
        self.calls_listCallsAction.setShortcut("Ctrl+Alt+C")
        self.calls_listCallsAction.setToolTip("Listar Chamados")
        self.calls_listCallsAction.setStatusTip("Listar Chamados")
        self.calls_listCallsAction.triggered.connect(self.showCallsListSubWindow)

        # --> Chamados->Chamados de Engenharia #
        self.calls_engineeringCallsAction = QAction("Chamado de Engenharia", self)
        self.calls_engineeringCallsAction.setIcon(QIcon("images/engineer_call.png"))
        self.calls_engineeringCallsAction.setToolTip("Abrir Chamado de Engenharia")
        self.calls_engineeringCallsAction.setStatusTip("Abrir Chamado de Engenharia")
        self.calls_engineeringCallsAction.triggered.connect(self.showCreateEngCallWindow)

        # --> Insumos->Listar Insumos #
        self.inputs_listInputsAction = QAction("Listar &Insumos", self)
        self.inputs_listInputsAction.setShortcut("Ctrl+Alt+I")
        self.inputs_listInputsAction.setToolTip("Listar Insumos")
        self.inputs_listInputsAction.setStatusTip("Listar Insumos")
        self.inputs_listInputsAction.triggered.connect(self.showInputsListSubWindow)

        # --> Insumos->Editar Categorias #
        self.input_editCategoriesAction = QAction("Editar Categorias", self)
        self.input_editCategoriesAction.setIcon(QIcon("images/input_categories.png"))
        self.input_editCategoriesAction.setToolTip("Editar Categorias dos Insumos")
        self.input_editCategoriesAction.setStatusTip("Editar Categorias dos Insumos")
        self.input_editCategoriesAction.triggered.connect(self.showEditCategoriesInputWindow)

        # --> Relatorio->Relatório de Chamados #
        self.reports_callsReportAction = QAction("Relatório de Chamados", self)
        self.reports_callsReportAction.setIcon(QIcon("images/calls_report_2.png"))
        self.reports_callsReportAction.setShortcut("Ctrl+R")
        self.reports_callsReportAction.setToolTip("Relatório de Chamados")
        self.reports_callsReportAction.setStatusTip("Relatório de Chamados")
        self.reports_callsReportAction.triggered.connect(self.showCallsReportSubWindow)

        # # --> Relatorios->Relatório de Manutenção Preventiva #
        # self.reports_indicatorSearchAction = QAction("Relatório de Manutenção Preventiva", self)
        # self.reports_indicatorSearchAction.setIcon(QIcon(":images/detailed_call_report.png"))
        # self.reports_indicatorSearchAction.setShortcut("Ctrl+I")
        # self.reports_indicatorSearchAction.setToolTip("Pesquisa de Indicador")
        # self.reports_indicatorSearchAction.setStatusTip("Pesquisa de Indicador")
        # self.reports_indicatorSearchAction.triggered.connect(self.showIndicatorSearchSubWindow)

        # --> Relatorios->Pesquisa de Indicador #
        self.reports_indicatorSearchAction = QAction("Pesquisa de Indicador", self)
        self.reports_indicatorSearchAction.setIcon(QIcon(":/detailed_call_report.png"))
        self.reports_indicatorSearchAction.setShortcut("Ctrl+I")
        self.reports_indicatorSearchAction.setToolTip("Pesquisa de Indicador")
        self.reports_indicatorSearchAction.setStatusTip("Pesquisa de Indicador")
        self.reports_indicatorSearchAction.triggered.connect(self.showIndicatorSearchSubWindow)


        # --> Arquivos->Enviar Plano de Produção #
        self.files_sendProdPlanAction = QAction("&Enviar Plano de Produção", self)
        self.files_sendProdPlanAction.setIcon(QIcon("images/prod_plan_2.png"))
        self.files_sendProdPlanAction.setShortcut("Ctrl+E")
        self.files_sendProdPlanAction.setToolTip("Enviar Plano de Produção")
        self.files_sendProdPlanAction.setStatusTip("Enviar Plano de Produção")
        self.files_sendProdPlanAction.triggered.connect(self.sendProdFileSubWindow)

        # --> Arquivos->Listar Notas Fiscais #
        self.files_listInvoicesAction = QAction("Listar &Notas Fiscais", self)
        self.files_listInvoicesAction.setIcon(QIcon("images/invoices2.png"))
        self.files_listInvoicesAction.setShortcut("Ctrl+N")
        self.files_listInvoicesAction.setToolTip("Listar Notas Fiscais")
        self.files_listInvoicesAction.setStatusTip("Listar Notas Fiscais")
        self.files_listInvoicesAction.triggered.connect(self.showInvoicesListSubWindow)

        # --> Equipamentos->Vincular Equipamentos a Produtos #
        self.equipments_vinculateEquipmentsAction = QAction("Vincular Equipamentos e Produtos", self)
        self.equipments_vinculateEquipmentsAction.setIcon(QIcon("images/chain.png"))
        #self.equipments_vinculateEquipmentsAction.setShortcut("Ctrl+D")
        self.equipments_vinculateEquipmentsAction.setToolTip("Vincular Equipamentos a Produtos.")
        self.equipments_vinculateEquipmentsAction.setStatusTip("Vincular Equipamentos a Produtos.")
        self.equipments_vinculateEquipmentsAction.triggered.connect(self.showEquipmentsVinculationSubWindow)
        
        # --> Equipamentos->Listar Dispositivos #
        self.equipments_listDevicesAction = QAction("Listar &Dispositivos", self)
        self.equipments_listDevicesAction.setIcon(QIcon("images/scanner.png"))
        self.equipments_listDevicesAction.setShortcut("Ctrl+D")
        self.equipments_listDevicesAction.setToolTip("Listar Dispositivos de Teste e Gravação")
        self.equipments_listDevicesAction.setStatusTip("Listar Dispositivos de Teste e Gravação")
        self.equipments_listDevicesAction.triggered.connect(self.showDevicesListSubWindow)

        # --> Equipamentos->Devolver Equipamentos #
        self.equipments_returnEquipmentsAction = QAction("Devolver Equipamentos", self)
        self.equipments_returnEquipmentsAction.setIcon(QIcon("images/send_equipment.png"))
        self.equipments_returnEquipmentsAction.setToolTip("Devolver Equipamentos")
        self.equipments_returnEquipmentsAction.setStatusTip("Devolver Equipamentos")
        self.equipments_returnEquipmentsAction.triggered.connect(self.showReturnEquipmentsSubWindow)

        # --> Equipamentos->Receber Equipamentos #
        self.equipments_receiveEquipmentsAction = QAction("Receber Equipamentos", self)
        self.equipments_receiveEquipmentsAction.setIcon(QIcon("images/receive_equipment.png"))
        self.equipments_receiveEquipmentsAction.setToolTip("Receber Equipamentos")
        self.equipments_receiveEquipmentsAction.setStatusTip("Receber Equipamentos")
        self.equipments_receiveEquipmentsAction.triggered.connect(self.showReceiveEquipmentsSubWindow)

        # --> Equipamentos->Manutenção Preventiva #
        self.equipments_listMaintenancesAction = QAction("Manutenção Preventiva", self)
        self.equipments_listMaintenancesAction.setIcon(QIcon("images/maintenance.png"))
        self.equipments_listMaintenancesAction.setToolTip("Manutenção Preventiva")
        self.equipments_listMaintenancesAction.setStatusTip("Manutenção Preventiva")
        self.equipments_listMaintenancesAction.triggered.connect(self.showListMaintenancesSubWindow)

        # --> Equipamentos->Formulários de Manutenção #
        self.equipments_listMaintenanceFormsAction = QAction("Formulários de Manutenção", self)
        self.equipments_listMaintenanceFormsAction.setIcon(QIcon("images/formulario.png"))
        self.equipments_listMaintenanceFormsAction.setToolTip("Formulários de Manutenção")
        self.equipments_listMaintenanceFormsAction.setStatusTip("Formulários de Manutenção")
        self.equipments_listMaintenanceFormsAction.triggered.connect(self.showListMaintenanceFormsSubWindow)

###############################################################################################################################################################################

    def setupMenuBar(self):
        """
        This method builds the menuBar elements and actions
        """
        # --> Iniciar #
        self.startMenu = self.menuBar().addMenu("&Iniciar")
        if self.loggedUser["category"] <= 10:
            self.startMenu.addAction(self.start_clientsAndResponsiblesAction)
        self.startMenu.addAction(self.start_quitAction)

        # --> Chamados #
        self.callsMenu = self.menuBar().addMenu("&Chamados")
        self.callsMenu.addAction(self.calls_listCallsAction)
        if self.loggedUser["category"] <= 20:
            self.callsMenu.addAction(self.calls_engineeringCallsAction)
     

        # --> Insumos #
        #self.inputsMenu = self.menuBar().addMenu("I&nsumos")
        #self.inputsMenu.addAction(self.inputs_listInputsAction)
        #self.inputsMenu.addAction(self.input_editCategoriesAction)

        # Relatorios
        self.reportsMenu = self.menuBar().addMenu("Relatórios")
        self.reportsMenu.addAction(self.reports_callsReportAction)
        if self.loggedUser["category"] <= 40:
            self.reportsMenu.addAction(self.reports_indicatorSearchAction)
            

        # Arquivos
        if self.loggedUser["category"] <= 50:
            self.filesMenu = self.menuBar().addMenu("&Arquivos")
            self.filesMenu.addAction(self.files_sendProdPlanAction)
            if self.loggedUser["category"] <= 40:
                self.filesMenu.addAction(self.files_listInvoicesAction)

        # Equipamentos
        if self.loggedUser["category"] <= 40:
            self.equipmentsMenu = self.menuBar().addMenu("&Equipamentos")

            if self.loggedUser["category"] <= 20:
                self.equipmentsMenu.addAction(self.equipments_vinculateEquipmentsAction)
            
            self.equipmentsMenu.addAction(self.equipments_listDevicesAction)
            self.equipmentsMenu.addAction(self.equipments_returnEquipmentsAction)
            self.equipmentsMenu.addAction(self.equipments_receiveEquipmentsAction)

            self.equipmentsMenu.addAction(self.equipments_listMaintenancesAction)
            self.equipmentsMenu.addAction(self.equipments_listMaintenanceFormsAction)

###############################################################################################################################################################################

    def setupToolBar(self):
        """
        This method builds the Toolbar elements and actions
        """
        # --> Iniciar ToolBar #
        self.startToolbar = self.addToolBar("Iniciar")
        self.startToolbar.setObjectName("StartToolBar")
        self.startToolbar.addAction(self.start_quitAction)
        if self.loggedUser["category"] <= 10:
            self.startToolbar.addAction(self.start_clientsAndResponsiblesAction)

        # --> Chamados #
        self.callsToolbar = self.addToolBar("Chamados")
        self.callsToolbar.setObjectName("CallsToolBar")
        self.callsToolbar.addAction(self.calls_listCallsAction)

        # Relatorios
        self.reportsToolbar = self.addToolBar("Relatórios")
        self.reportsToolbar.setObjectName("ReportsToolBar")
        self.reportsToolbar.addAction(self.reports_callsReportAction)

        if self.loggedUser["category"] <= 40:
            self.reportsToolbar.addAction(self.reports_indicatorSearchAction)
            

         # Arquivos
        if self.loggedUser["category"] <= 50:
            self.filesToolbar = self.addToolBar("Arquivos")
            self.filesToolbar.setObjectName("FilesToolBar")
            self.filesToolbar.addAction(self.files_sendProdPlanAction)
            if self.loggedUser["category"] <= 40:
                self.filesToolbar.addAction(self.files_listInvoicesAction)
        
       # Equipamentos
        if self.loggedUser["category"] <= 40:
            self.equipmentsToolbar = self.addToolBar("Equipamentos")
            self.equipmentsToolbar.setObjectName("EquipmentsToolBar")

            if self.loggedUser["category"] <= 20:
                self.equipmentsToolbar.addAction(self.equipments_vinculateEquipmentsAction)
            
            self.equipmentsToolbar.addAction(self.equipments_listDevicesAction)
            self.equipmentsToolbar.addAction(self.equipments_returnEquipmentsAction)
            self.equipmentsToolbar.addAction(self.equipments_receiveEquipmentsAction)

            self.equipmentsToolbar.addAction(self.equipments_listMaintenancesAction)
            self.equipmentsToolbar.addAction(self.equipments_listMaintenanceFormsAction)

        

###############################################################################################################################################################################

    def login(self):
        """
        This method loads the Login Dialog in modal mode
        """
        loginWindow = loginwindow.LoginWindow(self.terminateApplication, self)
        loginWindow.exec_()
        #sleep(2)
        #QTimer.singleShot(self.TIME_BEFORE_BEGIN, self.checkProdPlan)
        self.prodPlanTimer.timeout.connect(self.checkProdPlan)
        self.prodPlanTimer.start(60000)

###############################################################################################################################################################################
        
    def updateUserData(self, userData):
        """
        This method is called by loginwindow to update the data of the logged user
        """
        self.loggedUser["name"] = userData[0]
        self.loggedUser["login"] = userData[1]
        self.loggedUser["id"] = int(userData[2])
        self.loggedUser["category"] = int(userData[3])

        self.userBarLabel.setText("{0} ".format(userData[0]))

        # --> create the actions for the menu and the toolbar #
        self.createUserActions()
        self.setupMenuBar()
        self.setupToolBar()

###############################################################################################################################################################################

    def terminateApplication(self):
        """
        This method therminates the application
        """
        self.close()

###############################################################################################################################################################################


    def setStatusBarMessage(self, message, duration=None, warning=False):
        """
        This method is used as substitute for the command statusBar().showMessage
        It was done because the showMessage changes the statusbar appearance
        """
        if warning:
            self.statusLabel.setStyleSheet("QLabel {color: red; font-weight: bold}")
        else:
            self.statusLabel.setStyleSheet("QLabel {color: black}")

        self.statusLabel.setText(message)
        if duration is not None:
            QTimer.singleShot(duration, self.clearStatusBarMessage)

###############################################################################################################################################################################

    def clearStatusBarMessage(self):
        """
        Clear the statusbar message
        """
        self.statusLabel.setText(" ")

#####################################################################
##################### FROM HERE ACTION METHODS ######################
#####################################################################

    def showClientResponsibleSubWindow(self):
        if not self.logged:
            return

        if "clientresponsiblewindow" in self.openedSubWindows.keys():
            self.MDI.setActiveSubWindow(self.openedSubWindows["clientresponsiblewindow"])
            return

        clientResponsibleWindow = clientresponsiblewindow.ClientResponsibleWindow(self)
        self.openedSubWindows["clientresponsiblewindow"] = clientResponsibleWindow
        self.MDI.addSubWindow(clientResponsibleWindow)
        clientResponsibleWindow.show()

        xPos = (self.screenResolution['w'] - clientResponsibleWindow.width()) / 2
        yPos = ((self.screenResolution['h'] - 140) - clientResponsibleWindow.height()) / 2

        clientResponsibleWindow.move(xPos, yPos)

###############################################################################################################################################################################

    def askBeforeTerminate(self):
        """
        This method is used to ask the user if he wants to quit the application
        """
        messageBox = QMessageBox()
        messageBox.setIcon(QMessageBox.Question)
        messageBox.setWindowIcon(QIcon(":/question.png"))
        messageBox.setWindowTitle("Sair?")
        messageBox.setText("Tem certeza que deseja sair?")
        messageBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        messageBox.button(QMessageBox.Yes).setText("Sim")
        messageBox.button(QMessageBox.Yes).setCursor(QCursor(Qt.PointingHandCursor))
        messageBox.button(QMessageBox.No).setText("Não")
        messageBox.button(QMessageBox.No).setCursor(QCursor(Qt.PointingHandCursor))

        messageBox.exec_()

        # if the Yes button was clicked
        if messageBox.clickedButton() == messageBox.button(QMessageBox.Yes):
            self.terminateApplication()

###############################################################################################################################################################################

    def showIndicatorSearchSubWindow(self):
        """
        This method is used to call a subwindow used to search for values of the past indicators
        """

        if not self.logged:
            return

        # if the window is already opened it will be activated
        if "indicatorsearchwindow" in self.openedSubWindows.keys():
            self.MDI.setActiveSubWindow(self.openedSubWindows["indicatorsearchwindow"])
            return

        indSearchWindow = indicatorsearchwindow.IndicatorSearchWindow(self)
        self.openedSubWindows["indicatorsearchwindow"] = indSearchWindow
        self.MDI.addSubWindow(indSearchWindow)
        indSearchWindow.show()

        xPos = (self.screenResolution['w'] - indSearchWindow.width()) / 2
        yPos = ((self.screenResolution['h'] - 140) - indSearchWindow.height()) / 2

        indSearchWindow.move(xPos, yPos)

###############################################################################################################################################################################

    def showEditCategoriesInputWindow(self):
        """
        This method is used to call the Input Categories Edit Window
        """
        if not self.logged:
            return
        
        editInputCategoriesWindow = editcategoriesinputwindow.EditCategoriesInputWindow(self)
        editInputCategoriesWindow.setModal(True)
        editInputCategoriesWindow.show()
        editInputCategoriesWindow.raise_()
        editInputCategoriesWindow.activateWindow()
        editInputCategoriesWindow.show()

        xPos = (self.screenResolution['w'] - editInputCategoriesWindow.width()) / 2
        yPos = (self.screenResolution['h'] - editInputCategoriesWindow.height()) / 2

        editInputCategoriesWindow.move(xPos, yPos)

###############################################################################################################################################################################

    def showInputsListSubWindow(self):
        """
        This method is responsible for showing the MDI sub window listinputs
        """
        if not self.logged:
            return

        # if the window is already opened it will be activated
        if "listinputswindow" in self.openedSubWindows.keys():
            self.MDI.setActiveSubWindow(self.openedSubWindows["listinputswindow"])
            return
        # else it will be created, added to the opened window list
        listInputsSubWindow = listinputswindow.ListInputsWindow(self)
        self.openedSubWindows["listinputswindow"] = listInputsSubWindow
        self.MDI.addSubWindow(listInputsSubWindow)
        listInputsSubWindow.show()

        xPos = (self.screenResolution['w'] - listInputsSubWindow.width()) / 2
        yPos = ((self.screenResolution['h'] - 140) - listInputsSubWindow.height()) / 2

        listInputsSubWindow.move(xPos, yPos)

###############################################################################################################################################################################

    def showCreateEngCallWindow(self):
        """
        This method is responsible for showing the MDI sub window create eng call window
        """
        if not self.logged:
            return

        # if the window is already opened it will be activated
        if "createengcallwindow" in self.openedSubWindows.keys():
            self.MDI.setActiveSubWindow(self.openedSubWindows["createengcallwindow"])
            return
        # else it will be created, added to the opened window list
        createEngCallWindow = createengcallwindow.CreateEngCallWindow(self)
        self.openedSubWindows["createengcallwindow"] = createEngCallWindow
        self.MDI.addSubWindow(createEngCallWindow)
        createEngCallWindow.show()

        xPos = (self.screenResolution['w'] - createEngCallWindow.width()) / 2
        yPos = ((self.screenResolution['h'] - 140) - createEngCallWindow.height()) / 2

        createEngCallWindow.move(xPos, yPos)

###############################################################################################################################################################################

    def showCallsListSubWindow(self):
        """
        This method is used to show the MDI sub window listcalls
        """
        if not self.logged:
            return

        # if the window is already opened it will be activated
        if "listcallswindow" in self.openedSubWindows.keys():
            self.MDI.setActiveSubWindow(self.openedSubWindows["listcallswindow"])
            return
        
        # else it will be created, added to the opened window list
        listCallsSubWindow = listcallswindow.ListCallsWindow(self)
        self.openedSubWindows["listcallswindow"] = listCallsSubWindow
        self.MDI.addSubWindow(listCallsSubWindow)
        listCallsSubWindow.show()

        xPos = (self.screenResolution['w'] - listCallsSubWindow.width()) / 2
        yPos = ((self.screenResolution['h'] - 140) - listCallsSubWindow.height()) / 2

        listCallsSubWindow.move(xPos, yPos)

###############################################################################################################################################################################

    def showCallsReportSubWindow(self):
        """
        This method is used to show de MDI subwindow responsible for showing the calls report
        """
        if not self.logged:
            return
        
        # if the window is already opened it will be activated
        if "callsreportwindow" in self.openedSubWindows.keys():
            self.MDI.setActiveSubWindow(self.openedSubWindows["callsreportwindow"])
            return

        # else it will be created, added to the opened window list
        callsReportSubWindow = callsreportwindow.CallsReportWindow(self)
        self.openedSubWindows["callsreportwindow"] = callsReportSubWindow
        self.MDI.addSubWindow(callsReportSubWindow)
        callsReportSubWindow.show()

        xPos = (self.screenResolution['w'] - callsReportSubWindow.width()) / 2
        yPos = ((self.screenResolution['h'] - 140) - callsReportSubWindow.height()) / 2

        callsReportSubWindow.move(xPos, yPos)

###############################################################################################################################################################################

    def sendProdFileSubWindow(self):
        """
        This method is used to show the Subwindow responsible for uploading the production plan
        """
        if not self.logged:
            return
        
        if "prodplanuploadwindow" in self.openedSubWindows.keys():
            self.MDI.setActiveSubWindow(self.openedSubWindows["prodplanuploadwindow"])
            return

        prodPlanUploadWindow = fileuploadwindow.ProductionPlanUploadWindow(self)
        self.openedSubWindows["prodplanuploadwindow"] = prodPlanUploadWindow
        self.MDI.addSubWindow(prodPlanUploadWindow)
        prodPlanUploadWindow.show()

        xPos = (self.screenResolution['w'] - prodPlanUploadWindow.width()) / 2
        yPos = ((self.screenResolution['h'] - 140) - prodPlanUploadWindow.height()) / 2

        prodPlanUploadWindow.move(xPos, yPos)

###############################################################################################################################################################################

    def showInvoicesListSubWindow(self):
        """
        This method is called to show the Subwindow responsible for listing the Invoices of the Test Jigs
        Received by the clients
        """

        if not self.logged:
            return
        
        if "listinvoiceswindow" in self.openedSubWindows.keys():
            self.MDI.setActiveSubWindow(self.openedSubWindows["listinvoiceswindow"])
            return

        listInvoicesSubWindow = listinvoiceswindow.ListInvoicesWindow(self)
        self.openedSubWindows["listinvoiceswindow"] = listInvoicesSubWindow
        self.MDI.addSubWindow(listInvoicesSubWindow)
        listInvoicesSubWindow.show()

        xPos = (self.screenResolution['w'] - listInvoicesSubWindow.width()) / 2
        yPos = ((self.screenResolution['h'] - 140) - listInvoicesSubWindow.height()) / 2

        listInvoicesSubWindow.move(xPos, yPos)

###############################################################################################################################################################################

    def showDevicesListSubWindow(self):
        """
        This method is called to show the Subwindow responsible for listing the Test Jigs
        """
        if not self.logged:
            return
        
        if "listdeviceswindow" in self.openedSubWindows.keys():
            self.MDI.setActiveSubWindow(self.openedSubWindows["listdeviceswindow"])
            return

        listDevicesSubWindow = listdeviceswindow.ListDevicesWindow(self)
        self.openedSubWindows["listdeviceswindow"] = listDevicesSubWindow
        self.MDI.addSubWindow(listDevicesSubWindow)
        listDevicesSubWindow.show()

        xPos = (self.screenResolution['w'] - listDevicesSubWindow.width()) / 2
        yPos = ((self.screenResolution['h'] - 140) - listDevicesSubWindow.height()) / 2

        listDevicesSubWindow.move(xPos, yPos)

###############################################################################################################################################################################

    def showReturnEquipmentsSubWindow(self):
        """
        This method is called to show the return equipments dialog. The dialog will be opened modally,
        not allowing the user to change the system data before close the dialog, preventing data integrity
        problems
        """
        returnEquipmentsWindow = returnequipmentswindow.ReturnEquipmentsWindow(None, None, None, self)
        returnEquipmentsWindow.setModal(True)

        returnEquipmentsWindow.show()
          
        xPos = (self.screenResolution['w'] - returnEquipmentsWindow.width()) / 2
        yPos = (self.screenResolution['h'] - returnEquipmentsWindow.height()) / 2
            
        returnEquipmentsWindow.move(xPos, yPos)
        returnEquipmentsWindow.raise_()
        returnEquipmentsWindow.activateWindow()

###############################################################################################################################################################################

    def showReceiveEquipmentsSubWindow(self):
        """
        This method is called to show the return equipments dialog. The dialog will be opened modally,
        not allowing the user to change the system data before close the dialog, preventing data integrity
        problems
        """
        receiveEquipmentsWindow = receiveequipmentswindow.ReceiveEquipmentsWindow(None, None, None, self)
        receiveEquipmentsWindow.setModal(True)

        receiveEquipmentsWindow.show()
          
        xPos = (self.screenResolution['w'] - receiveEquipmentsWindow.width()) / 2
        yPos = (self.screenResolution['h'] - receiveEquipmentsWindow.height()) / 2
            
        receiveEquipmentsWindow.move(xPos, yPos)
        receiveEquipmentsWindow.raise_()
        receiveEquipmentsWindow.activateWindow()

###############################################################################################################################################################################

    def showEquipmentsVinculationSubWindow(self):
        """
        This method is called to show the Subwindow responsible vinculate the equipments to the products
        """
        if not self.logged:
            return
        
        if "equipmentsvinculationwindow" in self.openedSubWindows.keys():
            self.MDI.setActiveSubWindow(self.openedSubWindows["equipmentsvinculationwindow"])
            return

        equipmentsVinculationWindow = equipmentsvinculationwindow.EquipmentsVinculationWindow(self)
        self.openedSubWindows["equipmentsvinculationwindow"] = equipmentsVinculationWindow
        self.MDI.addSubWindow(equipmentsVinculationWindow)
        equipmentsVinculationWindow.show()

        xPos = (self.screenResolution['w'] - equipmentsVinculationWindow.width()) / 2
        yPos = ((self.screenResolution['h'] - 140) - equipmentsVinculationWindow.height()) / 2

        equipmentsVinculationWindow.move(xPos, yPos)

###############################################################################################################################################################################

    def showListMaintenancesSubWindow(self):
        """
        This method is called to show the window that lists the preemptive maintenance
        """
        if not self.logged:
            return
        
        if "listmaintenanceswindow" in self.openedSubWindows.keys():
            self.MDI.setActiveSubWindow(self.openedSubWindows["listmaintenanceswindow"])
            return

        listMaintenancesWindow = listmaintenanceswindow.ListMaintenancesWindow(self)
        self.openedSubWindows["listmaintenanceswindow"] = listMaintenancesWindow
        self.MDI.addSubWindow(listMaintenancesWindow)
        listMaintenancesWindow.show()

        xPos = (self.screenResolution['w'] - listMaintenancesWindow.width()) / 2
        yPos = ((self.screenResolution['h'] - 140) - listMaintenancesWindow.height()) / 2

        listMaintenancesWindow.move(xPos, yPos)


###############################################################################################################################################################################

    def showListMaintenanceFormsSubWindow(self):
        """
        This method is called to show the window that lists the mantenance forms 
        """

        
        if not self.logged:
            return
        
        if "listmaintenanceformswindow" in self.openedSubWindows.keys():
            self.MDI.setActiveSubWindow(self.openedSubWindows["listmaintenanceformswindow"])
            return

        listMaintenanceFormsWindow = listmaintenanceformswindow.ListMaintenanceFormsWindow(self)
        self.openedSubWindows["listmaintenanceformswindow"] = listMaintenanceFormsWindow
        self.MDI.addSubWindow(listMaintenanceFormsWindow)
        listMaintenanceFormsWindow.show()

        xPos = (self.screenResolution['w'] - listMaintenanceFormsWindow.width()) / 2
        yPos = ((self.screenResolution['h'] - 140) - listMaintenanceFormsWindow.height()) / 2

        listMaintenanceFormsWindow.move(xPos, yPos)

        
        

###############################################################################################################################################################################

    def checkProdPlan(self):
        """
        This method is called every 10 minutes to check if the production
        plan for the next day was uploaded
        """
        if self.loggedUser["category"] > 50:
            return
        
        try:
            now = datetime.now()
            tomorrow = datetime.today() + timedelta(days=1)
            date = str(tomorrow).split(" ")[0]
            time = str(tomorrow).split(" ")[1]

            hour = time.split(":")[0]

            if not self.productionChecker.checkProductionUpload(date) and int(hour) > 14:
                self.setStatusBarMessage("PLANO DE PRODUÇÃO NÃO ENVIADO!", None, True)


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
        

def main():
    """
    This method invokes the main window
    """
    app = QApplication(sys.argv)
    app.setOrganizationName("Hi-Mix Eletrônicos S/A")
    app.setOrganizationDomain("www.hi-mix.com.br")
    app.setApplicationName("Calltest")
    app.setWindowIcon(QIcon(":/icon.png"))

    screenResolution = app.desktop().screenGeometry()

    form = MainWindow()
    form.screenResolution['w'] = screenResolution.width()
    form.screenResolution['h'] = screenResolution.height()
    form.show()
    app.exec_()


main()
