import pytest
from .. import MessageParser
from . import test_data


def test_check_fixing_encoding_in_name():
    testMessageParser = MessageParser()
    assert testMessageParser.fix_encoding(
        test_data.bad_sender_name_json) == test_data.good_sender_name_json


def test_check_fixing_encoding_in_title():
    testMessageParser = MessageParser()
    assert testMessageParser.fix_encoding(
        test_data.bad_title_json) == test_data.good_title_json


def test_check_fixing_encoding_in_emoji():
    testMessageParser = MessageParser()
    assert testMessageParser.fix_encoding(
        test_data.bad_emoji_json) == test_data.good_emoji_json


def test_check_participants_exists():
    testMessageParser = MessageParser()
    assert not testMessageParser.is_valid_conversation(
        test_data.no_participants_json)


def test_check_messages_exists():
    testMessageParser = MessageParser()
    assert not testMessageParser.is_valid_conversation(
        test_data.no_messages_json)


def test_check_title_exists():
    testMessageParser = MessageParser()
    assert not testMessageParser.is_valid_conversation(test_data.no_title_json)


def test_check_is_still_participant_exists():
    testMessageParser = MessageParser()
    assert not testMessageParser.is_valid_conversation(
        test_data.no_is_still_participant_json)


def test_check_thread_type_exists():
    testMessageParser = MessageParser()
    assert not testMessageParser.is_valid_conversation(
        test_data.no_thread_type_json)


def test_check_proper_json():
    testMessageParser = MessageParser()
    assert testMessageParser.is_valid_conversation(
        test_data.bad_sender_name_json)


def test_check_participants_name():
    testMessageParser = MessageParser()
    assert not testMessageParser.validate_participants(test_data.no_name_array)


def test_json_file_read():
    testMessageParser = MessageParser()
    assert testMessageParser.parse_json(
        "./tests/message_test.json") == test_data.returned_json_data
