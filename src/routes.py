from flask import Flask
from flask import redirect, render_template, request, flash, session

from app import app 

from application_logic import Application_logic
from exceptions import CredentialsException, DatabaseException

import sys

application = Application_logic()

def handleFormInput():
    message_content = request.form["message_content"]
    application.submit_new_message(message_content)

@app.route("/", methods=["GET","POST"])
def index():
    if not application.is_logged_in():
        return redirect("login")
    if request.method == "POST":
        handleFormInput()
        return redirect("/")
    messages = application.get_messages()
    return render_template("main.html.jinja", messages=messages)

@app.route("/register", methods=["GET", "POST"])
def register():
    if application.is_logged_in():
        return redirect("/")
    placeholder_username = ""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        rpt_password = request.form["rpt_password"]
        # print(f"username:{username}, password:{password}, rpt_password:{rpt_password}", file=sys.stdout)
        try:
            application.register_user(username, password, rpt_password)
            application.login_user(username, password)
            return redirect("/")
        except (CredentialsException, DatabaseException) as e:
            flash(e)
            placeholder_username = username
    return render_template("credentials.html.jinja", form_type="register", placeholder_username=placeholder_username)

@app.route("/login", methods=["GET", "POST"])
def login():
    if application.is_logged_in():
        return redirect("/")
    placeholder_username = ""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        try:
            application.login_user(username, password)
            return redirect("/")
        except (CredentialsException, DatabaseException) as e:
            flash(e)
            placeholder_username = username
    return render_template("credentials.html.jinja", form_type="login", placeholder_username=placeholder_username)

@app.route("/logout", methods=["GET"])
def logout():
    application.logout_user()
    return redirect("/")

