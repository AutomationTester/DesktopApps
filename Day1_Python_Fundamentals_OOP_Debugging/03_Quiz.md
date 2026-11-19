# Day 1 Quiz - Python Fundamentals, OOP and Debugging

**Instructions:** 20 multiple-choice questions. Choose **one** answer for each. Time: 15-20 minutes.
The answer key with explanations is at the bottom. Please do not scroll down until you have finished.

---

**1. Which statement about Python is TRUE?**
- A) Python code must be compiled before every run
- B) Python uses indentation to group blocks of code
- C) Python uses curly braces `{ }` to mark code blocks
- D) Python is not case-sensitive

**2. What does this code print?**
```python
print(type(3.0))
```
- A) `<class 'int'>`
- B) `<class 'float'>`
- C) `<class 'str'>`
- D) `3.0`

**3. What is the output?**
```python
qty = "5"
print(qty + "5")
```
- A) `10`
- B) `55`
- C) `TypeError`
- D) `5 5`

**4. What is the value of `17 % 5`?**
- A) `3.4`
- B) `3`
- C) `2`
- D) `85`

**5. Given `results = ["PASS", "FAIL", "SKIP"]`, what is `results[-1]`?**
- A) `"PASS"`
- B) `"FAIL"`
- C) `"SKIP"`
- D) `IndexError`

**6. Which data type is the best choice for one row of login test data such as username, password and expected result?**
- A) `set`
- B) `tuple` of numbers
- C) `dict`
- D) `bool`

**7. What does this expression return?**
```python
username_ok = True
password_ok = False
username_ok and not password_ok
```
- A) `True`
- B) `False`
- C) `None`
- D) `SyntaxError`

**8. What is printed?**
```python
crash_count = 4
if crash_count > 1:
    print("Medium")
elif crash_count > 3:
    print("High")
else:
    print("Low")
```
- A) `High`
- B) `Medium`
- C) `Medium` and `High`
- D) `Low`

**9. How many times does this loop print?**
```python
for step in range(1, 5):
    print(step)
```
- A) 3
- B) 4
- C) 5
- D) 6

**10. Which keyword stops a loop completely?**
- A) `continue`
- B) `pass`
- C) `break`
- D) `return False`

**11. What does a Python function return if it has no `return` statement?**
- A) `0`
- B) `False`
- C) An empty string `""`
- D) `None`

**12. Given `def log(message, level="INFO"):`, which call is INVALID?**
- A) `log("Started")`
- B) `log("Started", "DEBUG")`
- C) `log(level="ERROR", message="Crash")`
- D) `log()`

**13. In OOP, what is an object?**
- A) A blueprint that defines attributes and methods
- B) An instance created from a class
- C) A built-in Python keyword
- D) A special kind of loop

**14. When does `__init__` run?**
- A) Only when you call `obj.__init__()` yourself
- B) When the program ends
- C) Automatically, when a new object is created
- D) Every time any method of the object is called

**15. What does `self` refer to inside an instance method?**
- A) The class itself
- B) The current object
- C) The parent class
- D) The Python interpreter

**16. What is the purpose of `super().__init__(title)` inside a child class constructor?**
- A) It creates a second, separate object
- B) It runs the parent class constructor, so the parent's attributes are set up
- C) It deletes the parent class
- D) It makes all attributes private

**17. Which option BEST describes encapsulation in Python?**
- A) Writing all code in one file
- B) Bundling data with the methods that control it, and protecting it with `_name` or `@property`
- C) One class inheriting from another
- D) Using many `print()` statements

**18. Which code raises a `KeyError`?**
- A) `[1, 2, 3][5]`
- B) `{"user": "admin"}["password"]`
- C) `int("abc")`
- D) `"text" + 5`

**19. In the VS Code debugger, what does Step Into (F11) do?**
- A) Runs the whole program without stopping
- B) Runs the current line in one go and stops at the next line
- C) Moves inside the function being called on the current line
- D) Removes all breakpoints

**20. In `try / except / else / finally`, which block ALWAYS runs, whether an error happened or not?**
- A) `try`
- B) `except`
- C) `else`
- D) `finally`

---
---

## Answer Key

| Q | Answer | Explanation |
|---|--------|-------------|
| 1 | **B** | Python uses indentation (usually 4 spaces) to define blocks. It is interpreted and case-sensitive. |
| 2 | **B** | `3.0` has a decimal point, so it is a `float`. |
| 3 | **B** | Both values are strings, so `+` joins them: `"5" + "5"` gives `"55"`. |
| 4 | **C** | `%` gives the remainder: 17 = 5 x 3 + **2**. |
| 5 | **C** | A negative index counts from the end. `-1` is the last item. |
| 6 | **C** | A dictionary maps names to values, for example `{"username": ..., "password": ..., "expected": ...}`. |
| 7 | **A** | `not False` is `True`, and `True and True` is `True`. |
| 8 | **B** | The first True condition wins. `4 > 1` is True, so `elif` is never checked. (This is a logic bug if `High` was intended.) |
| 9 | **B** | `range(1, 5)` gives 1, 2, 3 and 4. The stop value is not included. |
| 10 | **C** | `break` exits the loop. `continue` only skips to the next round. |
| 11 | **D** | Without `return`, a function returns `None`. |
| 12 | **D** | `message` has no default value, so it must be given. `log()` raises a `TypeError`. |
| 13 | **B** | The class is the blueprint, and an object is an instance made from it. |
| 14 | **C** | Python calls the constructor automatically, for example at `AppWindow("Calculator")`. |
| 15 | **B** | `self` is the object the method was called on. Python passes it automatically. |
| 16 | **B** | Without it, parent attributes such as `self.title` are never created, which leads to an `AttributeError`. |
| 17 | **B** | Encapsulation means keeping data together with its rules and controlling access to it. Option C describes inheritance. |
| 18 | **B** | Accessing a missing dictionary key raises `KeyError`. The others raise IndexError, ValueError and TypeError. |
| 19 | **C** | Step Into enters the called function. Step Over (F10) runs the line in one go. |
| 20 | **D** | `finally` always runs, which makes it the place for cleanup such as closing the application. |

**Scoring guide:** 17-20 excellent | 13-16 good, revise weak areas | below 13 re-read the handbook and redo the labs.
