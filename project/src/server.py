# -*- coding: utf-8 -*-
""" Implementation for server.py """

# import sys
import re
from json import dumps
from flask import Flask, request, url_for, send_file
from flask_cors import CORS
from error import InputError

################################### auth #######################################
from auth import auth_login
from auth import auth_logout
from auth import auth_register
from auth import auth_passwordreset_request
from auth import auth_password_reset
################################## channel #####################################
from channel import channel_invite
from channel import channel_details
from channel import channel_messages
from channel import channel_join
from channel import channel_leave
from channel import channel_addowner
from channel import channel_removeowner
################################## channels ####################################
from channels import channels_list
from channels import channels_listall
from channels import channels_create
################################## message #####################################
from message import message_send
from message import message_remove
from message import message_edit
from message import message_react
from message import message_unreact
from message import message_pin
from message import message_unpin
from message import message_sendlater
#################################### user ######################################
from user import user_profile
from user import user_profile_setname
from user import user_profile_setemail
from user import user_profile_sethandle
from user import user_profile_uploadphoto
#################################### other #####################################
from other import clear
from other import users_all
from other import admin_user_remove
from other import admin_userpermission_change
from other import search
################################## standup #####################################
from standup import standup_active
from standup import standup_send
from standup import standup_start
################################################################################


def default_handler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response


APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, default_handler)


# Example


@APP.route("/echo", methods=['GET'])
def echo():
    data = request.args.get('data')
    if data == 'echo':
        raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data
    })


##################################### auth #####################################


@APP.route("/auth/login", methods=["POST"])
def server_auth_login():
    """ A http funtion that do auth_login """
    payload = request.get_json()
    info = auth_login(
        payload.get("email"),
        payload.get("password")
    )
    return dumps(info)


@APP.route("/auth/logout", methods=["POST"])
def server_auth_logout():
    """ A http funtion that do auth_logout """
    payload = request.get_json()
    info = auth_logout(payload.get("token"))
    return dumps(info)


@APP.route("/auth/register", methods=["POST"])
def server_auth_register():
    """ A http funtion that do auth_register """
    payload = request.get_json()
    info = auth_register(
        payload.get("email"),
        payload.get("password"),
        payload.get("name_first"),
        payload.get("name_last")
    )
    return dumps(info)


@APP.route("/auth/passwordreset/request", methods=["POST"])
def server_auth_passwordreset_request():
    """ A http function will send the rest_code to user's email"""
    payload = request.get_json()
    info = auth_passwordreset_request(payload.get("email"))
    return dumps(info)


@APP.route("/auth/passwordreset/reset", methods=["POST"])
def server_auth_password_reset():
    """ A http function will reset the user's password"""
    payload = request.get_json()
    info = auth_password_reset(payload.get(
        "reset_code"), payload.get("new_password"))
    return dumps(info)

################################## channel #####################################


@APP.route("/channel/invite", methods=["POST"])
def server_channel_invite():
    """ A http funtion that do channel_invite """
    payload = request.get_json()
    info = channel_invite(
        payload.get("token"),
        int(payload.get("channel_id")),
        int(payload.get("u_id"))
    )
    return dumps(info)


@APP.route("/channel/details", methods=["GET"])
def server_channel_details():
    """ A http funtion that do channel_details """
    payload = request.args
    info = channel_details(
        payload.get("token"),
        int(payload.get("channel_id"))
    )
    return dumps(info)


@APP.route("/channel/messages", methods=["GET"])
def server_channel_messages():
    """ A http funtion that do channel_messages """
    payload = request.args
    info = channel_messages(
        payload.get("token"),
        int(payload.get("channel_id")),
        int(payload.get("start")),
    )
    return dumps(info)


@APP.route("/channel/leave", methods=["POST"])
def server_channel_leave():
    """ A http funtion that do channel_leave """
    payload = request.get_json()
    info = channel_leave(
        payload.get("token"),
        int(payload.get("channel_id"))
    )
    return dumps(info)


@APP.route("/channel/join", methods=["POST"])
def server_channel_join():
    """ A http funtion that do channel_join """
    payload = request.get_json()
    info = channel_join(
        payload.get("token"),
        int(payload.get("channel_id"))
    )
    return dumps(info)


@APP.route("/channel/addowner", methods=["POST"])
def server_channel_addowner():
    """ A http funtion that do channel_addowner """
    payload = request.get_json()
    info = channel_addowner(
        payload.get("token"),
        int(payload.get("channel_id")),
        int(payload.get("u_id"))
    )
    return dumps(info)


@APP.route("/channel/removeowner", methods=["POST"])
def server_channel_removeowner():
    """ A http funtion that do channel_removeowner """
    payload = request.get_json()
    info = channel_removeowner(
        payload.get("token"),
        int(payload.get("channel_id")),
        int(payload.get("u_id"))
    )
    return dumps(info)


# ################################## channels ####################################


@APP.route("/channels/list", methods=["GET"])
def server_channels_list():
    """ A http funtion that do channels_list """
    payload = request.args
    info = channels_list(payload.get("token"))
    return dumps(info)


@APP.route("/channels/listall", methods=["GET"])
def server_channels_listall():
    """ A http funtion that do channels_listall """
    payload = request.args
    info = channels_listall(payload.get("token"))
    return dumps(info)


@APP.route("/channels/create", methods=["POST"])
def server_channels_create():
    """ A http funtion that do channels_create """
    payload = request.get_json()
    info = channels_create(
        payload.get("token"),
        payload.get("name"),
        bool(payload.get("is_public"))
    )
    return dumps(info)


# ################################## message #####################################

@APP.route("/message/send", methods=["POST"])
def server_message_send():
    """ A http funtion that do message_send """
    payload = request.get_json()
    info = message_send(
        payload.get("token"),
        int(payload.get("channel_id")),
        payload.get("message")
    )
    return dumps(info)


@APP.route("/message/remove", methods=["DELETE"])
def server_message_remove():
    """ A http funtion that do message_remove """
    payload = request.get_json()
    info = message_remove(
        payload.get("token"),
        int(payload.get("message_id"))
    )
    return dumps(info)


@APP.route("/message/edit", methods=["PUT"])
def server_message_edit():
    """ A http funtion that do message_edit """
    payload = request.get_json()
    info = message_edit(
        payload.get("token"),
        int(payload.get("message_id")),
        payload.get("message")
    )
    return dumps(info)


@APP.route("/message/react", methods=["POST"])
def server_message_react():
    """ A http funtion that do message_react """
    payload = request.get_json()
    info = message_react(
        payload.get("token"),
        int(payload.get("message_id")),
        int(payload.get("react_id")),
    )
    return dumps(info)


@APP.route("/message/unreact", methods=["POST"])
def server_message_unreact():
    """ A http funtion that do message_unreact """
    payload = request.get_json()
    info = message_unreact(
        payload.get("token"),
        int(payload.get("message_id")),
        int(payload.get("react_id")),
    )
    return dumps(info)


@APP.route("/message/pin", methods=["POST"])
def server_message_pin():
    """A http function that pin the message"""
    payload = request.get_json()
    info = message_pin(
        payload.get("token"),
        int(payload.get("message_id")),
    )
    return dumps(info)


@APP.route("/message/unpin", methods=["POST"])
def server_message_unpin():
    """A http function that unpin the message"""
    payload = request.get_json()
    info = message_unpin(
        payload.get("token"),
        int(payload.get("message_id")),
    )
    return dumps(info)


@APP.route("/message/sendlater", methods=["POST"])
def server_message_sendlater():
    payload = request.get_json()
    info = message_sendlater(
        payload.get("token"),
        int(payload.get("channel_id")),
        payload.get("message"),
        int(payload.get("time_sent"))
    )
    return dumps(info)

#################################### user ######################################


@APP.route("/user/profile", methods=["GET"])
def server_user_profile():
    """ A http funtion that do user_profile """
    payload = request.args
    info = user_profile(
        payload.get("token"),
        int(payload.get("u_id"))
    )
    return dumps(info)


@APP.route("/user/profile/setname", methods=["PUT"])
def server_user_profile_setname():
    """ A http funtion that do user_profile_setname """
    payload = request.get_json()
    info = user_profile_setname(
        payload.get("token"),
        payload.get("name_first"),
        payload.get("name_last")
    )
    return dumps(info)


@APP.route("/user/profile/setemail", methods=["PUT"])
def server_user_profile_setemail():
    """ A http funtion that do user_profile_setemail """
    payload = request.get_json()
    info = user_profile_setemail(
        payload.get("token"),
        payload.get("email")
    )
    return dumps(info)


@APP.route("/user/profile/sethandle", methods=["PUT"])
def server_user_profile_sethandle():
    """ A http funtion that do user_profile_sethandle """
    payload = request.get_json()
    info = user_profile_sethandle(
        payload.get("token"),
        payload.get("handle_str")
    )
    return dumps(info)


@APP.route("/user/profile/uploadphoto", methods=["POST"])
def server_user_profile_uploadphoto():
    """ A http funtion that upload user's requested photo to the server """
    payload = request.get_json()
    user_profile_uploadphoto(
        payload.get("token"), payload.get("img_url"),
        int(payload.get("x_start")), int(payload.get("y_start")),
        int(payload.get("x_end")), int(payload.get("y_end")),
    )
    token_payload = re.search(r"\.(.+?)\.", payload.get("token")).group(0)
    file_name = token_payload[1:len(token_payload) - 1] + ".jpg"

    static_url = url_for("static", filename=file_name)
    host_url = request.url_root[:len(request.url_root) - 1]
    payload["img_url"] = host_url + static_url

    user_profile_uploadphoto(
        payload.get("token"), payload.get("img_url"),
        int(payload.get("x_start")), int(payload.get("y_start")),
        int(payload.get("x_end")), int(payload.get("y_end")),
    )

    return payload["img_url"]


@APP.route("/static/<image>")
def server_display_image(image):
    """ A http funtion that display image """
    return send_file(f"../static/{image}", mimetype='image/jpg')


#################################### other #####################################

@APP.route("/users/all", methods=["GET"])
def server_users_all():
    """ A http funtion that do users_all """
    payload = request.args
    info = users_all(payload.get("token"))
    return dumps(info)


@APP.route("/admin/user/remove", methods=["DELETE"])
def server_admin_user_remove():
    """ A http funtion that do admin_userpermission_change """
    payload = request.get_json()
    info = admin_user_remove(
        payload.get("token"),
        int(payload.get("u_id")),
    )
    return dumps(info)


@APP.route("/admin/userpermission/change", methods=["POST"])
def server_admin_userpermission_change():
    """ A http funtion that do admin_userpermission_change """
    payload = request.get_json()
    info = admin_userpermission_change(
        payload.get("token"),
        int(payload.get("u_id")),
        int(payload.get("permission_id"))
    )
    return dumps(info)


@APP.route("/search", methods=["GET"])
def server_search():
    """ A http funtion that do search """
    payload = request.args
    info = search(
        payload.get("token"),
        payload.get("query_str")
    )
    return dumps(info)


@APP.route("/standup/start", methods=["POST"])
def server_standup_start():
    """ A http funtion that do standup_start """
    payload = request.get_json()
    info = standup_start(
        payload.get("token"),
        int(payload.get("channel_id")),
        int(payload.get("length"))
    )
    return dumps(info)


@APP.route("/standup/active", methods=["GET"])
def server_standup_active():
    """ A http funtion that do standup_active """
    payload = request.args
    info = standup_active(
        payload.get("token"),
        int(payload.get("channel_id"))
    )
    return dumps(info)


@APP.route("/standup/send", methods=["POST"])
def server_standup_send():
    """ A http funtion that do standup_send """
    payload = request.get_json()
    info = standup_send(
        payload.get("token"),
        int(payload.get("channel_id")),
        payload.get("message"),
    )
    return dumps(info)


@APP.route("/clear", methods=["DELETE"])
def server_clear():
    """ A http funtion that clear all the data """
    clear()
    return {}


if __name__ == "__main__":
    # APP.run(port=0)   # Do not edit this port
    APP.run(port=5000, debug=True)  # For Debug Only
