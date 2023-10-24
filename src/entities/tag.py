from markupsafe import escape

class Tag:
    def __init__(self, tag_id, tag):
        self.tag_id = tag_id
        self.tag = tag

    @property
    def markupsafe_tag(self):
        return escape(self.tag)

    def __str__(self):
        return self.tag

    def __repr__(self):
        return f"Tag({self.tag_id}, '{self.tag}')"
