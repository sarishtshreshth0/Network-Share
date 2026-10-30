import socket
import threading 

ob = socket.socket()
ob.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ob.bind(("localhost", 2301))
ob.listen(4)

clients = {}
print("Server is running on port 2301")

def send_msg_client(clients):
    try:
        while True:
            reply = input("Reply to client --> ").split('|')
            name , message = reply[0] , reply[-1]
            if name == 'broadcast':
                for name in clients:
                    clients[name].sendall(message.encode("utf-8"))    
            elif name in clients:
                clients[name].sendall(message.encode("utf-8"))
            else:
                print(name , ' is not connected till now')
    except OSError as e:
        print('Socket error:' , e)
    

def handle_client(client_obj , addr):
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
        client_obj.close()
        print("Client socket closed")
try:
    while True:
        client_obj , addr = ob.accept()
        name = client_obj.recv(1024).decode('utf-8')
        clients[name] = client_obj
        t1 = threading.Thread(target = handle_client  , args = (client_obj , addr))
        thread_send = threading.Thread(target = send_msg_client , args = (clients,))
        t1.start()
        thread_send.start()
        print(clients)

except KeyboardInterrupt:
    print("\n Server Shutting down")

finally:
    ob.close()