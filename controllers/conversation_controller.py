import os
from ..parsers.conversation_parser import ConversationParser
from ..managers.conversation_manager import ConversationManager


class ConversationController:
    def __init__(self):
        self.conversation_parser = ConversationParser()
        self.conversation_manager = ConversationManager()

    def add_json_to_db(self, file):
        conversation = self.conversation_parser.parse_json(file)
        if self.conversation_manager.is_conversation_valid(conversation):
            status = self.conversation_manager.commit_conversation(
                conversation)
        return {"status": status}

    def add_jsons_to_db(self, folder):
        # assume that the file path is actually a folder containing .json
        rootdir = folder
        # iterates through all the file paths in the directory and appends any json files into array
        for subdir, _, files in os.walk(rootdir):
            for filename in files:
                filepath = subdir + os.sep + filename
                if filepath.endswith(".json") and "message" in filename:
                    print("Adding " + filepath + " to db")
                    self.add_json_to_db(filepath)
