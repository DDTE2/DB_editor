import sys
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication, QFileDialog
from PyQt5.QtGui import QIcon
from SQL.Table_list import creat_list
from SQL.DB_algs.export import export_data

class Menu(QMainWindow):
    def __init__(self):
        super().__init__()
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
            exitAction.triggered.connect(qApp.quit)
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

def Menu_Start():
    app = QApplication(sys.argv)
    ex = Menu()
    sys.exit(app.exec_())