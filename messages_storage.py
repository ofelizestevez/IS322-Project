import os
import json

class MessageStorage:
    def __init__(self, file):
        self.file = file
        self.messages = self.load_messages()

    def load_messages(self):
        
        if os.path.exists(self.file):
            print("file exists")
            with open(self.file, "r") as file:
                return json.load(file)
        else:
            print("starting anew")
            return {}

    def save_messages(self):
        print("printing messages")
        print(self.messages)
        with open(self.file, "w") as file:
            
            json.dump(self.messages, file)

    def clear_file(self):
        open(self.file, 'w').close()  # Clear the file

    def add_message(self, author_id, content):
        if author_id not in self.messages:
            self.messages[author_id] = [content]
        else:
            self.messages[author_id].append(content)

        # Save messages to file after each addition
        self.save_messages()
