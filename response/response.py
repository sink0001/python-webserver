from exceptions import InvalidStatusCode


def write_status_line(status_code: int) -> str:
    if status_code < 100 or status_code > 599:
        raise InvalidStatusCode(f"gave an invalid status code, {status_code}")

    status_codes = {
        200: "OK",
        400: "Bad Request",
        500: "Internal Server Error"
    }
    
    try:
        return f"HTTP/1.1 {status_code} {status_codes[status_code]}"
    except KeyError:
        return f"HTTP/1.1 {status_code}"