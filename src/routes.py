from flask import Flask
from flask import render_template

from app import app

@app.route('/')
def index():
    return render_template('main.html.jinja')

