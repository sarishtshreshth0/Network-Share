import socket
import threading
import struct
ob =socket.socket()
ob.connect(('localhost' , 2301))
name_forming = b'shreshth'
entire=struct.pack('!I' , len(name_forming)) + name_forming
ob.sendall(entire)

def recv_exact(sock , size):
    data = bytearray()
    while len(data) < size:
        chunk = sock.recv(size - len(data))
        if not chunk:
            return None
        data.extend(chunk)
    return bytes(data)

def recieve_message(sock):
    header = recv_exact(sock , 4)
    if header is None:
        return None
    message_length = struct.unpack('!I' , header)[0]
    message = recv_exact(sock, message_length)
    return message

def handle_server_send_msg(ob):
    try:
        while True:
            msg = input('enter message for the server --> ').encode('utf-8')
            if msg == 'no':
                break
            forming_msg=struct.pack('!I' , len(msg)) + msg
            ob.sendall(forming_msg)
            print('msg successfully sent --: ' , forming_msg)
            
    except KeyboardInterrupt:
        print('\n Shutting down')

def handle_server_recv_msg(ob):
    try:
        while True:
            reply = recieve_message(ob)
            if not reply:
                print('user -- disconnected')
                break
            print(reply.decode('utf-8'))
    except Exception as e:
        print('Error : ' , e)
    

t1 = threading.Thread(target =handle_server_send_msg , args = (ob,))
t1.start()
t2 = threading.Thread(target = handle_server_recv_msg , args = (ob,))
t2.start()