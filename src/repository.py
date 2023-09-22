from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

from os import getenv

from app import app

import sys

class Repository:
    def __init__(self):
        db_url = getenv("DATABASE_URL")
        app.config["SQLALCHEMY_DATABASE_URI"] = db_url
        self.db = SQLAlchemy(app)

    def get_messages(self):
        query = "SELECT author, time, content FROM message"
        result = self.db.session.execute(text(query))
        messages = result.fetchall()
        return messages

    def append_new_message(self, author: str, time_str: str, content:str):
        query = "INSERT INTO message (author, time, content) VALUES (:author, :time_str, :content)"
        values = {"author":author, "time_str":time_str, "content":content}
        self.db.session.execute(text(query), values)
        self.db.session.commit()
        return

