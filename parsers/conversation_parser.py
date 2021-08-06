from .message_parser import MessageParser
from .participant_parser import ParticipantParser
from ..models.conversation import Conversation
from ..models.message import Message
import json


class ConversationParser:
    def __init__(self):
        self.message_parser = MessageParser()
        self.participant_parser = ParticipantParser()

    def parse_json(self, file):
        with open(file, 'r', encoding="utf8") as f:
            jsonData = json.loads(f.read())
        conversation = self.parse_conversation(jsonData)
        return conversation

    def parse_conversation(self, json):
        conversation = Conversation()
        if "participants" in json and isinstance(json["participants"], list):
            list_of_participants = []
            for participant in json["participants"]:
                list_of_participants.append(
                    self.participant_parser.parse_participant(participant))
            conversation.add_participants(list_of_participants)
        if "messages" in json and isinstance(json["messages"], list):
            list_of_messages = []
            for message in json["messages"]:
                list_of_messages.append(
                    self.message_parser.parse_message(message))
            conversation.add_messages(list_of_messages)
        if "thread_path" in json and isinstance(json["thread_path"], str) and "_" in json["thread_path"]:
            conversation.add_thread_path(json["thread_path"].split("_", 1)[1])
        return conversation

    def create_list_of_messages(self, messages):
        validated_messages = []
        for message in messages:
            if self.validate_message(message):
                validated_messages.append(self.create_message_model(message))
            else:
                print("Error parsing message", message)
        return validated_messages

    def create_message_model(self, message):
        optionalParams = {
            "content": "",
            "reactions": [],
            "photos": [],
            "share": {},
        }
        for key in optionalParams.keys():
            if key in message:
                optionalParams[key] = message[key]
        return Message(message["sender_name"], message["timestamp_ms"], optionalParams["content"], optionalParams["reactions"], message["type"], optionalParams["photos"], optionalParams["share"])
