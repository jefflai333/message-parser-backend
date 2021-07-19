import json
import re
from ftfy import fix_text


def message_parser():
    with open('./test/message_10.json', 'r', encoding="utf8") as f:
        jsonData = json.loads(f.read())
    return jsonData


def fix_encoding(jsonData):
    if isinstance(jsonData, str):
        return fix_text(jsonData)
    elif isinstance(jsonData, dict):
        for json_key, json_value in jsonData.items():
            jsonData[json_key] = fix_encoding(json_value)
    elif isinstance(jsonData, list):
        for json_value in jsonData:
            fix_encoding(json_value)
    else:
        return jsonData
    return jsonData

def validate_participants(participantsData):
    for participant in participantsData:
        if "name" not in participant:
            return False
    return True

def validate_reactions(reactionsData):
    for reaction in reactionsData:
        if "reaction" not in reaction or "actor" not in reaction:
            return False
    return True

def validate_messages(messagesData):
    requiredKeys = ["sender_name", "timestamp_ms", "reactions", "type"]
    for message in messagesData:
        for key in requiredKeys:
            if key not in message:
                return False
        if not validate_reactions(message["reactions"]):
            return False
    return True

def validate_json(jsonData):
    requiredKeys = ["participants", "messages", "title", "is_still_participant", "thread_type", "thread_path"]
    for key in requiredKeys:
        if key not in jsonData:
            return False
    isParticipantsValid = validate_participants(jsonData["participants"])
    isMessagesValid = validate_messages(jsonData["messages"])
    return isParticipantsValid and isMessagesValid

