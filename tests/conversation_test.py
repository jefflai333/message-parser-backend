import pytest
from .. import Conversation
from . import test_data

def test_check_reactions():
    testConversation = Conversation()
    assert not testConversation.validate_reactions(
        test_data.no_reaction_array)


def test_check_actors():
    testConversation = Conversation()
    assert not testConversation.validate_reactions(test_data.no_actor_array)


def test_check_no_reaction_in_messages():
    testConversation = Conversation()
    assert not testConversation.validate_messages(
        test_data.no_reaction_in_messages_array)


def test_check_no_sender_name_in_messages():
    testConversation = Conversation()
    assert not testConversation.validate_messages(
        test_data.no_sender_name_array)


def test_check_no_timestamp_ms_in_messages():
    testConversation = Conversation()
    assert not testConversation.validate_messages(
        test_data.no_timestamp_ms_array)

# this one should be true because content can be empty if a message was deleted


def test_check_no_content_in_messages():
    testConversation = Conversation()
    assert testConversation.validate_messages(test_data.no_content_array)


def test_check_no_reactions_in_messages():
    testConversation = Conversation()
    assert not testConversation.validate_messages(
        test_data.no_reactions_array)


def test_check_no_type_in_messages():
    testConversation = Conversation()
    assert not testConversation.validate_messages(test_data.no_type_array)