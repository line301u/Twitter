from bottle import get, view, request

@get("/signup")
@view("signup")
def _():
    try:
        error = request.params.get("error")
        return dict(error=error)
        
    except Exception as ex:
        print(ex)