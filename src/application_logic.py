from flask import session

from repository import Repository
import validation

from exceptions import CredentialsException, DatabaseException

from werkzeug.security import generate_password_hash, check_password_hash
from markupsafe import escape
# from datetime import datetime

import sys


class Application_logic:
    def __init__(self):
        self.repository = Repository()

    def is_logged_in(self):
        session_user = session.get("logged_in_user")
        if not session_user:
            return False
        if "username" not in session_user or "id" not in session_user:
            return False
        user = self.repository.get_user_by_username(session_user["username"])
        if not user:
            return False
        if session_user["id"] != user.id:
            return False
        return True

    def register_user(self, username, password, rpt_password):
        validation.validate_username(username)
        if self.repository.username_exists(username):
            raise CredentialsException("username already exists")
        validation.validate_password(password)
        if password != rpt_password:
            raise CredentialsException("passwords differ")
        password_hash = generate_password_hash(password)
        try:
            self.repository.insert_new_user(username, password_hash)
            return True
        except Exception as e:
            raise DatabaseException("error during inserting new user to database")

    def login_user(self, username, password):
        user = self.repository.get_user_by_username(username)
        if not user:
            raise CredentialsException("invalid username")
        password_hash = user.password
        if not check_password_hash(password_hash, password):
            raise CredentialsException("invalid password")
        session["logged_in_user"] = {
            "id": user.id,
            "username": user.username
        }
        return True

    def logout_user(self):
        del session["logged_in_user"]

    def get_messages(self):
        messages = self.repository.get_messages()
        safe_messages = []
        for message in messages:
            safe_message = {
            "author": message.author,
            "time": message.time,
            "content": escape(message.content)
            }
            safe_messages.append(safe_message)
        return safe_messages

    def submit_new_message(self, message_content):
        validation.validate_message(message_content)
        author = session["logged_in_user"]["username"]
        self.repository.append_new_message(author, message_content)


