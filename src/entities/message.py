from markupsafe import escape

class Message:
    def __init__(self, message_id, time, author, content):
        self.message_id = message_id
        self.time = time
        self.author = author
        self.content = content

    def markupsafe_date(self):
        return escape(self.time.strftime("%-d.%m.%Y"))
    
    def markupsafe_time(self):
        return escape(self.time.strftime("%H:%M"))

    def markupsafe_author(self):
        return escape(self.author)

    def markupsafe_content(self):
        return escape(self. content)

    def __str__(self):
        return self.content

    def __repr__(self):
        return f"Message({self.message_id}, {self.time}, {self.author}, {self.content})"
