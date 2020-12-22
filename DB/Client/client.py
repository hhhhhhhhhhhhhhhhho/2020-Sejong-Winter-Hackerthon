
import socket
import sys
import os
import io
from array import array
import base64
import cv2
import numpy

host = '172.30.1.34'
port = 9999
addr = (host, port)

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

def login(student_id, exam_id):
    print("login")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect(addr)
        except Exception as e:
            print(" (%s:%s) not connect" % addr)
            sys.exit()
        print("(%s:%s) connect" % addr)

        s.send('1'.encode())
        #학번 전송
        s.send(exam_id.encode())
        s.send(student_id.encode())
        
        length = recvall(s,16) #길이 16의 데이터를 먼저 수신하는 것은 여기에 이미지의 길이를 먼저 받아서 이미지를 받을 때 편리하려고 하는 것이다.
        print("length=", length)
        stringData = recvall(s, int(length))
        data = numpy.fromstring(stringData, dtype='uint8')
        decimg=cv2.imdecode(data,1)

        
        # 시험날짜
        exam_date = s.recv(10)
        # 시작시간
        start = s.recv(8)
        # 종료시간
        end = s.recv(8)
        # 학생 이름
        len = recvall(s, 16)
        name = recvall(s, int(len))
        # 과목명
        subname = s.recv(40)

        cv2.imshow('CLIENT',decimg)
        print("tcp client :: img receive...")
        cv2.waitKey(0)
        cv2.destroyAllWindows() 
        s.close()

        # 이미지, 과목명, 시험날짜, 시작시간, 끝시간, 학새이름
        data = list((decimg, subname.decode(), exam_date.decode(), start.decode(), end.decode(), name.decode()))
        return data


def cheating(student_id, exam_id, error_type):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect(addr)
        except Exception as e:
            print(" (%s:%s) not connect" % addr)
            sys.exit()
        print("(%s:%s) connect" % addr)

        s.send('2'.encode())
        #학번 전송
        s.send(student_id.encode())
        s.send(exam_id.encode())
        s.send(error_type.encode())
        #OpenCV를 이용해서 webcam으로 부터 이미지 추출
        capture = cv2.VideoCapture(0)
        ret, frame = capture.read()

        #추출한 이미지를 String 형태로 변환(인코딩)시키는 과정
        encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]
        result, imgencode = cv2.imencode('.jpg', frame, encode_param)
        data = numpy.array(imgencode)
        stringData = data.tostring()
        
        #String 형태로 변환한 이미지를 socket을 통해서 전송
        s.send(str(len(stringData)).ljust(16).encode())
        s.send(stringData)
        s.close()

        #다시 이미지로 디코딩해서 화면에 출력. 그리고 종료
        decimg=cv2.imdecode(data,1)
        cv2.imshow('CLIENT',decimg)
        cv2.waitKey(0)
        cv2.destroyAllWindows() 

def send_clipboard(student_id, exam_id, clipboard):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect(addr)
        except Exception as e:
            print(" (%s:%s) not connect" % addr)
            sys.exit()
        print("(%s:%s) connect" % addr)

        s.send('3'.encode())

        # 학번, 시험번호 전송
        s.send(exam_id.encode())
        s.send(student_id.encode())
        s.send(clipboard.encode())

        s.close()

def run():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect(addr)
        except Exception as e:
            print(" (%s:%s) not connect" % addr)
            sys.exit()
        print("(%s:%s) connect" % addr)

        #학번 전송
        s.send(id.encode())

        data = cv2.imread('H:\\2020Hackathon\\team\\2020-Sejong-Winter-Hackerthon\\DB\\Client\\test.jpg', cv2.IMREAD_UNCHANGED)

         # '.jpg'means that the img of the current picture is encoded in jpg format, and the result of encoding in different formats is different.
        img_encode = cv2.imencode('.jpg', data)[1]
        # imgg = cv2.imencode('.png', img)

        data_encode = numpy.array(img_encode)
        stringData = data_encode.tostring()

        #String 형태로 변환한 이미지를 socket을 통해서 전송
        s.send(str(len(stringData)).ljust(16).encode())
        s.send(stringData)
        s.close()

        cv2.imshow('CLIENT',data)
        cv2.waitKey(0)
        cv2.destroyAllWindows() 


'''
if __name__ == '__main__':
    run()
'''


#cheating('18011529', '1', '2')
