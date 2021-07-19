import pytest
import message_parser
from . import test_data


def test_check_fixing_encoding_in_name():
    assert message_parser.fix_encoding(
        test_data.bad_sender_name_json) == test_data.good_sender_name_json


def test_check_fixing_encoding_in_title():
    assert message_parser.fix_encoding(
        test_data.bad_title_json) == test_data.good_title_json


def test_check_fixing_encoding_in_emoji():
    assert message_parser.fix_encoding(
        test_data.bad_emoji_json) == test_data.good_emoji_json


def test_check_participants_exists():
    assert not message_parser.validate_json(test_data.no_participants_json)


def test_check_messages_exists():
    assert not message_parser.validate_json(test_data.no_messages_json)


def test_check_title_exists():
    assert not message_parser.validate_json(test_data.no_title_json)


def test_check_is_still_participant_exists():
    assert not message_parser.validate_json(test_data.no_is_still_participant_json)


def test_check_thread_type_exists():
    assert not message_parser.validate_json(test_data.no_thread_type_json)


def test_check_proper_json():
    assert message_parser.validate_json(test_data.bad_sender_name_json)


def test_check_participants_name():
    assert not message_parser.validate_participants(test_data.no_name_array)

def test_check_reactions():
    assert not message_parser.validate_reactions(test_data.no_reaction_array)

def test_check_actors():
    assert not message_parser.validate_reactions(test_data.no_actor_array)

def test_check_no_reaction_in_messages():
    assert not message_parser.validate_messages(test_data.no_reaction_in_messages_array)

def test_check_no_sender_name_in_messages():
    assert not message_parser.validate_messages(test_data.no_sender_name_array)

def test_check_no_timestamp_ms_in_messages():
    assert not message_parser.validate_messages(test_data.no_timestamp_ms_array)

# this one should be true because content can be empty if a message was deleted
def test_check_no_content_in_messages():
    assert message_parser.validate_messages(test_data.no_content_array)

def test_check_no_reactions_in_messages():
    assert not message_parser.validate_messages(test_data.no_reactions_array)

def test_check_no_type_in_messages():
    assert not message_parser.validate_messages(test_data.no_type_array)