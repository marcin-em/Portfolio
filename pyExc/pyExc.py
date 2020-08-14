import os
import sys
import csv
from PyQt5 import QtWidgets, QtCore, QtGui

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.content = Content()
        self.setCentralWidget(self.content)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('pyExc')
        self.setFixedSize(400, 410)
        bar = self.menuBar()
        file = bar.addMenu('File')
        about = bar.addMenu('About')
        open_action = QtWidgets.QAction('Open', self)
        save_action = QtWidgets.QAction('Save', self)
        quit_action = QtWidgets.QAction('Quit', self)
        howto_action = QtWidgets.QAction('How to', self)
        about_action = QtWidgets.QAction('About', self)
        file.addAction(open_action)
        file.addAction(save_action)
        file.addAction(quit_action)
        about.addAction(howto_action)
        about.addAction(about_action)

        howto_action.triggered.connect(self.howto_trigger)
        about_action.triggered.connect(self.about_trigger)
        open_action.triggered.connect(self.open_trigger)
        save_action.triggered.connect(self.save_trigger)
        quit_action.triggered.connect(self.quit_trigger)

        self.show()

    def open_trigger(self):
        path = QtWidgets.QFileDialog.getOpenFileName(self, 'Open CSV', os.getenv('HOME'), 'CSV(*.csv)')
        if path[0] != '':
            with open(path[0], newline='') as cvs_file:
                self.content.table.setRowCount(0)
                self.content.table.setColumnCount(1)
                my_file = csv.reader(cvs_file, dialect='excel')
                for row_data in my_file:
                    row = self.content.table.rowCount()
                    self.content.table.insertRow(row)
                    if len(row_data) > 1:
                        self.content.table.setColumnCount(len(row_data))
                    for column, name in enumerate(row_data):
                        item = QtWidgets.QTableWidgetItem(name)
                        self.content.table.setItem(row, column, item)
                        
    def save_trigger(self):
        path = QtWidgets.QFileDialog.getSaveFileName(self, 'Save CSV', os.getenv('HOME'), 'CSV(*.csv)')
        if path[0] != '':
            with open(path[0], 'w', newline='') as cvs_file:
                writer = csv.writer(cvs_file, dialect='excel')
                for row in range(self.content.table.rowCount()):
                    row_data = []
                    for column in range(self.content.table.columnCount()):
                        item = self.content.table.item(row, column)
                        if item is not None:
                            row_data.append(item.text())
                        else:
                            row_data.append('')
                    writer.writerow(row_data)

    def quit_trigger(self):
        QtWidgets.qApp.quit()
    def about_trigger(self):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle('About app')
        msg.setStyleSheet("""
            QLabel 
            {
                min-width: 120px;
                font-size: 16px;
            }
            """)
        msg.setText('Made by M')

        msg.exec_()

    def howto_trigger(self):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle('How to')
        msg.setStyleSheet("""
            QLabel 
            {
                min-width: 200px;
                min-height: 120px;
                font-size: 16px;
            }
            """)
        msg.setText('\
1. Open CSV file\n\
2. Edit table with 3 buttons:\n\
    - Swap words\n\
    - Set lower case\n\
    - Set title case\n\
3. Save')

        msg.exec_()

class Content(QtWidgets.QWidget):
    
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.b1 = QtWidgets.QPushButton()
        self.b1.setIcon(QtGui.QIcon('img/button1.png'))
        self.b1.setIconSize(QtCore.QSize(150,50))

        self.b2 = QtWidgets.QPushButton()
        self.b2.setIcon(QtGui.QIcon('img/button2.png'))
        self.b2.setIconSize(QtCore.QSize(150,50))

        self.b3 = QtWidgets.QPushButton()
        self.b3.setIcon(QtGui.QIcon('img/button3.png'))
        self.b3.setIconSize(QtCore.QSize(150,50))

        self.table = QtWidgets.QTableWidget(12,1)
        self.table.setColumnWidth(0,170)

        self.b1.setSizePolicy(
            QtWidgets.QSizePolicy.Preferred,
            QtWidgets.QSizePolicy.Expanding)
        self.b2.setSizePolicy(
            QtWidgets.QSizePolicy.Preferred,
            QtWidgets.QSizePolicy.Expanding)
        self.b3.setSizePolicy(
            QtWidgets.QSizePolicy.Preferred,
            QtWidgets.QSizePolicy.Expanding)

        v_box = QtWidgets.QVBoxLayout()
        v_box.addWidget(self.b1)
        v_box.addWidget(self.b2)
        v_box.addWidget(self.b3)
        v_box.setSpacing(5)

        h_box = QtWidgets.QHBoxLayout()
        h_box.addLayout(v_box, 1)
        h_box.addWidget(self.table, 1)
        h_box.setContentsMargins(0,0,0,0)
        h_box.setSpacing(5)

        self.b1.clicked.connect(self.b1_swap)
        self.b2.clicked.connect(self.b2_lower)
        self.b3.clicked.connect(self.b3_upper)

        self.setLayout(h_box)

        self.show()

    def b1_swap(self):
        row_count = self.table.rowCount()
        for row in range(0, row_count):
            try:
                name = self.table.item(row, 0).text()
                name_split = name.split()
                name_split.reverse()
                name_reverse = ' '.join(name_split)
                self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(name_reverse))
            except:
                pass

    def b2_lower(self):
        row_count = self.table.rowCount()
        for row in range(0, row_count):
            try:
                name = self.table.item(row, 0).text()
                name_lower = name.lower()
                self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(name_lower))
            except:
                pass

    def b3_upper(self):
        row_count = self.table.rowCount()
        for row in range(0, row_count):
            try:
                name = self.table.item(row, 0).text()
                name_title = name.title()
                self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(name_title))
            except:
                pass

app = QtWidgets.QApplication(sys.argv)
main_window = MainWindow()
sys.exit(app.exec_())
