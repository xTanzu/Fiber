from flask import session

from repository import Repository
from entities.fiber import Fiber
from entities.tag import Tag
from entities.message import Message
import validation

from exceptions import DatabaseException

from werkzeug.security import generate_password_hash, check_password_hash

import sys

messages_per_page = 10

class Application_logic:
    def __init__(self):
        self.repository = Repository()

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
        user_row = self.repository.get_user_by_username(username)
        if not user_row:
            raise ValueError("invalid username")
        user = user_row._asdict()
        password_hash = user.pop("password")
        if not check_password_hash(password_hash, password):
            raise ValueError("invalid password")
        session["logged_in_user"] = user

    def is_logged_in(self):
        session_user = session.get("logged_in_user")
        if not session_user:
            return False
        if "username" not in session_user or "user_id" not in session_user:
            return False
        user = self.repository.get_user_by_username(session_user["username"])
        if not user:
            return False
        if session_user["user_id"] != user.user_id:
            return False
        return True

    def logout_user(self):
        del session["logged_in_user"]

    def get_all_recent_messages(self):
        user_id = session["logged_in_user"]["user_id"]
        message_rows = self.repository.get_all_recent_messages_from_all_users_fibers(user_id)
        messages = [Message(**row._asdict()) for row in message_rows]
        return messages[:messages_per_page]

    def get_messages_by_fiber_id(self, fiber_id):
        if not self.user_is_member_in_fiber(fiber_id):
            raise ValueError("not a member")
        message_rows = self.repository.get_messages_by_fiber_id(fiber_id)
        messages = [Message(**row._asdict()) for row in message_rows]
        return messages[:messages_per_page]

    def submit_new_message(self, message_content, fiber_id):
        if not self.user_is_member_in_fiber(fiber_id):
            raise ValueError("not a member")
        validation.validate_text(message_content, text_type="message")
        author_id = session["logged_in_user"]["user_id"]
        try:
            self.repository.append_new_message(author_id, fiber_id, message_content)
        except Exception as e:
            raise DatabaseException("error during submitting new message") from e

    def create_fiber(self, fibername, description, tags):
        validation.validate_name(fibername, name_type="fiber", exra_chars=" ")
        if self.repository.fibername_exists(fibername):
            raise ValueError(f"fibername \"{fibername}\" already exists");
        validation.validate_text(description, text_type="description")
        owner_id = session["logged_in_user"]["user_id"]
        tags = list(set(tags.split()))
        try:
            fiber_id = self.repository.insert_new_fiber(owner_id, fibername, description)
            for tag in tags:
                tag_id = self.repository.insert_tag_if_not_exists(tag)
                self.repository.associate_fiber_with_tag(fiber_id, tag_id)
            return fiber_id
        except Exception as e:
            raise DatabaseException("error during inserting new fiber to database") from e

    def get_fiber_by_fiber_id(self, fiber_id):
        fiber_row = self.repository.get_fiber_by_fiber_id(fiber_id)
        fiber = Fiber(**fiber_row._asdict())
        return fiber

    def get_users_fibers(self):
        user_id = session["logged_in_user"]["user_id"]
        fiber_rows = self.repository.get_fibers_by_user_id(user_id)
        fibers = [Fiber(**row._asdict()) for row in fiber_rows]
        return fibers

    def get_fibers_by_tag_id(self, tag_id):
        fiber_rows = self.repository.get_fibers_by_tag_id(tag_id)
        fibers = [Fiber(**row._asdict()) for row in fiber_rows]
        return fibers

    def join_user_to_fiber(self, fiber_id):
        user_id = session["logged_in_user"]["user_id"]
        fiber = self.repository.get_fiber_by_fiber_id(fiber_id)
        if not fiber:
            raise ValueError("Selected fiber does not exist")
        if self.user_is_member_in_fiber(fiber_id):
            raise ValueError("User is already a member")
        try:
            self.repository.associate_user_with_fiber(user_id, fiber_id)
        except Exception as e:
            raise DatabaseException("error during inserting user to fiber")

    def user_is_member_in_fiber(self, fiber_id):
        user_id = session["logged_in_user"]["user_id"]
        member_entry = self.repository.get_member_entry(user_id, fiber_id)
        if not member_entry:
            return False
        return True

    def get_display_tags(self):
        tag_rows = self.repository.get_all_tags()
        tags = [Tag(**row._asdict()) for row in tag_rows]
        return tags

