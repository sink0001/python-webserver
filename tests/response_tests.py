from response.response_services import make_status_line, make_headers
from response.HTTP_response import HTTP_response
from exceptions import InvalidStatusCodeError, IllegalDuplicateHeaderError


def test_status_line_creation() -> None:
    assert (make_status_line(200), make_status_line(400), make_status_line(500)) == ("HTTP/1.1 200 OK", "HTTP/1.1 400 Bad Request", "HTTP/1.1 500 Internal Server Error"), "Didn't convert status code to correct status line"
    assert make_status_line(210) == "HTTP/1.1 210", "didn't ommit status code description when faced with status code thats not in the handled cases"
    
    try:
        make_status_line(600)
    except InvalidStatusCodeError:
        pass
    else:
        raise AssertionError("didn't raise InvalidStatusCodeError when faced with code 600")
    
    try:
        make_status_line(99)
    except InvalidStatusCodeError:
        pass
    else:
        raise AssertionError("didn't raise InvalidStatusCodeError when faced with code 99")


def test_make_headers() -> None:
    assert make_headers(12, {}) == {"Content-Length": ["12"], "Connection": ["close"], "Content-Type": ["text/plain"]}, "make_headers() function didn't use default headers when no additional ones were given"
    assert make_headers(12, {"Foo": ["Bar", "Bazz"], "Connection": ["keep-alive"]}) == {"Content-Length": ["12"], "Connection": ["close", "keep-alive"], "Content-Type": ["text/plain"], "Foo": ["Bar", "Bazz"]}

    try:
        make_headers(12, {"Content-Type": ["foo/bazz"]})
    except IllegalDuplicateHeaderError:
        pass
    else:
        raise AssertionError("didn't raise IllegalDuplicateHeaderError when Content-Type given again in headers")

    try:
        make_headers(12, {"CoNtEnt-LeNgTH": ["foo/bazz"]})
    except IllegalDuplicateHeaderError:
        pass
    else:
        raise AssertionError("didn't raise IllegalDuplicateHeaderError when Content-Type given again in headers")


def test_HTTP_response_class() -> None:
    response1 = HTTP_response(200, "Hello World!!!", {"Foo": ["Bar", "Bazz"]})
    assert response1.status_line == "HTTP/1.1 200 OK"
    assert response1.headers == {"Content-Length": ["14"], "Connection": ["close"], "Content-Type": ["text/plain"], "Foo": ["Bar", "Bazz"]}, f"{response1.headers} not parsed correctly"
    assert response1.raw_response == b"HTTP/1.1 200 OK\r\nContent-Length: 14\r\nConnection: close\r\nContent-Type: text/plain\r\nFoo: Bar\r\nFoo: Bazz\r\n\r\nHello World!!!", "response raw value wasn't extracted correctly"

    response2 = HTTP_response(400, "Hello World!!!", {"Foo": ["Bar", "Bazz"], "Connection": ["keep-alive"]})
    assert response2.status_line == "HTTP/1.1 400 Bad Request"
    assert response2.headers == {"Content-Length": ["14"], "Connection": ["close", "keep-alive"], "Content-Type": ["text/plain"], "Foo": ["Bar", "Bazz"]}, f"{response2.headers} not parsed correctly"
    assert response2.raw_response == b"HTTP/1.1 400 Bad Request\r\nContent-Length: 14\r\nConnection: close\r\nConnection: keep-alive\r\nContent-Type: text/plain\r\nFoo: Bar\r\nFoo: Bazz\r\n\r\nHello World!!!", {response2.raw_response}

    response3 = HTTP_response(404, "Hello World!!!", {"Foo": ["Bar", "Bazz"], "connection": ["keep-alive"]})
    assert response3.status_line == "HTTP/1.1 404"
    assert response3.headers == {"Content-Length": ["14"], "Connection": ["close"], "connection": ["keep-alive"] ,"Content-Type": ["text/plain"], "Foo": ["Bar", "Bazz"]}, f"{response3.headers} not parsed correctly"
    assert response3.raw_response == b"HTTP/1.1 404\r\nContent-Length: 14\r\nConnection: close\r\nContent-Type: text/plain\r\nFoo: Bar\r\nFoo: Bazz\r\nconnection: keep-alive\r\n\r\nHello World!!!", f"{response3.raw_response}"

    assert HTTP_response(200, "", {}).raw_response == b"HTTP/1.1 200 OK\r\nContent-Length: 0\r\nConnection: close\r\n\r\n", f"{HTTP_response(200, "", {}).raw_response}"

    try:
        HTTP_response(99, "", {})
    except InvalidStatusCodeError:
        pass
    else:
        raise AssertionError("didn't raise InvalidStatusCodeError when faced with code 99")
    
    try:
        HTTP_response(200, "", {"content-TyPe": ["foo/bar"]})
    except IllegalDuplicateHeaderError:
        pass
    else:
        raise AssertionError("didn't raise IllegalDuplicateHeaderError when Content-Type given again in headers")


test_status_line_creation()
test_make_headers()
test_HTTP_response_class()