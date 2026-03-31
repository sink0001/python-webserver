import socket


def append_to_file(file_path: str, content: str) -> None:
    with open(file_path, "a") as file:
        file.write(content)


def main():
    HOST = "localhost"
    PORT = 12345
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # AF_INET stands for Adress Family (AF) INET so this socket is bound to an IPV4 address and can only interact with other sockets like this, socket.SOCK_STREAM specifies TCP
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST, PORT))
    print("bound TCP socket to 127.0.0.1:12345")
    sock.listen(10) # 10 is the backlog number or the number of connections that can be queued when the socket is busy

    while True:
        connection, address = sock.accept() # accept() does a TCP handshake with the client and also blocks the outer loop until a connection is gotten
        print(f"connection: {connection} address: {address}")

        current_line = b"" # once a connection has been gotten we want to read text data from it line by line and current_line is buffer I use in the inner loop which executes a bunch of times getting a new chunk of data each time
        while True: # once a TCP connection is established you read data from it until the other side closes the TCP connection, at which point you go back into the outer loop listening for a new connection
            chunk = connection.recv(8192) # This blocks the inner loop till the TCP connection is terminated at the client so that way we don't close it accidentally when the client temporarily stops sending data
            if not chunk: # If the data is too big and gets buffered (past 1024 here) it goes in the socket buffer and gets passed on the next iteration, if data stopped blocking and is None, the connection is closed so close inner loop
                if current_line:
                    append_to_file("incoming.txt", current_line.decode("utf-8"))
                break
            
            previous_newline = -1
            for i in range(len(chunk)):
                if chunk[i] == 10: # 10 is the byte for \n
                    current_line += chunk[previous_newline:i]
                    append_to_file("incoming.txt", current_line.decode("utf-8"))
                    current_line = b""
                    previous_newline = i
            if previous_newline == -1:
                current_line += chunk
            else:
                current_line += chunk[previous_newline:]

if __name__ == "__main__":
    main()