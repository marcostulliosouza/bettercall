from PyQt5.QtCore import (
    QSize,
    Qt,
    QTimer
    )

from PyQt5.QtGui import (
    QIcon,
    QFont,
    QPalette,
    QCursor
    )

from PyQt5.QtWidgets import (
    QMdiSubWindow,
    QPushButton,
    QLayout,
    QHBoxLayout,
    QTableWidget,
    QAbstractScrollArea,
    QTableWidgetItem,
    QHeaderView,
    QGroupBox,
    QLabel,
    QLineEdit,
    QGridLayout,
    QVBoxLayout,
    QWidget,
    QMessageBox
    )

from myExceptions import *

import callscontainer
import callwindow

#2024 -> adicionado função de disparar email caso haja atraso de chamado
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

__version__ = "2.0.1"

###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################
class MyQTableWidget(QTableWidget):
    """
    This class is used to create a personilized qtablewidget for the window
    """
    def __init__(self, parent=None):
        super(MyQTableWidget, self).__init__(parent)
        self.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.setAlternatingRowColors(True)
        self.setAutoFillBackground(True)
        self.setEditTriggers(QTableWidget.NoEditTriggers)
        self.setSelectionBehavior(QTableWidget.SelectRows)
        self.setSelectionMode(QTableWidget.SingleSelection)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.horizontalHeader().setStretchLastSection(True)
        self.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.horizontalHeader().setHighlightSections(False)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.setMinimumSize(QSize(1300, 420))
        self.verticalHeader().setVisible(False)

        tablePalette = QPalette()
        tablePalette.setColor(QPalette.Inactive, QPalette.Highlight, tablePalette.color(QPalette.Active, QPalette.Highlight))
        tablePalette.setColor(QPalette.Inactive, QPalette.HighlightedText, tablePalette.color(QPalette.Active, QPalette.HighlightedText))
        self.setPalette(tablePalette)

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
        
       

        # --> Create the Items for the table headers #
       
        self.setColumnCount(11)

        
        iconInThePlan = QTableWidgetItem(" ")
        totalDuration = QTableWidgetItem("Duração Total")
        answerDuration = QTableWidgetItem("Atendimento")
        createdBy = QTableWidgetItem("Criado Por")
        callType = QTableWidgetItem("Tipo de Chamado")
        callLocal = QTableWidgetItem("Local")
        client = QTableWidgetItem("Cliente")
        product = QTableWidgetItem("Produto")
        status = QTableWidgetItem("Status")
        support = QTableWidgetItem("Suporte Responsável")
        callDescription = QTableWidgetItem("Descrição do Chamado")

        # --> Set the Header Items #
        self.setHorizontalHeaderItem(0, iconInThePlan)
        self.setHorizontalHeaderItem(1, totalDuration)
        self.setHorizontalHeaderItem(2, answerDuration)
        self.setHorizontalHeaderItem(3, createdBy)
        self.setHorizontalHeaderItem(4, callType)
        self.setHorizontalHeaderItem(5, callLocal)
        self.setHorizontalHeaderItem(6, client)
        self.setHorizontalHeaderItem(7, product)
        self.setHorizontalHeaderItem(8, status)
        self.setHorizontalHeaderItem(9, support)
        self.setHorizontalHeaderItem(10, callDescription)

        self.horizontalHeader().resizeSection(0, 40)
        self.horizontalHeader().resizeSection(1, 100)
        self.horizontalHeader().resizeSection(2, 100)
        self.horizontalHeader().resizeSection(3, 120)
        self.horizontalHeader().resizeSection(4, 150)
        self.horizontalHeader().resizeSection(5, 120)
        self.horizontalHeader().resizeSection(6, 120)
        self.horizontalHeader().resizeSection(7, 120)
        self.horizontalHeader().resizeSection(8, 120)
        self.horizontalHeader().resizeSection(9, 160)
        self.horizontalHeader().resizeSection(10, 250)
        
        self.horizontalHeader().setStyleSheet(stylesheet)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)


###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################

class QIndicatorLabel(QLabel):
    """
    This class reimplements the QLabel class
    """
    def __init__(self, text="", parent=None):
        super(QIndicatorLabel, self).__init__(text, parent)

        regularFont = QFont()
        regularFont.setBold(False)

        self.setFixedWidth(250)
        self.setFont(regularFont)

###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################

class MyQLineEdit(QLineEdit):
    """
    This class reimplements the qpushbutton class
    """
    def __init__(self, text="", parent=None):
        super(MyQLineEdit, self).__init__(text, parent)

        boldFont = QFont()
        boldFont.setBold(True)

        self.setReadOnly(True)
        self.setMaximumSize(70, 50)
        self.setAlignment(Qt.AlignHCenter)
        self.setFont(boldFont)

###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################

class ListCallsWindow(QMdiSubWindow):
    """
    This class is responsible for rendering the "Listar Chamados" window
    as a MDI sub Window and for managing the data inside it
    """
    # --> constant id, used for location inside the openedSubWindows dictionary in the main window #
    SUBWINDOWID = "listcallswindow"
    
    def __init__(self, parent=None):
        super(ListCallsWindow, self).__init__(parent)
        self.parent = parent
        self.loggedUser = parent.loggedUser
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowFlags(Qt.SubWindow | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)

        self.emailSentForCalls = set()  # Conjunto para rastrear os IDs das chamadas para as quais o e-mail já foi enviado

        self.indicators = callscontainer.CallIndicators()
        self.userAnsweringCall = False
        self.callsList = callscontainer.CallContainer()
        self.updateTimer = QTimer()

        #######################################
        ##### build the "Chamados" window #####
        #######################################
        
        ##############################
        ##### Button ANSWER CALL #####
        ##############################
        self.answerCallButton = QPushButton(" Ver Chamado ")
        self.answerCallButton.setEnabled(False)
        self.answerCallButton.setCursor(QCursor(Qt.PointingHandCursor))

        self.updateTableButton = QPushButton(" Atualizar Tabela ")
        self.updateTableButton.setCursor(QCursor(Qt.PointingHandCursor))
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.answerCallButton)
        button_layout.addWidget(self.updateTableButton)
        button_layout.addStretch(1)

        #############################
        ##### Table CALLS TABLE #####
        #############################
        
        self.openedCallsTable = MyQTableWidget()

        ######################
        ##### INDICATORS #####
        ######################
        
        # --> daily INDICATORS #
        
        groupBoxTitleFont = QFont()
        groupBoxTitleFont.setBold(True)

        daily_groupBox = QGroupBox("Indicador Diário")
        daily_groupBox.setFont(groupBoxTitleFont)

        daily_totalAnsweredCallsLabel = QIndicatorLabel("Chamados atendidos:")
        self.daily_TotalAnsweredCallsField = MyQLineEdit()
        
        daily_avgCallTimeLabel = QIndicatorLabel("Tempo médio de atendimento:")
        self.daily_AvgCallTimeField = MyQLineEdit()
        
        daily_avgLateTimeLabel = QIndicatorLabel("Tempo médio de atraso:")
        self.daily_AvgLateTimeField = MyQLineEdit()
        
        daily_uptimeLabel = QIndicatorLabel("Uptime de Teste:")
        self.daily_uptimeField = MyQLineEdit("0,00%")
        
        daily_layout = QGridLayout()
        daily_layout.addWidget(daily_totalAnsweredCallsLabel, 0, 0)
        daily_layout.addWidget(self.daily_TotalAnsweredCallsField, 0, 1)
        daily_layout.addWidget(daily_avgCallTimeLabel, 1, 0)
        daily_layout.addWidget(self.daily_AvgCallTimeField, 1, 1)
        daily_layout.addWidget(daily_avgLateTimeLabel, 2, 0)
        daily_layout.addWidget(self.daily_AvgLateTimeField, 2, 1)
        daily_layout.addWidget(daily_uptimeLabel, 3, 0)
        daily_layout.addWidget(self.daily_uptimeField, 3, 1)

        daily_groupBox.setLayout(daily_layout)
                                
        
        # --> weekly INDICATORS #
        
        weekly_groupBox = QGroupBox("Indicador Semanal")
        weekly_groupBox.setFont(groupBoxTitleFont)

        weekly_totalAnsweredCallsLabel = QIndicatorLabel("Chamados atendidos:")
        self.weekly_TotalAnsweredCallsField = MyQLineEdit()
        
        weekly_avgCallTimeLabel = QIndicatorLabel("Tempo médio de atendimento:")
        self.weekly_AvgCallTimeField = MyQLineEdit()
        
        weekly_avgLateTimeLabel = QIndicatorLabel("Tempo médio de atraso:")
        self.weekly_AvgLateTimeField = MyQLineEdit()
        
        weekly_uptimeLabel = QIndicatorLabel("Uptime de Teste:")
        self.weekly_uptimeField = MyQLineEdit("0,00%")
        
        weekly_layout = QGridLayout()
        weekly_layout.addWidget(weekly_totalAnsweredCallsLabel, 0, 0)
        weekly_layout.addWidget(self.weekly_TotalAnsweredCallsField, 0, 1)
        weekly_layout.addWidget(weekly_avgCallTimeLabel, 1, 0)
        weekly_layout.addWidget(self.weekly_AvgCallTimeField, 1, 1)
        weekly_layout.addWidget(weekly_avgLateTimeLabel, 2, 0)
        weekly_layout.addWidget(self.weekly_AvgLateTimeField, 2, 1)
        weekly_layout.addWidget(weekly_uptimeLabel, 3, 0)
        weekly_layout.addWidget(self.weekly_uptimeField, 3, 1)

        weekly_groupBox.setLayout(weekly_layout)
        
        # --> monthly INDICATORS #
        
        monthly_groupBox = QGroupBox("Indicador Mensal")
        monthly_groupBox.setFont(groupBoxTitleFont)

        monthly_totalAnsweredCallsLabel = QIndicatorLabel("Chamados atendidos:")
        self.monthly_TotalAnsweredCallsField = MyQLineEdit()
        
        monthly_avgCallTimeLabel = QIndicatorLabel("Tempo médio de atendimento:")
        self.monthly_AvgCallTimeField = MyQLineEdit()
        
        monthly_avgLateTimeLabel = QIndicatorLabel("Tempo médio de atraso:")
        self.monthly_AvgLateTimeField = MyQLineEdit()
        
        monthly_uptimeLabel = QIndicatorLabel("Uptime de Teste:")
        self.monthly_uptimeField = MyQLineEdit("0,00%")
        
        monthly_layout = QGridLayout()
        monthly_layout.addWidget(monthly_totalAnsweredCallsLabel, 0, 0)
        monthly_layout.addWidget(self.monthly_TotalAnsweredCallsField, 0, 1)
        monthly_layout.addWidget(monthly_avgCallTimeLabel, 1, 0)
        monthly_layout.addWidget(self.monthly_AvgCallTimeField, 1, 1)
        monthly_layout.addWidget(monthly_avgLateTimeLabel, 2, 0)
        monthly_layout.addWidget(self.monthly_AvgLateTimeField, 2, 1)
        monthly_layout.addWidget(monthly_uptimeLabel, 3, 0)
        monthly_layout.addWidget(self.monthly_uptimeField, 3, 1)

        monthly_groupBox.setLayout(monthly_layout)

        #############################
        ##### INDICATORS LAYOUT #####
        #############################
        
        reportLayout = QHBoxLayout()
        reportLayout.addWidget(daily_groupBox)
        reportLayout.addStretch(1)
        reportLayout.addWidget(weekly_groupBox)
        reportLayout.addStretch(1)
        reportLayout.addWidget(monthly_groupBox)

        #######################################
        ##### LIST CALLS SUBWINDOW LAYOUT #####
        #######################################
        
        layout = QVBoxLayout()
        layout.addLayout(button_layout) 
        layout.addWidget(self.openedCallsTable)
        layout.addLayout(reportLayout)
        layout.addStretch(1)

        # --> create the centralWidget of the QMdiSubWindow and set its layout #
        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setWidget(centralWidget)       

        # --> connecting the signals #
        self.openedCallsTable.itemSelectionChanged.connect(self.enableButtonAnswerCall)
        self.openedCallsTable.itemDoubleClicked.connect(self.openAnswerCallWindow)
        self.answerCallButton.clicked.connect(self.openAnswerCallWindow)
        self.updateTableButton.clicked.connect(self.updateOpenedCallsTable)


        # --> load the subwindow data #
        self.updateOpenedCallsTable()
        
        # --> creates a periodic event that will update the calls screen #
        self.updateTimer.timeout.connect(self.updateOpenedCallsTable)
        self.updateTimer.start(60000)
        
        self.setWindowIcon(QIcon(":/calls.png"))
        self.updateSubWindowTitle()
        
        # --> Line responsible for preventing window resize
        #self.layout().setSizeConstraint(QLayout.SetFixedSize)

###############################################################################################################################################################################
              
    def verifyIfUserAnsweringCall(self):
        """
        This method verifies if there is any call being answered by the user, preventing him from
        opening another calls, opening directly the call that is being answered by the user
        """

        try:
            call = self.callsList.verifyAnyCallBeingAnswered(self.loggedUser['id'])

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
            
            
###############################################################################################################################################################################
       
    def openAnswerCallWindow(self):
        """
        This method is called when a call is double clicked or the button "answer call" is clicked
        """
        call = self.currentRowCall()

        try:
            callLocked = call.isLockedCall()
        except DatabaseConnectionError as error:
            place, cause = error.args

            message = "Falha em: " + place + "\nErro: " +cause
        
            messageBox = QMessageBox()
            messageBox.setText(message)
            messageBox.setWindowTitle("Erro!")
            messageBox.setIcon(QMessageBox.Critical)
            messageBox.setWindowIcon(QIcon(":/warning_icon.png"))
            messageBox.exec_()
            return False
        
                
        if not callLocked:
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

###############################################################################################################################################################################
        
    def enableButtonAnswerCall(self):
        """
        This method is used to enable the button "Answer Call" if any call is selected
        """
        if len(self.openedCallsTable.selectedItems()):
            self.answerCallButton.setEnabled(True)
        else:
            self.answerCallButton.setEnabled(False)


###############################################################################################################################################################################
        
    def updateOpenedCallsTable(self):
        """
        This method updates the table that has the opened calls
        """

        # --> Try to load the calls. If any problem happen the program is terminated #

        try:
            self.callsList.loadCalls()

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

        self.openedCallsTable.clearContents()
        self.openedCallsTable.setRowCount(len(self.callsList))
        self.updateSubWindowTitle()
        self.verifyIfUserAnsweringCall()
        self.updateIndicators()

        # --> QFont That determinates the apearance of the text in the table #

        fontStyle = QFont()
        fontStyle.setBold(True)

        for row, call in enumerate(self.callsList):
            # --> Icone #
            iconLabel = QLabel()
            
            if call.insidePlan == 1:
                iconLabel.setPixmap(QIcon(":/red_icon.png").pixmap(QSize(30,30)))
                iconLabel.setToolTip("Produto está contido no plano de produção.")
                iconLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            elif call.insidePlan == 0:
                iconLabel.setPixmap(QIcon(":/yellow_icon.png").pixmap(QSize(30,30)))
                iconLabel.setToolTip("Produto NÃO está contido no plano de produção.")
                iconLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            else:
                iconLabel.setPixmap(QIcon(":/blue_icon.png").pixmap(QSize(30,30)))
                iconLabel.setToolTip("Chamado de melhoria.")
                iconLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

            self.openedCallsTable.setCellWidget(row, 0, iconLabel)
            
                        
            # --> Duração Total #
            item = QTableWidgetItem(call.formatedTotalDuration)
            item.setData(Qt.UserRole, int(call.callId))
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            item.setFont(fontStyle)
            if call.totalDuration is not None and call.totalDuration > 30:
                item.setForeground(Qt.red)
            elif call.totalDuration is not None and call.totalDuration < 0:
                item.setForeground(Qt.blue)
                
            self.openedCallsTable.setItem(row, 1, item)

            # --> Verifica se o chamado dentro do plano
            # está mais de 30 minutos aberto e não foi atendido para disparar email
            # if call.totalDuration is not None and call.totalDuration > 30:
            #     if call.callId not in self.emailSentForCalls:
            #         self.sendEmailLateCalls(call)  # Aqui passamos o objeto 'call' como argumento
            #         self.emailSentForCalls.add(call.callId)

            # --> Duração Atendimento #
            if call.status != "ABERTO":
                item = QTableWidgetItem(call.formatedAnswerDuration)
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                item.setFont(fontStyle)
                if call.answerDuration and call.answerDuration > 30:
                    item.setForeground(Qt.red)
                self.openedCallsTable.setItem(row, 2, item)

            # --> Aberto por #
            item = QTableWidgetItem(call.creator)
            self.openedCallsTable.setItem(row, 3, item)
        
            # --> Tipo de Chamado #
            item = QTableWidgetItem(call.callType)
            self.openedCallsTable.setItem(row, 4, item)

            # --> Local #
            item = QTableWidgetItem(call.location)
            self.openedCallsTable.setItem(row, 5, item)

            # --> Cliente #
            item = QTableWidgetItem(call.client)
            self.openedCallsTable.setItem(row, 6, item)

            # --> Produto #
            item = QTableWidgetItem(call.product)
            item.setSizeHint(QSize(100, 0))
            self.openedCallsTable.setItem(row, 7, item)

            # --> Status #
            item = QTableWidgetItem(call.status)
            self.openedCallsTable.setItem(row, 8, item)

            # --> Suporte Responsável #
            item = QTableWidgetItem(call.support)
            item.setSizeHint(QSize(160, 0))
            self.openedCallsTable.setItem(row, 9, item)

            # --> Descrição do Chamado #
            item = QTableWidgetItem(call.description)
            self.openedCallsTable.setItem(row, 10, item)

            self.openedCallsTable.setRowHeight(row, 40)


###############################################################################################################################################################################

    def sendEmailLateCalls(self, call):
        # Configurações do servidor SMTP do Outlook (Office 365)
        smtp_server = 'smtp.office365.com'
        smtp_port = 587  # A porta padrão para TLS (STARTTLS)
        smtp_username = 'marcos.souza@hi-mix.com.br'
        smtp_password = '00@So@82'

        from_addr = 'marcos.souza@hi-mix.com.br'
        to_addrs = ['marcostullio.s@gmail.com']

        # Criar uma mensagem multipart (texto e HTML)
        message = MIMEMultipart()
        message['From'] = from_addr
        message['To'] = ', '.join(to_addrs)
        message['Subject'] = 'Aviso de Atraso no Atendimento de Chamado de Teste'

        # Adicionar corpo de texto ao e-mail, usando os atributos do objeto 'call'
        message.attach(MIMEText(f'Prezados,\n\nInformo que o chamado referente ao teste do produto '
                                f'{call.product} do cliente {call.client} ainda não foi atendido '
                                f'e está em aberto há {call.totalDuration} horas. \n\nAtenciosamente,', 'plain'))
        # Conectar ao servidor SMTP
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Ativar o TLS (STARTTLS)
        server.login(smtp_username, smtp_password)

        # Enviar e-mail
        server.sendmail(from_addr, to_addrs, message.as_string())

        # Encerrar a conexão com o servidor
        server.quit()


###############################################################################################################################################################################

    def updateSubWindowTitle(self):
        """
        This method is used to update the window title with the total number of opened calls
        """
        if len(self.callsList) != 1:
            self.setWindowTitle("Suporte à Linha - %d Chamados Abertos" % len(self.callsList))
        else:
            self.setWindowTitle("Suporte à Linha - 1 Chamado Aberto")

###############################################################################################################################################################################

    def updateIndicators(self):
        """
        this method is used to update the indicators through the CallIndicators class
        """

        try:
            self.indicators.loadIndicators()
            
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

        self.daily_TotalAnsweredCallsField.setText(str(self.indicators.dailyTotalCalls))
        self.daily_AvgCallTimeField.setText(self.indicators.dailyAvgAnswering)
        self.daily_AvgLateTimeField.setText(self.indicators.dailyAvgLate)
        self.daily_uptimeField.setText(self.indicators.dailyUpTime.replace(".", ","))

        self.weekly_TotalAnsweredCallsField.setText(str(self.indicators.weeklyTotalCalls))
        self.weekly_AvgCallTimeField.setText(self.indicators.weeklyAvgAnswering)
        self.weekly_AvgLateTimeField.setText(self.indicators.weeklyAvgLate)
        self.weekly_uptimeField.setText(self.indicators.weeklyUpTime.replace(".", ","))

        self.monthly_TotalAnsweredCallsField.setText(str(self.indicators.monthlyTotalCalls))
        self.monthly_AvgCallTimeField.setText(self.indicators.monthlyAvgAnswering)
        self.monthly_AvgLateTimeField.setText(self.indicators.monthlyAvgLate)
        self.monthly_uptimeField.setText(self.indicators.monthlyUpTime.replace(".", ","))
        
###############################################################################################################################################################################

    def currentRowCall(self):
        """
        This method returns the current selected row
        """
        row = self.openedCallsTable.currentRow()
        if row > -1:
            item = self.openedCallsTable.item(row, 1)
            key = item.data(Qt.UserRole)
            return self.callsList.callFromId(key)

        return None

###############################################################################################################################################################################

    def showEvent(self, event):
        """
        This method is called when the listcalls subwindow is opened
        """
        self.verifyIfUserAnsweringCall()

###############################################################################################################################################################################

    def closeEvent(self, event):
        """
        This method remove its reference from its parent opened sub window list before being closed
        """
        del self.parent.openedSubWindows[self.SUBWINDOWID]
        self.close()
