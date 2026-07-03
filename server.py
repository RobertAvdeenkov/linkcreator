import socket
from _thread import*
from datetime import datetime
count=1
def main(con):
    global count
    m=count
    con.sendall(f'Клиент под номером {m} подключился'.encode())
    count=count+1
    b=con.recv(1024).decode()
    if b=='/exit':
        con.sendall(f'Клиент под номером {m} отключился'.encode())
        con.close()
    else:
        con.sendall(b.encode())

server=socket.socket()
name=socket.gethostname()
port=12345
server.bind((name,port))
server.listen(5)

while True:
    con,adr=server.accept()
    start_new_thread(main,(con,))
