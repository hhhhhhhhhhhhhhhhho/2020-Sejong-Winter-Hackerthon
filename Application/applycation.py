import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from DB.Client import client
import clipboard
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer, QDateTime
from PyQt5.QtGui import QPalette, QColor, QPixmap

class MyApp(QWidget):

    def __init__(self):
        super().__init__()

        self.widget_title = QWidget(parent=self, flags=Qt.Widget)
        self.init_widget_title(self.widget_title)

        self.frame_info = QFrame()
        self.init_frame_info()

        self.widget_cam = QWidget(parent=self, flags=Qt.Widget)
        self.init_widget_cam()

        self.initUI()

    def init_widget_title(self, w):

        self.widget_title.setStyleSheet("background-color: rgb(240, 240, 240)")

        w.label_title = QLabel('I See You', w)
        w.label_title.setStyleSheet("Color: rgb(110, 110, 110)")
        font = w.label_title.font()
        font.setPointSize(20)
        font.setBold(True)
        w.label_title.setFont(font)

        w.label_ID = QLabel('17011477 목승주', w)
        w.label_ID.setStyleSheet("Color: rgb(50, 50, 50)")

        w.hbox_title = QHBoxLayout()
        w.hbox_title.addWidget(w.label_title)
        w.hbox_title.addStretch(1)
        w.hbox_title.addWidget(w.label_ID)

        w.setLayout(w.hbox_title)


    def init_frame_info(self):
        self.frame_info.setFrameShape(QFrame.Box)
        self.frame_info.setFrameShadow(QFrame.Raised)
        self.frame_info.setLineWidth(3)

        label_lecture = QLabel('2020년 2학기 컴퓨터구조 기말고사', self.frame_info)
        font = label_lecture.font()
        font.setBold(True)
        font.setPointSize(16)
        label_lecture.setFont(font)

        label_duration = QLabel('\n시험시간 : 2020/12/21 15:00 ~ 2020/12/21 16:30', self.frame_info)
        font = label_duration.font()
        font.setPointSize(12)
        font.setBold(True)
        label_duration.setFont(font)

        self.frame_info.label_time = QLabel('\n' + QDateTime.currentDateTime().toString(Qt.DefaultLocaleLongDate), self.frame_info)
        font = self.frame_info.label_time.font()
        font.setPointSize(12)
        font.setBold(True)
        self.frame_info.label_time.setFont(font)

        vbox_info = QVBoxLayout()
        vbox_info.addWidget(label_lecture)
        vbox_info.addWidget(label_duration)
        vbox_info.addWidget(self.frame_info.label_time)

        self.frame_info.setLayout(vbox_info)


    def init_widget_cam(self):
        self.widget_cam.btn_start = QPushButton('Clear clipboard and start!')
        self.widget_cam.btn_start.clicked.connect(self.startExam)

        pixmap = QPixmap('H:\\2020Hackathon\\team\\2020-Sejong-Winter-Hackerthon\\Application\\winter.jpg')
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
        #self.showMaximized()
        self.setFixedSize(800, 800)
        self.move(0, 0)

        pal = QPalette() # 배경색 변경
        pal.setColor(QPalette.Background, QColor(255, 255, 255))
        self.setPalette(pal)

        vbox = QVBoxLayout()
        vbox.addWidget(self.widget_title)
        vbox.addStretch(1)
        vbox.addWidget(self.frame_info)
        vbox.addStretch(2)
        vbox.addWidget(self.widget_cam)
        vbox.addStretch(1)
        vbox.setContentsMargins(0, 0, 0, 0)

        self.setLayout(vbox)

        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.setCurrentTime)
        self.timer.start()

        self.hide()

    def setCurrentTime(self):
        datetime = QDateTime.currentDateTime()
        self.frame_info.label_time.setText('\n' + datetime.toString(Qt.DefaultLocaleLongDate))

    def startExam(self):
        reply = QMessageBox.question(self, 'Message', '시험을 시작하시겠습니까?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            data = clipboard.clear_clipboard()
            data[256] = None
            self.widget_cam.btn_start.setDisabled(True)
            print('yes')
        else:
            print('no')



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

        img = client.login(id, num)
        print(id, num)


        self.hide()
        self.mainW.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sign_in = Sign_in(ex)
    sys.exit(app.exec_())
