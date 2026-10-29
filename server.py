import socket
import threading 
ob =socket.socket()
ob.bind(('localhost' , 2301))
ob.listen(4)

client_obj , addr = ob.accept()
print('connected with this address ', addr)
conn = True
while conn:
    message = input('message for the client -- >')
    if message == 'no':
        conn = False
        ob.close()
    
    client_obj.sendall(message.encode('utf-8'))
    msg=client_obj.recv(1024)
    print(msg.decode('utf-8'))

