
import socket


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(("127.0.0.1" , 5000))


class HTTPResponse:
    def __init__(self , status , headers , body):
        self.status = status
        self.headers = headers
        self.body = body
    def show_all(self):
        print('Status' , self.status)
        print('Headers' , self.headers)
        print('Body' ,  self.body)
    def get_header(self , name):
        print(self.headers.get(name.lower()))


def recv_exact(sock , size ):
    data = bytearray()

    while len(data) < size:
        chunk = sock.recv(size - len(data))
        if not chunk:
            raise ConnectionError('Connection closed before headers completed')
        data.extend(chunk)

    return bytes(data)

def read_chunked_body(sock):
    body = bytearray()

    while True:
        size_line = bytearray()
        while not size_line.endswith(b'\r\n'):
            chunk = sock.recv(1)
            if not chunk:
                raise ConnectionError('Shit')
            size_line.extend(chunk)

        size = int(size_line.strip() , 16)
        if size == 0:
            break
        data = recv_exact(sock , size)
        body.extend(data)
        ending = recv_exact(sock, 2)

        if ending != b"\r\n":
            raise ValueError("Invalid chunk ending")

    return bytes(body)

def read_http_body(sock, headers):

    transfer_encoding = headers.get("transfer-encoding", "").lower()

    if transfer_encoding == "chunked":
        return read_chunked_body(sock)

    elif "content-length" in headers:
        size = int(headers["content-length"])
        return recv_exact(sock, size)

    else:
        raise ValueError("Unsupported body framing")

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

raw_headers , body = response.split(b"\r\n\r\n"  ,1)
def parse_response(headers , body):
    ex_headers = headers.split(b'\r\n')
    Status = ex_headers[0].decode()
    dict_headers = {}
    for i in ex_headers[1:]:
        key, value = i.split(b':', 1)
        dict_headers[key.decode().strip().lower()] = value.decode().strip()
    result = read_http_body(client, dict_headers)
    all_response = HTTPResponse(Status , dict_headers , result.decode())
    return all_response

    
all_response = parse_response(raw_headers , body)
all_response.show_all()
all_response.get_header('content-length')
client.close()