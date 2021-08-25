# Meeting summary for lteration2

## 2020/10/12 Monday meeting01

- Main topic: have a basic understanding of lteration2 and assign tasks to group members(two file for each member).

- Summary of meeting:

  1. Browse the update of lteration 2 together.
  2. Determine the task for every member from 2020/10/12 to next meeting day:

     - Each member tries to work on two remaining files: message.py, other.py and user.py.
     - Next meeting will discuss about the functions and tests and assign the functions to different people to write the final version.
     - Task Disturbution Form

     | Group memebr | draft code for seperate file |
     | :----------- | :--------------------------- |
     | Mingyuan Cui | other.py user.py message.py  |
     | Haotian Lyu  | user.py message.py           |
     | Xing Shi     | user.py message.py           |
     | Xihao Liang  | other.py message.py          |
     | Wei Wei      | other.py user.py             |

- Questions (ask tutor by email):

  - How to deal with delected message, should we leave a blank dictionary key.
  - How to add more than one assignees for setting tasks in board on git.

- Next meeting time: 2020/10/16 Friday

## 2020/10/16 Friday meeting02

- Main topic: have a initial discussion about the three files' function
  for message.py, user.py and other.py.

- Answers of question from tutor:

  - When removing a message form a channel, the other message_id should not be changed.
  - We can use the int() function to ensure the timestamp takes into account hours, minutes and seconds.
  - The token and u_id in user_profile() function refer to different users.
    The person with "token" is trying to view the profile of "u_id".
  - channel should be determined from the message_id. The message_ia can be started with channel_id.

- Summary of meeting:

  1. have a general understanding of how each function works.
  2. Assign functions for each member to modify based on existing progress:

     - Task Disturbution Form

     | Group memebr | modify code for different function |
     | :----------- | :--------------------------------- |
     | Mingyuan Cui | message_remove                     |
     | Haotian Lyu  | message_send                       |
     | Xing Shi     | message_edit                       |
     | Xihao Liang  | functions in other                 |
     | Wei Wei      | functions in users                 |

  3. Finish all these functions and merge them into the Develop branch by each member.

- Questions (ask tutor by email):

  - When we try to remove the last message in a channel, should we remove its message_id

- Next meeting time: 17/10/2020

## 2020/10/18 Sunday meeting03

- Main topic: General meeting and modify functions in iteration 1.

- Summary of meeting:

  1. To Having a general understanding of how flask works.
  2. Solving questions from group members.
  3. Check all the functions and try to figure out where lose 6% marks for auto marking.
  4. Try to firgue out why losing 10% in manual marking.
  5. Get ready for Task Disturbution tomorrow.

- Questions (ask tutor by email):

  - [x] Details regarding losing marks
  - [x] `src/server` or `server`
  - [x] redefine `url` from outer scope

- Next meeting time: 19/10/2020

## 2020/10/19 Monday meeting04

- Main topic: assigned everyone's task for flask functions.

- Summary of meeting:

  1. Assigned each member's task for flask:

     | Group memebr | modify code for different function |
     | :----------- | :--------------------------------- |
     | Mingyuan Cui | auth.py channel.py message.py      |
     | Haotian Lyu  | auth.py channels.py other.py       |
     | Xing Shi     | auth.py user.py message.py         |
     | Xihao Liang  | auth.py channel.py channels.py     |
     | Wei Wei      | auth.py user.py other.py           |

  2. Determine the way to generating token and password.
  3. Discussed and reflected on the first iteration's problems.

- Questions (ask tutor by email):

  - [x] what is the meaning of more about functionality of system.
  - [x] How to use ARC to test token after using jwt.
  - [x] How to enter the input when the method is 'Get'.

- Next meeting time: 21/10/2020

## 2020/10/21 Wednesday meeting05

- Main topic: Fixing and discussing about bugs in server.py and http testing.

- Answers of question:

  - the token from jwt is bytes insted of string, therefore, we cant test it

- Summary of meeting:

  1. Help each other for testing http function
  2. Some group member can't run http testing, and had a discussion about how
     to fix it.

- Questions (ask tutor by email):

  - [x] when port = 0, clear doesn't matter in testing
  - [x] How to raise error in http testing
  - [x] Shold we store the data in json form offline,
        or we just need to transfer it into json when connecting to the network.

- Next meeting time: 22/10/2020

## 2020/10/22 Thursday meeting06

- Main topic: finish http test and then finsh functions for all files

- Answers of question:

  - we can indicate error reson with something like assert "Invalid token" in payload4.get("message").
  - werkzeug.exceptions appears to just be a module handling errors raised by flask functions,
    dont need to worry about it too much.
  - It is not necessary to store data persistently
    (meaning restarting the server can reset the data to empty if its easier).

- Summary of meeting:

  1. Each member in the group finished the http tests for seperate files and wrote functions for server.py
  2. Each member in the group merged their http tests to the Develop branch,
     and do the same procedure for server.py.

- Questions (ask tutor by email):

  - [ ] We try to indicate the error situation with the code like: assert resp_structure_code == TypeError.code,
        is it reasonable?
        v

- Next meeting time: to be continue ➡
