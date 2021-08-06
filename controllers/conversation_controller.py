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
        #return {"conv": conversation}
