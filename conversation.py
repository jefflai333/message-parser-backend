from .message import Message


class Conversation:
    def __init__(self, participants, messages, title, is_still_participant, thread_type, thread_path):
        self.participants = participants
        self.messages = self.create_list_of_messages(messages)
        self.title = title
        self.is_still_participant = is_still_participant
        self.thread_type = thread_type
        self.thread_path = thread_path

    def create_list_of_messages(self, messages):
        validated_messages = []
        for message in messages:
            if self.validate_message(message):
                validated_messages.append(self.create_message_model(message))
            else:
                print("Error parsing message", message)
        return validated_messages

    def create_message_model(self, message):
        content = ""
        reactions = []
        if message["content"]:
            content = message["content"]
        if message["reactions"]:
            reactions = message["reactions"]
        return Message(message["sender_name"], message["timestamp_ms"], content, reactions, message["type"])

    def validate_reactions(self, reactionsData):
        for reaction in reactionsData:
            if "reaction" not in reaction or "actor" not in reaction:
                return False
        return True

    def validate_message(self, message):
        requiredKeys = ["sender_name", "timestamp_ms", "type"]
        for key in requiredKeys:
            if key not in message:
                print("Missing key in message")
                return False
        if message["reactions"] and not self.validate_reactions(message["reactions"]):
            print("Reaction array poorly formatted")
            return False
        return True
