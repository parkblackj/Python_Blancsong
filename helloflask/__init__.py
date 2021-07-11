from flask import Flask, request, Response, make_response, session
from datetime import date, datetime, timedelta

app = Flask(__name__)
app.debug = True

app.config.update(
    SECRET_KEY="sadfsdfsadf",
    SESSION_COOKIE_NAME="pyweb_flask_session",
    PERMANENT_SESSION_LIFETIME=timedelta(31)
)


@app.route('/wc')
def wc():
    key = request.args.get("key")
    val = request.args.get("val")
    res = Response("SET COOKIE")
    res.set_cookie(key, val)
    session["Token"] = "123X"
    return make_response(res)


@app.route("/rc")
def rc():
    key = request.args.get("key")
    val = request.cookies.get(key)
    return "cookies[" + str(key) + "]=" + str(val) + "," + session.get("Token")


@app.route("/delsess")
def delsess():
    if session.get("Token"):
        del session["Token"]
    return "Session delete Compete"
