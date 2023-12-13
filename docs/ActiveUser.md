# Active User

Active User is the mechanism that allows you to keep track of the user that is currently logged in. It is likely a stopgap solution to the auth problem but it works for now.

## Logging in

To log in a user you use the UserService.login() method. This method takes in a username and password and returns a User object if the login was successful. If the login was unsuccessful it will raise a `AuthenticationError` exception.

## Accessing the currently logged in user

To access the currently logged in user you use the ActiveUser.get() method. This method returns a User object if there is a user logged in. If there is no user logged in it will raise a `AuthenticationError` exception.

## Checking permissions 

To check the permissions of the currently logged in user you would use `ActiveUser.get().has_permission(permission)`. This method takes in a permission string and returns a boolean. If the user has the permission it will return true, otherwise it will return false. You could also use
`ActiveUser.get().raise_without_permission(permission)` which will raise a `AuthorizationError` if the user does not have the permission. See [[Permissions]] for more information on permissions.

## Logging out

To log out a user you use the `UserService.logout()` method. 

