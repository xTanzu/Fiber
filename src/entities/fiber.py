from markupsafe import escape
from entities.tag import Tag

import sys

class Fiber:
    def __init__(self, fibername, description, tags, fiber_id=None, owner_id=None):
        self.fiber_id = fiber_id
        self.owner_id = owner_id
        self.fibername = fibername
        self.description = description
        self.tags = list(map(Fiber.from_str_to_tag, tags))

    @staticmethod
    def from_str_to_tag(tag_string):
        parts = tag_string.split()
        if len(parts) == 1:
            return Tag(None, parts[0])
        return Tag(*parts[:2])

    @property
    def tag_string_list(self):
        return [str(tag) for tag in self.tags]

    @property
    def markupsafe_fibername(self):
        return escape(self.fibername)

    @property
    def markupsafe_description(self):
        return escape(self.description)

    @property
    def markupsafe_tags_string(self):
        return " ".join([tag.markupsafe_tag for tag in self.tags])

    def __str__(self):
        return self.fibername

    def __repr__(self):
        tags_string = "', '".join([ str(x.tag_id) + " " + str(x) for x in self.tags ])
        return f"({self.fiber_id}, {self.owner_id}, '{self.fibername}', '{self.description}', ['{tags_string}'])"
        # ['{"', '".join(self.tags)}'])"
