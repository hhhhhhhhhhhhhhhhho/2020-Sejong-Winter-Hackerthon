import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from DB.Client import client
import clipboard
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer, QDateTime
from PyQt5.QtGui import QPalette, QColor, QPixmap
import person_count
import webbrowser

from time import sleep
import threading
import ctypes


class MyApp(QWidget):

    def __init__(self):
        super().__init__()

        self.id = ''
        self.exam_num = ''
        self.name = ''
        self.arr_info = []

        self.widget_title = QWidget(parent=self, flags=Qt.Widget)
        self.init_widget_title()

        self.frame_info = QFrame()
        self.init_frame_info()

        self.widget_cam = QWidget(parent=self, flags=Qt.Widget)
        self.init_widget_cam()

        self.dialog = QDialog()


        self.initUI()

    def init_widget_title(self):

        self.widget_title.setStyleSheet("background-color: rgb(240, 240, 240)")

        self.label_title = QLabel(self.widget_title)
        icon = QPixmap('icon.png')
        icon_scaled = icon.scaled(50, 50)
        self.label_title.setPixmap(icon_scaled)

        self.label_ID = QLabel(self.widget_title)
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

        self.label_lecture = QLabel(self.frame_info)
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

        self.widget_cam.btn_start.setFixedSize(200, 50)
        self.widget_cam.btn_start.clicked.connect(self.startExam)


        pixmap = QPixmap('sejong.jpg')
        self.widget_cam.label_img = QLabel()
        self.widget_cam.label_img.setPixmap(pixmap)

        hbox_btn = QHBoxLayout()
        hbox_btn.addStretch(1)
        hbox_btn.addWidget(self.widget_cam.btn_start)
        hbox_btn.addStretch(1)

        hbox_img = QHBoxLayout()
        hbox_img.addStretch(1)
        hbox_img.addWidget(self.widget_cam.label_img)
        hbox_img.addStretch(1)

        vbox_img = QVBoxLayout()
        vbox_img.addLayout(hbox_btn)
        vbox_img.addLayout(hbox_img)

        self.widget_cam.setLayout(vbox_img)

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

        #self.showFullScreen()
        self.hide()

    def setCurrentTime(self):
        datetime = QDateTime.currentDateTime()
        self.label_time.setText('\n' + datetime.toString(Qt.DefaultLocaleLongDate))

    def startExam(self):
        reply = QMessageBox.question(self, 'Message', '시험을 시작하시겠습니까?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            data = clipboard.clear_clipboard()
            if data==None:
                data='*'
            client.send_clipboard(self.id, self.exam_num, data)

            self.widget_cam.btn_start.setDisabled(True)
            print(123)
            print(data)
            person_count.start(self.arr_info[0])
            webbrowser.open('http://blackboard.sejong.ac.kr')

            sleep(1)
            lib = ctypes.windll.LoadLibrary('user32.dll')
            handle = lib.GetForegroundWindow()  # 활성화된 윈도우의 핸들얻음
            self.window = ctypes.create_unicode_buffer(255)  # 타이틀을 저장할 버퍼
            lib.GetWindowTextW(handle, self.window, ctypes.sizeof(self.window))  # 버퍼에 타이틀 저장

            window_thread = threading.Thread(target=self.check_window)
            window_thread.start()

        else:
            print('no')

    def exit_exam(self):
        reply = QMessageBox.question(self, 'Message', '시험을 종료하시겠습니까?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            sys.exit()

    def setID(self, id, exam_num):
        self.id = id
        self.exam_num = exam_num

    def run(self, arr_login):
        self.showFullScreen()
        self.arr_info = arr_login
        self.set_label_lecture()
        self.set_label_duration()
        self.set_label_ID()
        #os.startfile("filename.exe")
        #with Listener(on_press=self.on_press, on_release=self.on_release) as listener:  # Create an instance of Listener
         #   listener.join()  # Join the listener thread to the main thread to keep waiting for keys

    def set_label_ID(self):
        self.label_ID.setText(self.id + ' ' + self.arr_info[5])

    def set_label_duration(self):
        self.label_duration.setText("\n시험시간 : " + self.arr_info[3] + '~' + self.arr_info[4])

    def set_label_lecture(self):
        self.label_lecture.setText('2020년 2학기 ' + self.arr_info[1] + ' 기말고사')

    def on_press(self, key):  # The function that's called when a key is pressed
        # logging.info("Key pressed: {0}".format(key))
        print(key)
        sleep(1)
        sys.stdout.flush()

    def on_release(self, key):  # The function that's called when a key is released
        # logging.info("Key released: {0}".format(key))
        print(key)
        sleep(1)
        sys.stdout.flush()

    def check_window(self):
        while(True):
            lib = ctypes.windll.LoadLibrary('user32.dll')
            handle = lib.GetForegroundWindow()  # 활성화된 윈도우의 핸들얻음
            buffer = ctypes.create_unicode_buffer(255)  # 타이틀을 저장할 버퍼
            lib.GetWindowTextW(handle, buffer, ctypes.sizeof(buffer))  # 버퍼에 타이틀 저장

            if self.window.value != buffer.value:
                print('cheat')
                sleep(5)
                self.dialog.hide()


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
        exam_num = self.lineEdit_num.text()
        self.mainW.setID(id, exam_num)
        self.hide()

        arr_login = client.login(id, exam_num)

        self.mainW.run(arr_login)



if __name__ == '__main__':

    '''
    t1 = threading.Thread(target=QApplication(sys.argv))
    t2 = threading.Thread(target=MyApp())
    t3 = threading.Thread(target=Sign_in(MyApp()))
    t1.start()
    t2.start()
    t3.start()
    sys.exit(t2.exec_())
    '''
    app = QApplication(sys.argv)



    ex = MyApp()
    t1 = threading.Thread()
    #t1.start()
    sign_in = Sign_in(ex)


    sys.exit(app.exec_())
