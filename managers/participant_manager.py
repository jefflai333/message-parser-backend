from sys import getsizeof


class ParticipantManager:
    def __init__(self):
        pass

    def is_valid_participant(self, participant):
        if getsizeof(participant.name) > 255:
            print("Name too long")
            return False
        return True
