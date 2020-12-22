#import tcpServer
import serverApplycation
import sys


# andRaspTCP = tcpServer.TCPServer('172.30.1.34', 9999)
# andRaspTCP.start()

app = serverApplycation.QApplication(sys.argv)
ex = serverApplycation.MyApp()
sys.exit(app.exec_())

# server ip 주소 - ipconfig 명령으로 확인
