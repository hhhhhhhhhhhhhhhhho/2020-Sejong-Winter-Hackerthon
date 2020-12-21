import socket, threading
from PIL import Image
import os
import io
import cv2
import numpy

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

class TCPServerThread(threading.Thread):
    def __init__(self, tcpServerThreads, connections, connection, clientAddress):
        threading.Thread.__init__(self)

        self.tcpServerThreads = tcpServerThreads
        self.connections = connections
        self.connection = connection
        self.clientAddress = clientAddress

    def run(self):
        try:
             #String형의 이미지를 수신받아서 이미지로 변환 하고 화면에 출력
            length = recvall(self.connection,16) #길이 16의 데이터를 먼저 수신하는 것은 여기에 이미지의 길이를 먼저 받아서 이미지를 받을 때 편리하려고 하는 것이다.
            stringData = recvall(self.connection, int(length))
            data = numpy.fromstring(stringData, dtype='uint8')
            decimg=cv2.imdecode(data,1)
            cv2.imshow('SERVER',decimg)
            cv2.imwrite('H:\\2020Hackathon\\team\\2020-Sejong-Winter-Hackerthon\\DB\\Server\\images\\test.jpg', decimg)
            print("tcp server :: img receive...")
            cv2.waitKey(0)
            cv2.destroyAllWindows() 

        except:
            print("connect close")
            self.connections.remove(self.connection)
            self.tcpServerThreads.remove(self)
            exit(0)
        self.connections.remove(self.connection)
        self.tcpServerThreads.remove(self)

    def send(self, message):
        print("tcp server :: ", message)
        try:
            for i in range(len(self.connections)):
                self.connections[i].sendall(message.encode())
        except:
            pass


