from ..models.participant import Participant


class ParticipantParser:
    def __init__(self):
        pass

    def parse_participant(self, d):
        participant = Participant()
        if isinstance(d, str):
            participant.add_name(d)
        if isinstance(d, dict) and "name" in d:
            participant.add_name(d["name"])
        return participant
