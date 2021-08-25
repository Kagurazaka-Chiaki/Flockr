"""implement user.py"""

import urllib.request as request
from urllib.error import HTTPError, URLError
import re
from PIL import Image
from data import Data
import util as u
from error import InputError, AccessError


def get_user_detail(token):
    """ Get user detail by token """
    temp = {}
    for i in Data["users"]:
        if i.get("token") == token:
            temp = i
    return temp


def user_profile(token, u_id):
    """
    For a valid user, returns information about
    their user_id, email, first name, last name, and handle
    Args:
        token: A string used to identify a user
        u_id: The id of the user
    Returns:
        A list of all users and their associated details
        {
            'users': [
                {
                    'u_id': 1,
                    'email': 'cs1531@cse.unsw.edu.au',
                    'name_first': 'Hayden',
                    'name_last': 'Jacobs',
                    'handle_str': 'hjacobs',
                },
            ],
        }
    Raises:
        AccessError("Invalid token")
            when the token does not belong to a user
        InputError("Invalid u_id")
            when the u_id does not belong to a user
    """

    # check the u_id is valid or not
    if not u.is_user_id_valid(u_id):
        raise InputError("invalid u_id")
    # chech the token is valid or not
    if not u.is_token_valid(token):
        raise AccessError("invalid token")

    user_dict = get_user_detail(u.get_token(u_id))
    # u_id, email, name_first, name_last, handle_str, profile_img_url

    info_dict = {
        "u_id": u_id,
        "email": user_dict.get("email"),
        "name_first": user_dict.get("name_first"),
        "name_last": user_dict.get("name_last"),
        "handle_str": user_dict.get("handle_str"),
        "profile_img_url": user_dict.get("profile_img_url"),
    }

    return {
        "user": info_dict
    }


def user_profile_setname(token, name_first, name_last):
    """
    Update the authorised user's first and last name
    Args:
        token: A string used to identify a user
        name_first: updated name-first
        name_last: updated name_last
    Returns: {}
    Raises:
        InputError("Invalid token")
            when the token does not belong to a user
        InputError("Invalid name")
            when name_first and name_last are not between 1 and 50 characters
            inclusively in length
    """
    # check the length of name_first and name_last is valid
    if not u.is_name_in_range(name_first, name_last):
        raise InputError("Invalid name")
    # chech the token is valid or not
    if not u.is_token_valid(token):
        raise InputError("Invalid token")

    for user in Data["users"]:
        if user["token"] == token:
            user["name_first"] = name_first
            user["name_last"] = name_last

    return {}


def user_profile_setemail(token, email):
    """
    Update the authorised user's email address
    Args:
        token: A string used to identify a user
        email: updated email
    Returns: {}
    Raises:
        InputError("Invalid token")
            when the token does not belong to a user
        InputError("Invalid email")
            when Email entered is not a valid email
        InputError("Used email")
            when Email address is already being used by another user
    """
    # check the email is valid or not
    if not u.is_email_valid(email):
        raise InputError("Invalid email")
    # check whether this email is registered by other people
    if u.is_email_used(email):
        raise InputError("Used email")
    # check the token is valid or not
    if not u.is_token_valid(token):
        raise InputError("Invalid token")

    for user in Data["users"]:
        if user["token"] == token:
            user["email"] = email

    return {}


def user_profile_sethandle(token, handle_str):
    """
    Update the authorised user's handle (i.e. display name)
    Args:
        token: A string used to identify a user
        handle_str: updated handle_str
    Returns: {}
    Raises:
        InputError("Invalid token")
            when the token does not belong to a user
        InputError("Invalid handle_string")
            when handle_str is not between 3 and 20 characters in length
        InputError("Used handle_string")
            when handle is already used by another user
    """
    # check the token is valid or not
    if not u.is_token_valid(token):
        raise InputError("Invalid token")
    # check the lenth of hand_str is valid
    if not u.is_handle_in_range(handle_str):
        raise InputError("Invalid handle_string")
    # check whether this hand_str is used by other people or not
    if u.is_handle_str_used(handle_str):
        raise InputError("Used handle_string")

    for user in Data["users"]:
        if user["token"] == token:
            user["handle_str"] = handle_str

    return {}


def user_profile_uploadphoto(token, img_url, x_start, y_start, x_end, y_end):
    """
    Given a URL of an image on the internet,
    crops the image within bounds (x_start, y_start) and (x_end, y_end).
    Position (0,0) is the top left.

    Args:
        token:   (string)   identfy user
        img_url: (string)   image's url
        x_start: (interger) x start coordinate
        y_start: (interger) y start coordinate
        x_end:   (interger) x end coordinate
        y_end:   (interger) y end coordinate

    Returns: {}

    Raises:
        InputError("Invalid token")
            when the token does not belong to a user
        InputError(message)
            img_url returns an HTTP status other than 200.
        InputError("Invalid Dimensions")
            any of x_start, y_start, x_end, y_end are not within the dimensions
        InputError("Invalid Image")
            Image uploaded is not a JPG
    """

    if not u.is_token_valid(token):
        raise InputError("Invalid Token")

    if re.search(r"\/static\/", img_url) is None:

        token_payload = re.search(r"\.(.+?)\.", token).group(0)
        file_name = token_payload[1:len(token_payload) - 1]
        file_name = "static/" + file_name + ".jpg"

        try:
            request.urlretrieve(img_url, file_name)
        except (HTTPError, URLError) as message:
            raise InputError(message)

        img = Image.open(file_name)

        if not img.format in ("JPEG", "JPG"):
            raise InputError("Invalid Image")

        if not u.is_image_in_range(img, x_start, y_start, x_end, y_end):
            raise InputError("Invalid Dimensions")

        copied = img.crop((x_start, y_start, x_end, y_end))
        copied.save(file_name)
    else:
        user_dict = u.get_users_dict(token)
        user_dict["profile_img_url"] = img_url

    return {}
