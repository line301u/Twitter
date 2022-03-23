from bottle import get, post, request, redirect, response
import g
import mysql.connector
import imghdr
import os
import uuid
import time

@post("/tweet")
def _():
    try:
        # VALIDATION
        if not request.forms.get("tweet_text"):
            response.status = 400
            return "tweet_text"
        
        if len(request.forms.get("tweet_text")) > g.MAX_LENGHT_TWEET_TEXT:
            response.status = 400
            return "tweet_text"

        image = request.files.get("tweet_image")

        if image:
            file_name, file_extension = os.path.splitext(image.filename)

            # VALIDATE EXTENSION
            if file_extension not in (".png", ".jpeg", ".jpg"):
                return "image not allowed"

            # CREATE IMAGE NAME
            image_id = str(uuid.uuid4())
            image_name = f"{image_id}{file_extension}"

            # VALIDATE IMAGE NAME
            if len(image_name) > g.MAX_LENGHT_IMAGE_PATH:
                response.status = 400
                return "file name is too long"

            # SAVE IMAGE
            image.save(f"images/{image_name}")

            # VALIDATE IMAGE FILE 
            imghdr_extension = imghdr.what(f"images/{image_name}")
            if file_extension != f".{imghdr_extension}":
                print("not an image file")
                os.remove(f"images/{image_name}")
                return "not an image file"

        # SUCESS
        tweet_id = str(uuid.uuid4())
        tweet_text = request.forms.get("tweet_text")
        tweet_image_path = None
        if image : tweet_image_path = image_name
        tweet_created_at = int(time.time())
        user_id = request.get_cookie("user_id", secret=g.COOKIE_SECRET)

        tweet = {
            "tweet_id" : tweet_id,
            "tweet_text" : tweet_text,
            "tweet_image_path" : tweet_image_path,
            "tweet_created_at" : tweet_created_at,
            "tweet_updated_at" : None,
            "user_id" : user_id
        }

    except Exception as ex:
        print(ex)

    try:
        # CONNECT TO DATABASE
        connection = mysql.connector.connect(user="root", password="root", host="localhost", port="8889", database="twitter_single_page_app")
        
        if connection.is_connected():
            cursor = connection.cursor()

            cursor.execute("""
            INSERT INTO tweets (tweet_id, tweet_text, tweet_image_path, tweet_created_at, tweet_updated_at, tweet_user_id) 
            VALUES (%s, %s, %s, %s, null, %s)
            """, (tweet["tweet_id"], tweet["tweet_text"], tweet["tweet_image_path"], tweet["tweet_created_at"], tweet["user_id"]))

            # SUCESS
            connection.commit()

            return tweet

    except Exception as ex:
        print(ex)

    finally:
        connection.close()