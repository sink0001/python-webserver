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
    

def make_headers(content_length: int, additional_headers: dict[str, list]) -> dict[str, list[str]]:
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
    
    for header in additional_headers:
        if header.lower() in {"content-length", "content-type"}:
            content_length_count = [header.lower() for header in additional_headers].count("content-length")
            content_type_count = [header.lower() for header in additional_headers].count("content-type")
            raise IllegalDuplicateHeaderError(f"expected 1 content-length header, got {content_length_count} expected 1 content-type header got {content_type_count}")
        
        header_value = additional_headers[header]
        if header in final_headers:
            final_headers[header] += header_value
        else:
            final_headers[header] = header_value

    return final_headers