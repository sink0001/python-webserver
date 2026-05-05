from http_server.Server import Server
from parser.HTTP_request import HTTP_request
from response.HTTP_response import HTTP_response


def example_handler(request: HTTP_request) -> HTTP_response:
    target = request.request_line["target"]
    if target == "/":
        return HTTP_response(200, "Hello, this is the non-default homepage!", {})
    elif target == "/something":
        return HTTP_response(200, "This is the something page!", {})
    else:
        return HTTP_response(404, "", {})


if __name__ == "__main__":
    try:
        Server(12345, example_handler).serve()
    except KeyboardInterrupt:
        print("server shutting down...")
        quit()