from flask import *
from database.database import Database
from hash.hashgenerator import HashGenerator
app = Flask(__name__)
app.secret_key = "testMe"
db = Database()


@app.route("/")
def root():
    return render_template("main_page.html")


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


@app.route("/show")
def show():
    resp = db.showcontests(1)
    dictionary = resp['ContestsList'][::-1]
    print(dictionary)
    return render_template("showContests.html",resutl=dictionary)

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
        return render_template("sign_up_view.html")


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
    return "To be done!"


@app.route("/edit_profile")
def editProfile():
    return "To be done!"


@app.route("/join_contest")
def joinContest():
    #toDo
    return redirect(url_for("root"))

@app.route("/contest/<int:contest_id>")
def startContest(contest_id):
    if "username" in session:
        #contest = db.getContest(contest_id)
        return "Not prepared Yet"
    else:
        return "Log In to see the contest <a href='http://localhost:5000/login'>Log In</a>"