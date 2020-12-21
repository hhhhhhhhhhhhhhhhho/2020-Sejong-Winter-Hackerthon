import tcpServer


# server ip 주소 - ipconfig 명령으로 확인
andRaspTCP = tcpServer.TCPServer('127.0.0.1', 9999)
andRaspTCP.start()
