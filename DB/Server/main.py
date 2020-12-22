import tcpServer

# server ip 주소 - ipconfig 명령으로 확인
andRaspTCP = tcpServer.TCPServer('172.16.44.88', 9999)
andRaspTCP.start()
