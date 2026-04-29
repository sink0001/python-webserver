from response.response_services import make_status_line, make_headers
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


test_status_line_creation()
test_make_headers()