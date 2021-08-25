We implement admin/user/remove.
Given a User by their user ID, a global owner can remove the user from the slackr.
There are two types of errors for admin/user/remove:
InputError when:u_id does not refer to a valid user
AccessError whenThe authorised user is not an owner of the slackr


|Function Name|HTTP Method|Parameters|Return type|Exceptions|Description|
|------------|-------------|----------|-----------|----------|----------|
|admin/user/remove|DELETE|(token, u_id)|{}|**InputError** when:<li>u_id does not refer to a valid user</li>**AccessError** when:<li> the authorised user is not an owner of the slackr</li>|Given a User by their user ID, remove the user from the slackr.|
​