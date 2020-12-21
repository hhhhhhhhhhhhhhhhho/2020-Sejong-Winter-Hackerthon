import tcpServer

# server ip 주소 - ipconfig 명령으로 확인
andRaspTCP = tcpServer.TCPServer('192.168.35.190', 9999)
andRaspTCP.start()
