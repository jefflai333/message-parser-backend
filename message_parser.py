import json
from ftfy import fix_text


def message_parser():
    with open('./test/message_10.json', 'r', encoding="utf8") as f:
        jsonData = json.loads(f.read())
    return jsonData


def fix_encoding(jsonData):
    if isinstance(jsonData, str):
        print(fix_text(jsonData))
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
