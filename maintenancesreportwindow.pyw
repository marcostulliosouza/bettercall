from PyQt5.QtCore import (
        Qt,
        QTimer,
        QDate,
        QSize
    )

from PyQt5.QtGui import (
        QFont,
        QIcon,
        QPalette,
        QCursor
    )

from PyQt5.QtWidgets import (
        QMdiSubWindow,
        QGroupBox,
        QLabel,
        QDateEdit,
        QCalendarWidget,
        QLineEdit,
        QComboBox,
        QSpacerItem,
        QCheckBox,
        QPushButton,
        QLayout,
        QHBoxLayout,
        QVBoxLayout,
        QTableWidget,
        QAbstractScrollArea,
        QTableWidgetItem,
        QHeaderView,
        QWidget,
        QFileDialog,
        QMessageBox
    )

from myExceptions import *
import maintenancesreportcontainer

__version__ = "1.0.0"

###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################

class MyQLabel(QLabel):
    """
    This class reimplements the qlabel class
    """
    def __init__(self, text="", parent=None):
        super(MyQLabel, self).__init__(text, parent)
        boldFont = QFont()
        boldFont.setBold(True)

        self.setFixedWidth(110)
        self.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.setFont(boldFont)


###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################
class MyQDateEdit(QDateEdit):
    """
    This class reimplements the qdateedit class
    """
    def __init__(self, date=None, parent=None):
        super(MyQDateEdit, self).__init__(parent)

        calendarStylesheet = "QCalendarWidget QWidget#qt_calendar_navigationbar :hover{"\
                     "          font-weight: bold;" \
                     "          color: white;}" \
                     "QCalendarWidget QWidget#qt_calendar_navigationbar{"\
                     "          font-weight: bold;" \
                     "          color: white;" \
                     "          background-color: qlineargradient( " \
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
                     "                      stop: 1 #131313);}" \
                     "QCalendarWidget QWidget{"\
                     "          font-weight: bold;" \
                     "          selection-background-color: qlineargradient( " \
                     "                      x1:0, " \
                     "                      y1:0, " \
                     "                      x2:0, " \
                     "                      y2:1, " \
                     "                      stop:0 #7C7C7C, " \
                     "                      stop: 0.12 #898989, " \
                     "                      stop: 0.25 #999999, " \
                     "                      stop: 0.39 #777777, " \
                     "                      stop: 0.5 #5C5C5C, " \
                     "                      stop: 0.51 #333333, " \
                     "                      stop: 0.60 #444444, " \
                     "                      stop: 0.76 #5B5B5B, " \
                     "                      stop: 0.91 #4C4C4C, " \
                     "                      stop: 1 #434343);}"

        self.setCalendarPopup(True)
        self.setDisplayFormat("dd/MM/yyyy")
        self.calendarWidget().setHorizontalHeaderFormat(QCalendarWidget.NoHorizontalHeader)
        self.calendarWidget().setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.setStyleSheet(calendarStylesheet)
        self.setFocusPolicy(Qt.NoFocus)

        if date:
            self.setDate(date)


###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################

class MyQPushButton(QPushButton):
    """
    This class reimplements the qpushbutton class
    """
    def __init__(self, text="", parent=None):
        super(MyQPushButton, self).__init__(text, parent)

        regularFont = QFont()
        regularFont.setBold(False)

        self.setMinimumWidth(98)
        self.setFont(regularFont)
        self.setCursor(QCursor(Qt.PointingHandCursor))


###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################

class MyQLineEdit(QLineEdit):
    """
    This class reimplements the qlineedit class
    """
    def __init__(self, parent=None):
        super(MyQLineEdit, self).__init__(parent)

        regularFont = QFont()
        regularFont.setBold(False)
        
        self.setMinimumWidth(204)
        self.setFont(regularFont)

        
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
        self.setEditTriggers(QTableWidget.NoEditTriggers)
        self.setSelectionBehavior(QTableWidget.SelectRows)
        self.setSelectionMode(QTableWidget.SingleSelection)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.horizontalHeader().setStretchLastSection(True)
        self.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.horizontalHeader().setHighlightSections(False)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.setMinimumSize(QSize(870, 400))
        self.verticalHeader().setVisible(False)

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

        self.horizontalHeader().setStyleSheet(tableStylesheet)

        # --> Create the Items for the headers #
        self.setColumnCount(6)
        
        dateMaintenance = QTableWidgetItem("Data da Manutenção")
        totalDuration = QTableWidgetItem("Duração (min)")
        support = QTableWidgetItem("Suporte Responsável")
        dtDevice = QTableWidgetItem("Código do Dispositivo")
        deviceDescription = QTableWidgetItem("Descrição do Dispositivo")
        observation = QTableWidgetItem("Observação")



        # --> Set the Header Items #
        self.setHorizontalHeaderItem(0, dateMaintenance)
        self.setHorizontalHeaderItem(1, totalDuration)
        self.setHorizontalHeaderItem(2, support)
        self.setHorizontalHeaderItem(3, dtDevice)
        self.setHorizontalHeaderItem(4, deviceDescription)
        self.setHorizontalHeaderItem(5, observation)

        self.horizontalHeader().resizeSection(0, 150)
        self.horizontalHeader().resizeSection(1, 120)
        self.horizontalHeader().resizeSection(2, 150)
        self.horizontalHeader().resizeSection(3, 150)
        self.horizontalHeader().resizeSection(4, 150)
        self.horizontalHeader().resizeSection(5, 400)


###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################

class MaintenancesReportWindow(QMdiSubWindow):
    """
    This class is responsible for rendering the "Listar Manutenções" window
    as a MDI sub Window and for managing the data inside it
    """
    # --> Constant id, used for location inside the openedSubWindows dictionary in the main window #
    SUBWINDOWID = "maintenancesreportwindow"
    
    def __init__(self, parent=None):
        super(MaintenancesReportWindow, self).__init__(parent)
        self.parent = parent
        self.loggedUser = parent.loggedUser
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowFlags(Qt.SubWindow | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)

        self.maintenancesList = maintenancesreportcontainer.MaintenanceContainer()

        self.userAnsweringCall = False

        
        self.updateTimer = QTimer()

        self.isFiltering = False
        self.filteringFields = []

        ################################################
        # --> Build the "Relatório de Manutenção" window #
        ################################################

        # --> Building the filter groupbox #
        boldFont = QFont()
        boldFont.setBold(True)

        regularFont = QFont()
        regularFont.setBold(False)
        
        filterGroupBox = QGroupBox("Filtro")
        filterGroupBox.setFont(boldFont)

        # --> Maintenance Date #

        dateMaintenanceLabel = MyQLabel("Período: ")

                        
        self.fromDateField = MyQDateEdit(QDate.currentDate().addMonths(-1))
        
        untilLabel = QLabel(" até ")
        untilLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        untilLabel.setMinimumWidth(30)

        self.untilDateField = MyQDateEdit(QDate.currentDate())

        # --> Support #
        
        supportLabel = MyQLabel("Colaborador: ")
        self.filterSupportField = MyQLineEdit()
        
        # --> DT Device #
        dtDeviceLabel = MyQLabel("DT: ")
        self.filterDtDeviceField = MyQLineEdit()
        
        # --> Device Description #

        deviceDescriptionLabel = MyQLabel("Dispositivo: ")
        self.filterDeviceDescriptionField = MyQLineEdit()

        # --> Buttons #

        clearFilterButton = MyQPushButton(" Limpar ")
        filterButton = MyQPushButton(" Filtrar ")
        saveButton = MyQPushButton(" Salvar ")

        
        # --> First row layout #
        firstRowFilterLayout = QHBoxLayout()

        firstRowFilterLayout.addWidget(dateMaintenanceLabel)
        firstRowFilterLayout.addWidget(self.fromDateField)
        firstRowFilterLayout.addWidget(untilLabel)
        firstRowFilterLayout.addWidget(self.untilDateField)
        firstRowFilterLayout.addWidget(supportLabel)
        firstRowFilterLayout.addWidget(self.filterSupportField)
        firstRowFilterLayout.addWidget(dtDeviceLabel)
        firstRowFilterLayout.addWidget(self.filterDtDeviceField)
        firstRowFilterLayout.addStretch(1)

        # --> Second row Layout #
        secondRowFilterLayout = QHBoxLayout()

        secondRowFilterLayout.addWidget(deviceDescriptionLabel)
        secondRowFilterLayout.addWidget(self.filterDeviceDescriptionField)

         
        # --> Third row Layout #
        thirdRowFilterLayout = QHBoxLayout()

        thirdRowFilterLayout.addStretch(1)
        thirdRowFilterLayout.addWidget(clearFilterButton)
        thirdRowFilterLayout.addWidget(filterButton)
        thirdRowFilterLayout.addWidget(saveButton)


        # --> Filter groupbox layout #
        filterLayout = QVBoxLayout()
        filterLayout.addLayout(firstRowFilterLayout)
        filterLayout.addLayout(secondRowFilterLayout)
        filterLayout.addLayout(thirdRowFilterLayout)


        filterGroupBox.setLayout(filterLayout)

        ##################################
        # --> Table having all the Maintenance #
        ##################################
        
        self.maintenancesTable = MyQTableWidget()
         
        # --> Build the listMaintenance Subwindow #
        
        layout = QVBoxLayout()
        layout.addWidget(filterGroupBox) 
        layout.addWidget(self.maintenancesTable)
        layout.addStretch(1)

        # --> Create the centralWidget of the QMdiSubWindow and set its layout #
        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setWidget(centralWidget)       

        # --> Connecting the signals #
        # self.maintenancesTable.itemDoubleClicked.connect(self.openDetailedCallReportWindow)
        clearFilterButton.clicked.connect(self.clearFilter)
        filterButton.clicked.connect(self.filterTable)
        # saveButton.clicked.connect(self.saveReport)

        # --> Load the subwindow data #
        self.updateMaintenancesTable()

        # --> Creates a periodic event that will uplode the calls screen #
        self.updateTimer.timeout.connect(self.updateMaintenancesTable)
        self.updateTimer.start(60000)
        
        self.setWindowIcon(QIcon(":/prod_plan_2.png"))
        self.updateSubWindowTitle()

        # --> Line responsible for preventing window resize
        #self.layout().setSizeConstraint(QLayout.SetFixedSize)
        
###############################################################################################################################################################################


    def clearFilter(self):
        """
        This method is called when the button "Limpar" is clicked, cleaning the filter fields
        """
        self.isFiltering = False
        self.filteringFields = []

        self.fromDateField.setDate(QDate.currentDate().addMonths(-1))
        self.untilDateField.setDate(QDate.currentDate())

        self.filterSupportField.setText("")
        self.filterDtDeviceField.setText("")
        self.filterDeviceDescriptionField.setText("")


        self.updateMaintenancesTable()

# ###############################################################################################################################################################################
#

    def filterTable(self):
        """
        This method is called when the button "Filtrar" is clicked, creating the fields list
        that will be passed to the updateCallsTable
        """
        self.filteringFields = []

        fromDate = self.fromDateField.text().split("/")
        untilDate = self.untilDateField.text().split("/")

        self.filteringFields.append("DATE(lmd_data_hora_inicio) >= DATE('" + fromDate[2] + "-" + fromDate[1] + "-" + fromDate[0] + "')")
        self.filteringFields.append("DATE(lmd_data_hora_inicio) <= DATE('" + untilDate[2] + "-" + untilDate[1] + "-" + untilDate[0] + "')")


        if self.filterSupportField.text():
            self.filteringFields.append("col_nome LIKE '%" + self.filterSupportField.text() + "%'")

        if self.filterDtDeviceField.text():
            self.filteringFields.append("dis_id LIKE '%" + self.filterDtDeviceField.text() + "%'")

        if self.filterDeviceDescriptionField.text():
            self.filteringFields.append("dis_descricao LIKE '%" + self.filterDeviceDescriptionField.text() + "%'")

        if len(self.filteringFields):
            self.isFiltering = True
        else:
            self.isFiltering = False


        self.updateMaintenancesTable()
#
# ###############################################################################################################################################################################
#
#
#     # def openDetailedCallReportWindow(self):
#         """
#         This method is called when a call is double clicked or the button "answer call" is clicked
#         """
#         call = self.currentRowCall()
#
#         detailedCallReportWindow = detailedcallreportwindow.DetailedCallReportWindow(call, self)
#         detailedCallReportWindow.setModal(True)
#
#         detailedCallReportWindow.show()
#
#         xPos = (self.parent.screenResolution['w'] - detailedCallReportWindow.width()) / 2
#         yPos = (self.parent.screenResolution['h'] - detailedCallReportWindow.height()) / 2
#
#         detailedCallReportWindow.move(xPos, yPos)
#         detailedCallReportWindow.raise_()
#         detailedCallReportWindow.activateWindow()


###############################################################################################################################################################################

    def updateMaintenancesTable(self):
        """
        This method updates the table that has the opened maintenance
        """

        try:
            self.maintenancesList.loadMaintenances(self.isFiltering, self.filteringFields)
        except DatabaseConnectionError as error:
            place, cause = error.args

            message = "Falha em: " + place + "\nErro: " + cause

            messageBox = QMessageBox()
            messageBox.setText(message)
            messageBox.setWindowTitle("Erro!")
            messageBox.setIcon(QMessageBox.Critical)
            messageBox.setWindowIcon(QIcon(":/warning_icon.png"))
            messageBox.exec_()
            self.parent.close()
            return

        self.maintenancesTable.clearContents()
        self.maintenancesTable.setRowCount(len(self.maintenancesList))
        self.updateSubWindowTitle()

        # --> QFont That determinates the apearance of the text in the table #
        fontStyle = QFont()
        fontStyle.setBold(True)

        for row, maintenance in enumerate(self.maintenancesList):

            # --> Begin Date #
            item = QTableWidgetItem(str(maintenance.maintenance_log_inicio))
            item.setData(Qt.UserRole, int(maintenance.maintenance_log_id))
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.maintenancesTable.setItem(row, 0, item)

            # --> Total Duration #
            item = QTableWidgetItem(maintenance.maintenance_log_duracao_total)
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            item.setFont(fontStyle)
            if maintenance.maintenance_log_duracao_total and maintenance.maintenance_log_duracao_total > 30:
                item.setForeground(Qt.red)
            elif maintenance.maintenance_log_duracao_total and maintenance.maintenance_log_duracao_total < 0:
                item.setForeground(Qt.blue)
            self.maintenancesTable.setItem(row, 1, item)

            # --> Responsible #
            item = QTableWidgetItem(maintenance.colaborador_nome)
            self.maintenancesTable.setItem(row, 2, item)

            # --> DT #
            item = QTableWidgetItem(maintenance.dispositivo_id)
            self.maintenancesTable.setItem(row, 3, item)

            # --> descricao_dispositivo #
            item = QTableWidgetItem(maintenance.dispositivo_descricao)
            self.maintenancesTable.setItem(row, 4, item)

            # --> observacao #
            item = QTableWidgetItem(maintenance.maintenance_log_observacao)
            self.maintenancesTable.setItem(row, 5, item)



###############################################################################################################################################################################


    def updateSubWindowTitle(self):
        """
        This method is used to update the window title with the total number of opened calls
        """
        if len(self.maintenancesList) != 1:
            self.setWindowTitle("Relatório de Manutenção Preventiva - %d Atendimentos" % len(self.maintenancesList))
        else:
            self.setWindowTitle("Relatório de Manutenção Preventiva - 1 Atendimento")



###############################################################################################################################################################################
   
   
    def closeEvent(self, event):
        """
        This method remove its reference from its parent opened sub window list before being closed
        """
        del self.parent.openedSubWindows[self.SUBWINDOWID]
        self.close()
