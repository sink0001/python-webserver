from collections.abc import Callable
from parser.HTTP_request import HTTP_request
from response.HTTP_response import HTTP_response


class Handler:

    def __init__(self) -> None:
        self.route_handlers: dict[str, Callable[[HTTP_request], HTTP_response]] = {"/": lambda request: HTTP_response(200, "This is the default homepage!", {})}

    def route(self, target: str) -> Callable:
        def decorator(handler_func: Callable[[HTTP_request], HTTP_response]) -> Callable:
            self.route_handlers[target] = handler_func
            return handler_func
        return decorator

    def handle(self, request: HTTP_request) -> HTTP_response:
        target = request.request_line["target"]
        if target in self.route_handlers:
            return self.route_handlers[target](request)
        return HTTP_response(404, "", {})