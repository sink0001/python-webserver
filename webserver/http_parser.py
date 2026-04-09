from exceptions import MalformedRequestLineError


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
    Content-Length: 11
    Content-Type: application/json

    {key:value}

    and parse out the request line method, request target and http version
    here it'd be POST, /, HTTP/1.1
    '''
    split_index = request.index(b"\r\n")
    request_line_string = request[:split_index].decode("utf-8")
    rest_of_request = request[split_index+2:]

    request_line_parts = request_line_string.split(" ")
    if len(request_line_parts) != 3:
        raise MalformedRequestLineError(f"Expected 3 parts in request line, got {len(request_line_parts)}")
    request_line = {
        "method": request_line_parts[0],
        "target": request_line_parts[1],
        "http_version": request_line_parts[2]
    }

    return (request_line, rest_of_request)