from http_server.Server import Server


if __name__ == "__main__":
    try:
        Server(12345).serve()
    except KeyboardInterrupt:
        print("server shutting down...")
        quit()