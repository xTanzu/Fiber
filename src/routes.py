from flask import Flask
from flask import redirect, render_template, request

from app import app 

from application_logic import Application_logic

import sys

application = Application_logic()

def handleFormInput():
    message_content = request.form["message_content"]
    application.submit_new_message(message_content)

@app.route("/", methods=["GET","POST"])
def index():
    if request.method == "POST":
        handleFormInput()
        return redirect("/")
    messages = application.get_messages()
    return render_template("main.html.jinja", messages=(messages))


