import socket
import threading 

ob = socket.socket()
ob.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ob.bind(("localhost", 2301))
ob.listen(4)


print("Server is running on port 2301")

count = 0
def recv_msg_client(client_obj , addr):
    reply = input("Reply to client --> ")
    client_obj.sendall(reply.encode("utf-8"))
def handle_client(client_obj , addr):
    global count
    print("Connected with:", addr)
    try:
        while True:
            msg = client_obj.recv(1024)
            count +=1
            if not msg:
                print("Client disconnected:", addr)
                break

            print("Client:", msg.decode("utf-8"))
            thread_recv = threading.Thread(target = recv_msg_client , args = (client_obj , addr))
            thread_recv.start()
            if count >=1000:
                print('infinit loop')
                break
    except OSError as e:
        print("Socket error:", e)

    finally:
        client_obj.close()
        print("Client socket closed")
try:
    while True:
        client_obj , addr = ob.accept()
        t1 = threading.Thread(target = handle_client  , args = (client_obj , addr))
        t1.start()
except KeyboardInterrupt:
    print("\n Server Shutting down")

finally:
    ob.close()