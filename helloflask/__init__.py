from flask import Flask, request, Response, make_response, session, render_template, Markup
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta


app = Flask(__name__)
app.debug = True

app.config.update(
    SECRET_KEY="sadfsdfsadf",
    SESSION_COOKIE_NAME="pyweb_flask_session",
    PERMANENT_SESSION_LIFETIME=timedelta(31)
)


class FormInput:
    def __init__(self, id, name, value, checked, text):
        self.id = id
        self.name = name
        self.value = value
        self.checked = checked
        self.text = text


def make_date(dt, fmt):
    if not isinstance(dt, date):
        dt = datetime.strptime(dt, fmt)
        return dt

    else:
        return dt


@app.template_filter("sdt")
def sdt(dt, fmt="%Y-%m-%d"):
    d = make_date(dt, fmt)
    wd = d.weekday()
    return 1 if wd == 6 else wd*-1


@app.template_filter("month")
def month(dt, fmt="%Y-%m-%d"):
    d = make_date(dt, fmt)
    return d.month


@app.template_filter("edt")
def edt(dt, fmt="%Y-%m-%d"):
    d = make_date(dt, fmt)
    nextmonth = d + relativedelta(months=1)
    return (nextmonth - timedelta(1)).day + 1


@app.route("/")
def apps():
    rds = []
    for i in [1, 2, 3]:
        id = "r"+str(i)
        name = "radiotest"
        value = i
        checked = ""
        if i == 2:
            checked = "checked"
        text = "RadioTest"+str(i)
        p = rds.append(FormInput(id, name, value, checked, text))
        now = "2021-07-17 17:30"
        d = datetime.strptime("2021-07-01", "%Y-%m-%d")
        year = request.args.get("year", date.today().year, int)
    return render_template("app.html", year=year, ttt="TestTTT", radioList=rds, today=now)


@app.template_filter('ymd')
def datetime_ymd(dt, fmt='%y-%m-%d'):
    if isinstance(dt, date):
        return "<strong>%s</strong>" % dt.strftime(fmt)
    else:
        return dt


@app.template_filter('simpledate')
def simpledate(at):
    if not isinstance(at, date):
        at = datetime.strptime(at, "%Y-%m-%d %H:%M")
    if (datetime.now() - at).days < 1:
        fmt = "%H:%M"
    else:
        fmt = "%m:%d"
    return "<strong>%s</strong>" % at.strftime(fmt)


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
    py = Nav("?????????", "https://search.naver.com")
    java = Nav("??????", "https://search.naver.com")
    t_prg = Nav("??????????????? ??????", "https://search.naver.com", [py, java])

    jinja = Nav("jinja", "https://search.naver.com")
    gc = Nav("Genshi,Cheetah", "https://search.naver.com")
    flask = Nav("????????????", "https://search.naver.com", [jinja, gc])

    spr = Nav("?????????", "https://search.naver.com")
    ndjs = Nav("??????JS", "https://search.naver.com")
    t_spr = Nav("??? ???????????????", "https://search.naver.com", [flask, spr, ndjs])

    my = Nav("?????? ??????", "https://search.naver.com")
    issue = Nav("?????? ?????????", "https://search.naver.com")
    t_others = Nav("??????", "https://search.naver.com", [my, issue])

    return render_template("index.html", navs=[t_prg, t_spr, t_others])


@app.route("/tmpl2")
def tmpl2():
    a = (1, "??????1", "?????????", True, [])
    b = (2, "??????2", "?????????", True, [a])
    c = (3, "??????3", "?????????", False, [a, b])
    d = (4, "??????4", "?????????", False, [a, b, c])

    return render_template("index.html", lst2=[a, b, c, d])


@app.route("/tmpl")
def t():
    tit = Markup("<strong>Title</strong>")
    mu = Markup("<h1>iii=<i>%s</i></h1>")
    h = mu % "Italic"
    lst = [("??????1", "?????????", True), ("??????2", "?????????", True),
           ("??????3", "?????????", False), ("??????4", "?????????", False)]

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
