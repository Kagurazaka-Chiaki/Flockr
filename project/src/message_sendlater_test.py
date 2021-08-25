# -*- coding: utf-8 -*-
""" HTTP tests for message_sendlater.py """

from random import randint, sample, choice
from string import ascii_letters, digits
import pytest

from auth import auth_register
from channel import channel_messages
from channels import channels_create
from message import message_sendlater

from error import InputError, AccessError
from other import clear
from datetime import timezone, datetime


def test_valid_message_sendlater():
    user_1 = auth_register("simple@example.com", "123456", "Hayden", "Jacobs")

    user_2 = auth_register("simple@example.org",
                           "123456", "Ian", "Thorvaldson")

    info = channels_create(user_1.get("token"), "COMP1531", True)

    channels_create(user_2.get("token"), "COMP2521", True)

    random_string = ''.join(sample(ascii_letters + digits, randint(2, 5)))

    interval = datetime.now(timezone.utc).timestamp() + 1

    with pytest.raises(InputError):
        message_sendlater(
            user_1.get("token"), info.get("channel_id"),
            random_string * 1200, interval
        )

    with pytest.raises(AccessError):
        message_sendlater(
            user_2.get("token"), info.get("channel_id"),
            random_string, interval
        )

    with pytest.raises(InputError):
        message_sendlater(
            user_1.get("token"), info.get("channel_id") + randint(10, 20),
            random_string, interval
        )

    with pytest.raises(InputError):
        message_sendlater(
            user_1.get("token"), info.get("channel_id"),
            random_string, interval - 10
        )

    message_id = message_sendlater(
        user_1.get("token"), info.get("channel_id"),
        random_string, interval
    )

    dict_message = channel_messages(
        user_1.get("token"), info.get("channel_id"), 0
    )
    assert dict_message["end"] == -1

    message_list = dict_message.get("messages")

    assert message_list[0].get("message_id") == message_id.get("message_id")
