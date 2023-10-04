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

    def username_exists(self, username):
        query = """
            SELECT 
                id 
            FROM 
                users 
            WHERE 
                username=:username
            """
        values = {"username":username}
        result = self.db.session.execute(text(query), values)
        user = result.fetchone()
        if not user:
            return False
        return True

    def insert_new_user(self, username, password):
        query = """
            INSERT INTO users
                (username, password)
            VALUES
                (:username, :password)
            """
        values = {"username":username, "password":password}
        self.db.session.execute(text(query), values)
        self.db.session.commit()

    def get_user_by_username(self, username):
        query = """
            SELECT
                id, username, password 
            FROM
                users
            WHERE
                username=:username
            """
        values = {"username":username}
        result = self.db.session.execute(text(query), values)
        user = result.fetchone()
        return user

    def get_messages(self):
        query = """
            SELECT 
                author, time, content 
            FROM 
                messages
            ORDER BY
                time DESC
            """
        result = self.db.session.execute(text(query))
        messages = result.fetchall()
        return messages

    def append_new_message(self, author, content):
        query = """
            INSERT INTO messages 
                (author, time, content) 
            VALUES 
                (:author, NOW(), :content)
            """
        values = {"author":author, "content":content}
        self.db.session.execute(text(query), values)
        self.db.session.commit()

