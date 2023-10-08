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
        values = {"username": username}
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
        values = {"username": username, "password": password}
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
        values = {"username": username}
        result = self.db.session.execute(text(query), values)
        user = result.fetchone()
        return user

    def get_all_recent_messages_from_all_users_fibers(self, user_id):
        query = """
            SELECT M.time, U.username author, M.content 
            FROM messages M 
                INNER JOIN user_fibers UF 
                    ON M.fiber_id = UF.fiber_id 
                INNER JOIN users U 
                    ON M.author_id = U.id 
            WHERE UF.user_id = :user_id
            ORDER BY M.time DESC
        """
        values = {"user_id": user_id}
        result = self.db.session.execute(text(query), values)
        messages = result.fetchall()
        return messages

    def get_messages_by_fiber_id(self, fiber_id):
        query = """
            SELECT M.time, U.username author, M.content 
            FROM messages M 
                INNER JOIN users U 
                    ON M.author_id = U.id 
            WHERE M.fiber_id = :fiber_id
            ORDER BY M.time DESC
        """
        values = {"fiber_id": fiber_id}
        result = self.db.session.execute(text(query), values)
        messages = result.fetchall()
        return messages

    def append_new_message(self, author_id, fiber_id, content):
        query = """
            INSERT INTO messages 
                (time, author_id, fiber_id, content) 
            VALUES 
                (NOW(), :author_id, :fiber_id, :content)
            """
        values = {"author_id": author_id, "fiber_id": fiber_id, "content": content}
        self.db.session.execute(text(query), values)
        self.db.session.commit()

    def insert_new_fiber(self, owner_id, fibername, description):
        query = """
            INSERT INTO fibers
                (owner_id, fibername, description)
            VALUES
                (:owner_id, :fibername, :description)
            RETURNING
                id
            """
        values = {"owner_id": owner_id, "fibername": fibername, "description": description}
        result = self.db.session.execute(text(query), values)
        fiber_id = result.fetchone()[0]
        query = """
            INSERT INTO user_fibers
                (user_id, fiber_id)
            VALUES
                (:user_id, :fiber_id)
            """
        values = {"user_id": owner_id, "fiber_id": fiber_id}
        self.db.session.execute(text(query), values)
        self.db.session.commit()
        return fiber_id

    def fibername_exists(self, fibername):
        query = """
            SELECT 
                id 
            FROM 
                fibers 
            WHERE 
                fibername=:fibername
        """
        values = {"fibername": fibername}
        result = self.db.session.execute(text(query), values)
        fiber = result.fetchone()
        if not fiber:
            return False
        return True

    def get_fiber_by_fiber_id(self, fiber_id):
        query = """
            SELECT id, fibername, description 
            FROM fibers 
            WHERE id = :fiber_id;
        """
        values = {"fiber_id": fiber_id}
        result = self.db.session.execute(text(query), values)
        fiber = result.fetchone()
        return fiber

    def insert_new_user_to_fiber(user_id, fiber_id):
        # query = """
        #     INSERT INTO user_fibers
        #         (user_id, fiber_id)
        #     VALUES
        #         (:user_id, :fiber_id)
        #     """
        # values = {"user_id": user_id, "fiber_id": fiber_id}
        # self.db.session.execute(text(query), values)
        # self.db.session.commit()
        pass

    def get_fibers_by_user_id(self, user_id):
        query = """
            SELECT 
                F.id, F.fibername, F.description 
            FROM 
                user_fibers UF 
            INNER JOIN 
                fibers F 
            ON 
                UF.fiber_id = F.id 
            WHERE 
                UF.user_id = :user_id
        """
        values = {"user_id": user_id}
        result = self.db.session.execute(text(query), values)
        fibers = result.fetchall()
        return fibers

    def insert_tag_if_not_exists(self, tag):
        query = """
            WITH s AS (
                SELECT id 
                FROM tags 
                WHERE tag = :tag
            ), i AS (
                INSERT INTO tags (tag) 
                SELECT :tag 
                WHERE NOT EXISTS (select 1 from s) 
                RETURNING id
            ) 
            SELECT id 
            FROM i 
            UNION ALL 
            SELECT id 
            FROM s
        """
        values = {"tag": tag}
        result = self.db.session.execute(text(query), values)
        tag_id = result.fetchone()[0]
        self.db.session.commit()
        return tag_id

    def associate_fiber_with_tag(self, fiber_id, tag_id):
        query = """
            INSERT INTO fiber_tags
                (fiber_id, tag_id)
            VALUES
                (:fiber_id, :tag_id)
        """
        values = {"fiber_id": fiber_id, "tag_id": tag_id}
        self.db.session.execute(text(query), values)
        self.db.session.commit()

    def get_member_entry(self, user_id, fiber_id):
        query = """
            SELECT
                *
            FROM
                user_fibers
            WHERE
                user_id = :user_id
            AND 
                fiber_id = :fiber_id
        """
        values = {"user_id":user_id, "fiber_id":fiber_id}
        result = self.db.session.execute(text(query), values)
        member_entry = result.fetchone()[0]
        return member_entry
