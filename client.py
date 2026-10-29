import socket

ob =socket.socket()
ob.connect(('localhost' , 2301))

conn = True

while conn:
    msg = input('enter message for the server --> ')
    if msg == 'no':
        ob.close()
        conn = False
    ob.sendall(msg.encode('utf-8'))
    reply = ob.recv(1024)
    
    print(reply.decode('utf-8'))