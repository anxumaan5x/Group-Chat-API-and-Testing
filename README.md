Group Chat APIs and Unit Testing. 

Developed by Anshuman Gogoi, email: anxumaan@gmail.com

How to Run:

1. Run “**pip install -r requirements.txt”** on the terminal to install all the dependencies.
1. Run **“flask run”** on the terminal to start the application. You can then test the APIs using Postman.
1. Execute the “**utest.py”** file to run the unit tests.



|***Sl No.***|***Endpoint***|***Functionality***|***POST Request Payload (if any)***|
| -: | :- | :- | :- |
|1|***/api/v1/signup***|Endpoint for sign up which creates new admin user|<p>{</p><p>`	`“username”: username,</p><p>`	`“password”: password<br>}</p>|
|2|***/api/v1/ login***|Endpoint for logging in users.|<p>{</p><p>`	`“username”: username,</p><p>`	`“password”: password<br>}</p>|
|3|***/api/v1/add\_user***|Endpoint for admins to create new users with default password.|<p>{</p><p>`	`“username”: username<br>}</p>|
|4|***/api/v1/change\_password***|Endpoint for users to change their password.|<p>{</p><p>`	`“password”: password,</p><p>`	`“new\_password”: new\_password<br>}</p>|
|5|***/api/v1/edit\_user***|Endpoint for admins to edit users.|<p>{</p><p>`	`“username”: username,</p><p>`	`“new\_username”: new\_username,</p><p>`	`“password”:password,</p><p>`	`“type”: type<br>}</p>|
|6|***/api/v1/logout***|Endpoint for logging out users.||
|7|***/api/v1/create\_group***|Endpoint for users to create new groups.|<p>{</p><p>`	`“groupname”: groupname</p><p>}</p>|
|8|***/api/v1/delete\_group/{id}***|Endpoint for users to delete particular group.||
|9|***/api/v1/search\_groups***|Endpoint for users to see the groups that they are a member of.||
|10|***/api/v1/add\_members/{group\_id}/{user\_id}***|Endpoint for users to add other users to a group.||
|11|***/api/v1/send\_message/{group\_id}***|Endpoint for users to send chat messages in a group.|<p>{</p><p>`	`“message”: message</p><p>}</p>|
|12|***/api/v1/like\_message/{chat\_id}***|Endpoint for users to like a chat message.||
|*13*|***/api/v1/view\_message/{group\_id}***|Endpoint for users to view all chats in a group.||


