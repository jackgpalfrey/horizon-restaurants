# Styleguide 

## PEP8
In general follow PEP8. I'd recommend using an autopep8 linter to ensure you are in compliance. Below are some of the more important rules if you can't be bothered to read the whole thing.

---

## Pascal Case For Classes
```python
# Correct
class MyClass:
    pass

# Incorrect
class myClass:
    pass
```

---
  
## All Caps Snake Case For Constants
```python
# Correct
MY_CONSTANT = 1

# Incorrect
my_constant = 1
```

---

# Snake Case prefaced with _ for private properties and methods
```python
# Correct
class MyClass:
    def __init__(self):
        self._my_private_property = 1

    def _my_private_method(self):
        pass

# Incorrect
class MyClass:
    def __init__(self):
        self.my_private_property = 1

    def my_private_method(self):
        pass
```

---
  
## Snake Case For Everything Else
```python
# Correct
my_variable = 1

# Incorrect
myVariable = 1
```

---

## Avoid magic literals
```python
# Correct
PI = 3.14
radius = 10

area = math.pi * radius ** 2

# Incorrect
area = 3.14 * 10 ** 2
```

---

## Consistent function prefixes (e.g. create, get, set, etc.)
- Get for short get operations
- Fetch for longer get operations (e.g from database or REST api)
- Set for setting a property of an object
- Check for functions that return a boolean
- Create for creating a new object
- Update for updating an existing object
- Delete for deleting something

---

## Think about your variable names and function names for the love of god
  - Avoid "i", "temp", "arr" etc
  - Avoid single letter variables unless they are used in a loop where the iteration is irrelevant
  - Prefer verbosity over briefness
  - Preface booleans with is_ or has_
  - Arguements, class attributes and return values should have type hints

---

## 4 spaces for indentation
4 spaces discourages deep nesting. That's a good thing

---

## Use type hints always
Always use type hints in function definitions and class attributes. This makes it easier to understand what a function does and what it returns. It also makes it easier to catch bugs. You can exclude it for `self` and `cls` in methods.

```python
# Correct
def my_function(my_arg: int) -> str:
    return str(my_arg)

# Incorrect
def my_function(my_arg):
    return str(my_arg)
```

---

## Use docstrings when typehints and function name is insufficent   
  - You should not need to read the code to understand what a function does including any quirks.
  - Ensure when changing a function the docstring is still accurate

---

## Use comments as an absolute last resort
If you use comments they should be explaining why not what. If you need to explain what the code does you should refactor it to be more self descriptive. If you need to explain why make sure you can't refactor to make it more obvious.

---

## Prefer guard clauses over if else when possible (generally minimise nesting)
```python
# Correct
def my_function(my_arg: int) -> str:
    if my_arg == 0:
        return "zero"

    if my_arg > 20:
        return "huge"
    
    if my_arg > 10:
        return "big"

    return "tiny"

# Incorrect
def my_function(my_arg: int) -> str:
    result = ""

    if my_arg == 0:
        result = "zero"
    elif my_arg > 20:
        result = "huge"
    elif my_arg > 10:
        result = "big"
    else:
        result = "tiny"
```

---

## Prefer switch (match) statements over elif when possible
```python
# Correct
def my_function(my_arg: int) -> str:
    match my_arg:
        case 0:
            return "zero"
        case 5:
            return "five"
        case 10:
            return "ten"
        case _:
            return "other"

# Incorrect
def my_function(my_arg: int) -> str:
    result = ""

    if my_arg == 0:
        result = "zero"
    elif my_arg == 5:
        result = "five"
    elif my_arg == 10:
        result = "ten"
    else:
        result = "other"
```

---

## When using try except prefer catching specific errors rather than a bare except, 
When you want to catch all errors use `except Exception` rather than `except:`. This is because `except:` will catch all errors including `KeyboardInterrupt` and `SystemExit` which you probably don't want to catch. 

```python
# Correct
try:
    do_something()
except ValueError:
    handle_value_error()
except TypeError:
    handle_type_error()

# Incorrect
try:
    do_something()
except:
    handle_error()
```

---

## Split complex conditionals into their own variables
```python
# Correct
IS_ONLINE_ADMIN = user.is_admin() and user.is_online()
IS_AVAILABLE = not user.is_budy() and not user.is_away()

if IS_ONLINE_ADMIN and IS_AVAILABLE:
    do_something()

# Incorrect
if user.is_admin() and user.is_online() and not user.is_busy() and not user.is_away():
    do_something()
```

---

## Other
- Use Python 3.10
- Use `_` for throwaway arguments
- Always close files or even better use `with` syntax
- Avoid global variables at all costs
- Prefer f strings over .format and string concatenation
- Prefer "" over ''
- Keep it DRY and follow SRP, generally minimise side effects.
- Pefer `is not` over `not ... is`
- Prefer `is None` over `== None`
- Prefer `if bool` and `if not bool` over `if bool == True`
- Prefer dict.get() over dict[]
- REFACTOR, REFACTOR, REFACTOR
- Remember lists and dicts are passed by ref not value