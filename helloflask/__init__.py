from flask import Flask, request, Response, make_response, session, render_template, Markup
from datetime import date, datetime, timedelta

app = Flask(__name__)
app.debug = True

app.config.update(
    SECRET_KEY="sadfsdfsadf",
    SESSION_COOKIE_NAME="pyweb_flask_session",
    PERMANENT_SESSION_LIFETIME=timedelta(31)
)


@app.route("/main")
def main():
    return render_template("main.html")


class Nav:
    def __init__(self, title, url="#", children=[]):
        self.title = title
        self.url = url
        self.children = children


@app.route("/tmpl3")
def tmpl3():
    py = Nav("파이썬", "https://search.naver.com")
    java = Nav("자바", "https://search.naver.com")
    t_prg = Nav("프로그래밍 언어", "https://search.naver.com", [py, java])

    jinja = Nav("jinja", "https://search.naver.com")
    gc = Nav("Genshi,Cheetah", "https://search.naver.com")
    flask = Nav("플라스크", "https://search.naver.com", [jinja, gc])

    spr = Nav("스프링", "https://search.naver.com")
    ndjs = Nav("노드JS", "https://search.naver.com")
    t_spr = Nav("웹 프레임워크", "https://search.naver.com", [flask, spr, ndjs])

    my = Nav("나의 일상", "https://search.naver.com")
    issue = Nav("이슈 게시판", "https://search.naver.com")
    t_others = Nav("기타", "https://search.naver.com", [my, issue])

    return render_template("index.html", navs=[t_prg, t_spr, t_others])


@app.route("/tmpl2")
def tmpl2():
    a = (1, "만남1", "김검모", True, [])
    b = (2, "만남2", "노사연", True, [a])
    c = (3, "만남3", "노사봉", False, [a, b])
    d = (4, "만남4", "아이유", False, [a, b, c])

    return render_template("index.html", lst2=[a, b, c, d])


@app.route("/tmpl")
def t():
    tit = Markup("<strong>Title</strong>")
    mu = Markup("<h1>iii=<i>%s</i></h1>")
    h = mu % "Italic"
    lst = [("만남1", "김검모", True), ("만남2", "노사연", True),
           ("만남3", "노사봉", False), ("만남4", "아이유", False)]

    return render_template("index.html", title=tit, mu=h, lst=lst)


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
