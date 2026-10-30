import socket
import threading

ob =socket.socket()
ob.connect(('localhost' , 2301))
ob.sendall('shreshth'.encode('utf-8'))
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
        while True:
            reply = ob.recv(1024)
            if not reply:
                print('user -- disconnected')
                break
            print(reply.decode('utf-8'))
    except KeyboardInterrupt:
        print('\n Shutting down')
    

t1 = threading.Thread(target =handle_server_send_msg , args = (ob,))
t1.start()
t2 = threading.Thread(target = handle_server_recv_msg , args = (ob,))
t2.start()