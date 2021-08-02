import json
from ftfy import fix_text
from .conversation import Conversation


class MessageParser:
    def __init__(self, file):
        self.jsonData = self.parse_json(file)
        self.conversation = self.create_conversation_model()

    def parse_json(self, file):
        with open(file, 'r', encoding="utf8") as f:
            jsonData = json.loads(f.read())
        jsonData = self.fix_encoding(jsonData)
        return jsonData

    def create_conversation_model(self):
        if self.is_valid_conversation():
            return Conversation(self.jsonData["participants"], self.jsonData["messages"], self.jsonData["title"], self.jsonData["is_still_participant"], self.jsonData["thread_type"], self.jsonData["thread_path"])
        else:
            return "Error converting json file into a conversation"

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

    def validate_participants(self):
        for participant in self.jsonData["participants"]:
            if "name" not in participant:
                print("Participants array poorly formatted")
                return False
        return True

    def is_valid_conversation(self):
        requiredKeys = ["participants", "messages", "title",
                        "is_still_participant", "thread_type", "thread_path"]
        for key in requiredKeys:
            if key not in self.jsonData:
                return False
        isParticipantsValid = self.validate_participants()
        return isParticipantsValid
