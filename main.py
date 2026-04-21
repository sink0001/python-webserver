import socket
from parser.HTTP_request import HTTP_request
from exceptions import RequestContinuityError


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

        http_request = 0
        current_request = b""
        current_body = b""
        body_bytes_left = -1
        while True:
            chunk = connection.recv(8192)
            if not chunk:
                break
            
            for i in range(len(chunk)):
                current_character = bytes([chunk[i]])
                current_request += current_character

                if body_bytes_left > 0:
                    current_body += current_character
                    body_bytes_left -= 1
                if body_bytes_left == 0:
                    if not http_request:
                        raise RequestContinuityError(f"Expected a current http request object when waiting for its body {current_body}, instead got {http_request}")
                    http_request.parse_body(current_body)
                    print(f"Body:\n{http_request.body}")
                    current_body = b""
                    body_bytes_left = -1

                if current_request[-4:] == b"\r\n\r\n":
                    http_request = HTTP_request(current_request)

                    if "content-length" in http_request.headers:
                        body_bytes_left = int(http_request.headers["content-length"][0])

                        print(f"Request line:\n- Method: {http_request.request_line["method"]}\n- Target: {http_request.request_line["target"]}\n- Version: {http_request.request_line["http_version"]}")
                        for header_name in http_request.headers:
                            for header_value in http_request.headers[header_name]:
                                print(f"{header_name}: {header_value}")
                    
                    current_request = b""



if __name__ == "__main__":
    main()