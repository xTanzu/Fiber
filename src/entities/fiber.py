from markupsafe import escape
from entities.tag import Tag

import sys

class Fiber:
    def __init__(self, fiber_id, owner_id, fibername, description, tags):
        self.fiber_id = fiber_id
        self.owner_id = owner_id
        self.fibername = fibername
        self.description = description
        self.tags = [Tag(*tag.split(" ", 1)) if tag else None for tag in tags]

    def markupsafe_fibername(self):
        return escape(self.fibername)

    def markupsafe_description(self):
        return escape(self.description)

    def __str__(self):
        return self.fibername

    def __repr__(self):
        tags_string = "', '".join([ str(x.tag_id) + " " + str(x) for x in self.tags ])
        return f"({self.fiber_id}, {self.owner_id}, '{self.fibername}', '{self.description}', ['{tags_string}'])"
        # ['{"', '".join(self.tags)}'])"
