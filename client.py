import socket

client=socket.socket()
name=socket.gethostname()
port=12345
client.connect((name,port))
print('Connected')
b=''
print(client.recv(1024).decode())
while b!='/exit':
    client.send(input('Enter:').encode())
    print(client.recv(1024).decode())
client.close()