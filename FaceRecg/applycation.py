import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
#from DB.Client import client
import clipboard
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer, QDateTime
from PyQt5.QtGui import QPalette, QColor, QPixmap
import person_count
import webbrowser

class MyApp(QWidget):

    def __init__(self):
        super().__init__()

        self.id = ''
        self.pw = ''

        self.widget_title = QWidget(parent=self, flags=Qt.Widget)
        self.init_widget_title()

        self.frame_info = QFrame()
        self.init_frame_info()

        self.widget_cam = QWidget(parent=self, flags=Qt.Widget)
        self.init_widget_cam()

        self.initUI()

    def init_widget_title(self):

        self.widget_title.setStyleSheet("background-color: rgb(240, 240, 240)")

        self.label_title = QLabel(self.widget_title)
        icon = QPixmap('icon.png')
        icon_scaled = icon.scaled(50, 50)
        self.label_title.setPixmap(icon_scaled)

        self.label_ID = QLabel('17011477 목승주', self.widget_title)
        self.label_ID.setStyleSheet("Color: rgb(50, 50, 50)")

        hbox_title = QHBoxLayout()
        hbox_title.addWidget(self.label_title)
        hbox_title.addStretch(1)
        hbox_title.addWidget(self.label_ID)

        self.widget_title.setLayout(hbox_title)


    def init_frame_info(self):
        self.frame_info.setFrameShape(QFrame.Box)
        self.frame_info.setFrameShadow(QFrame.Raised)
        self.frame_info.setLineWidth(3)

        self.label_lecture = QLabel('2020년 2학기 컴퓨터구조 기말고사', self.frame_info)
        font = self.label_lecture.font()
        font.setBold(True)
        font.setPointSize(16)
        self.label_lecture.setFont(font)

        hbox_lecture = QHBoxLayout()
        hbox_lecture.addStretch(1)
        hbox_lecture.addWidget(self.label_lecture)
        hbox_lecture.addStretch(1)

        self.label_duration = QLabel('\n시험시간 : ', self.frame_info)
        hbox_duration = QHBoxLayout()
        hbox_duration.addStretch(1)
        hbox_duration.addWidget(self.label_duration)
        hbox_duration.addStretch(1)

        font = self.label_duration.font()
        font.setPointSize(12)
        font.setBold(True)
        self.label_duration.setFont(font)

        self.label_time = QLabel('\n' + QDateTime.currentDateTime().toString(Qt.DefaultLocaleLongDate), self.frame_info)
        font = self.label_time.font()
        font.setPointSize(12)
        font.setBold(True)
        self.label_time.setFont(font)

        hbox_time = QHBoxLayout()
        hbox_time.addStretch(1)
        hbox_time.addWidget(self.label_time)
        hbox_time.addStretch(1)

        vbox_info = QVBoxLayout()
        vbox_info.addLayout(hbox_lecture)
        vbox_info.addLayout(hbox_duration)
        vbox_info.addLayout(hbox_time)

        self.frame_info.setLayout(vbox_info)


    def init_widget_cam(self):
        self.widget_cam.btn_start = QPushButton('Clear clipboard and start!')
        #self.widget_cam.btn_start.setMaximumWidth(500)
        self.widget_cam.btn_start.setFixedSize(200, 50)
        self.widget_cam.btn_start.clicked.connect(self.startExam)


        pixmap = QPixmap('winter.jpg')
        self.widget_cam.label_img = QLabel()
        self.widget_cam.label_img.setPixmap(pixmap)

        self.widget_cam.hbox_btn = QHBoxLayout()
        self.widget_cam.hbox_btn.addStretch(1)
        self.widget_cam.hbox_btn.addWidget(self.widget_cam.btn_start)
        self.widget_cam.hbox_btn.addStretch(1)

        self.widget_cam.hbox_img = QHBoxLayout()
        self.widget_cam.hbox_img.addStretch(1)
        self.widget_cam.hbox_img.addWidget(self.widget_cam.label_img)
        self.widget_cam.hbox_img.addStretch(1)

        self.widget_cam.vbox_img = QVBoxLayout()
        self.widget_cam.vbox_img.addLayout(self.widget_cam.hbox_btn)
        self.widget_cam.vbox_img.addLayout(self.widget_cam.hbox_img)

        self.widget_cam.setLayout(self.widget_cam.vbox_img)

    def initUI(self):

        self.setWindowTitle('I See You')

        pal = QPalette() # 배경색 변경
        pal.setColor(QPalette.Background, QColor(255, 255, 255))
        self.setPalette(pal)

        self.btn_exit = QPushButton('시험 종료', self)
        self.btn_exit.setFixedSize(100, 80)
        self.btn_exit.clicked.connect(self.exit_exam)

        hbox_exit = QHBoxLayout()
        hbox_exit.addStretch(1)
        hbox_exit.addWidget(self.btn_exit)

        vbox = QVBoxLayout()
        vbox.addWidget(self.widget_title)
        vbox.addStretch(1)
        vbox.addWidget(self.frame_info)
        vbox.addStretch(2)
        vbox.addWidget(self.widget_cam)
        vbox.addStretch(1)
        vbox.addLayout(hbox_exit)
        vbox.setContentsMargins(0, 0, 0, 0)

        self.setLayout(vbox)

        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.setCurrentTime)
        self.timer.start()

        #self.setGeometry(0, 0, 800, 800)
        #self.show()
        self.showFullScreen()
        #self.hide()

    def setCurrentTime(self):
        datetime = QDateTime.currentDateTime()
        self.label_time.setText('\n' + datetime.toString(Qt.DefaultLocaleLongDate))

    def startExam(self):
        reply = QMessageBox.question(self, 'Message', '시험을 시작하시겠습니까?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            data = clipboard.clear_clipboard()
            #client.send_clipboard()
            self.widget_cam.btn_start.setDisabled(True)
            print('yes')
            person_count.start()
            webbrowser.open('http://blackboard.sejong.ac.kr')

        else:
            print('no')

    def exit_exam(self):
        reply = QMessageBox.question(self, 'Message', '시험을 종료하시겠습니까?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            sys.exit()

    def setID(self, id, num):
        self.id = id
        self.num = num

    def run(self):
        self.show()
        print(self.id, self.num)

    def set_duration(self, start, end):
        self.label_duration.setText("\n시험시간 : " + start + ' ~ ' + end)



class Sign_in(QWidget):

    def __init__(self, widget):
        super().__init__()
        self.mainW = widget
        self.initUI()

    def initUI(self):
        self.setWindowTitle('I SEE YOU')
        self.move(300, 300)
        self.resize(400, 200)

        self.label_ID = QLabel('학번', self)
        self.lineEdit_ID = QLineEdit(self)

        self.label_num = QLabel('학수번호', self)
        self.lineEdit_num = QLineEdit(self)
        self.lineEdit_num.returnPressed.connect(self.log_in)

        self.btn_return = QPushButton('로그인', self)
        self.btn_return.setMaximumHeight(100)
        self.btn_return.clicked.connect(self.log_in)

        grid = QGridLayout()
        grid.addWidget(self.label_ID, 0, 0)
        grid.addWidget(self.lineEdit_ID, 0, 1)
        grid.addWidget(QLabel('', self), 1, 0)
        grid.addWidget(self.label_num, 2, 0)
        grid.addWidget(self.lineEdit_num, 2, 1)

        hbox = QHBoxLayout()
        hbox.addStretch(2)
        hbox.addLayout(grid)
        hbox.addStretch(1)
        hbox.addWidget(self.btn_return)
        hbox.addStretch(2)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        vbox.addStretch(1)

        self.setLayout(vbox)
        self.center()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def log_in(self):
        id = self.lineEdit_ID.text()
        num = self.lineEdit_num.text()
        self.mainW.setID(id, num)

        #img = client.login(id, num)

        self.hide()
        self.mainW.run()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.set_duration('12:00', '13:30')
    #sign_in = Sign_in(ex)
    sys.exit(app.exec_())
