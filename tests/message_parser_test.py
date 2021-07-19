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
