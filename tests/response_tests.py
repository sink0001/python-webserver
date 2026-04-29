from response.response import write_status_line
from exceptions import InvalidStatusCode


def test_status_line_writing() -> None:
    assert (write_status_line(200), write_status_line(400), write_status_line(500)) == ("HTTP/1.1 200 OK", "HTTP/1.1 400 Bad Request", "HTTP/1.1 500 Internal Server Error"), "Didn't convert status code to correct status line"
    assert write_status_line(210) == "HTTP/1.1 210", "didn't ommit status code description when faced with status code thats not in the handled cases"
    
    try:
        write_status_line(600)
    except InvalidStatusCode:
        pass
    else:
        raise AssertionError("didn't raise InvalidStatusCode when faced with code 600")
    
    try:
        write_status_line(99)
    except InvalidStatusCode:
        pass
    else:
        raise AssertionError("didn't raise InvalidStatusCode when faced with code 99")


test_status_line_writing()