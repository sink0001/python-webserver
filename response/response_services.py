from exceptions import InvalidStatusCodeError, IllegalDuplicateHeaderError


def make_status_line(status_code: int) -> str:
    if status_code < 100 or status_code > 599:
        raise InvalidStatusCodeError(f"gave an invalid status code, {status_code}")

    status_codes = {
        200: "OK",
        400: "Bad Request",
        500: "Internal Server Error"
    }

    try:
        return f"HTTP/1.1 {status_code} {status_codes[status_code]}"
    except KeyError:
        return f"HTTP/1.1 {status_code}"
    

def make_headers(content_length: int, headers: dict[str, list]) -> dict[str, list[str]]:
    if content_length > 0:
        final_headers = {
            "Content-Length": [str(content_length)],
            "Connection": ["close"],
            "Content-Type": ["text/plain"]
        }
    else:
        final_headers = {
            "Content-Length": [str(content_length)],
            "Connection": ["close"],
        }
    
    for header in headers:
        lower_header = header.lower()
        header_value = headers[header]

        if lower_header == "content-length":
            raise IllegalDuplicateHeaderError(f"expected 1 content-length header and 1 content-type header")
        elif lower_header == "connection":
            final_headers["Connection"] = header_value
        else:
            final_headers[header] = header_value

    return final_headers