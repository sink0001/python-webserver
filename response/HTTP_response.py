from response.response_services import make_status_line, make_headers


class HTTP_response:
    def __init__(self, status_code: int, body: str, additional_headers: dict[str, list[str]]) -> None:
        self.status_line = make_status_line(status_code)
        self.status_code = status_code
        self.body = body
        self.headers = make_headers(len(body), additional_headers)


    @property
    def raw_response(self) -> bytes:
        response = b""

        response += self.status_line.encode("utf-8") + b"\r\n"

        for header in self.headers:
            for header_value in self.headers[header]:
                response += f"{header}: {header_value}".encode("utf-8") + b"\r\n"
        
        response += b"\r\n" + self.body.encode("utf-8")
        return response