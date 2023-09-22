from repository import Repository

from datetime import datetime

import sys

class Application_logic:
    def __init__(self):
        self.repository = Repository()
        self.signed_in_user = "Taneli Härkönen"

    def get_messages(self):
        messages = self.repository.get_messages()
        return messages

    def submit_new_message(self, message_content: str):
        format_str = "%Y-%m-%dT%H:%M:%S.%f"
        time_str = datetime.now().strftime(format_str)
        author = self.signed_in_user
        self.repository.append_new_message(author, time_str, message_content)


