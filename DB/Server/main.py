import tcpServer

# server ip 주소 - ipconfig 명령으로 확인
andRaspTCP = tcpServer.TCPServer('172.30.1.34', 9999)
andRaspTCP.start()
