from flask import session

from repository import Repository
import validation

from exceptions import DatabaseException

from werkzeug.security import generate_password_hash, check_password_hash
from markupsafe import escape
# from datetime import datetime

import sys

messages_per_page = 10

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
        validation.validate_name(username, name_type="user")
        if self.repository.username_exists(username):
            raise ValueError("username already exists")
        validation.validate_password(password)
        if password != rpt_password:
            raise ValueError("passwords differ")
        password_hash = generate_password_hash(password)
        try:
            self.repository.insert_new_user(username, password_hash)
        except Exception as e:
            raise DatabaseException("error during inserting new user to database")

    def login_user(self, username, password):
        user = self.repository.get_user_by_username(username)
        if not user:
            raise ValueError("invalid username")
        password_hash = user.password
        if not check_password_hash(password_hash, password):
            raise ValueError("invalid password")
        session["logged_in_user"] = {
            "id": user.id,
            "username": user.username
        }

    def logout_user(self):
        del session["logged_in_user"]

    def get_all_recent_messages(self):
        user_id = session["logged_in_user"]["id"]
        messages = self.repository.get_all_recent_messages_from_all_users_fibers(user_id)
        safe_messages = self.escape_messages(messages)
        return safe_messages[:messages_per_page]

    def get_messages_by_fiber_id(self, fiber_id):
        if not self.user_is_member_in_fiber(fiber_id):
            raise ValueError("not a member")
        messages = self.repository.get_messages_by_fiber_id(fiber_id)
        safe_messages = self.escape_messages(messages)
        return safe_messages[:messages_per_page]

    def escape_messages(self, messages):
        safe_messages = []
        for message in messages:
            safe_message = {
                "time": message.time,
                "author": message.author,
                "content": escape(message.content)
            }
            safe_messages.append(safe_message)
        return safe_messages

    def submit_new_message(self, message_content, fiber_id):
        if not self.user_is_member_in_fiber(fiber_id):
            raise ValueError("not a member")
        validation.validate_text(message_content, text_type="message")
        author_id = session["logged_in_user"]["id"]
        self.repository.append_new_message(author_id, fiber_id, message_content)

    def get_fiber_by_fiber_id(self, fiber_id):
        fiber = self.repository.get_fiber_by_fiber_id(fiber_id)
        safe_fiber = self.escape_fibers([fiber,])[0]
        return safe_fiber

    def get_users_fibers(self):
        user_id = session["logged_in_user"]["id"]
        fibers = self.repository.get_fibers_by_user_id(user_id)
        safe_fibers = self.escape_fibers(fibers)
        return safe_fibers

    def escape_fibers(self, fibers):
        safe_fibers = []
        for fiber in fibers:
            safe_fiber = {
                "id": fiber.id,
                "fibername": escape(fiber.fibername),
                "description": escape(fiber.description)
            }
            safe_fibers.append(safe_fiber)
        return safe_fibers

    def create_fiber(self, fibername, description, tags):
        validation.validate_name(fibername, name_type="fiber", exra_chars=" ")
        if self.repository.fibername_exists(fibername):
            raise ValueError(f"fibername \"{fibername}\" already exists");
        validation.validate_text(description, text_type="description")
        owner_id = session["logged_in_user"]["id"]
        tags = list(set(tags.split()))
        try:
            fiber_id = self.repository.insert_new_fiber(owner_id, fibername, description)
            for tag in tags:
                tag_id = self.repository.insert_tag_if_not_exists(tag)
                self.repository.associate_fiber_with_tag(fiber_id, tag_id)
                # print(f"tag '{tag}', with id:{tag_id}, associated with fiber '{fibername}', with id:{fiber_id}", file=sys.stdout)
            return fiber_id
        except Exception as e:
            raise DatabaseException("error during inserting new fiber to database") from e

    def user_is_member_in_fiber(self, fiber_id):
        user_id = session["logged_in_user"]["id"]
        member_entry = self.repository.get_member_entry(user_id, fiber_id)
        if not member_entry:
            return False
        return True

