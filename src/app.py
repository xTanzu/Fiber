from flask import Flask

from dotenv import load_dotenv

from os import getenv

import sys

load_dotenv()

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")

from routes import *


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
