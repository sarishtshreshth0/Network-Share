import socket
import threading

agent = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
agent.connect(("127.0.0.1", 2301))

print("Connected to VPS!")

def receive_msg():
    while True:
        data = agent.recv(1024)

        if not data:
            print("VPS disconnected")
            break

        print("\nVPS:", data.decode())

threading.Thread(target=receive_msg, daemon=True).start()

while True:
    msg = input("Enter message: ")

    if msg == "exit":
        break

    agent.sendall(msg.encode())

agent.close()