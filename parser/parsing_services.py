from exceptions import MalformedRequestLineError, MalformedHeaderError


def parse_request_line(request: bytes) -> tuple[dict[str, str], bytes]:
    '''
    take in HTTP request and parse the request line so take in
    POST / HTTP/1.1
    Host: localhost:12345
    User-Agent: curl/8.15.0
    Accept: */*

    and parse out the request line method, request target and http version
    here it'd be POST, /, HTTP/1.1
    '''
    split_index = request.index(b"\r\n")
    request_line_string = request[:split_index].decode("utf-8")
    rest_of_request = request[split_index+2:]

    request_line_parts = request_line_string.split(" ")
    if len(request_line_parts) != 3:
        raise MalformedRequestLineError(f"expected 3 parts in request line, got {len(request_line_parts)}")
    request_line = {
        "method": request_line_parts[0],
        "target": request_line_parts[1],
        "http_version": request_line_parts[2]
    }

    return (request_line, rest_of_request)


def header_name_valid(header_name: bytes) -> bool:
    for i in range(len(header_name)):
        byte_int = header_name[i]
        if not (65 <= byte_int <= 90 or # A-Z
                97 <= byte_int <= 122 or # a-z
                48 <= byte_int <= 57 or # 0-9
                byte_int in { # "!", "#", "$", "%", "&", "'", "*", "+", "-", ".", "^", "_", "`", "|", "~"
                    33, 35, 36, 37, 38, 39, 42, 43,
                    45, 46, 94, 95, 96, 124, 126
                }): return False
    return True


def parse_headers(request_headers: bytes) -> dict[str, list[str]]:
    '''
    take in the headers part of a HTTP request (rest of request after parse_request_line)
    return a dict of headers, e.g. take in Host: localhost:12345\r\nUser-Agent: curl/8.15.0\r\nAccept: */*
    and return {"Host": "localhost:12345", "User-Agent": "curl/8.15.0", "Accept": "*/*"}
    '''
    if not request_headers.strip():
        return {}
    
    each_request_header = request_headers.split(b"\r\n")
    request_header_dict = dict()
    for header in each_request_header:
        if not header:
            continue
        if b":" in header:
            header_name, header_value = header.split(b":", 1)
            if not header_name_valid(header_name):
                raise MalformedHeaderError(f"header name {header_name} contains an illegal character")
            
            decoded_header_name = header_name.decode("utf-8").lower()
            if request_header_dict.get(decoded_header_name):
                request_header_dict[decoded_header_name].append(header_value.decode("utf-8").strip().lower())
            else:
                request_header_dict[decoded_header_name] = [header_value.decode("utf-8").strip().lower()]
        else:
            raise MalformedHeaderError(f"expected ':' in header but ':' wasn't found")

    return request_header_dict