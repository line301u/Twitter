from bottle import get, put, request, redirect, response
import g
import time
import imghdr
import os
import uuid
import mysql.connector

@put("/update-tweet/<tweet_id>")
def _(tweet_id):
    try:
        # VALIDATION
        if not request.forms.get("tweet_text"):
            response.status = 400
            return "tweet_text is missing"
        if len(request.forms.get("tweet_text")) > g.MAX_LENGHT_TWEET_TEXT:
            response.status = 400
            return f"tweet_text is too long, the max amount of characters is {g.MAX_LENGHT_TWEET_TEXT}"
        if not tweet_id:
            response.status = 204
            return "tweet_id missing"

        # CONNECT TO DATABASE
        connection = mysql.connector.connect(user="root", password="root", host="localhost", port="8889", database="twitter_single_page_app")
        
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)

            cursor.execute("SELECT tweet_id FROM tweets WHERE tweet_id = %s", (tweet_id, ))
            tweet_id_from_db = cursor.fetchone()

            # CHECK IF TWEET_ID IS IN DATABASE
            if tweet_id != tweet_id_from_db["tweet_id"]:
                response.status = 204
                return "tweet_id not is not in database"

        # VALIDATE IMAGE
        tweet_image = request.files.get("tweet_image")

        if tweet_image:
            file_name, file_extension = os.path.splitext(tweet_image.filename)

            # VALIDATE EXTENSION
            if file_extension not in (".png", ".jpeg", ".jpg"):
                return "image not allowed"

            # CREATE IMAGE NAME
            image_id = str(uuid.uuid4())
            tweet_image_name = f"{image_id}{file_extension}"

            # VALIDATE IMAGE NAME
            if len(tweet_image_name) > g.MAX_LENGHT_IMAGE_PATH:
                response.status = 400
                return "file name is too long"

            # SAVE IMAGE
            tweet_image.save(f"images/{tweet_image_name}")

            # VALIDATE IMAGE FILE 
            imghdr_extension = imghdr.what(f"images/{tweet_image_name}")
            if file_extension != f".{imghdr_extension}":
                print("not an image file")
                os.remove(f"images/{tweet_image_name}")
                return "not an image file"

        # SUCESS
        tweet_text = request.forms.get("tweet_text")
        tweet_updated_at = int(time.time())
        tweet_image_path = request.forms.get("tweet_image_path")

        if tweet_image and tweet_image_path != tweet_image_name : tweet_image_path = tweet_image_name

        updated_tweet = {
            "tweet_id" : tweet_id,
            "tweet_text" : tweet_text,
            "tweet_image_path" : tweet_image_path,
            "tweet_updated_at" : tweet_updated_at
        }
        print(updated_tweet)
    except Exception as ex:
        print(ex)
        
    finally:
        connection.close()

    try:
        # CONNECT TO DATABASE
        connection = mysql.connector.connect(user="root", password="root", host="localhost", port="8889", database="twitter_single_page_app")
        
        if connection.is_connected():
            cursor = connection.cursor()

            cursor.execute("""
            UPDATE tweets
            SET tweet_text = %s, tweet_image_path = %s, tweet_updated_at = %s
            WHERE tweet_id = %s
            """, (updated_tweet["tweet_text"], updated_tweet["tweet_image_path"], updated_tweet["tweet_updated_at"], updated_tweet["tweet_id"]))

            # SUCSESS
            connection.commit()

            return updated_tweet
    
    except Exception as ex:
        print(ex)
    
    finally:
        connection.close()
    