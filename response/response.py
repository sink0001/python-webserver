


def write_status_line(status_code: int) -> str:
    status_lines = {
        200: "OK",
        400: "Bad Request",
        500: "Internal Server Error"
    }
    return status_lines[status_code]