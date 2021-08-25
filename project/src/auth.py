# -*- coding: utf-8 -*-
""" Implementation for auth.py """

import smtplib
import random
import string
from email.mime.text import MIMEText
from email.header import Header
import hashlib
import jwt

import util as u
from error import InputError
from data import Data



SECRET = "COMP1531"


def generate_token(u_id, email):
    """ Generate token """
    jwt_info = {"u_id": u_id, "email": email}
    return jwt.encode(jwt_info, SECRET, algorithm="HS256")


def generate_password(raw_password):
    """ Generate password """
    return hashlib.sha256(raw_password.encode()).hexdigest()


def auth_login(email, password):
    """
    Given a registered users' email and password
    and generates a valid token for the user to remain authenticated

    Args:
        email:A string of email of the user
        password: A string of password of the user

    Returns:
        A dictionary with user's u_id and token who login

        {'u_id': i.get("u_id"),
        'token': i.get("token"),}

    Raises:
        InputError("Invalid Email"): the input email is invalid
        InputError("Not Belong To A User"): the email entered not belong to a user

    """
    status = False
    login_dict = {}

    if not u.is_email_valid(email):
        raise InputError("Invalid Email")

    if not u.is_email_used(email):
        raise InputError("Not Belong To A User")

    for i in Data["users"]:
        if (i.get("email") == email and i.get("password") == generate_password(password)):
            i["login"] = True
            status = True
            login_dict = {
                'u_id': i.get("u_id"),
                'token': i.get("token"),
            }
    if not status:
        raise InputError("Incorrect Password")
    return login_dict


def auth_logout(token):
    """
    Given an active token, invalidates the token to log the user out.
    If a valid token is given, and the user is successfully logged out,
    it returns true, otherwise false.

    Args:
        token: A string used to identify a user.

    Returns:
        A dictionary with key "is_success" which shows the success or not of logout

        {'is_success': False}

    Raises:
        None

    """
    if not u.is_token_valid(token):
        return {'is_success': False}

    users_list = Data["users"]
    for i in users_list:
        if i.get("token") == token:
            i["login"] = False
    return {'is_success': True}


def auth_register(email, password, name_first, name_last):
    """
    Given a user's first and last name, email address, and password,
    create a new account for them and return a new token for authentication
    in their session.
    A handle is generated that is the concatentation
    of a lowercase-only first name and last name.
    If the concatenation is longer than 20 characters,
    it is cutoff at 20 characters.
    If the handle is already taken, you may modify the handle
    in any way you see fit to make it unique.

    Args:
        email:A string of email of the user.
        password: A string of password of the user.
        name_first: A string of register's first name
        name_last: A string of register's last name

    Returns:
        A dictionary with new user's u_id and token

        {'u_id': new_uid,
        'token': new_token,}

    Raises:
        InputError("Used Email"): The email the user want to register has been used
        InputError("Invalid Email"): The email the user want to register is invalid
        InputError("Invalid Password"): The password the user use is Invalid
        InputError("Invalid User Name"): The user's not valid

    """
    if u.is_email_used(email):
        raise InputError("Used Email")
    if not u.is_email_valid(email):
        raise InputError("Invalid Email")
    if u.is_password_short(password):
        raise InputError("Invalid Password")
    if not u.is_name_in_range(name_first, name_last):
        raise InputError("Invalid User Name")

    new_uid = u.get_last_id(Data["users"], "u_id") + 1

    # new_token = name_first + "_" + name_last + str(new_uid)
    new_token = generate_token(new_uid, email).decode()
    new_password = generate_password(password)

    new_handle = (name_first[0] + name_last).lower()
    uid_length = len(str(new_uid))
    new_handle = new_handle[0:20 - uid_length] + str(new_uid)
    permission_id = u.generate_permission_id(Data["users"])

    new_dic = {
        "u_id": new_uid,
        "email": email,
        "password": new_password,
        "name_first": name_first,
        "name_last": name_last,
        "handle_str": new_handle,
        "token": new_token,
        "login": False,
        "permission_id": permission_id,
        "profile_img_url": "",
        "reset_code": ""
    }

    Data["users"].append(new_dic)
    return {
        'u_id': new_uid,
        'token': new_token,
    }


def auth_passwordreset_request(email):
    """

    Given an email address, if the user is a registered user, send's them a an
    email containing a specific secret code, that when entered in
    auth_passwordreset_reset, shows that the user trying to reset the password
    is the one who got sent this email.
    Args:
        email:A string of email of the user.
    Raises:
        InputError("Used Email"): The email the user want to register has been used
    Return:
        {}
    """
    if not u.is_email_used(email):
        raise InputError("Unused email")

    from_addr = "willauunsw@gmail.com"
    password = "Comp1531"
    to_addr = email
    smtp_server = "smtp.gmail.com"
    random_str = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(5))
    while u.check_reset_code(random_str):
        random_str = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(5))

    message = f'This is your verification code: {random_str}. \n Please do not tell others!!!'
    msg = MIMEText(message, 'plain', 'utf-8')
    msg['From'] = u.format_addr('Flockr <%s>' % from_addr)
    msg['To'] = u.format_addr(to_addr)
    msg['Subject'] = Header("Flockr verification code", 'utf-8').encode()

    server = smtplib.SMTP(smtp_server, 587)
    server.set_debuglevel(1)
    server.ehlo()
    server.starttls()
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()

    for user in Data["users"]:
        if user["email"] == email:
            user["reset_code"] = random_str

    return{}

def auth_password_reset(reset_code, new_password):
    """
    Given a reset code for a user,
    set that user's new password to the password provided

    Args:
        reset_code: The verfication code helps user to change the password.
        new_password: The new password the users want to reset.
    Raises:
        InputError("invalid reset code"): The reset_code is not correct.
        InputError("invalid password"): The new_password is not valid.
    Return:
        {}
    """
    if not u.check_reset_code(reset_code):
        raise InputError("invalid reset code")
    if u.is_password_short(new_password):
        raise InputError("invalid password")

    user_change = u.get_info_from_reset(reset_code)

    user_change["password"] = generate_password(new_password)
    user_change["reset_code"] = ""

    return{}
