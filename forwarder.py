import socket
import threading


def forward(source, destination):
    try:
        while True:
            data = source.recv(4096)

            if not data:
                break

            destination.sendall(data)

    except OSError as e:
        print("Forwarding error:", e)

    finally:
        try:
            destination.shutdown(socket.SHUT_WR)
        except OSError:
            pass


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.setsockopt(
    socket.SOL_SOCKET,
    socket.SO_REUSEADDR,
    1
)

server.bind(("127.0.0.1", 9000))
server.listen(5)

print("Forwarder running on port 9000")

while True:
    client, addr = server.accept()

    print("New client:", addr)

    target = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    target.connect(("127.0.0.1", 5000))

    t1 = threading.Thread(
        target=forward,
        args=(client, target)
    )

    t2 = threading.Thread(
        target=forward,
        args=(target, client)
    )

    t1.start()
    t2.start()

    def cleanup(t1, t2, client, target):
        t1.join()
        t2.join()

        client.close()
        target.close()

    threading.Thread(
        target=cleanup,
        args=(t1, t2, client, target),
        daemon=True
    ).start()