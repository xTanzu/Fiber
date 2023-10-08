from flask import Flask
from flask import redirect, render_template, request, flash, session

from app import app 

from application_logic import Application_logic
from exceptions import DatabaseException

import sys

application = Application_logic()

@app.route("/", methods=["GET","POST"])
def index():
    if not application.is_logged_in():
        return redirect("/login")
    messages = application.get_all_recent_messages()
    fibers = application.get_users_fibers()
    return render_template("main.html.jinja", messages=messages, fibers=fibers)

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
        except (ValueError, DatabaseException) as e:
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
        except (ValueError, DatabaseException) as e:
            flash(e)
            placeholder_username = username
    return render_template("credentials.html.jinja", form_type="login", placeholder_username=placeholder_username)

@app.route("/logout", methods=["GET"])
def logout():
    application.logout_user()
    return redirect("/")

@app.route("/create_fiber", methods=["GET", "POST"])
def create_fiber():
    if not application.is_logged_in():
        return redirect("/login")
    fibername, description, tags = ("",)*3
    if request.method == "POST":
        fibername = request.form["fibername"]
        description = request.form["fiber_description"]
        tags = request.form["fiber_tags"]
        try:
            fiber_id = application.create_fiber(fibername, description, tags)
            return redirect(f"fiber/{fiber_id}")
        except (ValueError, DatabaseException) as e:
            flash(e)
    fibers = application.get_users_fibers()
    return render_template("fiber.html.jinja", edit_state="create", fibers=fibers, fibername=fibername, description=description, tags=tags)

@app.route("/fiber/<fiber_id>", methods=["GET", "POST"])
def view_fiber(fiber_id):
    if not application.is_logged_in():
        return redirect("/login")
    if not application.user_is_member_in_fiber(fiber_id):
        return redirect("/")
    placeholder_message = ""
    if request.method == "POST":
        message_content = request.form["message_content"]
        try:
            application.submit_new_message(message_content, fiber_id)
            return redirect(f"fiber/{fiber_id}")
        except (ValueError, DatabaseException) as e:
            flash(str(e))
            placeholder_message = message_content
    open_fiber = application.get_fiber_by_fiber_id(fiber_id)
    print(open_fiber["id"], file=sys.stdout)
    messages = application.get_messages_by_fiber_id(fiber_id)
    fibers = application.get_users_fibers()
    return render_template("fiber.html.jinja", open_fiber=open_fiber, messages=messages, fibers=fibers, placeholder_message=placeholder_message)

