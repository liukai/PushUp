_ERROR = "error"
_SUCCESS = "ok"

def make_error_response(message):
    return {"result": _ERROR, "data": message}
def make_success_response(data):
    return {"result": _SUCCESS, "data": data}
