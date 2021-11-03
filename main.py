from flask import Flask, render_template, request, session
import json

from werkzeug.utils import redirect

app = Flask(__name__)


@app.route("/")
def homepage():
    return render_template("index.html")


@app.route("/about", methods=['GET', 'POST'])
def about():
    if request.method == 'POST':
        return render_template("aboutandhelp.html", toprint="about")


@app.route("/help", methods=['GET', 'POST'])
def help():
    if request.method == 'POST':
        return render_template('aboutandhelp.html', toprint="help")


@app.route("/create", methods=['GET', 'POST'])
def create():
    if request.method == 'POST':

        return render_template(f'aboutandhelp.html', toprint="create")


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return render_template('aboutandhelp.html', toprint="login")


@app.route("/success", methods=['GET', 'POST'])
def success():
    if request.method == 'POST':
        compname = request.form["compname"]
        compdesc = request.form["compdesc"]
        comptype = request.form["comptype"]
        comppass = request.form["comppass"]
        compbalance = str("$1000000")
        session["compname"] = compname
        session["compdesc"] = compdesc
        session["comptype"] = comptype
        session["comppass"] = comppass
        session["compbalance"] = compbalance
        session["getstarted"] = str("False")
        session["optiondone"] = -1

        req = {
            "name": session["compname"],
            "desc": session["compdesc"],
            "type": session["comptype"],
            "password": session["comppass"],
            "balance": session["compbalance"],
            "getstarted": session["getstarted"]
        }

        reqstarter = {
            "company": [{
                "name": session["compname"],
                "desc": session["compdesc"],
                "type": session["comptype"],
                "password": session["comppass"],
                "balance": session["compbalance"],
                "getstarted": session["getstarted"]}]
        }

        jsontosave = json.dumps(req, indent=2)
        jsontosavestarter = json.dumps(reqstarter, indent=2)
        with open("creds.json", 'r') as res:
            try:
                jsonobjmain = json.loads(res.read())
                for i, j in jsonobjmain.items():
                    j.append(req)
                required = json.dumps(jsonobjmain, indent=2)
                with open("creds.json", 'w') as fre:
                    fre.write(required)
            except Exception as e:
                with open("creds.json", 'w') as imp:
                    imp.write(jsontosavestarter)

        return render_template("aboutandhelp.html", toprint="success")


@app.route("/checklogin", methods=['GET', 'POST'])
def checklogin():
    if request.method == 'POST':
        print(request.form['compnamelogin'])
        print(request.form['comppasslogin'])
        return render_template('youtube.html')


@app.route("/user", methods=["GET", "POST"])
def user():
    if request.method == "POST":
        return render_template("index.html", login="true")


@app.route("/you", methods=["GET", "POST"])
def info():
    if request.method == "POST":
        return render_template("aboutandhelp.html", toprint="info")


@app.route("/setup", methods=["GET", "POST"])
def mainsim():

    if session["getstarted"] == "False":
        if request.method == "POST":
            session['optiondone'] += 1
            return render_template(f"/companies/{session['comptype']}.html", balance=session['compbalance'], getstarted="False", optiondone=session['optiondone'])
    elif session["getstarted"] == "True":
        if request.method == "POST":
            return render_template(f"/companies/{session['comptype']}.html", balance=session["compbalance"], getstarted="True")


@app.route("/updatejson", methods=["GET", "POST"])
def updatejson():
    if request.method == "POST":
        session['optiondone'] += 1
        with open("creds.json", 'r') as wb:
            jsonobjs = json.loads(wb.read())
        mylist = jsonobjs['company']
        for i in mylist:
            if i['name'] == session['compname']:
                i['country'] = request.form['country']
        savingfile = json.dumps(jsonobjs, indent=2)
        with open("creds.json", 'w') as fds:
            fds.write(savingfile)

        print(request.form["country"])
        return render_template(f"/companies/{session['comptype']}.html", balance=session['compbalance'], getstarted="False", optiondone=session['optiondone'])


if __name__ == "__main__":
    app.secret_key = '#ycoqcv9lu'
    app.config['SESSION_TYPE'] = 'filesystem'

    app.run(debug=True)