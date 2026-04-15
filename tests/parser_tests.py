from parser.parsing_services import parse_request_line, parse_headers
from parser.HTTP_request import HTTP_request
from exceptions import MalformedRequestLineError, MalformedHeaderError


def test_http_request_line_parsing() -> None:
    example_working_post_request = b"POST / HTTP/1.1\r\nHost: localhost:12345\r\nUser-Agent: curl/8.15.0\r\nAccept: */*\r\nContent-Length: 11\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\n{key:value}"
    assert (
        parse_request_line(example_working_post_request)
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
        parse_request_line(bad_request)
    except MalformedRequestLineError:
        pass
    else:
        raise AssertionError("request line parsing function didn't raise a MalformedRequestLineError when given the bad request line: / HTTP/1.1")


def test_http_header_parsing() -> None:
    correct_test_input = b"Host: localhost:12345\r\nUser-Agent: curl/8.15.0\r\nAccept: */*\r\n\r\n"
    assert (parse_headers(correct_test_input) == {"host": ["localhost:12345"], "user-agent": ["curl/8.15.0"], "accept": ["*/*"]}), "didn't parse headers for correctly formed input correctly"
    assert (parse_headers(b"Host: localhost:12345") == {"host": ["localhost:12345"]}), "didn't parse headers for correctly formed input correctly"

    assert (parse_headers(b"\r\n") == {}), "didn't return an empty dictionary when no headers were given"

    assert (parse_headers(b"Foo: Bar\r\nFoo: Bazz\r\nlocalhost:12345") == {"foo": ["bar", "bazz"], "localhost": ["12345"]}), "didn't return one list with multiple values when same header name given multiple times"

    try:
        parse_headers(b"Host : localhost:12345\r\nUser-Agent: curl/8.15.0\r\n\r\n")
    except MalformedHeaderError:
        pass
    else:
        raise AssertionError("header line parsing function didn't raise a MalformedHeaderError when given a header with a trailing whitespace in the header name")
    
    try:
        parse_headers(b"Host localhost:12345\r\nUser-Agent: curl/8.15.0\r\n\r\n")
    except MalformedHeaderError:
        pass
    else:
        raise AssertionError("header line parsing function didn't throw a MalformedHeaderError when one of the headers didn't contain a ':'")
    
    try:
        parse_headers(b"H@st: localhost:12345")
    except MalformedHeaderError:
        pass
    else:
        raise AssertionError("header name contained an illegal character but function didn't raise a MalformedHeaderError")


def test_HTTP_request_class() -> None:
    good_request = b"POST / HTTP/1.1\r\nHost: localhost:12345\r\nUser-Agent: curl/8.15.0\r\nAccept: */*\r\n\r\n"
    http_request = HTTP_request(good_request)
    assert (http_request.request == good_request), f"http request object's request attribute {http_request.request} isn't equal to the request {good_request}"
    assert (http_request.request_line == {"method": "POST", "target": "/", "http_version": "HTTP/1.1"}), "http request object's request line didn't correctly parse the request line POST / HTTP/1.1"
    assert (http_request.headers == {"host": ["localhost:12345"], "user-agent": ["curl/8.15.0"], "accept": ["*/*"]}), "http request object's headers dictionary was incorrect"

    try:
        HTTP_request(b"Host: localhost:12345\r\nUser-Agent: curl/8.15.0\r\n\r\n")
    except MalformedRequestLineError:
        pass
    else:
        raise AssertionError("http request object didn't raise MalformedRequestLineError when there was no request line present")
    
    assert (HTTP_request(b"POST / HTTP/1.1\r\n").headers == {}), f"headers dictionary isn't empty when http request object is created with only request line, instead it is {HTTP_request(b"POST / HTTP/1.1\r\n").headers}"

    try:
        HTTP_request(b"POST / HTTP/1.1\r\nHost localhost:12345\r\nUser-Agent: curl/8.15.0\r\n\r\n")
    except MalformedHeaderError:
        pass
    else:
        raise AssertionError("http request object didn't raise MalformedHeaderError when header was missing a ':'")


test_http_request_line_parsing()
test_http_header_parsing()
test_HTTP_request_class()