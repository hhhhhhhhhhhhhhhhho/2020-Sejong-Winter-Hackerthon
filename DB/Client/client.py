
import socket
import sys
from PIL import Image
import os
import io
from array import array
import base64
import cv2
import numpy

host = '127.0.0.1'
port = 9999
addr = (host, port)

def run():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect(addr)
        except Exception as e:
            print(" (%s:%s) not connect" % addr)
            sys.exit()
        print("(%s:%s) connect" % addr)

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


if __name__ == '__main__':
    run()