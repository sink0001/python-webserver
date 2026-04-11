from webserver import http_parser
from exceptions import MalformedRequestLineError, MalformedHeaderError


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
                b"Host: localhost:12345\r\nUser-Agent: curl/8.15.0\r\nAccept: */*\r\nContent-Length: 11\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\n{key:value}"
                )
            ), "incorrectly parsed request line from POST / HTTP/1.1\r\nHost: localhost:12345\r\nUser-Agent: curl/8.15.0\r\nAccept: */*\r\nContent-Length: 11\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\n{key:value}"
    
    bad_request = b"/ HTTP/1.1\r\nHost: localhost:12345\r\nUser-Agent: curl/8.15.0\r\nAccept: */*\r\nContent-Length: 11\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\n{key:value}"
    try:
        http_parser.parse_request_line(bad_request)
    except MalformedRequestLineError:
        pass
    else:
        raise AssertionError("request line parsing function didn't raise a MalformedRequestLineError when given the bad request line: / HTTP/1.1")


def test_http_header_parsing() -> None:
    correct_test_input = b"Host: localhost:12345\r\nUser-Agent: curl/8.15.0\r\nAccept: */*\r\n\r\n"
    assert (http_parser.parse_headers(correct_test_input) == {"host": "localhost:12345", "user-agent": "curl/8.15.0", "accept": "*/*"}), "didn't parse headers for correctly formed input correctly"
    assert (http_parser.parse_headers(b"Host: localhost:12345") == {"host": "localhost:12345"}), "didn't parse headers for correctly formed input correctly"

    assert (http_parser.parse_headers(b"\r\n") == {}), "didn't return an empty dictionary when no headers were given"

    try:
        http_parser.parse_headers(b"Host : localhost:12345\r\nUser-Agent: curl/8.15.0\r\n\r\n")
    except MalformedHeaderError:
        pass
    else:
        raise AssertionError("header line parsing function didn't raise a MalformedHeaderError when given a header with a trailing whitespace in the header name")
    
    try:
        http_parser.parse_headers(b"Host localhost:12345\r\nUser-Agent: curl/8.15.0\r\n\r\n")
    except MalformedHeaderError:
        pass
    else:
        raise AssertionError("header line parsing function didn't throw a MalformedHeaderError when one of the headers didn't contain a ':'")
    
    try:
        http_parser.parse_headers(b"H@st: localhost:12345")
    except MalformedHeaderError:
        pass
    else:
        raise AssertionError("header name contained an illegal character but function didn't raise a MalformedHeaderError")


test_http_request_line_parser()
test_http_header_parsing()