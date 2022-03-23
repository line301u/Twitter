from bottle import get, post, request, redirect, response
import uuid
import g
import re
import mysql.connector
import time

@post("/signup")
def _():
    try:
        # VALIDATION
        if not request.forms.get("user_name"):
            response.status = 400
            return redirect(f"/signup?error=user_name")

        if len(request.forms.get("user_name")) > g.MAX_LENGHT_USER_NAME: 
            response.status = 400
            return redirect(f"/signup?error=user_name")

        if not request.forms.get("user_first_name"):
            response.status = 400
            return redirect(f"/signup?error=user_first_name")

        if len(request.forms.get("user_first_name")) > g.MAX_LENGHT_USER_FIRST_NAME: 
            response.status = 400
            return redirect(f"/signup?error=user_first_name")
        
        if not request.forms.get("user_last_name"):
            response.status = 400
            return redirect(f"/signup?error=user_last_name")

        if len(request.forms.get("user_last_name")) > g.MAX_LENGHT_USER_LAST_NAME: 
            response.status = 400
            return redirect(f"/signup?error=user_last_name")

        if not request.forms.get("user_email"):
            response.status = 400
            return redirect(f"/signup?error=user_email")

        if len(request.forms.get("user_email")) > g.MAX_LENGHT_USER_EMAIL: 
            response.status = 400
            return redirect(f"/signup?error=user_email")

        if not re.match(g.REGEX_EMAIL, request.forms.get("user_email")):
            response.status = 400
            return redirect(f"/signup?error=user_email")

        if not request.forms.get("user_password"):
            response.status = 400
            return redirect(f"/signup?error=password")  

        if len(request.forms.get("user_password")) < g.MIN_LENGHT_USER_PASSWORD: 
            response.status = 400
            return redirect(f"/signup?error=password")

        if len(request.forms.get("user_password")) > g.MAX_LENGHT_USER_PASSWORD: 
            response.status = 400
            return redirect(f"/signup?error=password")

        # SUCESS
        user_id = str(uuid.uuid4())
        user_name = request.forms.get("user_name")
        user_first_name = request.forms.get("user_first_name")
        user_last_name = request.forms.get("user_last_name")
        user_email = request.forms.get("user_email")
        user_password = request.forms.get("user_password")

    except Exception as ex:
        raise
        if 'user_email' in str(ex):
            print("email already exist")
        
        return "something when wrong"

    try: 
        # CONNECT TO DATABASE
        connection = mysql.connector.connect(user="root", password="root", host="localhost", port="8889", database="twitter_single_page_app")
        
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)

            cursor.execute("""
            INSERT INTO users (user_id, user_name, user_first_name, user_last_name, user_email, user_password, user_created_at) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (user_id, user_name, user_first_name, user_last_name, user_email, user_password, int(time.time())))

            # SUCESS
            connection.commit()

    except Exception as ex:
        print(ex)
        return("something went wrong")

    finally:
        connection.close()