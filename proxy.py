import socket
from socket import error
import random
import getopt
import sys
class ProxyServerTest():
    def __init__(self,port,filename):
        #AF_INET　　——————————    使用IPv4
        #SOCK_STREAM      TCP套接字类型  一般这种类型比较有用
        self.ip_list = {}
        self.port = port
        self.filename = filename
    def Loadips(self):
        print("[*]Loading file proxy ip...")
        with open(self.filename) as content:
            lines = content.readlines()
            for line in lines:
                ip, port = line.strip().split(":",1)
                self.ip_list[ip] = port
        print('[*]Prepare proxy ip')
    def run(self):
        while True:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                # bind 绑定到某端口，用于服务端
                server.bind(('127.0.0.1', int(self.port))) #9999为端口，可更改
                # 连接数量
                server.listen(10)
                print('[*]Waiting connection..')
            except error as e:
                print("[-]Warning : " + str(e))
                return "create error"
            # 接收一个连接.该socket 必须要绑定一个地址和监听连接.返回值是一对（conn，address）
            connection, addr = server.accept()
            print('[*]accept connect from ' + str(addr))
            # 接收客户端发来的消息,data为bytes类型的数据
            try:
                data = connection.recv(1024)
                if not data:
                    break
                    print('[*] Waiting accept data...')
            except error as e:
                print('[-]accept error: ' + str(e))
            print('[*]accept data from client success')
            while True:
                count = 5
                #创建连接到proxy服务器的socket
                proxyserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                proxyip = random.sample(self.ip_list.keys(), 1)
                print("[!]Now proxy ip:" + proxyip[0])
                proxyport = self.ip_list[proxyip[0]]
                # 将接收数据转发给代理服务器
                while count:
                    #测试连接
                    try:
                        proxyserver.settimeout(10)
                        proxyserver.connect((proxyip[0], int(proxyport)))
                        print('[*]connect to proxy server success')
                        break
                    except:
                        count -= 1
                        print("[-]Connect failed,Reconnect {} times will change proxy ip .." .format(count))
                        continue
                break
            try:
                proxyserver.send(data)
                print('[*]sending data to proxy server success')
            except error as e:
                print("[-]Sent error : " + str(e))
                return "send error"
                    #发送数据
            while True:
                # 将代理服务器的回应转发给客户端
                print('[*]recive data from proxy server..')
                try:
                    data_res = proxyserver.recv(1024)
                    print(data_res)
                    if data_res == b'':
                        break
                    print('[*]: Send data...')
                    connection.send(data_res)
                except socket.timeout as e:
                    print("[-]data send client error: " + str(e))
                    continue
                # 关闭连接
            print('[!]Broking connection')
            server.close()
            proxyserver.close()

def usage():
    print('python proxy.py -f <filename> [-p <port>] [-h]')
    print(' -f |--file <filename>')
    print(' -p |--port Set proxy port,default 9999')
    print(' -h |--help Shows this help\n')
    print('Eg. python proxy.py -f ip.txt -p 9999\n')
def main(argv):
    port = 9999
    try:
        opts, args = getopt.getopt(argv, 'hf:p:', ['help', 'file=', 'port='])
    except getopt.GetoptError:
        usage()
        sys.exit(-1)
    for i,u in opts:
        if i in ('-h','--help'):
            usage()
            exit(-1)
        if i in ('-f','--file'):
            filename = u
        if i in ('-p','--port'):
            port = u
    try:
        if filename == '':
            usage()
            sys.exit(-1)
    except:
        usage()
        sys.exit(-1)
    print('\033[01;32m[*] start process...\033[0m')
    start = ProxyServerTest(port,filename)
    start.Loadips()
    start.run()

 if __name__ == '__main__':
    main(sys.argv[1:])
