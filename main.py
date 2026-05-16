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
    return HTTP_response(200, "This is something", {"connection": ["keep-alive"]})

@handler.route("/cool-page")
def cool(request: HTTP_request) -> HTTP_response:
    response_body = ""
    if request.body:
        response_body = f"Hello, your body is: \n{request.body}"
    else:
        response_body = "Hello"
    return HTTP_response(200, response_body, {})

@handler.route("/myproblem")
def my_problem(request: HTTP_request):
    raise Exception("something went wrong")

if __name__ == "__main__":
    try:
        Server(12345, handler.handle).serve()
    except KeyboardInterrupt:
        print("server shutting down...")
        quit()