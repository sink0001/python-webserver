from http_server.Server import Server
from parser.HTTP_request import HTTP_request
from response.HTTP_response import HTTP_response
from handler.Handler import Handler


handler = Handler()

@handler.route("/")
def home(request: HTTP_request) -> HTTP_response:
    return HTTP_response(200, "Hello, this is the non default home-page!", {"connection": ["keep-alive"]})

@handler.route("/something")
def something(request: HTTP_request) -> HTTP_response:
    return HTTP_response(200, "This is something", {})


if __name__ == "__main__":
    try:
        Server(12345, handler.handle).serve()
    except KeyboardInterrupt:
        print("server shutting down...")
        quit()