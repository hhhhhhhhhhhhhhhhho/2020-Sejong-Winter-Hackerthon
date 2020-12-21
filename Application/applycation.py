import sys
import clipboard
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import QTimer, QDateTime
from PyQt5.QtGui import QPalette, QColor, QPixmap

class MyApp(QWidget):

    def __init__(self):
        super().__init__()

        self.widget_title = QWidget(parent=self, flags=Qt.Widget)
        self.init_widget_title(self.widget_title)

        self.widget_info = QWidget(parent=self, flags=Qt.Widget)
        self.init_widget_info()

        self.widget_cam = QWidget(parent=self, flags=Qt.Widget)
        self.init_widget_cam()

        self.initUI()

    def init_widget_title(self, w):

        #self.widget_title.setStyleSheet("background-color: white")


        w.label_title = QLabel('I See You', w)
        font = w.label_title.font()
        font.setPointSize(20)
        font.setBold(True)
        w.label_title.setFont(font)

        w.label_ID = QLabel('17011477 목승주', w)

        w.hbox_title = QHBoxLayout()
        w.hbox_title.addWidget(w.label_title)
        w.hbox_title.addStretch(1)
        w.hbox_title.addWidget(w.label_ID)

        w.setLayout(w.hbox_title)


    def init_widget_info(self):


        self.widget_info.label_lecture = QLabel('\n2020년 2학기 컴퓨터구조', self.widget_info)
        font = self.widget_info.label_lecture.font()
        font.setBold(True)
        font.setPointSize(16)
        self.widget_info.label_lecture.setFont(font)

        self.widget_info.label_duration = QLabel('\n시험시간 : 2020/12/21 15:00 ~ 2020/12/21 16:30', self.widget_info)
        font = self.widget_info.label_duration.font()
        font.setPointSize(12)
        font.setBold(True)
        self.widget_info.label_duration.setFont(font)

        self.widget_info.label_time = QLabel('\n' + QDateTime.currentDateTime().toString(Qt.DefaultLocaleLongDate), self.widget_info)
        font = self.widget_info.label_time.font()
        font.setPointSize(12)
        font.setBold(True)
        self.widget_info.label_time.setFont(font)

        self.widget_info.vbox_info = QVBoxLayout()
        self.widget_info.vbox_info.addWidget(self.widget_info.label_lecture)
        self.widget_info.vbox_info.addWidget(self.widget_info.label_duration)
        self.widget_info.vbox_info.addWidget(self.widget_info.label_time)

        self.widget_info.setLayout(self.widget_info.vbox_info)


    def init_widget_cam(self):
        self.widget_cam.btn_start = QPushButton('Clear cipboard and start!')
        self.widget_cam.btn_start.clicked.connect(self.getClipboard)

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
        #self.showMaximized()
        self.setFixedSize(800, 800)
        self.move(0, 0)

        pal = QPalette() # 배경색 변경
        pal.setColor(QPalette.Background, QColor(255, 255, 255))
        self.setPalette(pal)

        vbox = QVBoxLayout()
        vbox.addWidget(self.widget_title)
        vbox.addWidget(self.widget_info)
        vbox.addStretch(2)
        vbox.addWidget(self.widget_cam)
        vbox.addStretch(1)

        self.setLayout(vbox)

        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.setCurrentTime)
        self.timer.start()

        self.show()

    def setCurrentTime(self):
        datetime = QDateTime.currentDateTime()
        self.widget_info.label_time.setText('\n' + datetime.toString(Qt.DefaultLocaleLongDate))

    def getClipboard(self):
        data = clipboard.clear_clipboard()
        print(data)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
