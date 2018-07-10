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


@app.route("/createContest")
def createContest():
    return render_template("contestRegister.html")


@app.route("/addContest", methods=["POST"])
def addContest():
    resp = db.addConetest(request.form["titleTxt"],request.form["description"],
                          request.form["first"], request.form["second"],request.form["third"],request.form["forth"],
                          request.form["fee"], request.form["starttime"], request.form["endtime"],
                          True, 1, -100000000, "NothingYet")

    if resp['Status'] == 1:
        return redirect(url_for("root"))
    else:
        return "Contest Not Created - <a href='/createContest'>createContest<a>"


@app.route("/")
def root():
    logIn = None
    if "username" in session:
        logIn = [True, session["username"]]
    else:
        logIn = False
    ranking=db.viewranking()
    resp = db.showcontests(1)
    globalContestList = resp['ContestsList'][::-1]
    return render_template("showContests.html",resutl=globalContestList,ranking=ranking,logIn=logIn)

@app.route("/login")
def loginView():
    if not ("username" in session):
        return render_template("logInForm.html")
    else:
        flash("You are already logged in!\n")
        return redirect(url_for("root"))

@app.route("/auth", methods=["post"])
def auth():
    if db.passwordCheck(request.form["username"], HashGenerator.md5HashGenerator(request.form["password"])):
        session["username"] = request.form["username"]
        session["userid"] = 5
        print (session["username"])
        print(request.form["password"])
        return redirect(url_for("root"))
    else:
        flash("Wrong password!\n")
        return redirect(url_for("loginView"))


@app.route("/logout")
def logout():
    if "username" in session:
        session.pop('username', None)
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
    if db.signup(request.form["email"], request.form["username"],
                 HashGenerator.md5HashGenerator(request.form["password"])):
        return redirect(url_for("root"))


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
        flash("Not ")
        return redirect(request.referrer)

@app.route("/contest/<int:contest_id>")
def startContest(contest_id):
    name = None
    if "username" in session:
        return render_template("singleContestView.html",contest_name=contest_id, contest_id=contest_id)
    else:
        return "Log In to see the contest <a href='http://localhost:5000/login'>Log In</a>"

@app.route("/entercontest/<int:contest_id>")
def entercontest(contest_id):
    if "username" in session:
        return render_template("enterContest.html", contest_name=contest_id)
    else:
        return "You are not logged in! <a href=\"http://localhost:5000/login\">LogIN</a>"

@app.route("/show_result", methods=["post"])
def show_result():
    return