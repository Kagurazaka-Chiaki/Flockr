# -*- coding: utf-8 -*-
""" Implementation of tests for auth.py"""
import pytest

from auth import auth_register, auth_login, auth_logout
from other import clear
from error import InputError


# these funtions test the edge case (InputError) for auth_register, auth_login, auth_logout
def test_auth_register_invaild_email():
    """ test for invalid_email(InputError) situtation for auth_register """
    with pytest.raises(InputError):
        auth_register("simpleexample.org", "123456", "AAA", "BBB")


def test_auth_register_first_name_short():
    """ test for short_first_name(InputError) situtation for auth_register"""
    with pytest.raises(InputError):
        auth_register("simple@example.org", "123456", "", "BBB")


def test_auth_register_last_name_short():
    """ test for short_last_name(InputError) situtation for auth_register"""
    with pytest.raises(InputError):
        auth_register("validemail@exaple.org", "123456", "AAAA", "")


def test_auth_register_firt_name_too_long():
    """ test for short_last_name(InputError) situtation for auth_register"""
    with pytest.raises(InputError):
        auth_register("validemail@exaple.org", "123456",
                      "this_is_too_long_name_which_has_more_than_fifty_characters", "BBB")


def test_auth_register_last_name_too_long():
    """ test for long_last_name(InputError) situtation for auth_register"""
    with pytest.raises(InputError):
        auth_register("validemail@exaple.org", "123456", "AAAA",
                      "this_is_too_long_name_which_has_more_than_fifty_characters")


def test_auth_register_short_password():
    """ test for short_password(InputError) situtation for auth_register"""
    with pytest.raises(InputError):
        auth_register("simple@example.org", "123", "AAA", "BBB")


def test_auth_register_used_email():
    """ test for uesd_email(InputError) situtation for auth_register"""
    auth_register("thisisusedemail@example.org", "123456", "AAA", "BBB")
    with pytest.raises(InputError):
        auth_register("thisisusedemail@example.org", "123456", "AAA", "BBB")
    clear()


def test_auth_login_invalid_email():
    """ test for invalid_email(InputError) situtation for auth_login"""
    with pytest.raises(InputError):
        auth_login("ankitrai326.com", "aaaaaaa")


def test_auth_login_not_user_email():
    """ test for email which is not belong to the user (InputError) situtation for auth_login"""
    with pytest.raises(InputError):
        auth_login("bill333@Amazon.com", "aaaaaaa")


def test_auth_login_incorrect_password():
    """ test for incorrect_password(InputError) situtation for auth_login"""
    auth_register("tom444@ins.com", "correctpassword", "AAA", "BBB")
    with pytest.raises(InputError):
        auth_login("tom444@ins.com", "incorrectpassword")
    clear()


def test_auth_logout_incorrect_token():
    """ test for incorrect_token(InputError) situtation for auth_logout"""
    assert not auth_logout('invalid_token').get("is_success")


# these functions test the successful case for auth_register, auth_login, auth_logout
def test_auth_register_success():
    """ test whether auth_register can work correctly or not"""
    password = 'thisisvalidpassword'
    info_one = auth_register("validemailtom@ins.com", password, "Tom", "David")
    info_two = auth_register("validemailjulia@ins.com",
                             password, "Kai", "Julia")
    info_three = auth_register(
        "validemailmeiyu@ins.com", password, "Marry", "Yu")

    # if the auth_register work correctly, the u_ids of these two users are different
    assert info_one['u_id'] != info_two['u_id']
    assert info_two['u_id'] != info_three['u_id']
    assert info_three['u_id'] != info_one['u_id']
    # if the auth_register work correctly, we can login and logout the user

    auth_login("validemailtom@ins.com", password)
    auth_login("validemailjulia@ins.com", password)
    # after login in , then we can logout the user we test whether
    # the auth_register return the correct token
    result_login_one = auth_logout(info_one['token'])
    result_login_two = auth_logout(info_two['token'])
    assert result_login_one['is_success']
    assert result_login_two['is_success']

    clear()


def test_auth_login_success():
    """ test whether auth_login can work correctly or not"""
    password = 'thisisvalidpassword'
    auth_register("validemailtom@ins.com", password, "Tom", "David")
    auth_register("validemailjulia@ins.com", password, "Kai", "Julia")
    auth_register("validemailmeiyu@ins.com", password, "Marry", "Yu")

    # if the auth_register work correctly, we can login and logout the user
    info_one = auth_login("validemailtom@ins.com", password)
    info_two = auth_login("validemailjulia@ins.com", password)
    info_three = auth_login("validemailmeiyu@ins.com", password)

    assert info_one['u_id'] != info_two['u_id']
    assert info_two['u_id'] != info_three['u_id']
    assert info_three['u_id'] != info_one['u_id']
    # after login in , then we can logout the user
    # we test whether the auth_login return the correct token
    result_login_one = auth_logout(info_one['token'])
    result_login_two = auth_logout(info_two['token'])
    assert result_login_one['is_success']
    assert result_login_two['is_success']

    clear()


def test_auth_logout_success():
    """ test whether auth_logout can work correctly or not"""
    password = 'thisisvalidpassword'
    auth_register("validemailtom@ins.com", password, "Tom", "David")
    auth_register("validemailjulia@ins.com", password, "Kai", "Julia")
    auth_register("validemailmeiyu@ins.com", password, "Marry", "Yu")

    info_one = auth_login("validemailtom@ins.com", password)
    info_two = auth_login("validemailjulia@ins.com", password)

    result_login_one = auth_logout(info_one['token'])
    result_login_two = auth_logout(info_two['token'])
    # after login in , then we can logout the user
    # we test whether the auth_logout return the correct form
    assert result_login_one['is_success']
    assert result_login_two['is_success']

    clear()
