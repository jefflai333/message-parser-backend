from .message import Message


class Conversation:
    def __init__(self):
        self.participants = []
        self.messages = []
        self.title = ""
        self.is_still_participant = False
        self.thread_type = ""
        self.thread_path = ""

    def __init__(self, participants, messages, title, is_still_participant, thread_type, thread_path):
        self.participants = participants
        self.messages = self.create_list_of_messages(messages)
        self.title = title
        self.is_still_participant = is_still_participant
        self.thread_type = thread_type
        self.thread_path = thread_path

    def add_conversation(self, participants, messages, title, is_still_participant, thread_type, thread_path):
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

    def validate_reactions(self, reactionsData):
        for reaction in reactionsData:
            if "reaction" not in reaction or "actor" not in reaction:
                return False
        return True

    def validate_photos(self, photosData):
        for photo in photosData:
            if "uri" not in photo or "creation_timestamp" not in photo:
                return False
        return True

    def validate_share(self, share):
        if "link" not in share:
            return False
        return True

    def validate_message(self, message):
        requiredKeys = ["sender_name", "timestamp_ms", "type"]
        for key in requiredKeys:
            if key not in message:
                print("Missing key in message")
                return False
        optionalKeys = {
            "reactions": self.validate_reactions,
            "photos": self.validate_photos,
            "share": self.validate_share,
        }
        # for key, value in optionalKeys.items():
        #     if key in message and not message[value](message[key]):
        #         print(key + " key poorly formatted")
        #         return False
        if "reactions" in message and not self.validate_reactions(message["reactions"]):
            print("Reaction array poorly formatted")
            return False
        if "photos" in message and not self.validate_photos(message["photos"]):
            print("Photos array poorly formatted")
            return False
        if "share" in message and not self.validate_share(message["share"]):
            print("share not properly formatted")
            return False
        return True
