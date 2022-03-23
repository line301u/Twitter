from bottle import get, view
import mysql.connector


@get("/")
@view("index")
def _():
    try:
        # CONNECT TO DATABASE
        connection = mysql.connector.connect(user="root", password="root", host="localhost", port="8889", database="twitter_single_page_app")
        
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)

            # GET ALL TWEETS BY USER ID
            cursor.execute("SELECT * FROM tweets ORDER BY tweet_created_at DESC")
            tweets = cursor.fetchall()

        return dict(tweets=tweets)

    except Exception as ex:
        print(ex)

    finally:
        connection.close()