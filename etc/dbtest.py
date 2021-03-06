
import socket
import sys
import os
import io
from array import array
import base64
import cv2
import numpy

host = '172.16.44.88'
port = 9999
addr = (host, port)
id = '18011529'

def login(student_id, exam_id):
    print("login")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect(addr)
        except Exception as e:
            print(" (%s:%s) not connect" % addr)
            sys.exit()
        print("(%s:%s) connect" % addr)

        #학번 전송
        s.send(student_id.encode())
        s.send(student_exam.encode())

        s.close()

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

        '''
        #OpenCV를 이용해서 webcam으로 부터 이미지 추출
        capture = cv2.VideoCapture(0)
        ret, frame = capture.read()

        #추출한 이미지를 String 형태로 변환(인코딩)시키는 과정
        encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]
        result, imgencode = cv2.imencode('.jpg', frame, encode_param)
        data = numpy.array(imgencode)
        stringData = data.tostring()
        '''

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
        #다시 이미지로 디코딩해서 화면에 출력. 그리고 종료
        decimg=cv2.imdecode(data,1)
        cv2.imshow('CLIENT',decimg)
        cv2.waitKey(0)
        cv2.destroyAllWindows() 
        '''

'''
if __name__ == '__main__':
    run()
'''

cheating('18011529', '1', '2')
