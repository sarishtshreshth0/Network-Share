
import socket
import threading
import struct

HOST = "127.0.0.1"
PORT = 2301
MAX_SIZE = 1024 * 1024

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(10)

clients = {}
send_lock_clients = {}
clients_lock = threading.Lock()

print(f"Server running on port {PORT}")


# ---------------- RECEIVE FUNCTIONS ----------------

def recv_exact(sock, size):
    data = bytearray()

    while len(data) < size:
        chunk = sock.recv(size - len(data))

        if not chunk:
            return None

        data.extend(chunk)

    return bytes(data)


def receive_message(sock):
    header = recv_exact(sock, 4)

    if header is None:
        return None

    message_length = struct.unpack("!I", header)[0]

    if message_length > MAX_SIZE:
        raise ValueError("Message too large")

    return recv_exact(sock, message_length)


# ---------------- SEND FUNCTION ----------------

def send_message(sock, lock, message):
    message_bytes = message.encode("utf-8")

    if len(message_bytes) > MAX_SIZE:
        raise ValueError("Message too large")

    packet = struct.pack("!I", len(message_bytes)) + message_bytes

    with lock:
        sock.sendall(packet)


# ---------------- REMOVE CLIENT ----------------

def remove_client(name, client_obj):
    with clients_lock:

        # Prevent an old handler from removing a newer connection
        if clients.get(name) is client_obj:
            clients.pop(name, None)
            send_lock_clients.pop(name, None)

    try:
        client_obj.close()
    except OSError:
        pass

    print(f"{name} disconnected")


# ---------------- CLIENT HANDLER ----------------

def handle_client(client_obj, addr, name):

    print("Connected:", name, addr)

    try:
        while True:

            msg = receive_message(client_obj)

            if msg is None:
                break

            print(f"{name}: {msg.decode('utf-8')}")

    except (OSError, ValueError) as e:
        print("Client error:", name, e)

    finally:
        remove_client(name, client_obj)


# ---------------- SERVER SENDER ----------------

def send_msg_client():

    while True:

        try:
            reply = input("Reply to client --> ")

            if "|" not in reply:
                print("Format: username|message")
                print("Broadcast: broadcast|message")
                print("Disconnect: disconnect|username")
                continue

            whom, message = reply.split("|", 1)

            targets = []

            # Disconnect client
            if whom == "disconnect":

                with clients_lock:
                    sock = clients.get(message)
                    lock = send_lock_clients.get(message)

                if sock is None:
                    print("Client not found")
                    continue
                
                # Coordinate close with any active send
                with lock:
                    remove_client(message, sock)

                continue

            # Get recipient sockets and their locks
            with clients_lock:

                if whom == "broadcast":

                    targets = [
                        (name, sock, send_lock_clients[name])
                        for name, sock in clients.items()
                    ]

                elif whom in clients:

                    targets = [
                        (
                            whom,
                            clients[whom],
                            send_lock_clients[whom]
                        )
                    ]

                else:
                    print("Client not connected:", whom)
                    continue

            # Send outside dictionary lock
            for name, sock, lock in targets:

                try:
                    send_message(sock, lock, message)

                except (OSError, ValueError) as e:
                    print("Send error:", name, e)
                    remove_client(name, sock)

        except (KeyboardInterrupt, EOFError):
            print("\nServer sender stopped")
            break


# ---------------- ACCEPT CLIENTS ----------------

sender_thread = threading.Thread(
    target=send_msg_client,
    daemon=True
)

sender_thread.start()

try:

    while True:

        client_obj, addr = server.accept()

        try:
            # Receive username
            name_data = receive_message(client_obj)

            if name_data is None:
                client_obj.close()
                continue

            name = name_data.decode("utf-8")

            if not name or "|" in name:
                client_obj.close()
                continue

            with clients_lock:

                # Reject duplicate username
                if name in clients:
                    client_obj.close()
                    print("Duplicate username:", name)
                    continue

                clients[name] = client_obj
                send_lock_clients[name] = threading.Lock()

            thread = threading.Thread(
                target=handle_client,
                args=(client_obj, addr, name),
                daemon=True
            )

            thread.start()

            print("Current clients:", list(clients.keys()))

        except (OSError, ValueError, UnicodeDecodeError) as e:
            print("Connection setup error:", e)
            client_obj.close()

except KeyboardInterrupt:
    print("\nServer shutting down")

finally:

    with clients_lock:
        active_clients = list(clients.values())
        clients.clear()
        send_lock_clients.clear()

    for sock in active_clients:
        try:
            sock.close()
        except OSError:
            pass

    server.close()
