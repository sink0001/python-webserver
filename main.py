import socket
from parser.HTTP_request import HTTP_request


def main():
    HOST = "localhost"
    PORT = 12345
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST, PORT))
    print("bound TCP socket to 127.0.0.1:12345")
    sock.listen(10)

    while True:
        connection, address = sock.accept()
        print(f"connection: {connection} address: {address}")

        current_request = b""
        while True:
            chunk = connection.recv(8192)
            if not chunk:
                break
            
            for i in range(4, len(chunk)+1):
                last_4_bytes = chunk[i-4:i]
                if i % 4 == 0:
                    current_request += last_4_bytes

                if last_4_bytes == b"\r\n\r\n":
                    http_request = HTTP_request(current_request)
                    request_line, headers = http_request.request_line, http_request.headers

                    print(f"Request line:\n- Method: {request_line["method"]}\n- Target: {request_line["target"]}\n- Version: {request_line["http_version"]}")
                    for header in headers:
                        for value in headers[header]:
                            print(f"{header}: {value}")

                    current_request = b""

if __name__ == "__main__":
    main()