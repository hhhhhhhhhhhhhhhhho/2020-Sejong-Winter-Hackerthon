import os
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer, QDateTime
from PyQt5.QtGui import QPalette, QColor, QPixmap
#import person_count
import webbrowser
import tcpServer

class MyApp(QWidget):

    def __init__(self):
        super().__init__()

        self.widget_title = QWidget(parent=self, flags=Qt.Widget)
        self.table = QTableWidget(parent=self)

        self.init_widget_title()
        self.init_widget_table()
        self.initUI()
        self.show()

        andRaspTCP = tcpServer.TCPServer('172.30.1.34', 9999, self)
        andRaspTCP.start()

        
    def init_widget_title(self):

        self.widget_title.setStyleSheet("background-color: rgb(240, 240, 240)")

        self.label_title = QLabel(self.widget_title)

        self.label_ID = QLabel('관리자', self.widget_title)
        self.label_ID.setStyleSheet("Color: rgb(50, 50, 50)")

        hbox_title = QHBoxLayout()
        hbox_title.addWidget(self.label_title)
        hbox_title.addStretch(1)
        hbox_title.addWidget(self.label_ID)

        self.widget_title.setLayout(hbox_title)

    def init_widget_table(self):
        self.table.setFixedSize(1000, 300)
        #self.table.resize(500, 300)
        # 표의 크기를 지정
        #self.table.setStyleSheet('border-style: None;')
        self.table.setColumnCount(6)
        self.table.setRowCount(0)
        # 열 제목 지정
        self.table.setHorizontalHeaderLabels(
            ['EXAM ID', 'STUDENT ID', 'TIME', 'ERROR TYPE', 'IMAGE PATH', 'REMARKS']
        )
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 셀 내용 채우기
        # self.table.setItem(0, 0, QTableWidgetItem('A'))
        # self.table.setItem(1, 0, QTableWidgetItem('B'))
        # self.table.setItem(2, 0, QTableWidgetItem('C'))
        # self.table.setItem(0, 1, QTableWidgetItem('1'))
        # self.table.setItem(1, 1, QTableWidgetItem('2'))
        # self.table.setItem(2, 1, QTableWidgetItem('3'))

    def initUI(self):

        self.setWindowTitle('I See You')
        self.setFixedSize(1000, 500)
        pal = QPalette() # 배경색 변경
        pal.setColor(QPalette.Background, QColor(255, 255, 255))
        self.setPalette(pal)

        hbox_table = QHBoxLayout()
        hbox_table.setGeometry
        hbox_table.addStretch(1)
        hbox_table.addWidget(self.table)
        hbox_table.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addWidget(self.widget_title)
        vbox.addStretch(1)
        vbox.addLayout(hbox_table)
        vbox.addStretch(1)
        vbox.setContentsMargins(0, 0, 0, 0)
        
        self.setLayout(vbox)

        self.hide()

    def run(self, arr_login):
        self.showFullScreen()
        self.arr_info = arr_login
        self.set_lecture()
        self.set_duration()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    
    def add_row(self, exam_id, student_id, time, error_type, image_path, remarks):
        row_count = self.table.rowCount()
        print("row_count1", row_count)
        self.table.setRowCount(row_count+1)
        row_count = self.table.rowCount()
        print("row_count2", row_count)
        self.table.setItem(row_count-1, 0, QTableWidgetItem(exam_id))
        self.table.setItem(row_count-1, 1, QTableWidgetItem(student_id))
        self.table.setItem(row_count-1, 2, QTableWidgetItem(time))
        self.table.setItem(row_count-1, 3, QTableWidgetItem(error_type))
        self.table.setItem(row_count-1, 4, QTableWidgetItem(image_path))
        self.table.setItem(row_count-1, 5, QTableWidgetItem(remarks))

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = MyApp()
#     ex.add_row()
#     sys.exit(app.exec_())
