from flask import Flask

from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

from routes import *


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
