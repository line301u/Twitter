from bottle import get, post, request, redirect, response
import g
import re
import mysql.connector
import json
import uuid

@post("/login")
def _():
    try:
        # VALIDATION
        if not request.forms.get("user_email"):
            response.status = 400
            return redirect("/login?error=user_email")

        if len(request.forms.get("user_email")) > g.MAX_LENGHT_USER_EMAIL: 
            response.status = 400
            return redirect(f"/login?error=user_email")

        if not re.match(g.REGEX_EMAIL, request.forms.get("user_email")):
            response.status = 400
            return redirect("/login?error=user_email")

        user_email = request.forms.get("user_email")
        
        if not request.forms.get("user_password"):
            response.status = 400
            return redirect(f"/login?error=user_password&user_email={user_email}")

        if len(request.forms.get("user_password")) < g.MIN_LENGHT_USER_PASSWORD:
            response.status = 400
            return redirect(f"/login?error=user_password&user_email={user_email}")

        if len(request.forms.get("user_password")) > g.MAX_LENGHT_USER_PASSWORD:
            response.status = 400
            return redirect(f"/login?error=user_password&user_email={user_email}")

        user_password = request.forms.get("user_password")

    except Exception as ex:
        raise
        print(ex)

    try:
        # CONNECT TO DATABASE
        connection = mysql.connector.connect(user="root", password="root", host="localhost", port="8889", database="twitter_single_page_app")
        
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE user_email = %s", (user_email, ))
            user_db = cursor.fetchone()

            # CHECK IF USER_EMAIL IS IN USERS TABLE
            if user_db and user_password == user_db["user_password"]:
                user_session_id = str(uuid.uuid4())
                
                cursor.execute("""
                INSERT INTO sessions (session_id)
                VALUES (%s);
                """,
                ([user_session_id]))

                connection.commit()

                # SET USER_SESSION_ID IN COOKIE
                response.set_cookie("user_session_id", user_session_id, secret= g.COOKIE_SECRET)
                response.set_cookie("user_id", user_db["user_id"], secret= g.COOKIE_SECRET)
                
                # SUCESS
                return redirect("/control_panel")
                    
            return redirect("/login")

    except Exception as ex:
        raise
        print(ex)

    finally:
        connection.close()
