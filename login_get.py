from bottle import get, view, request

@get("/login")
@view("login")
def _():
    try:
        user_email = request.params.get("user_email")
        error = request.params.get("error")
        
        return dict(error=error, user_email=user_email)
        
    except Exception as ex:
        print(ex)