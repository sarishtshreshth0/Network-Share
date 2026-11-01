import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind(("127.0.0.1", 2301))
server.listen(5)

print("VPS is listening...")

client, address = server.accept()
print("Laptop connected:", address)

while True:
    data = client.recv(1024)

    if not data:
        print("Laptop disconnected")
        break

    print("Laptop:", data.decode())

    reply = input("Reply to laptop: ")

    client.sendall(reply.encode())

client.close()
server.close()