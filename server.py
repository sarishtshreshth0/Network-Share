import socket
import threading 
import struct
ob = socket.socket()
ob.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ob.bind(("localhost", 2301))
ob.listen(4)

clients = {}
clients_lock = threading.Lock()
print("Server is running on port 2301")


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

def send_msg_client(clients):
    try:
        while True:
            reply = input("Reply to client --> ").split('|')
            whom , message = reply[0] , reply[-1]
            names_list = []
            with clients_lock:
                if whom == 'disconnect':
                    if message in clients:
                        save = clients[message]
                        clients.pop(message )
                        print(message , ' is forcefully removed')
                        save.close()
                elif whom == 'broadcast':
                    names_list = list(clients.values())    
                elif whom in clients:
                    names_list = [clients[whom]]
                else:
                    print(whom , ' is not connected till now')
            for name_ref in names_list:
                try:
                    formed_msg = struct.pack('!I' , len(message)) + message.encode('utf-8')
                    name_ref.sendall(formed_msg)
                except Exception as e:
                    print('Error ' , e)
    except OSError as e:
        print('Socket error:' , e)
    

def handle_client(client_obj , addr, name , clients):
    print("Connected with:", addr)
    try:
        while True:
            msg = recieve_message(client_obj)
            if not msg:
                print("Client disconnected:", addr)
                break
            print("Client:", msg.decode("utf-8"))
            
    except OSError as e:
        print("Socket error:", e)

    finally:
        with clients_lock:
            if clients.get(name) is client_obj: 
                clients.pop(name , None)
        client_obj.close()
        print("Client socket closed")



thread_send = threading.Thread(target = send_msg_client , args = (clients,))
thread_send.start()
try:
    max_size = 1024*1024
    while True:
        client_obj , addr = ob.accept()
        print(client_obj)
        name = recieve_message(client_obj)
        print(name)
        with clients_lock:
            clients[name.decode('utf-8')] = client_obj
        t1 = threading.Thread(target = handle_client  , args = (client_obj , addr , name ,clients))
        t1.start()
        print(clients)

except KeyboardInterrupt:
    print("\n Server Shutting down")

finally:
    ob.close()