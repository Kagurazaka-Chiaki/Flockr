# Meeting summary

## 2020/09/20 Sunday meeting01

- Main topic: everyone read the project and trying to write the auth with test and will discuss on next Thursday.

- Summary of meeting:

  1. Read the project Readme.md together and dicussed about the project requirements.
  2. Determined the structure of git:
     - Always ensure the "master" branch is correct and clean, so all the test and implementation of code will be done in other branch.
     - Create a new branch called "Develop" to implement and add test for the function in interation 1.
     - Then, each member create new branch for every test and function they implement.
     - When every member checked and agree that the tests and function is implemented correctly, 
       we then merge the code to the "Develop" branch.
     - We will merge "Develop" to the "master" after finishing the whole interation 1 on the "Develop" branch.

- Next meeting time: 2020/09/24 Thursday

## 2020/09/24 Thursday meeting02

- Main topic: auth.py auth_test.py.

- The idea for implementing auth:

  - Data: we use a dictionary including 'users' and 'channels' and in the key 'users' we used a list of dictionary to store each user's data.
    the data for users include 'u_id', 'email', 'password', 'first_name', 'last_name', 'handle_str' and 'token'.
  - Auth_login:
    - First check the email is valid or not by calling another function email_check().
    - Then iterate over the list of 'users' to find the dictionary that contained the  same email, 
      if can't find the dictionary with the input email, raises an inputerror.
    - After that, check the password to see whether the password is correct. If it is , return {'u_id','token'} in that dictionary if not, raises input error.
  - Auth_register:
    - First check the email's validity as same as we do in auth_login.
    - Then iterate over the list of 'users' to see if there contained the same registered email address, raises input error if it does.
    - The next step is to use the name_first and name_last to generate the unique 'handle_str' and iterate again to check the duplicate 'handle_str',
    - If there already exist a same 'handle_str', change the new 'handle_str' by adding a number after it.
    - And create the new dictionary that contained the input data, new 'handle_str', the new 'u_id' and the new token.
    - Lastly, append the new dictionary to the 'user' list and return its {u_id,token}.

- Questions (asked on Friday's lab):

  - Handle_str: what's this, and how to use it? is handle same with token?
  - Token: how we generate token now? and do we need to change the way of generating token in further iteration.
  - Return error: What is the form of returning the error ? Is it the same as the required output format? like {u_id, token}.

- Next meeting time: 2020/09/25 Friday (lab)

## 2020/09/25 Friday meeting03

- Main topic: selected and integrated 5 members' auth.py and auth_test.py into one file, then push to the Develop branch.

- Answers of question from tutor:

  - Handle str can be set by ourselves and write the rule in the assumptions.md.
  - Token is the unique one to indentify a user and we can also set the rule of token and write it in assumptions.md too.
  - About error, the function not return but raise the error in error.py like InputError and AccessError.

- Summary of meeting:

  1. We asked tutor Ian Thorvaldson about the questions we have in last meeting and try to modified everyone's auth.py and auth_test.py.
  2. Every member showed his own code and tests, and briefly described the design ideas.
  3. We discussed together and selected the best way of implementing each function.
  4. By using zoom and wechat, we did group programming and intergrated the functions and tests from different members to the auth.py and auth_test.py.
  5. Determined the task of every member from 2020/09/25 to next meeting day:
     - Everyone try to write all tests and functions in channel.py and channels.py.
     - Next meeting will discuss about the functions and tests and assign the functions to different people to write the final version.

- Questions (ask tutor by email):

  - Can we use try-except-else in auth.py to raise the error and return the string of error type?
  - Can we add more types of InputError and AccessError in test?

- Next meeting time: 2020/09/27 Sunday

## 2020/09/27 Sunday meeting04

- Main topic: determine final data stucture and modify the auth_test and assign two functions to each member to implement.

- Answers of questions last meeting by tutor:

  - Don't put try-except-else in the function, the function should return error not return some string.
  - Feel free to add our own errors, just put them in assumptions docment if they're not in spec.

- Summary of meeting:

  1. According to tutor's reply, we fixed the auth.py and it's tests.
  2. After discussing three types of data structure, we determined one of them to be the final data structure for interation 1.
  3. Talk over how to write each function in channel.py and channels.py and assign to every member(with each function's test):
  4. Task Distribution Form

     | Group memebr |                functions                 |
     |--------------|------------------------------------------|
     | Mingyuan Cui |   channel_invite(), channels_create()    |
     | Haotian Lyu  |   channel_detail(), channel_message()    |
     |   Xing Shi   |     channel_leave(), channel_join()      |
     | Xihao Liang  | channel_addowner(), channel_removeowner()|
     |   Wei Wei    |   channels_list(), channels_listall()    |

- Next meeting time: 2020/09/28 Monday

## 2020/09/28 Monday meeting05

- Main topic: See everyone's function and discuss about improvement and integrate the referenced functions to one file util.py.

- Summary of meeting:

  1. Everyone showed the functions they write and we discussed about how to improve the functions and tests.
  2. Move the referenced functions to a file called util.py and unified the functions which achieve the same goal.

- Questions:(ask tutor on lab and help session):

  - About clear() functions in other.py, do we need to write clear() function by ourselves or just use python function clear(), like Data["uses"].clear()?
  - How to do the blackbox tests for the correct condition of some functions that just return {}?
  - For the channel_message, we don't have function to send message to the channel ,how we test the correct condition.

- Next meeting time: 2020/10/02 Friday

## 2020/10/02 Friday meeting06

- Main topic: implement and modified all functions in channel.py and channels.py and merge it to "Develop".

- Answers of questions last meeting by tutor:

  - We need to write the clear() function by ourselves, and because of blackbox testing, we can't use Data["uses"].clear() in test file.
  - We can only use the function we build in auth.py, channel.py and channels.py like channel_detail to test the append information in data structure.
  - It will not be fully testable this iteration because you don't write message_send. However you can still do some basic tests to ensure the output is constructed correctly for a channel with no messages in it - and then test it properly when message_send is implemented in a later iteration.

- Summary of meeting:

  1. Modified the tests file with clear() function in other.py to initialize the data.
  2. we create a new branch with prefix 'feature' for every one or two functions. 
  3. first we push the test and code for the function to the 'feature' branch, 
     then we test the file with pytest, coverage and pylint, if everything went well and every member is happy about it, 
     we will then merge the 'feature' branch to the "Develop" branch.
  4. Found and fixed some bug in the implementation file and test.
  5. Complete the assumption.md and Meeting_summmary.md.
  6. Do the final check and test on next day.

- Next meeting time: 2020/10/08
