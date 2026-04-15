from parser.parsing_services import parse_request_line, parse_headers


class HTTP_request:
    def __init__(self, request: bytes) -> None:
        self.request = request
        self.request_line, rest_of_request = parse_request_line(request)
        self.headers = parse_headers(rest_of_request)