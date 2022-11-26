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

from SQL.DB_algs.key_check import check

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
        self.cw = QWidget(self)  # Create a central widget
        self.setCentralWidget(self.cw)  # Install the central widge

        columns, data = table_gen(name)
        self.columns = columns

        grid_layout = QGridLayout(self)  # Create QGridLayout

        self.cw.setLayout(grid_layout)  # Set this layout in central widget

        self.table = QTableWidget(self)  # Create a table
        self.table.setColumnCount(len(columns))  # Set three columns

        self.l = L = self.L = len(data)
        l = len(data[0])
        self.table.setRowCount(L)  # and one row

        # Set the table headers
        self.table.setHorizontalHeaderLabels(columns)

        x = check(name)

        self.max_index = 0
        for i in range(L):
            self.max_index = max(int(data[i][0]), self.max_index)

            for j in range(l):
                item = QTableWidgetItem(str(data[i][j]))
                if j in x:
                    item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                self.table.setItem(i, j, item)

        # Do the resize of the columns by content

        grid_layout.addWidget(self.table, 0, 0)  # Adding the table to the grid

        add_row = QPushButton('Добавить строку', self)
        add_row.clicked.connect(self.add_button)
        '''del_row = QPushButton('Удалить строку', self)
        del_row.clicked.connect(self.del_button)'''
        save_row = QPushButton('Сохранить таблицу', self)
        save_row.clicked.connect(partial(self.save_button, name))

        grid_layout.addWidget(add_row, 1, 0)  # Adding the table to the grid
        '''grid_layout.addWidget(del_row, 2, 0)  # Adding the table to the grid'''
        grid_layout.addWidget(save_row, 3, 0)  # Adding the table to the grid

        del columns, data, i, self.L

    def add_button(self):
        row = self.table.rowCount()

        self.table.insertRow(row)
        self.table.selectRow(row)

        self.max_index += 1

        item = QTableWidgetItem(str(self.max_index))
        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)

        self.table.setItem(row, 0, item)

        try:
            x = self.table.item(row, 1).text()
            print(str(x))
        except Exception as err:
            print(err, row)

    def del_button(self):
        if self.table.selectionModel().hasSelection():
            for index in self.table.selectedIndexes():
                self.table.removeRow(index.row())

    def save_button(self, name):
        file_name = QFileDialog.getSaveFileName(self, 'Сохранить таблицу', '', 'SQL (.sql)')[0]
        if not('.sql' in file_name):
            file_name += '.sql'

        request = f'UPDATE `{name}` SET '

        with open(file_name, 'w', encoding='windows-1251') as file:
            ml = self.table.rowCount()
            for i in range(self.l):
                T = []
                for j in range(1, self.table.columnCount()):
                    T.append(f"`{self.columns[j]}`='{self.table.item(i, j).text()}'")

                T = ''+ ','.join(T) +''
                T += f" WHERE `{self.columns[0]}`={self.table.item(i, 0).text()};\n"
                file.write(request + T)

def Menu_Start():
    app = QApplication(sys.argv)
    ex = Menu()
    sys.exit(app.exec_())