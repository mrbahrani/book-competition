from flask import *
from database.database import Database
from hash.hashgenerator import HashGenerator
app = Flask(__name__)
app.secret_key = "testMe"
db = Database()
globalContestList = []

# @app.route("/")
# def root():
#
#     ranking = db.viewranking()
#     return render_template("main_page.html")


@app.route("/")
def root():
    logIn = None
    if "userid" in session:
        logIn = [True, session["username"]]
    else:
        logIn = False
    print(logIn)
    ranking=db.viewranking()
    print("here")
    resp = db.showcontests(1)
    print(resp)
    ContestList = resp['ContestsList']
    return render_template("showContests.html",resutl=ContestList,ranking=ranking,logIn=logIn)


@app.route("/createContest")
def createContest():
    if "userid" in session:
        return render_template("contestRegister.html")
    else:
        return "Not Logged In yet"



@app.route("/addContest", methods=["POST"])
def addContest():
    if "userid" in session:
        resp = db.addConetest(request.form["titleTxt"],request.form["description"],
                              request.form["first"], request.form["second"],request.form["third"],request.form["forth"],
                              request.form["fee"], request.form["starttime"], request.form["endtime"],
                              True, 1, -100000000, "NothingYet")

        if resp['Status'] == 1:
            return redirect(url_for("root"))
        else:
            return "Contest Not Created - <a href='/createContest'>createContest<a>"
    else:
        return "Not LoggedIn"


@app.route("/login")
def loginView():
    if not ("userid" in session):
        return render_template("logInForm.html")
    else:
        flash("You are already logged in!\n")
        return redirect(url_for("root"))

@app.route("/auth", methods=["post"])
def auth():
    userid = db.login(None,request.form["username"] ,request.form["password"])
    if userid:
        session["userid"] = userid
        session["username"] = request.form["username"]
        return redirect(url_for("root"))
    else:
        flash("Wrong password!\n")
        return redirect(url_for("loginView"))


@app.route("/logout")
def logout():
    if "userid" in session:
        session.pop('username', None)
        session.pop('userid', None)
        return redirect(url_for("root"))
    else:
        flash("You are not logged in!\n")
        return redirect(url_for("root"))

@app.route("/signup")
def signUpView():
    if "username" in session:
        return "You are already logged in as %s\n" %session["username"]
    else:
        return render_template("logInForm.html")


@app.route("/signup_check", methods=["post"])
def signUpCheck():
    if len(request.form["username"])<6:
        flash("Username must be longer than 6 characters")
        return redirect(url_for("signUpView"))
    if len(request.form["password"])<6:
        flash("Password must be longer than 6 characters")
        return redirect(url_for("signUpView"))
    if '@' in request.form["username"]:
        flash("@ may not be in username")
        return redirect(url_for("signUpView"))
    if db.signup(request.form["email"], request.form["username"],
                 request.form["password"]):
        print("GOh")
        return redirect(url_for("root"))
    else: return "Something unexpected!"


@app.route("/view_profile/<int:userid>")
def viewProfile(userid):
    user = db.getprofile(userid)
    return "To be done!"


@app.route("/edit_profile")
def editProfile():
    return "To be done!"

@app.route("/edit", methods=["post"])
def edit():
    db.editprofile()
    return redirect(url_for("editProfile"))


@app.route("/joincontest/<int:contestid>")
def joinContest(contestid):
    s = db.joincontest(contestid,session["userid"])
    s = True
    if s:
        return redirect("http://localhost:5000/entercontest/%d" %contestid)
    else:
        flash("Not Startable Yet!")
        return redirect(request.referrer)


@app.route("/contest/<int:contest_id>")
def startContest(contest_id):
    name = None
    if "username" in session:
        contest = db.viewinformation(contest_id)
        contest= contest
        return render_template("singleContestView.html",cn=contest,contest_id=contest_id)
    else:
        return "Log In to see the contest <a href='http://localhost:5000/login'>Log In</a>"


@app.route("/entercontest/<int:contest_id>")
def entercontest(contest_id):
    if "userid" in session:
        qs = db.getcontest(contest_id)
        return render_template("enterContest.html", contest_name=contest_id, questions=qs)
    else:
        return "You are not logged in! <a href=\"http://localhost:5000/login\">LogIN</a>"


@app.route("/show_result", methods=["post"])
def show_result():
    return