from PyQt5.QtCore import (
        Qt,
        QDate
    )

from PyQt5.QtGui import (
        QFont,
        QIcon,
        QCursor
    )

from PyQt5.QtWidgets import (
        QMdiSubWindow,
        QDialog,
        QLabel,
        QDateEdit,
        QCalendarWidget,
        QPushButton,
        QLineEdit,
        QLayout,
        QHBoxLayout,
        QVBoxLayout,
        QWidget
    )

import qrc_resources
from magicDB import *
from myExceptions import *

import callscontainer

__version__ = "2.0.0"



###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################

class MyQDateEdit(QDateEdit):

    def __init__(self, parent=None):
        super(MyQDateEdit, self).__init__(parent)
        self.setDate(QDate.currentDate().addDays(-1))
        self.setMaximumDate(QDate.currentDate().addDays(-1))
        self.setFixedWidth(80)
        self.setCalendarPopup(True)
        self.setDisplayFormat("dd/MM/yyyy")
        self.calendarWidget().setHorizontalHeaderFormat(QCalendarWidget.NoHorizontalHeader)
        self.calendarWidget().setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        stylesheet = "QCalendarWidget QWidget#qt_calendar_navigationbar :hover{"\
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

        self.setStyleSheet(stylesheet)
        self.setFocusPolicy(Qt.NoFocus)
        

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

        self.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.setFont(boldFont)
        


###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################

class MyQLineEdit(QLineEdit):
    """
    This class reimplements the qlabel class
    """
    def __init__(self, text="", parent=None):
        super(MyQLineEdit, self).__init__(text, parent)

        boldFont = QFont()
        boldFont.setBold(True)
        
        self.setFixedWidth(90)
        self.setReadOnly(True)
        self.setAlignment(Qt.AlignHCenter)
        self.setFont(boldFont)

###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################


class IndicatorSearchWindow(QMdiSubWindow):

    # --> Constant id, used for location inside the openedSubWindows dictionary in the main window #
    SUBWINDOWID = "indicatorsearchwindow"

    def __init__(self, parent=None):
        super(IndicatorSearchWindow, self).__init__(parent)
        self.parent = parent        
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowFlags(Qt.SubWindow | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
        self.indicatorSearch = callscontainer.CallsIndicatorsReport()

        
        #########################################
        ####### --> DATE LABEL AND FIELD ########
        #########################################

        #dateIndicatorFromLabel = MyQLabel(" ")
        dateIndicatorToLabel = MyQLabel(" até ")
        
        # --> Begin Date #
        self.dateIndicatorFieldBegin = MyQDateEdit()
        self.dateIndicatorFieldBegin.setDate(QDate.currentDate().addMonths(-1).addDays(-1))
        
        
        # --> End Date #
        self.dateIndicatorFieldEnd = MyQDateEdit()
        self.dateIndicatorFieldEnd.setDate(QDate.currentDate().addDays(-1))
        
        self.searchButton = QPushButton( "Buscar" )
        self.searchButton.setFixedWidth(90)
        self.searchButton.setCursor(QCursor(Qt.PointingHandCursor))

        #########################################
        ####### --> CALLS LABEL AND FIELD #######
        #########################################

        totalCallsLabel = MyQLabel("Chamados com Indicador:")
        self.totalCallsField = MyQLineEdit(" ")

        totalProdTimeLabel = MyQLabel("Tempo Total de Produção:")
        self.totalProdTimeField = MyQLineEdit(" ")

        totalLateTimeLabel = MyQLabel("Tempo Total de Atraso:")
        self.totalLateTimeField = MyQLineEdit(" ")

        totalAnswerTimeLabel = MyQLabel("Tempo Total de Atendimento:")
        self.totalAnswerTimeField = MyQLineEdit(" ")
    
        avgLateTimeLabel = MyQLabel("Tempo Médio de Atraso:")
        self.avgLateTimeField = MyQLineEdit(" ")

        avgAnswerTimeLabel = MyQLabel("Tempo Médio de Atendimento:")
        self.avgAnswerTimeField = MyQLineEdit(" ")

        lateTimeByTotalTimeLabel = MyQLabel("Atraso Total / Tempo Total:")
        self.lateTimeByTotalTimeField = MyQLineEdit(" ")

        uptimeLabel = MyQLabel("Uptime de Teste:")
        self.uptimeField = MyQLineEdit(" ")

        #####################################
        ######### --> LAYOUT BUILD ##########
        #####################################

        dateFieldLayout = QHBoxLayout()
        #dateFieldLayout.addWidget(dateIndicatorLabel)
        dateFieldLayout.addWidget(self.dateIndicatorFieldBegin)
        dateFieldLayout.addWidget(dateIndicatorToLabel)
        dateFieldLayout.addWidget(self.dateIndicatorFieldEnd)
        dateFieldLayout.addWidget(self.searchButton)

        totalCallsLayout = QHBoxLayout()
        totalCallsLayout.addWidget(totalCallsLabel)
        totalCallsLayout.addStretch(1)
        totalCallsLayout.addWidget(self.totalCallsField)
        
        totalProdTimeLayout = QHBoxLayout()
        totalProdTimeLayout.addWidget(totalProdTimeLabel)
        totalProdTimeLayout.addStretch(1)
        totalProdTimeLayout.addWidget(self.totalProdTimeField)
        
        totalLateTimeLayout = QHBoxLayout()
        totalLateTimeLayout.addWidget(totalLateTimeLabel)
        totalLateTimeLayout.addStretch(1)
        totalLateTimeLayout.addWidget(self.totalLateTimeField)
        
        totalAnswerTimeLayout = QHBoxLayout()
        totalAnswerTimeLayout.addWidget(totalAnswerTimeLabel)
        totalAnswerTimeLayout.addStretch(1)
        totalAnswerTimeLayout.addWidget(self.totalAnswerTimeField)
        
        avgLateTimeLayout = QHBoxLayout()
        avgLateTimeLayout.addWidget(avgLateTimeLabel)
        avgLateTimeLayout.addStretch(1)
        avgLateTimeLayout.addWidget(self.avgLateTimeField)
                

        avgAnswerTimeLayout = QHBoxLayout()
        avgAnswerTimeLayout.addWidget(avgAnswerTimeLabel)
        avgAnswerTimeLayout.addStretch(1)
        avgAnswerTimeLayout.addWidget(self.avgAnswerTimeField)
        

        lateTimeByTotalTimeLayout = QHBoxLayout()
        lateTimeByTotalTimeLayout.addWidget(lateTimeByTotalTimeLabel)
        lateTimeByTotalTimeLayout.addStretch(1)
        lateTimeByTotalTimeLayout.addWidget(self.lateTimeByTotalTimeField)
        
        
        uptimeLayout = QHBoxLayout()
        uptimeLayout.addWidget(uptimeLabel)
        uptimeLayout.addStretch(1)
        uptimeLayout.addWidget(self.uptimeField)
         

        windowLayout = QVBoxLayout()
        windowLayout.addLayout(dateFieldLayout)
        windowLayout.addLayout(totalCallsLayout)
        windowLayout.addLayout(totalProdTimeLayout)
        windowLayout.addLayout(totalAnswerTimeLayout)
        windowLayout.addLayout(totalLateTimeLayout)
        windowLayout.addLayout(avgAnswerTimeLayout)
        windowLayout.addLayout(avgLateTimeLayout)
        windowLayout.addLayout(lateTimeByTotalTimeLayout)
        windowLayout.addLayout(uptimeLayout)
        

        # --> Create a central widget for the window Layout #
        centralWidget = QWidget()
        centralWidget.setLayout(windowLayout)
        self.setWidget(centralWidget)


        self.searchButton.clicked.connect(self.searchIndicator)
        self.setWindowIcon(QIcon(":/detailed_call_report.png"))
        self.setWindowTitle("Pesquisa de Indicador")


        # --> Line responsible for preventing window resize
        #self.layout().setSizeConstraint(QLayout.SetFixedSize)

###############################################################################################################################################################################

    def searchIndicator(self):
        searchDateDayBegin = str(self.dateIndicatorFieldBegin.date().day()).zfill(2)
        searchDateMonthBegin = str(self.dateIndicatorFieldBegin.date().month()).zfill(2)
        searchDateYearBegin = str(self.dateIndicatorFieldBegin.date().year())
        dateStringBegin = searchDateYearBegin + "-" + searchDateMonthBegin + "-" +searchDateDayBegin

        searchDateDayEnd = str(self.dateIndicatorFieldEnd.date().day()).zfill(2)
        searchDateMonthEnd = str(self.dateIndicatorFieldEnd.date().month()).zfill(2)
        searchDateYearEnd = str(self.dateIndicatorFieldEnd.date().year())
        dateStringEnd = searchDateYearEnd + "-" + searchDateMonthEnd + "-" +searchDateDayEnd

        try:
            self.indicatorSearch.searchIndicator(dateStringBegin, dateStringEnd)
        except DatabaseConnectionError as error:
            message = "Falha em: " + place + "\nErro: " +cause
            messageBox = QMessageBox()
            messageBox.setText(message)
            messageBox.setWindowTitle("Erro!")
            messageBox.setIcon(QMessageBox.Critical)
            messageBox.setWindowIcon(QIcon(":/warning_icon.png"))
            messageBox.exec_()
            return


        # --> Populate the Fields #
        self.totalCallsField.setText(str(self.indicatorSearch.totalCalls))
        self.totalProdTimeField.setText(self.indicatorSearch.formatedTotalProductionMinutes)
        self.totalAnswerTimeField.setText(self.indicatorSearch.formatedTotalAnsweringMinutes)
        self.totalLateTimeField.setText(self.indicatorSearch.formatedtotalLateMinutes)

        if int(self.indicatorSearch.totalCalls) > 0:
            answerAVG = round(self.indicatorSearch.totalAnsweringMinutes / self.indicatorSearch.totalCalls)
            lateAVG = round(self.indicatorSearch.totalLateMinutes / self.indicatorSearch.totalCalls)
            
            self.avgAnswerTimeField.setText("%02d:%02d" % divmod(answerAVG, 60))
            self.avgLateTimeField.setText("%02d:%02d" % divmod(lateAVG, 60))

            tprod = self.indicatorSearch.totalProductionMinutes
            tansw = self.indicatorSearch.totalAnsweringMinutes
            tlate = self.indicatorSearch.totalLateMinutes
            
            tcall = tlate + tansw
            if tcall:
                tlatebytcall = tlate / tcall
            else:
                tlatebytcall = 0

            self.lateTimeByTotalTimeField.setText("{:.2f}%".format(tlatebytcall*100))
            

            if tprod:
                uptime = (tprod - (tansw + tlate))/tprod
            else:
                uptime = 0
             
            self.uptimeField.setText("{:.2f}%".format(uptime*100))


            
        else:
            self.avgAnswerTimeField.setText("00:00")
            self.avgLateTimeField.setText("00:00")
            self.lateTimeByTotalTimeField.setText("0.00%")
            self.uptimeField.setText("0.00%")

            
###############################################################################################################################################################################
        

    def closeEvent(self, event):
        """
        This method remove its reference from its parent opened sub window list before being closed
        """
        del self.parent.openedSubWindows[self.SUBWINDOWID]
        self.close()
