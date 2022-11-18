import sys
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication, QFileDialog
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel

from SQL.Table_list import creat_list
from SQL.DB_algs.export import export_data
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import QSize, Qt
from SQL.DB_algs.table_gen import table_gen
from functools import partial

from json import dumps

class Menu(QMainWindow):
    def __init__(self):
        super().__init__()
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(500, 500))  # Set sizes

        self.table_list = creat_list()
        self.edit()
        self.export()
        self.impor()

        self.setGeometry(0, 0, 300, 300)
        self.setWindowTitle('Редактирование базы данных')
        self.show()

    def edit(self):
        self.statusBar()
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('Редактировать')

        for c in self.table_list:
            exitAction = QAction(c, self)
            exitAction.triggered.connect(partial(self.table_gen, name=c))
            fileMenu.addAction(exitAction)

    def export(self):
        self.statusBar()
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('Экспорт')

        for c in self.table_list:
            exitAction = QAction(c, self)
            exitAction.triggered.connect(qApp.quit)
            fileMenu.addAction(exitAction)

    def impor(self):
        self.statusBar()
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('Импорт')

        exitAction = QAction('Выбрать файлы', self)
        exitAction.triggered.connect(self.file_import)
        fileMenu.addAction(exitAction)

    def file_import(self):
        data = QFileDialog.getOpenFileNames(self, 'Open File', '',
                                           'SQL File (*.sql)')
        data = data[0]
        for path in data:
            with open(path, 'r') as file:
                export_data(file.read())

    def table_gen(self, name):
        self.add_req = []
        self.del_req = []

        self.cw = QWidget(self)  # Create a central widget
        self.setCentralWidget(self.cw)  # Install the central widge

        columns, data = table_gen(name)
        self.columns = columns

        grid_layout = QGridLayout(self)  # Create QGridLayout

        self.cw.setLayout(grid_layout)  # Set this layout in central widget

        self.table = QTableWidget(self)  # Create a table
        self.table.setColumnCount(len(columns))  # Set three columns

        L = self.L = len(data)
        l = len(data[0])
        self.table.setRowCount(L)  # and one row

        # Set the table headers
        self.table.setHorizontalHeaderLabels(columns)

        # Fill the first line
        for i in range(L):
            for j in range(l):
                x = data[i][j]
                self.table.setItem(i, j, QTableWidgetItem(str(x)))

        # Do the resize of the columns by content

        grid_layout.addWidget(self.table, 0, 0)  # Adding the table to the grid

        add_row = QPushButton('Добавить строку', self)
        add_row.clicked.connect(self.add_button)
        del_row = QPushButton('Удалить строку', self)
        del_row.clicked.connect(self.del_button)
        save_row = QPushButton('Сохранить таблицу', self)
        save_row.clicked.connect(partial(self.save_button, name))

        grid_layout.addWidget(add_row, 1, 0)  # Adding the table to the grid
        grid_layout.addWidget(del_row, 2, 0)  # Adding the table to the grid
        grid_layout.addWidget(save_row, 3, 0)  # Adding the table to the grid

    def add_button(self):
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.selectRow(row)

    def del_button(self):
        if self.table.selectionModel().hasSelection():
            for index in self.table.selectedIndexes():
                self.table.removeRow(index.row())

    def save_button(self, name):
        file_name = QFileDialog.getSaveFileName(self, 'Сохранить таблицу', '', 'SQL (.sql)')[0]
        if not('.sql' in file_name):
            file_name += '.sql'

        request = f'INSERT INTO `{name}`'
        columns = [f'`{i}`' for  i in self.columns][1:]
        request += '('+','.join(columns)+') VALUES '

        with open(file_name, 'w') as file:
            for i in range(self.table.rowCount()):
                T = []
                for j in range(1, self.table.columnCount()):
                    T.append("'" + self.table.item(i, j).text() + "'")
                T = '('+ ','.join(T) +');'
                file.write(request + T)

def Menu_Start():
    app = QApplication(sys.argv)
    ex = Menu()
    sys.exit(app.exec_())