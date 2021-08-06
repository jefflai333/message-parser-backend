from .message_manager import MessageManager
from .participant_manager import ParticipantManager
from ..daos.conversation_dao import ConversationDAO


class ConversationManager:
    def __init__(self):
        self.message_manager = MessageManager()
        self.participant_manager = ParticipantManager()
        self.conversation_dao = ConversationDAO()

    def is_conversation_valid(self, conversation):
        requiredAttrs = ["participants", "messages", "thread_path"]
        for attrs in requiredAttrs:
            if not hasattr(conversation, attrs):
                return False
        if conversation.thread_path is None:
            print("thread_path doesn't exist")
            return False
        participants = []
        for participant in conversation.participants:
            if not self.participant_manager.is_valid_participant(participant):
                print("error with participant validation")
                return False
            participants.append(participant.name)
        for message in conversation.messages:
            if not self.message_manager.is_valid_message(message, participants):
                print("error with message validation")
                return False
        return True

    def commit_conversation(self, conversation):
        self.conversation_dao.save_conversation(conversation)
        return 1
