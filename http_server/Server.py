from http_server.server_services import http_server


class Server:

    def __init__(self, port) -> None:
        self.port = port

    def serve(self) -> None:
        http_server(self.port)