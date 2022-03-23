from bottle import run, static_file, get

#####################################
import signup_get               # GET
import home_get                 # GET
import login_get                # GET
import control_panel_get        # GET
import logout_get               # GET

import signup_post             # POST
import login_post              # POST
import tweet_post              # POST

import tweet_update            # PUT

import tweet_delete          # DELETE

#####################################
@get("/app.css")
def _():
    return static_file("app.css", root="./styles")

##############################
@get("/images/<image_name>")
def _(image_name):
    return static_file(image_name, root="./images")

#####################################
@get("/app.js")
def _():
    return static_file("app.js", root="./scripts")

#####################################
run(host="127.0.0.1", port=2222, debug=True, reloader=True)