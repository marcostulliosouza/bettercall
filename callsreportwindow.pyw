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
import callscontainer
import detailedcallreportwindow

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

class MyQCheckBox(QCheckBox):
    """
    This class reimplements the qcheckbox class
    """
    def __init__(self, text="", parent=None):
        super(MyQCheckBox, self).__init__(text, parent)

        self.setMinimumWidth(258)
        self.setChecked(True)

###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################

class MyQComboBox(QComboBox):
    """
    This class reimplements the qcombobox class
    """
    def __init__(self, parent=None):
        super(MyQComboBox, self).__init__(parent)

        regularFont = QFont()
        regularFont.setBold(False)
        
        self.setMinimumWidth(200)
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
        self.setColumnCount(11)
        
        openingDate = QTableWidgetItem("Data de Abertura")
        totalDuration = QTableWidgetItem("Duração Total")
        answerDuration = QTableWidgetItem("Atendimento")
        openedBy = QTableWidgetItem("Criado Por")
        callType = QTableWidgetItem("Tipo de Chamado")
        callLocal = QTableWidgetItem("Local")
        client = QTableWidgetItem("Cliente")
        product = QTableWidgetItem("Produto")
        status = QTableWidgetItem("Status")
        detractor = QTableWidgetItem("Detrator")
        support  = QTableWidgetItem("Suporte Responsável")

        # --> Set the Header Items #
        self.setHorizontalHeaderItem(0, openingDate)
        self.setHorizontalHeaderItem(1, totalDuration)
        self.setHorizontalHeaderItem(2, answerDuration)
        self.setHorizontalHeaderItem(3, openedBy)
        self.setHorizontalHeaderItem(4, callType)
        self.setHorizontalHeaderItem(5, callLocal)
        self.setHorizontalHeaderItem(6, client)
        self.setHorizontalHeaderItem(7, product)
        self.setHorizontalHeaderItem(8, status)
        self.setHorizontalHeaderItem(9, detractor)
        self.setHorizontalHeaderItem(10, support)

        self.horizontalHeader().resizeSection(0, 120)
        self.horizontalHeader().resizeSection(1, 100)
        self.horizontalHeader().resizeSection(2, 100)
        self.horizontalHeader().resizeSection(3, 120)
        self.horizontalHeader().resizeSection(4, 130)
        self.horizontalHeader().resizeSection(5, 100)
        self.horizontalHeader().resizeSection(6, 150)
        self.horizontalHeader().resizeSection(7, 150)
        self.horizontalHeader().resizeSection(8, 100)
        self.horizontalHeader().resizeSection(9, 200)
        self.horizontalHeader().resizeSection(10, 200)


###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################


class CallsReportWindow(QMdiSubWindow):
    """
    This class is responsible for rendering the "Listar Chamados" window
    as a MDI sub Window and for managing the data inside it
    """
    # --> Constant id, used for location inside the openedSubWindows dictionary in the main window #
    SUBWINDOWID = "callsreportwindow"
    
    def __init__(self, parent=None):
        super(CallsReportWindow, self).__init__(parent)
        self.parent = parent
        self.loggedUser = parent.loggedUser
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowFlags(Qt.SubWindow | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)

        self.indicators = callscontainer.CallIndicators()
        

        self.userAnsweringCall = False
        
        self.callsList = callscontainer.CallContainer()
        
        self.updateTimer = QTimer()

        self.isFiltering = False
        self.filteringFields = []

        ################################################
        # --> Build the "Relatório de Chamados" window #
        ################################################

        # --> Building the filter groupbox #
        boldFont = QFont()
        boldFont.setBold(True)

        regularFont = QFont()
        regularFont.setBold(False)
        
        filterGroupBox = QGroupBox("Filtro")
        filterGroupBox.setFont(boldFont)

        # --> Opening Date #

        openingDatetime = MyQLabel("Data de Abertura: ")
                        
        self.fromDateField = MyQDateEdit(QDate.currentDate().addDays(-1))
        
        untilLabel = QLabel(" até ")
        untilLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        untilLabel.setMinimumWidth(30)

        self.untilDateField = MyQDateEdit(QDate.currentDate())

        # --> Client #
        
        clientLabel = MyQLabel("Cliente: ")        
        self.filterClientField = MyQLineEdit()
        
        # --> Product #
        productLabel = MyQLabel("Produto: ")        
        self.filterProductField = MyQLineEdit()
        
        # --> Created By #

        callCreatorLabel = MyQLabel("Criado Por: ")        
        self.callCreatorField = MyQLineEdit()
       
        # --> Type #

        callTypeLabel = MyQLabel("Tipo: ")
        
        self.callTypeComboBox = MyQComboBox()
        self.populateCallTypesComboBox()

        # --> Status #
        statusLabel = MyQLabel("Status: ")
       
        self.callStatusComboBox = MyQComboBox()
        self.populateCallStatusComboBox()

        # --> Responsible #

        responsibleLabel = MyQLabel("Responsável: ")
        
        self.responsibleField = QLineEdit()
        self.responsibleField.setMinimumWidth(200)
        self.responsibleField.setFont(regularFont)

        # --> Checkboxes #
        self.insidePlanCheckBox = MyQCheckBox("Dentro do Plano de Produção")
        self.insidePlanCheckBox.setMinimumWidth(374)
        
        self.outsidePlanCheckBox = MyQCheckBox("Fora do Plano de Produção")
        self.outsidePlanCheckBox.setMinimumWidth(374)

        self.withDetractorCheckBox = MyQCheckBox("Com Detrator")
        
        self.withoutDetractorCheckBox = MyQCheckBox("Sem Detrator")
        
        # --> Buttons #

        clearFilterButton = MyQPushButton(" Limpar ")
        filterButton = MyQPushButton(" Filtrar ")
        saveButton = MyQPushButton(" Salvar ")

        
        # --> First row layout #
        firstRowFilterLayout = QHBoxLayout()
        
        firstRowFilterLayout.addWidget(openingDatetime)
        firstRowFilterLayout.addWidget(self.fromDateField)
        firstRowFilterLayout.addWidget(untilLabel)
        firstRowFilterLayout.addWidget(self.untilDateField)
        firstRowFilterLayout.addWidget(clientLabel)
        firstRowFilterLayout.addWidget(self.filterClientField)
        firstRowFilterLayout.addWidget(callTypeLabel)
        firstRowFilterLayout.addWidget(self.callTypeComboBox)
        firstRowFilterLayout.addStretch(1)

        # --> Second row Layout #
        secondRowFilterLayout = QHBoxLayout()
        
        secondRowFilterLayout.addWidget(callCreatorLabel)
        secondRowFilterLayout.addWidget(self.callCreatorField)
        secondRowFilterLayout.addWidget(productLabel)
        secondRowFilterLayout.addWidget(self.filterProductField)
        secondRowFilterLayout.addWidget(statusLabel)
        secondRowFilterLayout.addWidget(self.callStatusComboBox)
        secondRowFilterLayout.addStretch(1)

         
        # --> Third row Layout #
        thirdRowFilterLayout = QHBoxLayout()
        
        thirdRowFilterLayout.addWidget(self.insidePlanCheckBox)
        thirdRowFilterLayout.addWidget(self.withDetractorCheckBox)
        thirdRowFilterLayout.addStretch(1)
        thirdRowFilterLayout.addWidget(responsibleLabel)
        thirdRowFilterLayout.addWidget(self.responsibleField)

       
        # --> Fourth row Layout #
        fourthRowFilterLayout = QHBoxLayout()
        
        fourthRowFilterLayout.addWidget(self.outsidePlanCheckBox)
        fourthRowFilterLayout.addWidget(self.withoutDetractorCheckBox)
        fourthRowFilterLayout.addStretch(1)
        fourthRowFilterLayout.addWidget(clearFilterButton)
        fourthRowFilterLayout.addWidget(filterButton)
        fourthRowFilterLayout.addWidget(saveButton)


        # --> Filter groupbox layout #
        filterLayout = QVBoxLayout()
        filterLayout.addLayout(firstRowFilterLayout)
        filterLayout.addLayout(secondRowFilterLayout)
        filterLayout.addLayout(thirdRowFilterLayout)
        filterLayout.addLayout(fourthRowFilterLayout)


        filterGroupBox.setLayout(filterLayout)

        ##################################
        # --> Table having all the calls #
        ##################################
        
        self.callsTable = MyQTableWidget()
         
        # --> Build the listCalls Subwindow #
        
        layout = QVBoxLayout()
        layout.addWidget(filterGroupBox) 
        layout.addWidget(self.callsTable)
        layout.addStretch(1)

        # --> Create the centralWidget of the QMdiSubWindow and set its layout #
        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setWidget(centralWidget)       

        # --> Connecting the signals #
        self.callsTable.itemDoubleClicked.connect(self.openDetailedCallReportWindow)
        clearFilterButton.clicked.connect(self.clearFilter)
        filterButton.clicked.connect(self.filterTable)
        saveButton.clicked.connect(self.saveReport)
        self.insidePlanCheckBox.toggled.connect(self.insideCheckboxChecker)
        self.outsidePlanCheckBox.toggled.connect(self.outsideCheckboxChecker)

        self.withDetractorCheckBox.toggled.connect(self.withDetractorChecker)
        self.withoutDetractorCheckBox.toggled.connect(self.withoutDetractorChecker)

        # --> Load the subwindow data #
        self.updateCallsTable()

        # --> Creates a periodic event that will uplode the calls screen #
        self.updateTimer.timeout.connect(self.updateCallsTable)
        self.updateTimer.start(60000)
        
        self.setWindowIcon(QIcon(":/calls_report_2.png"))
        self.updateSubWindowTitle()

        # --> Line responsible for preventing window resize
        #self.layout().setSizeConstraint(QLayout.SetFixedSize)
        
###############################################################################################################################################################################


    def populateCallTypesComboBox(self):
        """
        This method is responsible for loading the calls types into the Call Types Combobox
        """
        
        callTypesList = callscontainer.CallTypeContainer()

        try:
            callTypesList.loadCallTypes()
        except DatabaseConnectionError as error:
            message = "Falha em: " + place + "\nErro: " +cause
            messageBox = QMessageBox()
            messageBox.setText(message)
            messageBox.setWindowTitle("Erro!")
            messageBox.setIcon(QMessageBox.Critical)
            messageBox.setWindowIcon(QIcon(":/warning_icon.png"))
            messageBox.exec_()
            return


        self.callTypeComboBox.addItem("TODOS", 0)

        for callType in callTypesList:
            self.callTypeComboBox.addItem(callType.callTypeDescription, callType.callTypeId)
       

###############################################################################################################################################################################


    def populateCallStatusComboBox(self):
        """
        This method is responsible for loading the calls status into the Calls Status Combobox
        """
        callStatusList = callscontainer.CallStatusContainer()

        try:
            callStatusList.loadCallStatus()
        except DatabaseConnectionError as error:
            message = "Falha em: " + place + "\nErro: " +cause
            messageBox = QMessageBox()
            messageBox.setText(message)
            messageBox.setWindowTitle("Erro!")
            messageBox.setIcon(QMessageBox.Critical)
            messageBox.setWindowIcon(QIcon(":/warning_icon.png"))
            messageBox.exec_()
            return
        
        self.callStatusComboBox.addItem("TODOS", 0)

        for callStatus in callStatusList:
            self.callStatusComboBox.addItem(callStatus.callStatusDescription, callStatus.callStatusId)


###############################################################################################################################################################################

    def withDetractorChecker(self, wasChecked):
        """
        This method is called when any of the checkbox in the filter is clicked
        don't allowing both to be unchecked
        """
        if not wasChecked:
            if not self.withoutDetractorCheckBox.isChecked():
                self.withDetractorCheckBox.setChecked(True)

###############################################################################################################################################################################

    def withoutDetractorChecker(self, wasChecked):
        """
        This method is called when any of the checkbox in the filter is clicked
        don't allowing both to be unchecked
        """
        if not wasChecked:
            if not self.withDetractorCheckBox.isChecked():
                self.withoutDetractorCheckBox.setChecked(True)
        
###############################################################################################################################################################################
        

    def insideCheckboxChecker(self, wasChecked):
        """
        This method is called when any of the checkbox in the filter is clicked
        don't allowing both to be unchecked
        """
        if not wasChecked:
            if not self.outsidePlanCheckBox.isChecked():
                self.insidePlanCheckBox.setChecked(True)


###############################################################################################################################################################################


    def outsideCheckboxChecker(self, wasChecked):
        """
        This method is called when any of the check box in the filter is clicked
        don't allowing both to be unchecked
        """
        if not wasChecked:
            if not self.insidePlanCheckBox.isChecked():
                self.outsidePlanCheckBox.setChecked(True)


###############################################################################################################################################################################


    def clearFilter(self):
        """
        This method is called when the button "Limpar" is clicked, cleaning the filter fields
        """
        self.isFiltering = False
        self.filteringFields = []        
        
        self.fromDateField.setDate(QDate.currentDate().addDays(-1))
        self.untilDateField.setDate(QDate.currentDate())
        
        self.filterClientField.setText("")
        self.filterProductField.setText("")
        self.callCreatorField.setText("")
        self.responsibleField.setText("")

        self.callTypeComboBox.setCurrentIndex(0)
        self.callStatusComboBox.setCurrentIndex(0)

        self.insidePlanCheckBox.setChecked(True)
        self.outsidePlanCheckBox.setChecked(True)

        self.withDetractorCheckBox.setChecked(True)
        self.withoutDetractorCheckBox.setChecked(True)

        self.updateCallsTable()

###############################################################################################################################################################################

        
    def filterTable(self):
        """
        This method is called when the button "Filtrar" is clicked, creating the fields list
        that will be passed to the updateCallsTable
        """
        self.filteringFields = []

        fromDate = self.fromDateField.text().split("/")
        untilDate = self.untilDateField.text().split("/")

        self.filteringFields.append("DATE(cha_data_hora_abertura) >= DATE('" + fromDate[2] + "-" + fromDate[1] + "-" + fromDate[0] + "')")
        self.filteringFields.append("DATE(cha_data_hora_abertura) <= DATE('" + untilDate[2] + "-" + untilDate[1] + "-" + untilDate[0] + "')")

        
        if self.filterClientField.text():
            self.filteringFields.append("cli_nome LIKE '%" + self.filterClientField.text() + "%'")

        if self.filterProductField.text():
            self.filteringFields.append("pro_nome LIKE '%" + self.filterProductField.text() + "%'")

        if self.callCreatorField.text():
            self.filteringFields.append("cha_operador LIKE '%" + self.callCreatorField.text() + "%'")

        if not self.insidePlanCheckBox.isChecked():
            self.filteringFields.append("cha_plano = '0'")
        elif not self.outsidePlanCheckBox.isChecked():
            self.filteringFields.append("cha_plano = '1'")

        if not self.withDetractorCheckBox.isChecked():
            self.filteringFields.append("dtr_indicador = '0'")
        elif not self.withoutDetractorCheckBox.isChecked():
            self.filteringFields.append("dtr_indicador = '1'")

       
        if self.callTypeComboBox.currentIndex() > 0:
            self.filteringFields.append("cha_tipo = '" +str(self.callTypeComboBox.itemData(self.callTypeComboBox.currentIndex()))+ "'")

        if self.callStatusComboBox.currentIndex() > 0:
            self.filteringFields.append("cha_status = '" +str(self.callStatusComboBox.itemData(self.callStatusComboBox.currentIndex()))+ "'")

        

        if self.responsibleField.text():
            self.filteringFields.append("col_nome LIKE '%" + self.responsibleField.text() + "%'")

        if len(self.filteringFields):
            self.isFiltering = True
        else:
            self.isFiltering = False
            

        self.updateCallsTable()

###############################################################################################################################################################################
        
        
    def openDetailedCallReportWindow(self):
        """
        This method is called when a call is double clicked or the button "answer call" is clicked
        """
        call = self.currentRowCall()

        detailedCallReportWindow = detailedcallreportwindow.DetailedCallReportWindow(call, self)
        detailedCallReportWindow.setModal(True)

        detailedCallReportWindow.show()
          
        xPos = (self.parent.screenResolution['w'] - detailedCallReportWindow.width()) / 2
        yPos = (self.parent.screenResolution['h'] - detailedCallReportWindow.height()) / 2
            
        detailedCallReportWindow.move(xPos, yPos)
        detailedCallReportWindow.raise_()
        detailedCallReportWindow.activateWindow()


###############################################################################################################################################################################
        
        
    def updateCallsTable(self):
        """
        This method updates the table that has the opened calls
        """

        try:
            self.callsList.loadCallsReport(self.isFiltering, self.filteringFields)
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
        


        self.callsTable.clearContents()
        self.callsTable.setRowCount(len(self.callsList))
        self.updateSubWindowTitle()
        
        # --> QFont That determinates the apearance of the text in the table #
        fontStyle = QFont()
        fontStyle.setBold(True)
        
        for row, call in enumerate(self.callsList):
            
                        
            # --> Opening Date #
            item = QTableWidgetItem(str(call.formatedOpeningDate))
            item.setData(Qt.UserRole, int(call.callId))
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.callsTable.setItem(row, 0, item)

            # --> Total Duration #
            item = QTableWidgetItem(call.formatedTotalDuration)
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            item.setFont(fontStyle)
            if call.totalDuration and call.totalDuration > 30:
                item.setForeground(Qt.red)
            elif call.totalDuration and call.totalDuration < 0:
                item.setForeground(Qt.blue)
            self.callsTable.setItem(row, 1, item)

            # --> Answering Duration #
            if call.statusId != 1:
                item = QTableWidgetItem(call.formatedAnswerDuration)
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                item.setFont(fontStyle)
                if call.answerDuration and call.answerDuration > 30:
                    item.setForeground(Qt.red)
                self.callsTable.setItem(row, 2, item)


            # --> Opened By #
            item = QTableWidgetItem(call.creator)
            self.callsTable.setItem(row, 3, item)

          
            # --> Call Type #
            item = QTableWidgetItem(call.callType)
            self.callsTable.setItem(row, 4, item)

            # --> Call Local #
            item = QTableWidgetItem(call.location)
            self.callsTable.setItem(row, 5, item)

            # --> Client #
            item = QTableWidgetItem(call.client)
            self.callsTable.setItem(row, 6, item)

            # --> Product #
            item = QTableWidgetItem(call.product)
            self.callsTable.setItem(row, 7, item)

            # --> Status #
            item = QTableWidgetItem(call.status)
            self.callsTable.setItem(row, 8, item)

            # --> Detractor #
            item = QTableWidgetItem(call.detractor)
            self.callsTable.setItem(row, 9, item)

            # --> Responsible #
            item = QTableWidgetItem(call.support)
            
            self.callsTable.setItem(row, 10, item)


###############################################################################################################################################################################


    def updateSubWindowTitle(self):
        """
        This method is used to update the window title with the total number of opened calls
        """
        if len(self.callsList) != 1:
            self.setWindowTitle("Relatório de Chamados - %d Chamados" % len(self.callsList))
        else:
            self.setWindowTitle("Relatório de Chamados - 1 Chamado")


###############################################################################################################################################################################

    def saveReport(self):
        """
        This method is responsible for saving the report data to an excel sheet
        """
        self.filteringFields = []

        fromDate = self.fromDateField.text().split("/")
        untilDate = self.untilDateField.text().split("/")

        self.filteringFields.append("DATE(cha_data_hora_abertura) >= DATE('" + fromDate[2] + "-" + fromDate[1] + "-" + fromDate[0] + "')")
        self.filteringFields.append("DATE(cha_data_hora_abertura) <= DATE('" + untilDate[2] + "-" + untilDate[1] + "-" + untilDate[0] + "')")

        
        if self.filterClientField.text():
            self.filteringFields.append("cli_nome LIKE '%" + self.filterClientField.text() + "%'")

        if self.filterProductField.text():
            self.filteringFields.append("pro_nome LIKE '%" + self.filterProductField.text() + "%'")

        if self.callCreatorField.text():
            self.filteringFields.append("cha_operador LIKE '%" + self.callCreatorField.text() + "%'")

        if not self.insidePlanCheckBox.isChecked():
            self.filteringFields.append("cha_plano = '0'")
        elif not self.outsidePlanCheckBox.isChecked():
            self.filteringFields.append("cha_plano = '1'")

       
        if self.callTypeComboBox.currentIndex() > 0:
            self.filteringFields.append("cha_tipo = '" +str(self.callTypeComboBox.itemData(self.callTypeComboBox.currentIndex()))+ "'")

        if self.callStatusComboBox.currentIndex() > 0:
            self.filteringFields.append("cha_status = '" +str(self.callStatusComboBox.itemData(self.callStatusComboBox.currentIndex()))+ "'")

        

        if self.responsibleField.text():
            self.filteringFields.append("col_nome LIKE '%" + self.responsibleField.text() + "%'")

        if len(self.filteringFields):
            self.isFiltering = True
        else:
            self.isFiltering = False

        
        reportPath = QFileDialog.getExistingDirectory(self, "Selecione o local onde o relatório será salvo", "/home", QFileDialog.ShowDirsOnly)
        if reportPath:
            try:
                report = callscontainer.CallsWorksheetReport(reportPath)
                report.generateReport(self.isFiltering, self.filteringFields)

                messageBox = QMessageBox()
                messageBox.setIcon(QMessageBox.Information)
                messageBox.setWindowIcon(QIcon(":/warning_icon.png"))
                messageBox.setWindowTitle("Sucesso!")
                messageBox.setText("Relatório salvo com sucesso.")
                    
                messageBox.exec_()
            except:
                messageBox = QMessageBox()
                messageBox.setWindowTitle("Falha ao salvar!")
                messageBox.setIcon(QMessageBox.Critical)
                messageBox.setText(
                    "Ocorreu um erro ao tentar salvar o relatório. Entre em contato com o administrador do sistema.")
                messageBox.exec_()
        
###############################################################################################################################################################################

    
    def currentRowCall(self):
        """
        This method returns the current selected row
        """
        row = self.callsTable.currentRow()
        if row > -1:
            item = self.callsTable.item(row, 0)
            key = item.data(Qt.UserRole)
            return self.callsList.callFromId(key)

        return None

###############################################################################################################################################################################
   
   
    def closeEvent(self, event):
        """
        This method remove its reference from its parent opened sub window list before being closed
        """
        del self.parent.openedSubWindows[self.SUBWINDOWID]
        self.close()
