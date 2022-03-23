from bottle import get, view, request, redirect, response
import mysql.connector
import g

@get("/control_panel")
@view("control_panel")
def _():
    try:
        user_session_id = request.get_cookie("user_session_id", secret=g.COOKIE_SECRET)

        # CONNECT TO DATABASE
        connection = mysql.connector.connect(user="root", password="root", host="localhost", port="8889", database="twitter_single_page_app")

        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)

            cursor.execute("SELECT session_id FROM sessions WHERE session_id = %s", (user_session_id, ))
            session_id_from_db = cursor.fetchone()

            # CHECK IF USER IS LOGGED IN
            if not session_id_from_db:
                response.status = 204
                return redirect("/login")
    
    except Exception as ex:
        print(ex)
    
    finally:
        connection.close()

    try:
        # CONNECT TO DATABASE
        connection = mysql.connector.connect(user="root", password="root", host="localhost", port="8889", database="twitter_single_page_app")
        
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)

            # GET ALL TWEETS BY USER ID
            user_id = request.get_cookie("user_id", secret=g.COOKIE_SECRET)
            cursor.execute("""SELECT *, FROM_UNIXTIME(tweet_created_at, '%h:%i %p, %d-%m-%Y') as tweet_created_at, FROM_UNIXTIME(tweet_updated_at, '%h:%i %p, %d-%m-%Y') as tweet_updated_at
            FROM tweets
            WHERE tweet_user_id = %s
            ORDER BY tweet_created_at DESC""", (user_id, ))
            tweets = cursor.fetchall()
            
        print(tweets)
        return dict(tweets=tweets)
    
    except Exception as ex:
        print(ex)
    
    finally:
        connection.close()