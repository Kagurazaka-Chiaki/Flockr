# -*- coding: utf-8 -*-
""" Tests for message.py """

from random import randint, sample, choice
from string import ascii_letters, digits
import pytest

from auth import auth_register
from channel import channel_messages
from channel import channel_invite
from channel import channel_addowner

from channels import channels_create

from message import message_send
from message import message_remove
from message import message_edit
from message import message_react
from message import message_unreact
from message import message_pin
from message import message_unpin

from error import InputError, AccessError
from other import clear


def test_valid_message_integration():
    """ valid message integration testing """
    clear()

    user_1 = auth_register("simple@example.com", "123456", "Hayden", "Jacobs")
    channel_1 = channels_create(user_1.get("token"), "COMP1531_Hayden", True)
    user_2 = auth_register(
        "simple@example.org",
        "123456",
        "Ian",
        "Thorvaldson"
    )
    channel_2 = channels_create(user_2.get("token"), "COMP1531_Ian", True)
    channel_invite(
        user_1.get("token"),
        channel_1.get("channel_id"),
        user_2.get("u_id")
    )
    channel_invite(
        user_2.get("token"),
        channel_2.get("channel_id"),
        user_1.get("u_id")
    )

    message_info_list = []

    for i in range(randint(5, 6)):
        random_string = ''.join(sample(ascii_letters + digits, randint(i, 10)))
        message_info = message_send(
            user_1.get("token"),
            channel_1.get("channel_id"),
            random_string
        )
        message_info_list.append(message_info.get("message_id"))

    remove_id = choice(message_info_list)
    message_remove(user_1.get("token"), remove_id)

    for i in range(randint(5, 6)):
        random_string = ''.join(sample(ascii_letters + digits, randint(i, 10)))
        message_info = message_send(
            user_2.get("token"),
            channel_1.get("channel_id"),
            random_string
        )
        message_info_list.append(message_info.get("message_id"))

    edit_id = choice(message_info_list)
    message_edit(user_1.get("token"), edit_id, "Ciallo")
    m_list = channel_messages(user_1.get(
        "token"), channel_1.get("channel_id"), 0)

    for i in m_list.get("messages"):
        if i.get("message_id") == edit_id:
            assert i.get("message") == "Ciallo"


def test_message_longer():
    """
    test the longer than 1000 characters message
    """
    clear()
    # building data structure

    dic_clearlove = auth_register("clearlove@gmail.com",
                                  "clearlove7", "Clear", "Love")
    token_wrong = dic_clearlove.get("token")
    name_wrong = "channel_clearlove"
    dic_channel_wrong = channels_create(token_wrong, name_wrong, True)
    channel_id_wrong = dic_channel_wrong.get("channel_id")

    # enter the message which longer than 1000 characters
    message_wrong = ""
    i = 0
    while i < 1001:
        message_wrong = message_wrong + "a"
        i = i + 1

    with pytest.raises(InputError):
        message_send(token_wrong, channel_id_wrong, message_wrong)

    message_wrong = " "
    for i in range(1001):
        message_wrong = message_wrong + " "

    with pytest.raises(InputError):
        message_send(token_wrong, channel_id_wrong, message_wrong)


def test_message_token_not_in():
    '''
    test the token that not in channel
    '''
    clear()
    # building data structure
    dic_jackey = auth_register("jackeychen@gmail.com",
                               "jackeychen", "Jackey", "Chen")
    token_test = dic_jackey.get("token")
    name_test = "channel_jackey"
    dic_channel = channels_create(token_test, name_test, True)
    channel_id_test = dic_channel.get("channel_id")

    dic_clearlove = auth_register("clearlove@gmail.com",
                                  "clearlove7", "Clear", "Love")
    token_wrong = dic_clearlove.get("token")
    name_wrong = "channel_clearlove"
    dic_channel_wrong = channels_create(token_wrong, name_wrong, True)
    channel_id_wrong = dic_channel_wrong.get("channel_id")

    # enter the token which is not belong to channel
    with pytest.raises(AccessError):
        message_send(token_test, channel_id_wrong, "deep ward")

    with pytest.raises(AccessError):
        message_send(token_wrong, channel_id_test, "no meaning")

    clear()


def test_invalid_channel():
    '''
    test the channel_id that not exist
    '''
    clear()
    # building data structure
    dic_clearlove = auth_register("clearlove@gmail.com",
                                  "clearlove7", "Clear", "Love")
    token_wrong = dic_clearlove.get("token")
    name_wrong = "channel_clearlove"
    dic_channel_wrong = channels_create(token_wrong, name_wrong, True)
    channel_id_wrong = dic_channel_wrong.get("channel_id")

    with pytest.raises(InputError):
        message_send(token_wrong, channel_id_wrong + 1, "fsdfsdf")

    clear()


def test_message_correct():
    """
    test correct condition for function message_send
    """

    clear()

    # building data structure
    dic_clearlove = auth_register("clearlove@gmail.com",
                                  "clearlove7", "Clear", "Love")
    token_wrong = dic_clearlove.get("token")
    name_wrong = "channel_clearlove"
    dic_channel_wrong = channels_create(token_wrong, name_wrong, True)
    channel_id_wrong = dic_channel_wrong.get("channel_id")

    dict_send1 = message_send(
        token_wrong, channel_id_wrong, "all we fight for")
    message_id1 = dict_send1.get("message_id")
    dict_send2 = message_send(token_wrong, channel_id_wrong, "deep ward")
    message_id2 = dict_send2.get("message_id")

    dict_message = channel_messages(token_wrong, channel_id_wrong, 0)
    assert dict_message["end"] == -1

    # test correct message
    for i in dict_message["messages"]:
        if i.get("message_id") == message_id1:
            assert i["message"] == "all we fight for"

    for i in dict_message["messages"]:
        if i.get("message_id") == message_id2:
            assert i["message"] == "deep ward"

    clear()


def test_valid_message_remove():
    """ valid message remove """
    clear()
    user = auth_register("simple@example.com", "123456", "Hayden", "Jacobs")
    info = channels_create(user.get("token"), "COMP1531", True)
    message1 = message_send(
        user.get("token"), info.get("channel_id"), "Hello")
    temp = message1.get("message_id")
    message_remove(user.get("token"), message1.get("message_id"))
    message2 = message_send(
        user.get("token"), info.get("channel_id"), "Hello")
    assert temp == message2.get("message_id")


def test_message_remove_invalid_message_id():
    """ test message remove within invalid message id """
    clear()
    user = auth_register("simple@example.com", "123456", "Hayden", "Jacobs")
    info = channels_create(user.get("token"), "COMP1531", True)
    message_send(
        user.get("token"),
        info.get("channel_id"),
        "Ciallo"
    )
    message = message_send(
        user.get("token"),
        info.get("channel_id"),
        "Ciallo"
    )
    message_remove(user.get("token"), message.get("message_id"))
    with pytest.raises(InputError):
        message_remove(user.get("token"), message.get("message_id"))


def test_message_remove_not_authorised():
    """ test message remove within not global owner or not channel owner"""
    clear()
    user1 = auth_register("simple@example.com", "123456", "Hayden", "Jacobs")
    user2 = auth_register("simple@example.org", "123456", "Ian", "Thorvaldson")
    info = channels_create(user1.get("token"), "COMP1531", True)
    message1 = message_send(
        user1.get("token"), info.get("channel_id"), "Ciallo")
    with pytest.raises(AccessError):  # not global owner
        message_remove(user2.get("token"), message1.get("message_id"))

    channel_invite(user1.get("token"), info.get(
        "channel_id"), user2.get("u_id"))

    with pytest.raises(AccessError):  # not channel owner
        message_remove(user2.get("token"), message1.get("message_id"))

    channel_addowner(user1.get("token"), info.get(
        "channel_id"), user2.get("u_id"))

    message_remove(user2.get("token"), message1.get("message_id"))
    message2 = message_send(
        user1.get("token"), info.get("channel_id"), "Ciallo")
    assert message1.get("message_id") == message2.get("message_id")


def test_message_remove_message_owner():
    """ test message remove within message owner but not global owner"""
    clear()
    user1 = auth_register("simple@example.com", "123456", "Hayden", "Jacobs")
    user2 = auth_register("simple@example.org", "123456", "Ian", "Thorvaldson")
    info = channels_create(user1.get("token"), "COMP1531", True)
    channel_invite(
        user1.get("token"), info.get("channel_id"), user2.get("u_id")
    )
    message1 = message_send(
        user2.get("token"), info.get("channel_id"), "Ciallo"
    )

    message_remove(user2.get("token"), message1.get("message_id"))

    message2 = message_send(
        user2.get("token"), info.get("channel_id"), "Ciallo"
    )
    assert message1.get("message_id") == message2.get("message_id")
    
    message3 = message_send(
        user2.get("token"), info.get("channel_id"), "World"
    )
    message_remove(user2.get("token"), message3.get("message_id"))

# test for message edit


def test_valid_message_edit():
    """ test valid suitation for message_edit """
    clear()
    user = auth_register("simple@example.com", "123456", "Hayden", "Jacobs")
    channel_id = channels_create(user.get("token"), "COMP1531", True)
    message1 = message_send(
        user.get("token"), channel_id.get("channel_id"), "Hello"
    )

    for i in range(2, 5):
        random_string = ''.join(sample(ascii_letters + digits, randint(i, 10)))
        message_send(
            user.get("token"), channel_id.get("channel_id"), random_string
        )
    
    message_edit(user.get("token"), message1.get("message_id"), "Ciallo")

    message_list = channel_messages(
        user.get("token"), channel_id.get("channel_id"), 0
    )

    for message_dic in message_list["messages"]:
        if message1.get("message_id") == message_dic.get("message_id"):
            assert message_dic.get("message") == "Ciallo"

    clear()
    user = auth_register("simple@example.com", "123456", "Hayden", "Jacobs")
    user2 = auth_register("simple@example2.com", "123456", "Michael", "Jacobs")
    channel_id = channels_create(user2.get("token"), "COMP1531", True)
    message1 = message_send(
        user2.get("token"), channel_id.get("channel_id"), "Hello"
    )

    message_edit(user.get("token"), message1.get("message_id"), "Ciallo")

    message_list = channel_messages(
        user2.get("token"), channel_id.get("channel_id"), 0
    )
    
    for message_dic in message_list["messages"]:
        assert message_dic.get("message") == "Ciallo"


def test_message_edit_empty_string():
    """ test the valid edit function when the message is blank """
    clear()
    user = auth_register("simple@example.com", "123456", "Hayden", "Jacobs")
    channel_id = channels_create(user.get("token"), "COMP1531", True)
    message1 = message_send(
        user.get("token"), channel_id.get("channel_id"), "Hello")

    temp = message1.get("message_id")
    message_edit(user.get("token"), message1.get("message_id"), "")
    message2 = message_send(
        user.get("token"), channel_id.get("channel_id"), "Hello")
    assert temp == message2.get("message_id")


def test_invalid_message_edit():
    """ test the wrong situation for message_edit """
    clear()
    user = auth_register("simple@example.com", "123456", "Hayden", "Jacobs")
    channel_id = channels_create(user.get("token"), "COMP1531", True)
    message1 = message_send(
        user.get("token"), channel_id.get("channel_id"), "Hello")

    user2 = auth_register("simple@example2.com", "123456", "Michael", "Jacobs")
    with pytest.raises(AccessError):
        message_edit(user2.get("token"), message1.get("message_id"), "Ciallo")


# test for message_react
def test_message_invalid_react_id():
    """ test invalid react_id situation for message_react """
    clear()
    user = auth_register("simple@example.com", "123456", "Hayden", "Jacobs")
    channel_id = channels_create(user.get("token"), "COMP1531", True)
    message1 = message_send(
        user.get("token"), channel_id.get("channel_id"), "Hello")

    with pytest.raises(InputError):
        message_react(user.get("token"), message1.get("message_id"), 2)


def test_message_react_not_exist():
    """test invalid message id for message_react"""
    clear()
    user = auth_register("simple@example.com", "123456", "Hayden", "Jacobs")
    channel_id = channels_create(user.get("token"), "COMP1531", True)
    message1 = message_send(
        user.get("token"), channel_id.get("channel_id"), "Hello")

    with pytest.raises(InputError):
        message_react(user.get("token"), message1.get("message_id") + 1, 1)


def test_message_react_already_exist():
    """test duplicate react situation for message_react"""
    clear()
    user = auth_register("simple@example.com", "123456", "Hayden", "Jacobs")
    channel_id = channels_create(user.get("token"), "COMP1531", True)
    message1 = message_send(
        user.get("token"), channel_id.get("channel_id"), "Hello")
    message_react(user.get("token"), message1.get("message_id"), 1)
    with pytest.raises(InputError):
        message_react(user.get("token"), message1.get("message_id"), 1)


def test_message_react_correct():
    """test correct situation for message_react"""
    clear()
    user = auth_register("simple@example.com", "123456", "Hayden", "Jacobs")
    user2 = auth_register("simple@example2.com", "123456", "Michael", "Jacobs")
    channel_id = channels_create(user.get("token"), "COMP1531", True)
    message_send(user.get("token"), channel_id.get("channel_id"), "Hello")
    message2 = message_send(
        user.get("token"), channel_id.get("channel_id"), "World")

    message_react(user.get("token"), message2.get("message_id"), 1)
    message_react(user2.get("token"), message2.get("message_id"), 1)

    info = channel_messages(user.get("token"), channel_id.get("channel_id"), 0)

    message_list = info["messages"]
    message_dict = message_list[0]
    react_list = message_dict["reacts"]

    assert user.get("u_id") in react_list[0]["u_ids"]
    assert user2.get("u_id") in react_list[0]["u_ids"]
    assert react_list[0]["is_this_user_reacted"]


def test_message_react_correct_long_list():
    """test correct situation for message_react with a long message list"""
    clear()
    user = auth_register("simple@example.com", "123456", "Hayden", "Jacobs")
    user2 = auth_register("simple@example2.com", "123456", "Michael", "Jacobs")
    channel_id = channels_create(user.get("token"), "COMP1531", True)
    channel_invite(
        user.get("token"),
        channel_id.get("channel_id"),
        user2.get("u_id"))

    for _ in range(100):
        last_message = message_send(user.get("token"), channel_id.get("channel_id"), "Hello")

    message_react(user.get("token"), last_message.get("message_id"), 1)

    info = channel_messages(user.get("token"), channel_id.get("channel_id"), 0)

    message_list = info["messages"]
    message_dict = message_list[0]
    react_list = message_dict["reacts"]

    assert user.get("u_id") in react_list[0]["u_ids"]
    assert react_list[0]["is_this_user_reacted"]


    info = channel_messages(user2.get("token"), channel_id.get("channel_id"), 0)
    message_list = info["messages"]
    message_dict = message_list[0]
    react_list = message_dict["reacts"]
    assert not react_list[0]["is_this_user_reacted"]


# test for message_unreact
def test_message_invalid_unreact_id():
    """ test invalid react_id situation for message_unreact """
    clear()
    user = auth_register("simple@example.com", "123456", "Hayden", "Jacobs")
    channel_id = channels_create(user.get("token"), "COMP1531", True)
    message1 = message_send(
        user.get("token"), channel_id.get("channel_id"), "Hello")
    message_react(user.get("token"), message1.get("message_id"), 1)
    with pytest.raises(InputError):
        message_unreact(user.get("token"), message1.get("message_id"), 2)


def test_message_unreact_not_exist():
    """ test invalid message_id situation for message_unreact """
    clear()
    user = auth_register("simple@example.com", "123456", "Hayden", "Jacobs")
    channel_id = channels_create(user.get("token"), "COMP1531", True)
    message1 = message_send(
        user.get("token"), channel_id.get("channel_id"), "Hello")
    message_react(user.get("token"), message1.get("message_id"), 1)
    with pytest.raises(InputError):
        message_unreact(user.get("token"), message1.get("message_id") + 1, 1)


def test_message_unreact_already_exist():
    """ test duplicate react situation for message_unreact """
    clear()
    user = auth_register("simple@example.com", "123456", "Hayden", "Jacobs")
    channel_id = channels_create(user.get("token"), "COMP1531", True)
    message1 = message_send(
        user.get("token"), channel_id.get("channel_id"), "Hello")
    with pytest.raises(InputError):
        message_unreact(user.get("token"), message1.get("message_id"), 1)


def test_message_unreact_correct():
    """ test correct situation for message_unreact """
    clear()
    user = auth_register("simple@example.com", "123456", "Hayden", "Jacobs")
    channel_id = channels_create(user.get("token"), "COMP1531", True)
    message_send(user.get("token"), channel_id.get("channel_id"), "Hello")
    message2 = message_send(
        user.get("token"), channel_id.get("channel_id"), "World")

    message_react(user.get("token"), message2.get("message_id"), 1)

    info = channel_messages(user.get("token"), channel_id.get("channel_id"), 0)

    message_list = info["messages"]
    message_dict = message_list[0]
    react_list = message_dict["reacts"]
    assert user.get("u_id") in react_list[0]["u_ids"]
    assert react_list[0]["is_this_user_reacted"]

    message_unreact(user.get("token"), message2.get("message_id"), 1)

    info = channel_messages(user.get("token"), channel_id.get("channel_id"), 0)

    message_list = info["messages"]
    message_dict = message_list[0]
    react_list = message_dict["reacts"]
    assert user.get("u_id") not in react_list[0]["u_ids"]
    assert not react_list[0]["is_this_user_reacted"]


def test_message_pin_not_exist():
    """ test invalid message id situation for message_pin """
    clear()
    user = auth_register("simple@example.com", "123456", "Hayden", "Jacobs")
    channel_id = channels_create(user.get("token"), "COMP1531", True)
    message1 = message_send(
        user.get("token"), channel_id.get("channel_id"), "Hello")

    with pytest.raises(InputError):
        message_pin(user.get("token"), message1.get("message_id") + 1)


def test_message_already_pin():
    """ test duplicate pin situation for message_pin """
    clear()
    user = auth_register("simple@example.com", "123456", "Hayden", "Jacobs")
    channel_id = channels_create(user.get("token"), "COMP1531", True)
    message1 = message_send(
        user.get("token"), channel_id.get("channel_id"), "Hello")

    message_pin(user.get("token"), message1.get("message_id"))

    with pytest.raises(InputError):
        message_pin(user.get("token"), message1.get("message_id"))


def test_message_pin_not_member():
    """ test not member situation for message_pin """
    clear()
    user = auth_register("simple@example.com", "123456", "Hayden", "Jacobs")
    channel_id = channels_create(user.get("token"), "COMP1531", True)
    message1 = message_send(
        user.get("token"), channel_id.get("channel_id"), "Hello")
    user2 = auth_register("simple2@example.com", "123456", "Hayden", "Jacobs")

    with pytest.raises(AccessError):
        message_pin(user2.get("token"), message1.get("message_id"))


def test_message_pin_not_owner():
    """ test not owner situation for message_pin """
    clear()
    user = auth_register("simple@example.com", "123456", "Hayden", "Jacobs")
    channel_id = channels_create(user.get("token"), "COMP1531", True)
    message1 = message_send(
        user.get("token"), channel_id.get("channel_id"), "Hello")
    user2 = auth_register("simple2@example.com", "123456", "Hayden", "Jacobs")

    channel_invite(user.get("token"), channel_id.get("channel_id"), user2.get("u_id"))

    with pytest.raises(AccessError):
        message_pin(user2.get("token"), message1.get("message_id"))


def test_message_unpin_not_exist():
    """ test invalid message id situation for message_unpin """
    clear()
    user = auth_register("simple@example.com", "123456", "Hayden", "Jacobs")
    channel_id = channels_create(user.get("token"), "COMP1531", True)
    message1 = message_send(
        user.get("token"), channel_id.get("channel_id"), "Hello")

    with pytest.raises(InputError):
        message_unpin(user.get("token"), message1.get("message_id") + 1)


def test_message_already_unpin():
    """ test duplicate pin situation for message_unpin """
    clear()
    user = auth_register("simple@example.com", "123456", "Hayden", "Jacobs")
    channel_id = channels_create(user.get("token"), "COMP1531", True)
    message1 = message_send(
        user.get("token"), channel_id.get("channel_id"), "Hello")

    message_pin(user.get("token"), message1.get("message_id"))
    message_unpin(user.get("token"), message1.get("message_id"))
    with pytest.raises(InputError):
        message_unpin(user.get("token"), message1.get("message_id"))


def test_message_unpin_not_member():
    """ test not member situation for message_unpin """
    clear()
    user = auth_register("simple@example.com", "123456", "Hayden", "Jacobs")
    channel_id = channels_create(user.get("token"), "COMP1531", True)
    message1 = message_send(
        user.get("token"), channel_id.get("channel_id"), "Hello")
    user2 = auth_register("simple2@example.com", "123456", "Hayden", "Jacobs")

    message_pin(user.get("token"), message1.get("message_id"))
    with pytest.raises(AccessError):
        message_unpin(user2.get("token"), message1.get("message_id"))


def test_message_unpin_not_owner():
    """ test not owner situation for message_unpin """
    clear()
    user = auth_register("simple@example.com", "123456", "Hayden", "Jacobs")
    channel_id = channels_create(user.get("token"), "COMP1531", True)
    message1 = message_send(
        user.get("token"), channel_id.get("channel_id"), "Hello")
    user2 = auth_register("simple2@example.com", "123456", "Hayden", "Jacobs")

    channel_invite(user.get("token"), channel_id.get("channel_id"), user2.get("u_id"))

    message_pin(user.get("token"), message1.get("message_id"))
    with pytest.raises(AccessError):
        message_unpin(user2.get("token"), message1.get("message_id"))


def test_message_pin_correct():
    """ test correct situation for message_pin """
    clear()
    user = auth_register("simple@example.com", "123456", "Hayden", "Jacobs")
    channel_id = channels_create(user.get("token"), "COMP1531", True)
    message_send(user.get("token"), channel_id.get("channel_id"), "Hello")

    message2 = message_send(
        user.get("token"), channel_id.get("channel_id"), "World")

    message_pin(user.get("token"), message2.get("message_id"))

    info = channel_messages(user.get("token"), channel_id.get("channel_id"), 0)

    message_list = info["messages"]
    message_dict = message_list[0]
    message_dict2 = message_list[1]
    is_pin2 = message_dict2["is_pinned"]
    is_pin = message_dict["is_pinned"]
    assert is_pin
    assert not is_pin2


def test_message_unpin_correct():
    """ test correct situation for message_unpin """
    clear()
    user = auth_register("simple@example.com", "123456", "Hayden", "Jacobs")
    channel_id = channels_create(user.get("token"), "COMP1531", True)
    message_send(user.get("token"), channel_id.get("channel_id"), "Hello")



    message2 = message_send(
        user.get("token"), channel_id.get("channel_id"), "World")


    message_pin(user.get("token"), message2.get("message_id"))
    info = channel_messages(user.get("token"), channel_id.get("channel_id"), 0)

    message_list = info["messages"]
    message_dict = message_list[0]
    message_dict2 = message_list[1]
    is_pin2 = message_dict2["is_pinned"]
    is_pin = message_dict["is_pinned"]
    assert is_pin
    assert not is_pin2

    message_unpin(user.get("token"), message2.get("message_id"))

    info = channel_messages(user.get("token"), channel_id.get("channel_id"), 0)
    message_list = info["messages"]
    message_dict = message_list[0]
    is_pin = message_dict["is_pinned"]
    assert not is_pin
