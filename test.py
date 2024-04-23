import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton, QWidget


class PaginatedTable(QMainWindow):
    def __init__(self):
        super().__init__()

        self.page_size = 5  # Tamanho da página
        self.current_page = 0  # Página atual

        self.data = [f'Dado {i + 1}' for i in range(50)]  # Dados de exemplo

        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Tabela Paginada")

        self.table = QTableWidget()
        self.table.setColumnCount(1)
        self.table.setHorizontalHeaderLabels(["Dados"])

        self.update_table()

        next_button = QPushButton("Próximo")
        next_button.clicked.connect(self.next_page)

        prev_button = QPushButton("Anterior")
        prev_button.clicked.connect(self.prev_page)

        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.addWidget(prev_button)
        layout.addWidget(next_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def update_table(self):
        self.table.setRowCount(self.page_size)

        start_index = self.current_page * self.page_size
        for i in range(self.page_size):
            if start_index + i < len(self.data):
                item = QTableWidgetItem(self.data[start_index + i])
                self.table.setItem(i, 0, item)
            else:
                break

    def next_page(self):
        max_page = len(self.data) // self.page_size
        if self.current_page < max_page:
            self.current_page += 1
            self.update_table()

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_table()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PaginatedTable()
    window.setGeometry(100, 100, 400, 300)
    window.show()
    sys.exit(app.exec_())