from http_server.server_services import http_server
from response.HTTP_response import HTTP_response
from parser.HTTP_request import HTTP_request
from collections.abc import Callable


class Server:

    def __init__(self, port, handler: Callable[[HTTP_request], HTTP_response]) -> None:
        self.port = port
        self.handler = handler

    def serve(self) -> None:
        http_server(self.port, self.handler)