from ..models.participant import Participant


class ParticipantParser:
    def __init__(self):
        pass

    def parse_participant(self, d):
        participant = Participant()
        if not isinstance(d, dict):
            return participant
        if "name" in d:
            participant.add_name(d["name"])
        return participant
