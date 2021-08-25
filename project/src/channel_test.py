# -*- coding: utf-8 -*-
""" Tests for channel.py """

from random import randint
import pytest

from auth import auth_register

from channel import channel_invite
from channel import channel_details, channel_messages
from channel import channel_addowner, channel_removeowner
from channel import channel_join, channel_leave

from channels import channels_create, channels_list

from message import message_send

from error import InputError, AccessError
from other import clear


def test_channel_invite_invalid_member():
    """ create one user and one invite duplicated user """
    clear()

    user1 = auth_register("simple@example.com", "123456", "Hayden", "Jacobs")
    cid = channels_create(user1.get("token"), "COMP1531", True)
    with pytest.raises(AccessError):
        channel_invite(
            user1.get("token"),
            cid.get("channel_id"),
            user1.get("u_id")
        )


def test_channel_invite_invalid_channel_id():
    """create two users and one invite another within a wrong channel id"""
    clear()
    user1 = auth_register("simple@example.com", "123456", "Hayden", "Jacobs")
    cid = channels_create(user1.get("token"), "COMP1531", True)
    user2 = auth_register("simple@example.org", "123456", "Ian", "Thorvaldson")
    random_number = randint(1, 100)
    wrong = cid.get("channel_id") + random_number
    with pytest.raises(InputError):
        channel_invite(user1.get("token"), wrong, user2.get("u_id"))


def test_channel_invite_invalid_user():
    """create two users and one invite another within a wrong user id"""
    clear()
    user1 = auth_register("simple@example.com", "123456", "Hayden", "Jacobs")
    cid = channels_create(user1.get("token"), "COMP1531", True)
    user2 = auth_register("simple@example.org", "123456", "Ian", "Thorvaldson")
    random_number = randint(1, 100)
    wrong = user2.get("u_id") + random_number
    with pytest.raises(InputError):
        channel_invite(user1.get("token"), cid.get("channel_id"), wrong)


def test_invalid_member():
    """create two users and one invite another within a wrong token"""
    clear()
    user1 = auth_register("simple@example.com", "123456", "Hayden", "Jacobs")
    cid = channels_create(user1.get("token"), "COMP1531", True)
    user2 = auth_register("simple@example.org", "123456", "Matthew", "Perry")
    with pytest.raises(AccessError):
        channel_invite(user2.get("token"), cid.get("channel_id"),
                       user2.get("u_id"))


def test_channel_invite_valid():
    """create two users and one invite another valid """
    clear()
    user1 = auth_register("simple@example.com", "123456", "Hayden", "Jacobs")
    cid = channels_create(user1.get("token"), "COMP1531", True)
    user2 = auth_register("simple@example.org", "123456", "Ian", "Thorvaldson")
    channel_invite(user1.get("token"), cid.get(
        "channel_id"), user2.get("u_id"))
    detail = channel_details(user1.get("token"), cid.get("channel_id"))
    u_list = list(map(lambda x: x.get("u_id"), detail.get("all_members")))
    assert user2.get("u_id") in u_list

# Test for channel_details()
def test_channel_details_error():
    """
    test the error condition for function channel_detail
    """
    clear()
    # enter the invalid channel_id
    with pytest.raises(InputError):
        channel_details("Mingyuan_cui#2", 3)

    with pytest.raises(InputError):
        channel_details("Haotian_lyu#1", 4)

    with pytest.raises(InputError):
        channel_details("abc", 5)

    # enter the token not belong to this channel
    dic_jackey = auth_register("jackeychen@gmail.com",
                               "jackeychen",
                               "Jackey",
                               "Chen")
    token_test = dic_jackey.get("token")
    name_test = "channel_jackey"
    dic_channel = channels_create(token_test, name_test, True)
    channel_id_test = dic_channel.get("channel_id")

    dic_clearlove = auth_register("clearlove@gmail.com",
                                  "clearlove7",
                                  "Clear",
                                  "Love")
    token_wrong = dic_clearlove.get("token")
    name_wrong = "channel_clearlove"
    dic_channel_wrong = channels_create(token_wrong, name_wrong, True)
    channel_id_wrong = dic_channel_wrong.get("channel_id")

    with pytest.raises(AccessError):
        channel_details(token_test, channel_id_wrong)

    with pytest.raises(AccessError):
        channel_details(token_wrong, channel_id_test)

    with pytest.raises(AccessError):
        channel_details("abc", channel_id_test)

    with pytest.raises(AccessError):
        channel_details("abc", channel_id_wrong)

    clear()


def test_channel_details_correct():
    """
    test the correct condition for function channel_details
    """
    # builing data structure
    dic_jackey = auth_register(
        "jackeychen@gmail.com", "jackeychen", "Jackey", "Chen"
    )
    token_test = dic_jackey.get("token")
    u_id_test = dic_jackey.get("u_id")
    name_test = "channel_jackey"
    dic_channel = channels_create(token_test, name_test, True)
    channel_id_test = dic_channel.get("channel_id")

    dic_clearlove = auth_register(
        "clearlove@gmail.com", "clearlove7", "Clear", "Love"
    )
    token_wrong = dic_clearlove.get("token")
    u_id_wrong = dic_clearlove.get("u_id")
    name_wrong = "channel_clearlove"
    dic_channel_wrong = channels_create(token_wrong, name_wrong, True)
    channel_id_wrong = dic_channel_wrong.get("channel_id")

    # test correct output of channel_detail
    dic_right = channel_details(token_test, channel_id_test)
    assert dic_right.get("name") == name_test
    assert(dic_right.get("owner_members") == [
        {
            'u_id': u_id_test,
            'name_first': "Jackey",
            'name_last': 'Chen',
            "profile_img_url": ""
        }
    ])
    assert(dic_right.get("all_members") == [
        {
            'u_id': u_id_test,
            'name_first': "Jackey",
            'name_last': 'Chen',
            "profile_img_url": ""
        }
    ])
    assert(channel_details(token_test, channel_id_test) == {
        'name': name_test,
        'owner_members': [
            {
                'u_id': u_id_test,
                'name_first': "Jackey",
                'name_last': 'Chen',
                "profile_img_url": ""
            },
        ],
        'all_members': [
            {
                'u_id': u_id_test,
                'name_first': "Jackey",
                'name_last': 'Chen',
                "profile_img_url": ""
            },
        ],
    })

    assert(channel_details(token_wrong, channel_id_wrong) == {
        'name': name_wrong,
        'owner_members': [
            {
                'u_id': u_id_wrong,
                'name_first': 'Clear',
                'name_last': 'Love',
                "profile_img_url": ""
            }
        ],
        'all_members': [
            {
                'u_id': u_id_wrong,
                'name_first': 'Clear',
                'name_last': 'Love',
                "profile_img_url": ""
            }
        ],
    })


# Test for channel_message()
def test_channel_message_error():
    """
    test error condition for function channel_message
    """
    # enter the invalid channel
    clear()
    with pytest.raises(InputError):
        channel_messages("Haotian_lyu#1", 3, 0)

    with pytest.raises(InputError):
        channel_messages("Haotian_lyu#1", 1, 0)

    with pytest.raises(InputError):
        channel_messages("Mingyuan_cui#2", 2, 0)

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

    # enter the token that not in channel
    with pytest.raises(AccessError):
        channel_messages(token_test, channel_id_wrong, 0)

    with pytest.raises(AccessError):
        channel_messages(token_wrong, channel_id_test, 100)

    with pytest.raises(AccessError):
        channel_messages("abc", channel_id_test, 0)

    with pytest.raises(AccessError):
        channel_messages("abc", channel_id_wrong, 0)

    # enter start that bigger than total
    with pytest.raises(InputError, match="Invalid start"):
        channel_messages(token_test, channel_id_test, 1)

    with pytest.raises(InputError, match="Invalid start"):
        channel_messages(token_wrong, channel_id_wrong, 1)

    with pytest.raises(InputError, match="Invalid start"):
        channel_messages(token_test, channel_id_test, 2)

    with pytest.raises(InputError, match="Invalid start"):
        channel_messages(token_wrong, channel_id_wrong, 2)


def test_channel_message_correct():
    """test correct condition for channel_message"""
    clear()
    # buliding data structure
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

    for i in dict_message["messages"]:
        if i.get("message_id") == message_id1:
            assert i["message"] == "all we fight for"

    for i in dict_message["messages"]:
        if i.get("message_id") == message_id2:
            assert i["message"] == "deep ward"

    j = 0
    while j < 51:
        message_send(token_wrong, channel_id_wrong, "all")
        j = j + 1

    dict_message = channel_messages(token_wrong, channel_id_wrong, 0)
    assert dict_message["end"] == 50

    dict_message = channel_messages(token_wrong, channel_id_wrong, 1)
    assert dict_message["end"] == 51


# Test for channel_leave()
def test_channel_leave_error():
    """test the situation in which the channel_leave function has an InputError"""
    clear()
    inform = auth_register("simple@example.com", "123456", "Hayden", "Jacobs")
    with pytest.raises(InputError, match="nonexistent Channel ID"):
        channel_leave(inform["token"], -1)

    # test the situation in which the channel_leave function has an AccessError
    clear()
    inform = auth_register("simple@example.com", "123456", "Hayden", "Jacobs")
    channels_create(inform["token"], "channel_test", "True")
    inform2 = auth_register("simple1@example.com",
                            "123456", "Sayden", "Jacobs")
    with pytest.raises(AccessError, match="You are not in this channel"):
        channel_leave(inform2["token"], 1)


def test_channel_leave():
    """The the success situation for the channel_leave"""
    clear()
    inform = auth_register("simple@example.com", "123456", "Hayden", "Jacobs")
    inform2 = auth_register("simple1@example.com",
                            "123456", "Michael", "Jacobs")

    result = channels_create(inform["token"], "channel_test", True)
    result2 = channels_create(inform2["token"], "Comp1531", True)
    result3 = channels_create(inform["token"], "COMP", True)

    channel_join(inform2["token"], result["channel_id"])
    channel_join(inform2["token"], result3["channel_id"])

    channel_leave(inform2["token"], result["channel_id"])
    channellist = channels_list(inform2["token"])
    u_list = list(map(lambda x: x["channel_id"], channellist["channels"]))

    assert result["channel_id"] not in u_list
    assert result2["channel_id"] in u_list
    assert result3["channel_id"] in u_list

    channel_leave(inform2["token"], result2["channel_id"])

    channellist = channels_list(inform2["token"])
    u_list = list(map(lambda x: x["channel_id"], channellist["channels"]))

    assert result["channel_id"] not in u_list
    assert result2["channel_id"] not in u_list
    assert result3["channel_id"] in u_list


# Test for channel_join()
def test_channel_join_error():
    """test the situation in which the channel_join function has an InputError"""
    clear()
    inform = auth_register("simple@example.com", "123456", "Hayden", "Jacobs")
    with pytest.raises(InputError, match="nonexistent Channel ID"):
        channel_join(inform["token"], -1)

    # test the situation in which the channel_join function has an AccessError
    clear()
    inform = auth_register("simple@example.com", "123456", "Hayden", "Jacobs")
    result = channels_create(inform["token"], "channel_test", False)
    inform2 = auth_register("simple1@example.com",
                            "123456", "Michael", "Jacobs")
    with pytest.raises(AccessError, match="This channel is private"):
        channel_join(inform2["token"], result["channel_id"])


def test_channel_join():
    """The the success situation for the channel_join"""

    clear()
    inform = auth_register("simple@example.com", "123456", "Hayden", "Jacobs")
    result = channels_create(inform["token"], "channel_test", True)
    inform2 = auth_register("simple1@example.com",
                            "123456", "Michael", "Jacobs")
    channel_join(inform2["token"], result["channel_id"])
    channellist = channels_list(inform2["token"])
    assert(channellist == {'channels': [{'channel_id': result["channel_id"],
                                         'name': 'channel_test'}]})


# Test for channel_addowner()
def test_valid_addowner():
    """
    Test that the addowner function is implemented correctly
    """
    clear()
    reg1 = auth_register("simple@example.org", "123456", "sh", "LA")
    reg2 = auth_register("simple2@gamil.com", "123456", "Tony", "Man")
    reg3 = auth_register("simple@mail.com", "easyPass", "Shin", "On")
    reg4 = auth_register("sets@exmaple.org", "pass222", "sets", "lol")

    info = channels_create(reg1["token"], "1531", True)

    channel_addowner(reg1["token"], info["channel_id"], reg2["u_id"])
    channel_addowner(reg2["token"], info["channel_id"], reg3["u_id"])
    channel_addowner(reg3["token"], info["channel_id"], reg4["u_id"])


def test_addowner_invalid_channel_id():
    """
    Test that will error occur when the channel_id is invalid for addowner
    """
    clear()
    reg1 = auth_register("simple@example.org", "123456", "sh", "LA")
    reg2 = auth_register("simple2@gamil.com", "123456", "Tony", "Man")

    with pytest.raises(InputError):
        channel_addowner(reg1["token"], -1, reg2["u_id"])

    with pytest.raises(InputError):
        channel_addowner(reg1["token"], 0, reg2["u_id"])

    with pytest.raises(InputError):
        channel_addowner(reg1["token"], 4, reg2["u_id"])

    with pytest.raises(InputError):
        channel_addowner(reg1["token"], "4", reg2["u_id"])

    with pytest.raises(InputError):
        channel_addowner(reg1["token"], "abcd", reg2["u_id"])

    with pytest.raises(InputError):
        channel_addowner(reg1["token"], "?????", reg2["u_id"])


def test_user_is_already_an_owner():
    """
    Test that will error occur if the user is already an owner for addowner
    """
    clear()
    reg1 = auth_register("simple@example.org", "123456", "sh", "LA")
    reg2 = auth_register("simple2@gamil.com", "123456", "Tony", "Man")

    info1 = channels_create(reg1["token"], "1531", True)
    info2 = channels_create(reg2["token"], "Comp", True)

    channel_addowner(reg1["token"], info1["channel_id"], reg2["u_id"])
    channel_addowner(reg2["token"], info2["channel_id"], reg1["u_id"])

    with pytest.raises(InputError):
        channel_addowner(reg1["token"], info1["channel_id"], reg1["u_id"])

    with pytest.raises(InputError):
        channel_addowner(reg2["token"], info1["channel_id"], reg1["u_id"])

    with pytest.raises(InputError):
        channel_addowner(reg2["token"], info2["channel_id"], reg1["u_id"])

    with pytest.raises(InputError):
        channel_addowner(reg2["token"], info2["channel_id"], reg2["u_id"])


def test_addowner_auth_user_is_not_owner():
    """
    Test that will error occur if authorised user is not owner for addowner
    """
    clear()
    reg1 = auth_register("simple@example.org", "123456", "sh", "LA")
    reg2 = auth_register("simple2@gamil.com", "123456", "Tony", "Man")
    reg3 = auth_register("simple@mail.com", "easyPass", "Shin", "On")

    info1 = channels_create(reg1["token"], "1531", True)
    info2 = channels_create(reg2["token"], "Comp", True)

    with pytest.raises(AccessError):
        channel_addowner(reg2["token"], info1["channel_id"], reg3["u_id"])

    with pytest.raises(AccessError):
        channel_addowner(reg3["token"], info2["channel_id"], reg1["u_id"])

    with pytest.raises(AccessError):
        channel_addowner("", info2["channel_id"], reg3["u_id"])

    with pytest.raises(AccessError):
        channel_addowner("ggwp", info2["channel_id"], reg3["u_id"])

    with pytest.raises(AccessError):
        channel_addowner(2, info1["channel_id"], reg2["u_id"])

# Test for channel_removeowner()


def test_valid_removeowner():
    """
    Test the removeowner function is implemented correctly
    """
    clear()
    reg1 = auth_register("simple@example.org", "123456", "sh", "LA")
    reg2 = auth_register("simple2@gamil.com", "123456", "Tony", "Man")
    reg3 = auth_register("simple@mail.com", "easyPass", "Shin", "On")
    reg4 = auth_register("sets@exmaple.org", "pass222", "sets", "lol")

    channels_create(reg1["token"], "1531", True)
    channels_create(reg2["token"], "Testing", True)
    info3 = channels_create(reg1["token"], "Comp1531", True)

    channel_addowner(reg1["token"], info3["channel_id"], reg2["u_id"])
    channel_addowner(reg1["token"], info3["channel_id"], reg3["u_id"])
    channel_addowner(reg1["token"], info3["channel_id"], reg4["u_id"])

    channel_removeowner(reg4["token"], info3["channel_id"], reg2["u_id"])
    channel_removeowner(reg4["token"], info3["channel_id"], reg1["u_id"])

    detail = channel_details(reg1.get("token"), info3.get("channel_id"))
    u_list = list(map(lambda x: x.get("u_id"), detail.get("owner_members")))
    assert reg2.get("u_id") not in u_list
    assert reg1.get("u_id") not in u_list


def test_removeowner_invalid_channel_id():
    """
    Test that will error occur if channel_id is invalid for removeowner
    """
    clear()
    reg1 = auth_register("simple@example.org", "123456", "sh", "LA")
    reg2 = auth_register("simple2@gamil.com", "123456", "Tony", "Man")

    with pytest.raises(InputError):
        channel_removeowner(reg1["token"], 0, reg2["u_id"])

    with pytest.raises(InputError):
        channel_removeowner(reg1["token"], 5, reg2["u_id"])

    with pytest.raises(InputError):
        channel_removeowner(reg1["token"], -2, reg2["u_id"])

    with pytest.raises(InputError):
        channel_removeowner(reg1["token"], ">>>>@", reg2["u_id"])

    with pytest.raises(InputError):
        channel_removeowner(reg1["token"], "4l", reg2["u_id"])


def test_user_is_already_not_an_owner():
    """
    Test that will error occur if user is not an owner for removeowner
    """
    clear()
    reg1 = auth_register("simple@example.org", "123456", "sh", "LA")
    reg2 = auth_register("simple2@gamil.com", "123456", "Tony", "Man")

    info1 = channels_create(reg1["token"], "1531", True)
    info2 = channels_create(reg2["token"], "Comp", True)

    with pytest.raises(InputError):
        channel_removeowner(reg1["token"], info1["channel_id"], reg2["u_id"])

    with pytest.raises(InputError):
        channel_removeowner(reg2["token"], info2["channel_id"], reg1["u_id"])


def test_removeowner_auth_user_is_not_owner():
    """
    Test that will error occur if authorised user is not owner for removeowner
    """
    clear()
    reg1 = auth_register("simple@example.org", "123456", "sh", "LA")
    reg2 = auth_register("simple2@gamil.com", "123456", "Tony", "Man")
    reg3 = auth_register("simple@mail.com", "easyPass", "Shin", "On")

    info1 = channels_create(reg1["token"], "1531", True)
    info2 = channels_create(reg2["token"], "Comp", True)

    with pytest.raises(AccessError):
        channel_removeowner(reg3["token"], info1["channel_id"], reg1["u_id"])

    with pytest.raises(AccessError):
        channel_removeowner("", info2["channel_id"], reg2["u_id"])

    with pytest.raises(AccessError):
        channel_removeowner(reg3["token"], info2["channel_id"], reg2["u_id"])

    with pytest.raises(AccessError):
        channel_removeowner(2, info2["channel_id"], reg2["u_id"])
