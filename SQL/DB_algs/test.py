from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import QSize, Qt
from SQL.DB_algs.table_gen import table_gen

class MainWindow(QMainWindow):
    # Override class constructor
    def __init__(self):
        # You must call the super class method
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(1000, 80))  # Set sizes
        self.setWindowTitle("Работа с QTableWidget")  # Set the window title
        self.cw = central_widget = QWidget(self)  # Create a central widget
        self.setCentralWidget(central_widget)  # Install the central widge

        self.DB_columns, self.DB_items = table_gen('pgusa_ru_access3')

        self.table()

    def table(self):
        grid_layout = QGridLayout(self)  # Create QGridLayout
        self.cw.setLayout(grid_layout)  # Set this layout in central widget

        table = QTableWidget(self)  # Create a table
        table.setColumnCount(len(self.DB_columns))  # Set three columns

        L = len(self.DB_items)
        l = len(self.DB_items[0])
        table.setRowCount(L)  # and one row

        # Set the table headers
        table.setHorizontalHeaderLabels(self.DB_columns)

        # Fill the first line
        for i in range(L):
            for j in range(l):
                x = self.DB_items[i][j]
                table.setItem(i, j, QTableWidgetItem(str(x)))

        # Do the resize of the columns by content

        grid_layout.addWidget(table, 0, 0)  # Adding the table to the grid



if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec())