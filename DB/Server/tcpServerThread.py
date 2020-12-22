import socket, threading
from PIL import Image
import os
import io
import cv2
import numpy
from datetime import datetime
import DBconnection

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

def detect_cheat(sock):
    student_id = sock.recv(8)
    exam_id = sock.recv(1)
    error_type = sock.recv(1)
    print(student_id.decode())
        #String형의 이미지를 수신받아서 이미지로 변환 하고 화면에 출력
    length = recvall(sock,16) #길이 16의 데이터를 먼저 수신하는 것은 여기에 이미지의 길이를 먼저 받아서 이미지를 받을 때 편리하려고 하는 것이다.
    stringData = recvall(sock, int(length))
    data = numpy.fromstring(stringData, dtype='uint8')
    decimg=cv2.imdecode(data,1)
    url = 'H:\\2020Hackathon\\team\\2020-Sejong-Winter-Hackerthon\\DB\\Server\\images\\' + datetime.now().strftime('%Y%m%d%H%M%S') + '.jpg'
    print(url)
    DBconnection.store_facelog(exam_id, student_id, url, error_type, "three")
    cv2.imshow('SERVER',decimg)
    cv2.imwrite(url, decimg)
    print("tcp server :: img receive...")
    cv2.waitKey(0)
    cv2.destroyAllWindows() 

def send_exam_student_data(sock):
    exam_id = sock.recv(1)
    student_id = sock.recv(8)
    print(student_id.decode())
    file = DBconnection.load_studentdata(exam_id, student_id)
    #String형의 이미지를 수신받아서 이미지로 변환 하고 화면에 출력
    data = cv2.imread(file[0][0], cv2.IMREAD_UNCHANGED)

    # '.jpg'means that the img of the current picture is encoded in jpg format, and the result of encoding in different formats is different.
    img_encode = cv2.imencode('.jpg', data)[1]

    data_encode = numpy.array(img_encode)
    stringData = data_encode.tostring()

    #String 형태로 변환한 이미지를 socket을 통해서 전송
    sock.send(str(len(stringData)).ljust(16).encode())
    sock.send(stringData)

    print("tcp server :: img send...")

    # 시험정보 넘김
    exam_data = DBconnection.load_examdata2(exam_id, student_id)
    # 시험날짜
    sock.send(exam_data[0][1].strftime("%Y-%m-%d").encode())
    # 시작시간
    sock.send(exam_data[0][1].strftime("%H:%M:%S").encode())
    # 종료시간
    sock.send(exam_data[0][2].strftime("%H:%M:%S").encode())
    # 사람이름
    sock.send(str(len(exam_data[0][3].encode())).ljust(16).encode())
    sock.send(exam_data[0][3].encode())
    # 과목명
    sock.send(exam_data[0][0].encode())

def receive_clipboard(sock):
    exam_id = sock.recv(1)
    student_id = sock.recv(8)
    clipboard = sock.recv(255)
    DBconnection.store_clipboard(exam_id, student_id, clipboard)

class TCPServerThread(threading.Thread):
    def __init__(self, tcpServerThreads, connections, connection, clientAddress):
        threading.Thread.__init__(self)

        self.tcpServerThreads = tcpServerThreads
        self.connections = connections
        self.connection = connection
        self.clientAddress = clientAddress

    def run(self):
        # try:
        type = self.connection.recv(1)
        if type.decode() == '1':
            send_exam_student_data(self.connection)
        if type.decode() == '2':
            detect_cheat(self.connection)
        if type.decode() == '3':
            receive_clipboard(self.connection)

        # except:
        #     print("connect close")
        #     self.connections.remove(self.connection)
        #     self.tcpServerThreads.remove(self)
        #     exit(0)
        self.connections.remove(self.connection)
        self.tcpServerThreads.remove(self)

    def send(self, message):
        print("tcp server :: ", message)
        try:
            for i in range(len(self.connections)):
                self.connections[i].sendall(message.encode())
        except:
            pass


