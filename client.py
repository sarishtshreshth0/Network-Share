import socket
import threading

ob =socket.socket()
ob.connect(('localhost' , 2301))

def handle_server_send_msg(ob):
    try:
        while True:
            msg = input('enter message for the server --> ')
            if msg == 'no':
                break
            ob.sendall(msg.encode('utf-8'))
    except KeyboardInterrupt:
        print('\n Shutting down')

def handle_server_recv_msg(ob):
    try:
        reply = ob.recv(1024)
        print(reply.decode('utf-8'))
    except KeyboardInterrupt:
        print('\n Shutting down')
    

t1 = threading.Thread(target =handle_server_send_msg , args = (ob ,))
t1.start()
t2 = threading.Thread(target = handle_server_recv_msg , args = (ob ,))

t2.start()