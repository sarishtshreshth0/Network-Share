
import socket


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(("127.0.0.1" , 5000))

def recv_exact(sock , size ):
    data = bytearray()

    while len(data) < size:
        chunk = sock.recv(size - len(data))
        if not chunk:
            raise ConnectionError('Connection closed before headers completed')
        data.extend(chunk)

    return bytes(data)



request = (
    "GET /about HTTP/1.1\r\n"
    "Host: 127.0.0.1:5000\r\n"
    "Connection: close\r\n"
    "\r\n"
)

client.sendall(request.encode('utf-8'))

def recv_headers(sock ):
    response = b''
    while b'\r\n\r\n' not in response:

        chunk = sock.recv(1)
      
        if not chunk:
            raise ConnectionError('headers gyab hogya')
        response += chunk
    return response

response  = recv_headers(client)

headers , body = response.split(b"\r\n\r\n"  ,1)

ex_headers = headers.split(b'\r\n')
print('Status:' , ex_headers[0].decode())
print('\nHeaders')
dict_headers = {}
for i in ex_headers[1:]:
    key, value = i.split(b':', 1)
    dict_headers[key.decode().strip()] = value.decode().strip()
print(dict_headers)
expected_length = int(dict_headers['Content-Length'])
print('\nBody')

result = recv_exact(client , expected_length)
print(result.decode())
client.close()