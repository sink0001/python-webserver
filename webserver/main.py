import socket


def main():
    HOST = "localhost"
    PORT = 12345
    LOGFILE_PATH = "./example_mini_server/incoming.txt"
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST, PORT))
    print("bound TCP socket to 127.0.0.1:12345")
    sock.listen(10)

    while True:
        connection, address = sock.accept()
        print(f"connection: {connection} address: {address}")

        current_line = b""
        while True:
            chunk = connection.recv(8192)
            if not chunk:
                break
            
            '''
            if theres a content-length maybe parse request line and headers first instead of waiting for efficiency
            for character in chunk: double CRLF is 4 bytes adjust for that
                current_request += character
                if character == double CRLF and Content-Length not in current_request:
                    parse_current_request()
                    do_current_request_logic()
                    current_request = b""
                elif character == double CRLF and Content-Length in current_request:
                    current_request += chunk[character:Content-Length+1]
                    parse_current_request()
                    do_current_request_logic()
                    current_request = b""
            '''