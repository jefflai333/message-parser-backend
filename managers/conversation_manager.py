from .message_manager import MessageManager
from .participant_manager import ParticipantManager
from ..models.conversation import Conversation


class ConversationManager:
    def __init__(self):
        self.message_manager = MessageManager()
        self.participant_manager = ParticipantManager()

    def validate_conversation(self):
        return 1

    def commit_conversation(self, conversation):
        return 1
