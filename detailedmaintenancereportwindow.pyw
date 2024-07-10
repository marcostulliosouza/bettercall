from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout, QGroupBox, QHBoxLayout
from PyQt5.QtCore import Qt
__version__ = "1.0.0"

import maintenancesreportcontainer


class DetailedMaintenanceReportWindow(QDialog):
    """
    Esta classe é responsável por exibir os detalhes de uma manutenção em uma janela modal.
    """
    def __init__(self,  maintenance=None, parent=None):
        super(DetailedMaintenanceReportWindow, self).__init__(parent)

        self.maintenance = maintenance
        self.parent = parent
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.editBeginning = 0
        self.editEnd = 0

        ########################################
        #### --> WINDOW LAYOUT CODE SESSION ####
        ########################################
        boldFont = QFont()
        boldFont.setBold(True)

        #######################
        #### --> CALL INFO ####
        #######################

        maintenanceInfoGroupBox = QGroupBox("Informações sobre a Manutenção:")
        maintenanceInfoGroupBox.setFont(boldFont)

        support = QLabel("Atendido por:")
        # self.createByData = MyQDataLabel(self.maintenance.)
        # # # Layout principal
        # # main_layout = QVBoxLayout()
        #
        # # # Exibir detalhes da manutenção
        # # maintenance_group_box = QGroupBox("Detalhes da Manutenção")
        # # maintenance_layout = QVBoxLayout()
        # # for item in self.maintenance.item:
        # #     maintenance_layout.addWidget(QLabel(f"{item['descricao']}: {item['situacao']} - {item['observacao']}"))
        # # maintenance_group_box.setLayout(maintenance_layout)
        # # Botão para fechar a janela
        # close_button = QPushButton("Fechar")
        # close_button.clicked.connect(self.close)
        #
        # # Adicionando widgets ao layout principal
        # main_layout.addWidget(maintenance_group_box)
        # main_layout.addWidget(close_button)
        # main_layout.addStretch()
        #
        # Aplicando o layout à janela
        self.setLayout(main_layout)
