""" temp http test for auth.py"""
import re
#import json
import signal
from time import sleep
from subprocess import Popen, PIPE

import pytest

import requests
from error import InputError


@pytest.fixture()
def _url():
    url_re = re.compile(r' \* Running on ([^ ]*)')
    # Use This On CSE
    server = Popen(["python3", "src/server.py"], stderr=PIPE, stdout=PIPE)
    # For Windows Only
    # server = Popen(["python", "src\\server.py"], stderr=PIPE, stdout=PIPE)
    line = server.stderr.readline()
    local_url = url_re.match(line.decode())
    # Get Last Line, For Debug Only
    while not bool(local_url):
        line = server.stderr.readline()
        local_url = url_re.match(line.decode())
    if local_url:
        yield local_url.group(1)  # url = local_url.group(1)
        # Terminate the server
        # server.send_signal(signal.SIGINT) -> (Ctrl + C)
        # For Windows and Linux
        server.send_signal(signal.SIGTERM)
        waited = 0
        while server.poll() is None and waited < 5:
            sleep(0.1)
            waited += 0.1
        if server.poll() is None:
            server.kill()
    else:
        server.kill()
        raise Exception("Couldn't get URL from local server")


def test_url(_url):
    '''
    A simple sanity test to check that your server is set up properly
    '''
    assert _url.startswith("http")


def test_auth_register_invalid_email(_url):
    '''
    test for auth/register about invalid email
    '''
    requests.delete(f'{_url}/clear')
    register_url = _url+"auth/register"
    response = requests.post(
        register_url,
        json={
            "email": "invalidemail",
            "password": "thisisvalid",
            "name_first": "Julia",
            "name_last": "Meiya"
        }
    )
    assert response.status_code == InputError.code
    requests.delete(f'{_url}/clear')


def test_auth_regiser_first_name_short(_url):
    '''
    test for auth/register about invalid first_name
    '''
    requests.delete(f'{_url}/clear')
    register_url = _url+"auth/register"
    response = requests.post(
        register_url,
        json={
            "email": "thisisvalid@simple.com",
            "password": "thisisvalid",
            "name_first": "",
            "name_last": "Meiya"
        }
    )
    assert response.status_code == InputError.code
    requests.delete(f'{_url}/clear')


def test_auth_register_last_name_short(_url):
    '''
    test for auth/register about invalid last_name
    '''
    requests.delete(f'{_url}/clear')
    register_url = _url+"auth/register"
    response = requests.post(
        register_url,
        json={
            "email": "thisisvalid@simple.com",
            "password": "thisisvalid",
            "name_first": "Julia",
            "name_last": ""
        }
    )
    assert response.status_code == InputError.code
    requests.delete(f'{_url}/clear')


def test_auth_register_firt_name_too_long(_url):
    '''
    test for auth/register about invalid first_name
    '''
    requests.delete(f'{_url}/clear')
    register_url = _url+"auth/register"
    invalid_first = "this_is_too_long_name_which_has_more_than_fifty_characters"
    response = requests.post(
        register_url,
        json={
            "email": "thisisvalid@simple.com",
            "password": "thisisvalid",
            "name_first": invalid_first,
            "name_last": "Meiya"
        }
    )
    assert response.status_code == InputError.code
    requests.delete(f'{_url}/clear')


def test_auth_register_last_name_too_long(_url):
    '''
    test for auth/register about invalid last_name
    '''
    requests.delete(f'{_url}/clear')
    register_url = _url+"auth/register"
    invalid_last = "this_is_too_long_name_which_has_more_than_fifty_characters"
    response = requests.post(
        register_url,
        json={
            "email": "thisisvalid@simple.com",
            "password": "thisisvalid",
            "name_first": "Julia",
            "name_last": invalid_last
        }
    )
    assert response.status_code == InputError.code
    requests.delete(f'{_url}/clear')


def test_auth_register_short_password(_url):
    '''
    test for auth/register about invalid password
    '''
    requests.delete(f'{_url}/clear')
    register_url = _url+"auth/register"
    response = requests.post(
        register_url,
        json={
            "email": "thisisvalid@simple.com",
            "password": "123",
            "name_first": "Julia",
            "name_last": "Meiya"
        }
    )
    assert response.status_code == InputError.code
    requests.delete(f'{_url}/clear')


def test_auth_register_used_email(_url):
    '''
    test for auth/register about used email
    '''
    requests.delete(f'{_url}/clear')
    register_url = _url+"auth/register"
    requests.post(
        register_url,
        json={
            "email": "thisisvalid@simple.com",
            "password": "thisisvalid",
            "name_first": "Julia",
            "name_last": "Meiya"
        }
    )
    response = requests.post(
        register_url,
        json={
            "email": "thisisvalid@simple.com",
            "password": "thisisanother",
            "name_first": "David",
            "name_last": "Bill"
        }
    )
    assert response.status_code == InputError.code
    requests.delete(f'{_url}/clear')


def test_auth_register_successful(_url):
    '''
    test for auth/register in server.py
    '''
    requests.delete(f'{_url}/clear')
    email = "thisisvalid@simple.com"
    password = "thisisvalidpassword"
    name_first = "David"
    name_last = "Bill"
    register_url = _url+"/auth/register"
    response_one = requests.post(
        register_url,
        json={
            "email": email,
            "password": password,
            "name_first": name_first,
            "name_last": name_last
        }
    )

    response_two = requests.post(
        register_url,
        json={
            "email": "thisisunqiue@qq.com",
            "password": "thisisvalid",
            "name_first": "Julia",
            "name_last": "Meiya"
        }
    )
    u_id_one = response_one.json().get("u_id")
    u_id_two = response_two.json().get("u_id")
    assert u_id_one != u_id_two
    token_one = response_one.json().get("token")
    token_two = response_two.json().get("token")

    login_url = _url+"/auth/login"
    requests.post(login_url, json={"email": "thisisvalid@simple.com",
                                   "password": "thisisvalidpassword"})
    requests.post(login_url, json={"email": "thisisunqiue@qq.com",
                                   "password": "thisisvalid"})

    logout_url = f"{_url}/auth/logout"
    logout_one = requests.post(logout_url, json={"token": token_one})
    logout_two = requests.post(logout_url, json={"token": token_two})

    assert logout_one.json().get("is_success")
    assert logout_two.json().get("is_success")
    requests.delete(f'{_url}/clear')


def test_auth_login_invalid_email(_url):
    """
    test invaild email when login
    """
    requests.delete(f'{_url}/clear')
    login_url = _url+"/auth/login"
    response = requests.post(
        login_url,
        json={
            "email": "thisisinvalid",
            "password": "thisisvalid"
        }
    )
    assert response.status_code == InputError.code
    requests.delete(f'{_url}/clear')


def test_auth_login_not_user_email(_url):
    """
    test when the email not register
    """
    requests.delete(f'{_url}/clear')
    login_url = _url+"/auth/login"
    response = requests.post(
        login_url,
        json={
            "email": "bill333@amazon.com",
            "password": "thisisvalid"
        }
    )
    assert response.status_code == InputError.code
    requests.delete(f'{_url}/clear')


def test_auth_login_incorrect_password(_url):
    """
    test when the password not register
    """
    requests.delete(f'{_url}/clear')
    login_url = _url+"/auth/login"
    register_url = _url+"/auth/register"
    requests.post(
        register_url,
        json={
            "email": "bill333@amazon.com",
            "password": "thisisvalid",
            "name_first": "David",
            "name_last": "Bill"
        }
    )
    response = requests.post(
        login_url,
        json={
            "email": "bill333@amazon.com",
            "password": "thisisnotcorrect"
        }
    )
    assert response.status_code == InputError.code
    requests.delete(f'{_url}/clear')


def test_auth_login_correct(_url):
    """
    test correct condition for auth/login
    """
    requests.delete(f"{_url}/clear")
    data_one = requests.post(f"{_url}/auth/register", json={
        "email": "lyuhaotian@gmail.com",
        "password": "lyuhaotian2001",
        "name_first": "Haotian",
        "name_last": "Lyu",
    })
    info_one = data_one.json()

    data_two = requests.post(f"{_url}/auth/login", json={
        "email": "lyuhaotian@gmail.com",
        "password": "lyuhaotian2001",
    })
    info_two = data_two.json()

    assert info_one.get("token") == info_two.get("token")
    assert info_one.get("u_id") == info_two.get("u_id")


def test_auth_logout_incorrect_token(_url):
    '''
    test invalid token in auth/logout
    '''
    requests.delete(f'{_url}/clear')
    logout_url = _url+"/auth/logout"
    login_url = _url+"/auth/login"
    register_url = _url+"/auth/register"
    requests.post(
        register_url,
        json={
            "email": "bill333@amazon.com",
            "password": "thisisvalid",
            "name_first": "David",
            "name_last": "Bill"
        }
    )
    requests.post(
        login_url,
        json={
            "email": "bill333@amazon.com",
            "password": "thisisvalid"
        }
    )
    response = requests.post(logout_url, json={"token": "invalidtoken"})
    assert not response.json().get("is_sussess")
    requests.delete(f'{_url}/clear')


def test_auth_logout_success(_url):
    '''
    test correct condition in auth/logout
    '''
    requests.delete(f'{_url}/clear')
    email = "thisisvalid@simple.com"
    password = "thisisvalidpassword"
    name_first = "David"
    name_last = "Bill"
    register_url = _url+"/auth/register"
    response_one = requests.post(
        register_url,
        json={
            "email": email,
            "password": password,
            "name_first": name_first,
            "name_last": name_last
        }
    )

    response_two = requests.post(
        register_url,
        json={
            "email": "thisisunqiue@qq.com",
            "password": "thisisvalid",
            "name_first": "Julia",
            "name_last": "Meiya"
        }
    )

    u_id_one = response_one.json().get("u_id")
    u_id_two = response_two.json().get("u_id")
    assert u_id_one != u_id_two
    token_one = response_one.json().get("token")
    token_two = response_two.json().get("token")

    login_url = _url+"/auth/login"
    requests.post(login_url, json={"email": "thisisvalid@simple.com",
                                   "password": "thisisvalidpassword"})
    requests.post(login_url, json={"email": "thisisunqiue@qq.com",
                                   "password": "thisisvalid"})

    logout_url = _url+"/auth/logout"
    logout_one = requests.post(logout_url, json={"token": token_one})
    logout_two = requests.post(logout_url, json={"token": token_two})

    assert logout_one.json().get("is_success")
    assert logout_two.json().get("is_success")
    requests.delete(f'{_url}/clear')
