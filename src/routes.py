from flask import Flask
from flask import render_template, request

from datetime import datetime

from app import app

import sys

messages = [{
    "author": "Taneli Härkönen",
    "time": "2023-09-14T23:13:28",
    "content": "Täällä istuskelen Spaten pöydän alla, ja yritän samalla miettiä miten Flaskilla tehdään sovelluksia."
    },{
    "author": "Elisa Koskiniemi",
    "time": "2023-09-14T23:17:09",
    "content": "Mun piti mennä jo aikasemmin nukkumaan kun huomenna on aamulla töitä"
    },{
    "author": "Christian Puolokainen",
    "time": "2023-09-14T23:19:25",
    "content": "Mulla on kyllä jo vähän ikävä spatenia kun en oo tottunu olee kotona ilman sitä..."
    },{
    "author": "Taneli Härkönen",
    "time": "2023-09-14T23:21:03",
    "content": "No mutta nopeesti noi pari päivää menee. Teil on salee siä mökillä tosi nastaa!"
    },{
    "author": "Christian Puolokainen",
    "time": "2023-09-14T23:23:04",
    "content": "Joo totta siis ei mtn ihan mahtava reissu tulossa!!"
    },{
    "author": "Elisa Koskiniemi",
    "time": "2023-09-14T23:24:09",
    "content": "Pitäkää ihan tosi kivaa reissua!! Ja sanokaa Simolle ja Liisalle terkkuja"
    }
]
topics = [{
    "name": "Kelmit",
    "tags": [
        "kelmeilemme",
        "kaveriporukka",
        "alkoholi",
        "tastingit",
        "urpoja"
        ]
    },
    {
    "name": "FPV flyers",
    "tags": [
        "FPV",
        "Queadcopter",
        "RC",
        "Ripping"
        ]
    },
    {
    "name": "Stack Overflow",
    "tags": [
        "coding",
        "web-development",
        "online help",
        "toxic environment"
        ]
    },
    {
    "name": "Barfools",
    "tags": [
        "bartending",
        "spirits",
        "alcohol",
        "cocktails",
        "whisky"
        ]
    },
    {
    "name": "Trailseekers",
    "tags": [
        "mountain biking",
        "MTB",
        "bike repairs",
        "parts knowledge",
        "trail company"
        ]
    }]

def handleFormInput():
    author = "Taneli Härkönen"
    format_str = "%Y-%m-%dT%H:%M:%S.%f"
    time_str = datetime.now().strftime(format_str)
    message_content = request.form["message_content"]
    message = {
        "author": author,
        "time": time_str,
        "content": message_content
        }
    messages.append(message)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        handleFormInput()
    return render_template("main.html.jinja", messages=(messages), topics=topics)

