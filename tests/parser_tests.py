from webserver import http_parser
from exceptions import MalformedRequestLineError


def test_http_request_line_parser() -> None:
    example_working_post_request = b"POST / HTTP/1.1\r\nHost: localhost:12345\r\nUser-Agent: curl/8.15.0\r\nAccept: */*\r\nContent-Length: 11\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\n{key:value}"
    assert (
        http_parser.parse_request_line(example_working_post_request)
            == (
                {
                    "method": "POST",
                    "target": "/",
                    "http_version": "HTTP/1.1"
                },
                "Host: localhost:12345\r\nUser-Agent: curl/8.15.0\r\nAccept: */*\r\nContent-Length: 11\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\n{key:value}"
                )
            ), "incorrectly parsed request line from POST / HTTP/1.1\r\nHost: localhost:12345\r\nUser-Agent: curl/8.15.0\r\nAccept: */*\r\nContent-Length: 11\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\n{key:value}"
    
    bad_request = b"/ HTTP/1.1\r\nHost: localhost:12345\r\nUser-Agent: curl/8.15.0\r\nAccept: */*\r\nContent-Length: 11\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\n{key:value}"
    try:
        http_parser.parse_request_line(bad_request)
    except MalformedRequestLineError:
        print("successfully threw MalformedRequestLineError when malformed request line was given")
    else:
        raise Exception("request line parsing function didn't raise a MalformedRequestLineError when given the bad request line: / HTTP/1.1")
    
test_http_request_line_parser()