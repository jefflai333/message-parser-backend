from sys import getsizeof


class MessageManager:
    def __init__(self):
        pass

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

    def is_valid_message(self, message):
        requiredAttrs = ["sender_name", "timestamp_ms", "content"]
        for attrs in requiredAttrs:
            if not hasattr(message, attrs):
                print("Missing attrs in message")
                return False
        if getsizeof(message.sender_name) > 255:
            print("Name too long")
            return False
        if getsizeof(message.content) > 65535:
            print("Content too long")
            return False
        if (message.timestamp_ms) < 0:
            print("Negative timestamp")
            return False
        return True
        # optionalKeys = {
        #     "reactions": self.validate_reactions,
        #     "photos": self.validate_photos,
        #     "share": self.validate_share,
        # }
        # for key, value in optionalKeys.items():
        #     if key in message and not message[value](message[key]):
        #         print(key + " key poorly formatted")
        #         return False
        # if "reactions" in message and not self.validate_reactions(message["reactions"]):
        #     print("Reaction array poorly formatted")
        #     return False
        # if "photos" in message and not self.validate_photos(message["photos"]):
        #     print("Photos array poorly formatted")
        #     return False
        # if "share" in message and not self.validate_share(message["share"]):
        #     print("share not properly formatted")
        #     return False
