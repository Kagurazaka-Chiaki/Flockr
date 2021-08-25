"""implement user_test.py"""

import pytest

from auth import auth_register
from channels import channels_create

from user import user_profile
from user import user_profile_setname
from user import user_profile_setemail
from user import user_profile_sethandle
from user import user_profile_uploadphoto

from error import InputError, AccessError
from other import clear

BLACK_HOLE_JPG_URL = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Black_hole_-_Messier_87_crop_max_res.jpg/260px-Black_hole_-_Messier_87_crop_max_res.jpg"
BLACK_HOLE_PNG_URL = "https://storage.googleapis.com/effective-might-295307.appspot.com/BlackHole.png"


def test_user_profile_invalid_u_id():
    """this will test invalid u_id"""
    clear()
    info = auth_register("validemailtom@ins.com",
                         "thisisvalidpassword", "Tom", "David")
    with pytest.raises(InputError):
        user_profile(info["token"], 108)
    clear()


def test_user_profile_invalid_token():
    """this will test invalid token"""
    clear()
    info = auth_register("validemail@ins.com",
                         "thisisvalidpassword", "Julia", "David")
    with pytest.raises(AccessError):
        user_profile("invalidtooken", info["u_id"])
    clear()


def test_user_profile_correct():
    """ this will test whether user_profile can work or not"""
    clear()
    info = auth_register("jackeychen@gmail.com",
                         "jackeychen", "Jackey", "Chen")
    token_test = info.get("token")
    id_test = info.get("u_id")

    dict_profile = user_profile(token_test, id_test)
    user_dict = dict_profile["user"]

    assert user_dict["u_id"] == id_test
    assert user_dict["name_first"] == "Jackey"
    assert user_dict["name_last"] == "Chen"
    assert user_dict["email"] == "jackeychen@gmail.com"
    clear()


def test_user_profile_set_invalid_name_first():
    """ this will test name_first is not between 1 and 50 characters inclusively in length"""
    clear()
    info = auth_register("validemail@ins.com",
                         "thisisvalidpassword", "Julia", "David")
    # short first name
    with pytest.raises(InputError):
        user_profile_setname(info["token"], "", "valid_last_name")
    # long first name
    with pytest.raises(InputError):
        user_profile_setname(info["token"],
                             "this_is_not_a_valid_first_name_because_it_is_too_long",
                             "valid_last_name")
    clear()


def test_user_profile_set_invalid_name_last():
    """ this will test name_last is not between 1 and 50 characters inclusively in length"""
    clear()
    info = auth_register("validemail@ins.com",
                         "thisisvalidpassword", "Julia", "David")
    # short last name
    with pytest.raises(InputError):
        user_profile_setname(info["token"], "valid_first_name", "")
    # long first name
    with pytest.raises(InputError):
        user_profile_setname(info["token"], "valid_first_name",
                             "this_is_not_a_valid_last_name_because_it_is_too_long")
    clear()


def test_user_profile_setname_invalid_token():
    """this will test invalid token"""
    clear()
    auth_register("validemail@ins.com",
                  "thisisvalidpassword", "Julia", "David")
    with pytest.raises(InputError):
        user_profile_setname("not_invalid", "valid_first", "valid_last")
    clear()


def test_user_profile_setname_correct():
    """ this will test whether user_profile_setname can work or not"""
    clear()
    dic_jackey = auth_register("addcdee@gmail.com",
                               "jackeychen", "Jackey", "Chen")
    dic_jackey = auth_register("jackeychen@gmail.com",
                               "jackeychen", "Jackey", "Chen")
    token_test = dic_jackey.get("token")
    id_test = dic_jackey.get("u_id")

    user_profile_setname(token_test, "qwerdf", "abcde")

    dict_profile = user_profile(token_test, id_test)
    user_dict = dict_profile["user"]

    assert user_dict["u_id"] == id_test
    assert user_dict["name_first"] == "qwerdf"
    assert user_dict["name_last"] == "abcde"
    assert user_dict["email"] == "jackeychen@gmail.com"

    clear()


def test_user_profile_setemail_invalid_email():
    """ this will test Email entered is not a valid email """
    clear()
    info = auth_register("validemailtom@ins.com",
                         "thisisvalidpassword", "Tom", "David")
    with pytest.raises(InputError):
        user_profile_setemail(info["token"], "invalid")
    clear()


def test_user_profile_setemail_used_email():
    """ this will test Email address is already being used by another user """
    clear()
    password = 'thisisvalidpassword'
    auth_register("thisisusedemail@used.com", password, "Tom", "David")
    info = auth_register("validemailjulia@ins.com", password, "Kai", "Julia")
    with pytest.raises(InputError):
        user_profile_setemail(info["token"], "thisisusedemail@used.com")
    clear()


def test_user_profile_setemail_invalid_token():
    """this will test invalid token"""
    clear()
    with pytest.raises(InputError):
        user_profile_setemail("invalid", "jackeychen@gmail.com")


def test_user_profile_setemail_correct():
    """ this will test whether user_profile_setemail can work or not"""
    clear()
    dic_jackey = auth_register("abcedfg@gmail.com",
                               "jackeychen", "Jackey", "Chen")
    dic_jackey = auth_register("jackeychen@gmail.com",
                               "jackeychen", "Jackey", "Chen")
    token_test = dic_jackey.get("token")
    id_test = dic_jackey.get("u_id")

    user_profile_setemail(token_test, "clearlove@gmail.com")

    dict_profile = user_profile(token_test, id_test)
    user_dict = dict_profile["user"]

    assert user_dict["u_id"] == id_test
    assert user_dict["name_first"] == "Jackey"
    assert user_dict["name_last"] == "Chen"
    assert user_dict["email"] == "clearlove@gmail.com"
    clear()


def test_user_profile_sethandle_invalid_token():
    """ this will test invalid token"""
    clear()
    dic_jackey = auth_register("jackeychen@gmail.com",
                               "jackeychen", "Jackey", "Chen")
    token_jackey = dic_jackey.get("token")
    user_profile_sethandle(token_jackey, "jackeychen7")

    with pytest.raises(InputError):
        user_profile_sethandle("invalid_token", "clearlove7")
    clear()


def test_user_profile_sethandle_invalid_handle():
    """ this will test invalid handle"""
    clear()
    dic_jackey = auth_register("jackeychen@gmail.com",
                               "jackeychen", "Jackey", "Chen")
    token_test = dic_jackey.get("token")

    # test invalid handle string
    handle_invalid = ""
    with pytest.raises(InputError):
        user_profile_sethandle(token_test, handle_invalid)

    i = 0
    while i <= 21:
        handle_invalid += "a"
        i = i + 1

    with pytest.raises(InputError):
        user_profile_sethandle(token_test, handle_invalid)
    clear()


def test_user_profile_sethandle_used_handle():
    """ this will test used_handle"""
    # test already used handle
    clear()
    dic_jackey = auth_register("jackeychen@gmail.com",
                               "jackeychen", "Jackey", "Chen")
    token_jackey = dic_jackey.get("token")

    dic_clearlove = auth_register("clearlove@gmail.com",
                                  "clearlove7", "Clear", "Love")
    token_clear = dic_clearlove.get("token")

    user_profile_sethandle(token_clear, "clearlove7")

    with pytest.raises(InputError):
        user_profile_sethandle(token_jackey, "clearlove7")
    clear()


def test_user_profile_sethandle_correct():
    """ this will test whether user_profile_sethandle can work or not"""
    clear()
    dic_jackey = auth_register("jackeychen@gmail.com",
                               "jackeychen", "Jackey", "Chen")
    token_test = dic_jackey.get("token")
    id_test = dic_jackey.get("u_id")

    user_profile_sethandle(token_test, "clearlove7")

    dict_profile = user_profile(token_test, id_test)
    user_dict = dict_profile["user"]

    assert user_dict["u_id"] == id_test
    assert user_dict["name_first"] == "Jackey"
    assert user_dict["name_last"] == "Chen"
    assert user_dict["email"] == "jackeychen@gmail.com"
    assert user_dict["handle_str"] == "clearlove7"
    clear()


def test_invalid_upload_photo_invalid_token():
    """ Test for upload_photo_invalid_token """
    clear()
    auth_register("simple@example.com", "123456", "Hayden", "Jacobs")
    with pytest.raises(InputError):
        user_profile_uploadphoto("user_1.get(\"token\")", BLACK_HOLE_JPG_URL, 50, 50, 200, 200)


def test_invalid_upload_photo_invalid_url():
    """ Test for upload_photo_invalid_url """
    clear()
    user_1 = auth_register("simple@example.com", "123456", "Hayden", "Jacobs")
    with pytest.raises(InputError):
        user_profile_uploadphoto(user_1.get("token"), "http://BLACK_HOLE_JPG_URL", 50, 50, 200, 200)


def test_invalid_upload_photo_invalid_image():
    """ Test for upload_photo_invalid_image """
    clear()
    user_1 = auth_register("simple@example.com", "123456", "Hayden", "Jacobs")
    with pytest.raises(InputError):
        user_profile_uploadphoto(user_1.get("token"), BLACK_HOLE_PNG_URL, 50, 50, 200, 200)


def test_invalid_upload_photo_invalid_size():
    """ Test for upload_photo_invalid_size """
    clear()
    user_1 = auth_register("simple@example.com", "123456", "Hayden", "Jacobs")
    with pytest.raises(InputError):
        user_profile_uploadphoto(user_1.get("token"), BLACK_HOLE_JPG_URL, 50, 50, 200, 900)


def test_valid_upload_photo_invalid_size():
    """ Test for valid upload photo """
    clear()
    user_1 = auth_register("simple@example.com", "123456", "Hayden", "Jacobs")
    user_profile_uploadphoto(user_1.get("token"), BLACK_HOLE_JPG_URL, 50, 50, 200, 200)
    user_profile_uploadphoto(user_1.get("token"), "http://localhost:80/static/", 50, 50, 200, 200)
