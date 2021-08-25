# Assumptions

### Data Storage Structure

```python
# assumed data storage structuer in data.py

Data = {
    "users": [
        {
            "u_id": 1,
            "email": "",
            "password": "",
            "name_first": "",
            "name_last": "",
            "handle_str": "",
            "token": "",
            "login": False,
            "permission_id": 2,
        },
    ],
    "channels": [
        {
            "channel_id": 1,
            "name": 'channel1',
            "owners_token": [],
            "users_token": [],
            "channel_message": [
                {
                    "message_id": 1,
                    "u_id": 1,
                    "is_pinned": False,
                    "reacts": ["react_u_id"],
                    "message": "",
                    "time_created": 1
                },
            ],
            "standup_buffer": [
              {
                "token": "",
                "message": "",
              },
            ],
            "is_public": True,
            "is_active": False,
        },
    ]
    "reset_codes": [
      {
        "code":"",
        "token":"",
      }
    ]
}


```

### Assumption for util.py

- the util.py is used to store referenced function which used in auth.py , channel.py and channels.py

### Assumptions for auth.py in interation 1

- auth_register:
  - new u_id when registering start from 1
  - new token use first name + "\_" + last name + string of u_id
  - new handle string use first character of first name + last name (all lower)
    handle string length minus uid length and then it plus uid string
    and we assume the number of users will not greater than 7.5 billion
    which is less than 20 characters' length
  - the initial login condition is False

### Assumptions for channels.py in interation 1

- channels_list:

  - check token each time as it may invalid and raise InputError

- channels_listall:

  - check token each time as it may invalid and raise InputError

- channels_create:
  - new channel_id start from 1 and +1 when each channel created
  - also need to check is token valid, so add InputError to check

### Assumptions for message.py in iteration 2

- message_send:
- assume the number of message is not larger than 2^32
- assume message id is start from 1
- check token each time as it may invalid and raise InputError

### Functionality Assumptions

- we assume the email are not allow for the upper letter,
  only lower letter and numbers allowed.
- we assume the jwt(token) will never time expiry.
- we assume permission id only 1, and 2
- we assume data are not stored persistently
- we assume that users can't invite dumplicated users who is already in channel (include user's self).
- In the backend users can login more than once without logout, we assume it will be limited on frontend.
- we assume the users can create channels with same name.
- Owners can delete other owner's perimission.

### Assumptions for message_sendlater in iteration 3
- The code below is based on the TimerThread in the module threading.py,
  we define a result function which return the self value.