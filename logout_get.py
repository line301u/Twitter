from bottle import get, request, redirect
import g
import mysql.connector

@get("/logout")
def _():
    try:
        # GET SESSION ID FROM COOKIE
        user_session_id = request.get_cookie("user_session_id", secret=g.COOKIE_SECRET)
        print(user_session_id)

        # CONNECT TO DATABASE
        connection = mysql.connector.connect(user="root", password="root", host="localhost", port="8889", database="twitter_single_page_app")
        
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)

            # REMOVE SESSION_ID FROM SESSIONS
            cursor.execute("""
            DELETE FROM sessions
            WHERE session_id = %s
            """, (user_session_id, ))

            # SUCESS
            connection.commit()

        return redirect("/login")

    except Exception as ex:
        raise
        print(ex)
        return "something went wrong"
    
    finally:
        connection.close()
