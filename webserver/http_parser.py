from exceptions import MalformedRequestLineError, MalformedHeaderError


'''
take in a HTTP request and parse out request line, headers, and body
--- EXAMPLE REQUEST ---
POST / HTTP/1.1
Host: localhost:12345
User-Agent: curl/8.15.0
Accept: */*
Content-Length: 11
Content-Type: application/json

{key:value}
-----------------------

--- EXAMPLE PARSED RETURN ---
{
    request_line: "POST / HTTP/1.1",
    headers: {
        "Host": "localhost:12345",
        "User-Agent": "curl/8.15.0",
        "Accept": "*/*",
        "Content-Length": 11,
        "Content-Type": "application/json"}
    },
    body: {
        key: value
    }
}
'''


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


def parse_headers(request_headers: bytes) -> dict[str, str]:
    '''
    take in the headers part of a HTTP request (rest of request after parse_request_line)
    return a dict of headers, e.g. take in Host: localhost:12345\r\nUser-Agent: curl/8.15.0\r\nAccept: */*
    and return {"Host": "localhost:12345", "User-Agent": "curl/8.15.0", "Accept": "*/*"}
    '''
    each_request_header = request_headers.split(b"\r\n")
    if len(each_request_header) == 1:
        return {}

    request_header_dict = dict()
    for header in each_request_header:
        if not header:
            continue
        if b":" in header:
            header_name, header_value = header.split(b":", 1)
            if b" " in header_name:
                raise MalformedHeaderError(f"expected no whitespaces in header name but header name had {header_name.count(b" ")} whitespaces")
            request_header_dict[header_name.decode("utf-8")] = header_value.decode("utf-8").strip()
        else:
            raise MalformedHeaderError(f"expected ':' in header but ':' wasn't found")
    
    return request_header_dict