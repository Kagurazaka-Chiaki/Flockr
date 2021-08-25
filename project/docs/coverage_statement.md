# Coverage statement
- The following functions in different files can't be covered by pytest.
## auth.py 63%  33 missing
1. auth_passwordreset_request(email).
2. auth_password_reset(reset_code, new_password).
- reason: Need to check the reset code from email, can't use pytest to cover, but we test it use frontend and email.
## channel.py 99%  2 partial
1. channel_messages(token, channel_id, start).
- reason: use if to check the react id equal to 1, were ever false, for conditions of other react id will be raised before.
## message.py 99%  2 partial
1. message_react(token, message_id, react_id).
2. message_unreact(token, message_id, react_id).
- reason: use if to check the react id equal to 1, were ever false, for conditions of other react id will be raised before.
## util.py  93%  10 missing 2 partial
1. format_addr(info).
2. Check_reset_code(reset_code).
3. get_info_form_reset(reset_code).
- reason: These three functions are related to email, which can??t use pytest to cover.
4. is_already_react(token,message_id,react).
- reason: use if to check the react id equal to 1, were ever false, for conditions of other react id will be raised before.
