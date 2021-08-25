# Meeting summary for lteration 3 2020

## 2020/10/30 Monday Meeting 01

- Main topic: Alocated jobs for iteration 3

- Summary of meeting:

  1. Browse the update of lteration 3 together.
  2. Determine the task for every member from 2020/10/30 to next meeting day:

     - Each member tries to work on five or six remaining functions.
     - Next meeting will discuss about the functions and tests and assign the functions to different people to write the final version.
     - Task Disturbution Form

     | Group memebr | draft code for seperate file      |
     | :----------- | :-------------------------------- |
     | Mingyuan Cui | message/pin/unpin/standup/user.py |
     | Haotian Lyu  | message.py uesr.py                |
     | Xing Shi     | message.py user.py                |
     | Xihao Liang  | standup.py auth.py user.py        |
     | Wei Wei      | standup.py auth.py  user.py       |

- Questions (ask tutor by email):

  - [] How to deal with email, should we use smtp, and reset password.
  - [] How to add picture, and check whether is valid, since frontend is not well done.
  - [] How to draw state dirgrame, since the final state is not sure, login or leave channel?

- Next meeting time: 2020/11/2 Monday

## 2020/11/2 Monday Meeting 02
- Main topic: push each member's work to the temp branch for iteration 3

- Answers of question:
  - We can use flask.mail or smtp to deal with email.
  - We can use PIL to deal with image.
  - State diagram should help explain how new features work, try to include anything relevent.


- Summary of meeting:

  1. Discuss on the new functions for iteration 3.
  2. Each member merged their work to the temp branch for iteration 3.
  3. Determine the task for every member from 2020/11/2 to next meeting day:

     - Each member tries to finish the http test for their previous work.
     - Next meeting will discuss about the further functions for iteration 4.
     - Task Disturbution Form

     | Group memebr | draft http test code for seperate file |
     | :----------- | :--------------------------------      |
     | Mingyuan Cui | message/pin/unpin/standup/user.py      |
     | Haotian Lyu  | message.py uesr.py                     |
     | Xing Shi     | message.py user.py                     |
     | Xihao Liang  | standup.py auth.py user.py             |
     | Wei Wei      | standup.py auth.py  user.py            |

- Questions (ask tutor by email):

  - [X] How to deal with local host, should we create a new email account for it?
  - [] How to test if we have upload some images and reset password?

## 2020/11/6 Friday Meeting 03 (lab)
- Main topic： http test for message and stand up and message_sendlater.

- Answers of questions:
  - we can create a new email account with dummy password.
  - we can show the tutor when we do the presentation.

- Summary of meeting:
  
  1. Discuss about the question during the http test.
  2. Dealing with the sendlater which had problem that no returns.
  3. try the connections between backend and frontend to test the message functions in iteration 3.
  4. try to solve the problems on upload images.
 
- Questions (ask tutor by email):
  
  - [X] Why the photo we try to uploead no error but the frontend can't show and the ARC's output is garbled.

- Next meeting time: 2020/11/09 Monday.

## 2020/11/9 Monday Meeting 04
- Main topic： Finish all the functions and test for all files.

- Answers of questions:
  - The problem on upload photo is solved, and it works both ARC and frontend

- Summary of meeting:
  
  1. Discuss about how to send the standup message, at the end we didn't find a new solution and back to the old ways of using standup active
  2. Discuss about how to test sendlater.
  3. Mingyuan theoretically find out that there might be some problem in send later, but after testing in frontend it shows no problem.
  4. We create a new branch for each different new feature.
  5. Implement the new function and tests in the new branches.
  6. After confirming the pylint and coverage meet the requirment, we merge the branches to Develop
 
- Questions (ask tutor by email):
  
  - [X] Can send later be implemented like this.
  - [X] Can the standup message to be send in standup active

- Next meeting time: 2020/11/13 Friday.

## 2020/11/13 Friday Meeting 05
- Main topic： Collect user's stories and draw state diagram.

- Answers of questions:
  - The problem on send_later is solved, and it works both ARC and frontend
  - standup message's issus is fixed.

- Summary of meeting:
  
  1. Make choice of user's stories.
  2. Base on the functionality we implemented, we draw the state diagram to show the relationship of seperate functions. 
  3. Rearrange the template the user's stories.
 
- Questions (ask tutor by email):
  
  - [] Does our state diagram correct or not?

- Next meeting time: 2020/11/14 Saturday.