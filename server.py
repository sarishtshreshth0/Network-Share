import socket
import threading 

ob = socket.socket()
ob.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ob.bind(("localhost", 2301))
ob.listen(4)

clients = {}
clients_lock = threading.Lock()
print("Server is running on port 2301")

def send_msg_client(clients):
    try:
        while True:
            reply = input("Reply to client --> ").split('|')
            whom , message = reply[0] , reply[-1]
            names_list = []
            with clients_lock:
                if whom == 'disconnect':
                        if message in clients:
                            clients[message].close()
                            clients = clients.pop(message , None)
                            print(message , ' is forcefully removed')
                elif whom == 'broadcast':
                    names_list = list(clients.values())    
                elif whom in clients:
                    names_list = [clients[whom]]
                else:
                    print(whom , ' is not connected till now')
            for name_ref in names_list:
                name_ref.sendall(message.encode("utf-8"))
            
    except OSError as e:
        print('Socket error:' , e)
    

def handle_client(client_obj , addr, name , clients):
    print("Connected with:", addr)
    try:
        while True:
            msg = client_obj.recv(1024)
            if not msg:
                print("Client disconnected:", addr)
                break

            print("Client:", msg.decode("utf-8"))
            
    except OSError as e:
        print("Socket error:", e)

    finally:
        with clients_lock:
            if name in clients:
                clients = clients.pop(name , None)
        client_obj.close()
        print("Client socket closed")
thread_send = threading.Thread(target = send_msg_client , args = (clients,))
thread_send.start()
try:
    while True:
        client_obj , addr = ob.accept()
        name = client_obj.recv(1024).decode('utf-8')
        with clients_lock:
            clients[name] = client_obj
        t1 = threading.Thread(target = handle_client  , args = (client_obj , addr , name ,clients))
        t1.start()
        print(clients)

except KeyboardInterrupt:
    print("\n Server Shutting down")

finally:
    ob.close()