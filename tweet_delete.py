from bottle import get, delete, request, response
import g
import mysql.connector

@delete("/delete-tweet/<tweet_id>")
def _(tweet_id):
    try:
        # VALIDATION
        if not tweet_id:
            response.status = 204
            return "no tweet_id"
        
        # CONNECT TO DATABASE
        connection = mysql.connector.connect(user="root", password="root", host="localhost", port="8889", database="twitter_single_page_app")
        
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)

            # CHECK IF TWEET_ID IS IN DATABASE
            cursor.execute("SELECT tweet_id FROM tweets WHERE tweet_id = %s", (tweet_id, ))
            tweet_id_from_db = cursor.fetchone()
            
            if tweet_id != tweet_id_from_db["tweet_id"]:
                response.status = 204
                return "tweet_id not is not in database"

    except Exception as ex:
        print(ex)
        return "something went wrong"
    
    finally:
        connection.close()

    try:
        # CONNECT TO DATABASE
        connection = mysql.connector.connect(user="root", password="root", host="localhost", port="8889", database="twitter_single_page_app")
        
        if connection.is_connected():
            cursor = connection.cursor()

            # DELETE TWEET BY ID
            cursor.execute("""
            DELETE FROM tweets
            WHERE tweet_id = %s
            """, (tweet_id, ))

            connection.commit()

            # SUCESS
            return "tweet deleted"

    except Exception as ex:
        print(ex)
        return "something went wrong"

    finally:
        connection.close()