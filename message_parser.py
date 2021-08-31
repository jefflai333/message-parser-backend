import json
import os
import pathlib
from natsort import natsort_key
from ftfy import fix_text


class MessageParser():
    def __init__(self):
        self.listOfJsons = []
        self.jsonData = []
        self.conversation = []

    def __init__(self, file):
        self.listOfJsons = self.create_list_of_jsons(file)
        self.listOfJsonData = self.parse_list_of_jsons()
        self.listOfConversations = self.create_list_of_conversations()

    def add_file(self, file):
        self.listOfJsons = self.create_list_of_jsons(file)
        self.listOfJsonData = self.parse_list_of_jsons()
        self.listOfConversations = self.create_list_of_conversations()

    def create_list_of_jsons(self, file):
        list_of_jsons = []
        # there is only one file if file ends in .json
        if file.endswith(".json"):
            list_of_jsons.append(file)
            return list_of_jsons
        # assume that the file path is actually a folder containing .json
        rootdir = file
        # iterates through all the file paths in the directory and appends any json files into array
        for subdir, _, files in os.walk(rootdir):
            for filename in files:
                filepath = subdir + os.sep + filename
                if filepath.endswith(".json") and "message" in filename:
                    list_of_jsons.append(filepath)
        # does a natural sort for messages with more than 10 html files
        # eg messages_1.html, messages_10.html, messages_2.html will sort into
        #messages_1.html, messages_2.html, messages_10.html
        if len(list_of_jsons) > 9:
            list_of_jsons = sorted(list_of_jsons, key=lambda x: list(
                natsort_key(s) for s in pathlib.Path(x).parts))
        return list_of_jsons

    def parse_list_of_jsons(self):
        parsed_json_list = []
        for file in self.listOfJsons:
            parsed_json = self.parse_json(file)
            parsed_json_list.append(self.fix_encoding(parsed_json))
        return parsed_json_list

    def create_list_of_conversations(self):
        list_of_conversations = []
        for parsed_json in self.listOfJsonData:
            list_of_conversations.append(
                self.create_conversation_model(parsed_json))
        return list_of_conversations

    def parse_json(self, file):
        with open(file, 'r', encoding="utf8") as f:
            jsonData = json.loads(f.read())
        return jsonData

    def create_conversation_model(self, jsonData):
        if self.is_valid_conversation(jsonData):
            return Conversation(jsonData["participants"], jsonData["messages"], jsonData["title"], jsonData["is_still_participant"], jsonData["thread_type"], jsonData["thread_path"])
        else:
            print("Error converting json file into a conversation")
            return

    def fix_encoding(self, jsonData):
        if isinstance(jsonData, str):
            return fix_text(jsonData)
        elif isinstance(jsonData, dict):
            for json_key, json_value in jsonData.items():
                jsonData[json_key] = self.fix_encoding(json_value)
        elif isinstance(jsonData, list):
            for json_value in jsonData:
                self.fix_encoding(json_value)
        else:
            return jsonData
        return jsonData

    def validate_participants(self, jsonData):
        for participant in jsonData["participants"]:
            if "name" not in participant:
                print("Participants array poorly formatted")
                return False
        return True

    def is_valid_conversation(self, jsonData):
        requiredKeys = ["participants", "messages", "title",
                        "is_still_participant", "thread_type", "thread_path"]
        for key in requiredKeys:
            if key not in jsonData:
                return False
        isParticipantsValid = self.validate_participants(jsonData)
        return isParticipantsValid
