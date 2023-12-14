# Permissions

The permission system is based off the yaml files under `config/roles/`. Each file represents a role, and each role has a set of permissions. The permissions are defined in the `permissions` section of the role file. Each permission is a string that represents a permission. A role file also consists of a required id field, a required name field and an optional extends field. 

## Inheritance

Roles support inheritance through the `extends` field. The extends field can either have an integer value representing the id of a role to inherit from or an integer array of ids to inherit from. The role will inherit all permissions from the role(s) it extends from.

## Explict Wildcard

The permission system supports an explict wildcard. By adding `.*` as a permission to a role it will give the role all permissions. Note permission negation does override this. See Permission Precedence for more information.

## Implicit Wildcards

The permission system supports implicit wildcards. This means that if a role has the `order` permission it will also have the `order.create` permission along with all other permissions following the `order.*` pattern. This is useful for giving a role all permissions for a specific resource. Note permission negation does override this. See Permission Precedence for more information.

## Permission Negation

By prefacing a permission with a `~` it will negate the permission. This means that if a role has the `order` permission but not the `~order.create` permission it will not have the `order.create` permission but will have everything else under `order.*` This is useful for giving a role all permissions for a specific resource except for a few. Note that negation overrides the explict and implicit wildcards. See Permission Precedence for more information.

## Permission Precedence

The permission system handles precedence in order of specificity. E.g `account.update.self` will override `account.update` which will override `account` etc. Explicit wildcards have the lowest precedence. 

## Permission Checks

To check a permission you have two methods available to you. `user.check_permission(permission: str)` and `user.raise_without_permission(permission: str)`. The first method will return a boolean value representing if the user has the permission or not. The second method will raise a `AuthorizationError` exception if the user does not have the permission.

## All Current Permissions

To add more create an issue on github. 

- `account.view.self` - View your own account - Staff
- `account.view.all` - View any account - Admin
- `account.create` - Create a new account - Admin
- `account.update.self` - Update your own account - Staff
- `account.update.all` - Update any account - Admin
- `account.update-role.all` - Update any account's role - Admin
- `account.delete.all` - Delete an account - Admin

- `report.view` - View and generate reports - Manager

- `discount.create` - Create a new discount - Manager
- `discount.update` - Update a discount - Manager
- `discount.delete` - Delete a discount - Manager

- `event.view` - View events - Manager
- `event.create` - Create a new event - Manager
- `event.update` - Update an event - Manager
- `event.delete` - Delete an event - Manager

- `table.create` - Create a new table - Manager
- `table.delete` - Delete a table - Manager
- `table.update` - Update a table - Manager

- `menu.category.create` - Create a new menu category - Chef
- `menu.category.update` - Update a menu category - Chef
- `menu.category.delete` - Delete a menu category - Chef
- `menu.item.create` - Create a new menu item - Chef
- `menu.item.update` - Update a menu item - Chef
- `menu.item.delete` - Delete a menu item - Chef

- `inventory.view` - View inventory - Kitchen Staff
- `inventory.create` - Create a new inventory item - Kitchen Staff
- `inventory.delete` - Delete an inventory item - Kitchen Staff
- `inventory.update` - Update an inventory item - Kitchen Staff
- `inventory.update.quantity` - Update an inventory item's quantity - Kitchen Staff

- `order.view` - View orders - Staff
- `order.make` - Create a new order and manipulate it - Frontend Staff
- `order.update` - Update an order after its been placed - Frontend Staff
- `order.update.status` - Update an order's status - Kitchen Staff
- `order.delete` - Delete/Cancel an order - Frontend Staff
- `order.discount` - Apply a discount to an order - Frontend Staff
- `order.discount-spot` - Apply an on the spot discount to an order - Manager

- `city.create` - Create a new city - Admin
- `city.update` - Update a city - Admin
- `city.delete` - Delete a city - Admin

- `branch.view` - View branches - Staff
- `branch.view.capacity` - View branch capacity - Staff
- `branch.create` - Create a new branch - Admin
- `branch.update` - Update a branch - Admin
- `branch.delete` - Delete a branch - Admin

- `reservation.view` - View reservations - Staff
- `reservation.create` - Create a new reservation - Frontend Staff
- `allbranches.reservation.create` - Create a new reservation at any branch - Manager
- `reservation.update` - Update a reservation - Frontend Staff
- `reservation.delete` - Delete a reservation - Frontend Staff

