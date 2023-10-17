from flask import Flask
from flask import redirect, url_for, render_template, request, flash, session

from app import app 

from application_logic import Application_logic
from exceptions import DatabaseException

import sys

application = Application_logic()

@app.route("/", methods=["GET","POST"])
def index():
    if not application.is_logged_in():
        return redirect(url_for("login"))
    tags = application.get_display_tags()
    messages = application.get_all_recent_messages()
    fibers = application.get_users_fibers()
    return render_template("main.html.jinja", tags=tags, messages=messages, fibers=fibers)

@app.route("/register", methods=["GET", "POST"])
def register():
    if application.is_logged_in():
        return redirect(url_for("index"))
    placeholder_username = ""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        rpt_password = request.form["rpt_password"]
        # print(f"username:{username}, password:{password}, rpt_password:{rpt_password}", file=sys.stdout)
        try:
            application.register_user(username, password, rpt_password)
            application.login_user(username, password)
            return redirect(url_for("index"))
        except (ValueError, DatabaseException) as e:
            flash(e)
            placeholder_username = username
    return render_template("credentials.html.jinja", form_type="register", placeholder_username=placeholder_username)

@app.route("/login", methods=["GET", "POST"])
def login():
    if application.is_logged_in():
        return redirect(url_for("index"))
    placeholder_username = ""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        try:
            application.login_user(username, password)
            return redirect(url_for("index"))
        except (ValueError, DatabaseException) as e:
            flash(e)
            placeholder_username = username
    return render_template("credentials.html.jinja", form_type="login", placeholder_username=placeholder_username)

@app.route("/logout", methods=["GET"])
def logout():
    application.logout_user()
    return redirect(url_for("login"))

@app.route("/create_fiber", methods=["GET", "POST"])
def create_fiber():
    if not application.is_logged_in():
        return redirect(url_for("login"))
    placeholder_fiber = {}
    if request.method == "POST":
        fiber = {
            "fibername": request.form["fibername"],
            "description": request.form["fiber_description"],
            "tags": list(set(request.form["fiber_tags"].split()))
        }
        try:
            fiber_id = application.create_fiber(**fiber)
            return redirect(f"fiber/{fiber_id}")
        except (ValueError, DatabaseException) as e:
            flash(e)
            placeholder_fiber = application.escape_fiber(fiber)
    tags = application.get_display_tags()
    fibers = application.get_users_fibers()
    return render_template("fiber.html.jinja", edit_state="create", tags=tags, fibers=fibers, placeholder_fiber=placeholder_fiber)

@app.route("/fiber/<fiber_id>", methods=["GET", "POST"])
def view_fiber(fiber_id):
    if not application.is_logged_in():
        return redirect(url_for("login"))
    if not application.user_is_member_in_fiber(fiber_id):
        flash("You are not a member in this fiber")
        return redirect(url_for("index"))
    placeholder_message = ""
    if request.method == "POST":
        message_content = request.form["message_content"]
        try:
            application.submit_new_message(message_content, fiber_id)
            return redirect(url_for("view_fiber", fiber_id=fiber_id))
        except (ValueError, DatabaseException) as e:
            flash(str(e))
            placeholder_message = message_content
    open_fiber = application.get_fiber_by_fiber_id(fiber_id)
    tags = application.get_display_tags()
    messages = application.get_messages_by_fiber_id(fiber_id)
    fibers = application.get_users_fibers()
    return render_template("fiber.html.jinja", open_fiber=open_fiber, tags=tags, messages=messages, fibers=fibers, placeholder_message=placeholder_message)

@app.route("/fibersbytag/<tag_id>", methods=["GET"])
def fibers_by_tag(tag_id):
    if not application.is_logged_in():
        return redirect(url_for("login"))
    tags = application.get_display_tags()
    fiber_matches = application.get_fibers_by_tag_id(tag_id)
    fibers = application.get_users_fibers()
    return render_template("fiber_matches.html.jinja", tags=tags, fiber_matches=fiber_matches, fibers=fibers) 

@app.route("/join_fiber/<fiber_id>", methods=["GET"])
def join_fiber(fiber_id):
    if not application.is_logged_in():
        return redirect(url_for("login"))
    if application.user_is_member_in_fiber(fiber_id):
        return redirect(url_for("view_fiber", fiber_id=fiber_id))
    try:
        application.join_user_to_fiber(fiber_id)
        return redirect(url_for("view_fiber", fiber_id=fiber_id))
    except (ValueError, DatabaseException) as e:
        flash(str(e))
    return redirect(url_for("create_fiber"))

