# Day 1 - Hands-on Lab Guide

**Course:** Python Desktop Application Automation Testing
**Day 1:** Python Fundamentals, OOP and Debugging

---

## Before you start

1. Open the folder `Day1_Python_Fundamentals_OOP_Debugging` in VS Code (**File > Open Folder**).
2. Open a terminal in VS Code (**Terminal > New Terminal**, or press ``Ctrl+` ``).
3. Move into the starter folder:
   ```
   cd hands_on\starter
   ```
4. Run a lab file with:
   ```
   python lab1_calculator.py
   ```
5. Work **only** in the `starter` folder. The `solutions` folder has the answers. Try on your own first.

| Lab | Topic (syllabus mapping) | File(s) | Time |
|-----|--------------------------|---------|------|
| Lab 1 | **Calculator using functions** | `lab1_calculator.py` | 40 min |
| Lab 2 | **OOP-based business logic** | `lab2_bank_account.py` | 50 min |
| Lab 3 | **Debugging faulty scripts** | `lab3_bug1_...` to `lab3_bug5_...` | 45 min |
| Lab 4 | Extra practice: loops, dicts and functions | `lab4_test_result_analyzer.py` | 30 min (optional / homework) |
| Lab 5 | Extra practice: exception handling | `lab5_safe_test_data_loader.py` | 30 min (optional / homework) |

> **Working rule for every lab:** make one small change, run the file, read the output. Repeat. Do not write 50 lines and then run the file for the first time.

---

## Lab 1 - Calculator using Functions

**Objective:** Write small, reusable functions. Call them from one "dispatcher" function. Check them with a data-driven self-test, the same way an automated test suite works.

**Estimated time:** 40 minutes

**Concepts used:** functions, parameters, return values, `if` conditions, dictionaries, `raise`, `try/except`, loops.

### Steps

1. Run the starter file as it is: `python lab1_calculator.py`.
   Most of the tests show `FAIL` with `actual=None`. That is expected. A function with no `return` gives back `None`.
2. **Task 1 - basic operations.** Complete `subtract`, `multiply` and `divide`.
   - In `divide`, if `b == 0`, run `raise ZeroDivisionError("Cannot divide by zero")`.
3. **Task 2 - extra operations.** Complete `power` (use `**`), `modulus` (use `%`, and raise `ZeroDivisionError` when `b == 0`) and `percentage`.
4. **Task 3 - dispatcher.** Add the missing operators to the `OPERATIONS` dictionary:
   ```python
   OPERATIONS = {"+": add, "-": subtract, "*": multiply, "/": divide, "**": power, "%": modulus}
   ```
   Then complete `calculate()`:
   - If the operator is not in the dictionary, `raise ValueError(f"Unsupported operator: {operator!r}")`.
   - Otherwise look up the function and return `function(a, b)`.
5. Run the file again. All tests except `CALC_07` should now pass.
6. **Task 5 - the float trap.** `CALC_07` fails because `0.1 + 0.2` gives `0.30000000000000004` on a computer. Change the comparison so that float values are compared with a small tolerance:
   ```python
   if isinstance(expected, float) and isinstance(actual, float):
       ok = abs(expected - actual) < 1e-9
   else:
       ok = expected == actual
   ```

### Expected output

```
============================================================
 CALCULATOR SELF-TEST
============================================================
 CALC_01  10 + 5     expected=15                 actual=15                   PASS
 CALC_02  10 - 15    expected=-5                 actual=-5                   PASS
 CALC_03  6 * 7      expected=42                 actual=42                   PASS
 CALC_04  9 / 2      expected=4.5                actual=4.5                  PASS
 CALC_05  2 ** 10    expected=1024               actual=1024                 PASS
 CALC_06  17 % 5     expected=2                  actual=2                    PASS
 CALC_07  0.1 + 0.2  expected=0.3                actual=0.30000000000000004  PASS
 CALC_08  5 / 0      expected=ZeroDivisionError  actual=ZeroDivisionError    PASS
 CALC_09  5 ^ 2      expected=ValueError         actual=ValueError           PASS
------------------------------------------------------------
 Passed 9/9  (100.0%)
 Overall: ALL TESTS PASSED
```

### Hints

- A function that only has `pass` returns `None`.
- Dictionary values can be **functions**. Write the function name **without** brackets: `"+": add`, not `"+": add()`.
- `OPERATIONS[operator]` gives you the function. `OPERATIONS[operator](a, b)` calls it.
- In the self-test, a `ZeroDivisionError` or `ValueError` is caught. Its **name** is stored as the actual result. This is how we test negative scenarios.

### Stretch goals

1. Add a `square_root(a)` function. Raise `ValueError` for negative numbers. Add a test row for it.
2. Add an **interactive mode**. When the script is started with `python lab1_calculator.py --interactive`, it should ask for two numbers and an operator using `input()` in a `while` loop, until the user types `q`. (The solution file shows one way to do this.)
3. Add 3 more test rows of your own, including one negative number case.

---

## Lab 2 - OOP-based Business Logic (PyBank)

**Objective:** Turn written business rules into classes, objects, methods, encapsulation and inheritance. Then check each rule with automated checks, like test cases.

**Estimated time:** 50 minutes

**Concepts used:** class, object, `__init__`, attributes, methods, `@property`, protected attributes (`_balance`), inheritance, `super()`, method overriding, custom exceptions.

### Business rules (requirements)

| Rule | Description |
|------|-------------|
| R1 | An account has an account number, holder name and an opening balance (default 0). A negative opening balance is not allowed. |
| R2 | `deposit(amount)`: the amount must be > 0, otherwise raise `ValueError`. |
| R3 | `withdraw(amount)`: the amount must be > 0. You cannot withdraw more than the available balance. If you try, raise `InsufficientFundsError`. |
| R4 | The balance must not be changed directly from outside the class. It is read-only through the `balance` property. |
| R5 | Every successful deposit or withdrawal is saved in the transaction history. |
| R6 | `SavingsAccount` must always keep a minimum balance of 1000. It can add interest (4% per year by default). |
| R7 | `CurrentAccount` allows an overdraft up to a limit (default 5000). |

### Steps

1. Run the starter: `python lab2_bank_account.py`. You will see `Passed 3/16` and some `ERROR` lines.
2. **R1** - in `Account.__init__`, raise `ValueError` if `opening_balance < 0`.
3. **R2/R3 validation** - complete `_validate_amount`. Raise `ValueError` when the amount is not an `int`/`float`, or when it is `<= 0`.
4. **R2, R5** - complete `deposit()`: validate, add to `self._balance`, record `"DEPOSIT"`, return the new balance.
5. **R3, R5** - complete `withdraw()`: validate, check `self.available_to_withdraw()`, subtract, record `"WITHDRAW"`, return the new balance.
6. Run again. Checks BR_01 to BR_10 should pass.
7. **R6** - complete `SavingsAccount`:
   - In `__init__`, call `super().__init__(account_no, holder, opening_balance)` and store `interest_rate`.
   - **Override** `available_to_withdraw()` so that it returns `max(0, self._balance - self.MIN_BALANCE)`.
   - Complete `add_interest()`.
8. **R7** - complete `CurrentAccount` with its own `__init__` (with `overdraft_limit=5000`) and an overridden `available_to_withdraw()` that returns `self._balance + self.overdraft_limit`.
9. Run again. Target: `Passed 16/16`.

### Expected output (final)

```
 BR_01  Opening balance is stored                               PASS
 ...
 BR_16  Current: cannot exceed overdraft limit                  PASS
------------------------------------------------------------------------
 Passed 16/16
```

The solution also prints an account statement and the `__str__` of each object.

### Hints

- `withdraw()` does not need to know the account type. It only calls `self.available_to_withdraw()`. Each child class gives its own answer. This is **polymorphism**, and it is the reason inheritance is so useful.
- BR_09 passes on its own because `balance` is a property **without a setter**. Try `acc.balance = 100` in your code and read the error message.
- If you see `AttributeError: 'SavingsAccount' object has no attribute '_balance'`, you forgot `super().__init__(...)`.

### Stretch goals

1. Add a `transfer(self, other_account, amount)` method. It should withdraw from one account and deposit into the other.
2. Add a daily withdrawal limit of 20,000 to `SavingsAccount`, and add a check for it.
3. Add `__len__` so that `len(account)` returns the number of transactions.

---

## Lab 3 - Debugging Faulty Scripts

**Objective:** Find and fix syntax errors, runtime errors and logic errors. Use tracebacks, print-based debugging and the VS Code debugger.

**Estimated time:** 45 minutes (Bug 5 is a bonus)

### Method: follow these steps for every bug

1. **Run** the script and read the output.
2. If there is a traceback, read the **last line** first (error type and message). Then read the **line number** just above it.
3. If there is no error but the output is wrong, compare **expected vs actual**. Add `print()` lines or set a **breakpoint** (F9) and press **F5**. Then use **F10** (step over) and **F11** (step into), and watch the Variables panel.
4. Fix **one** bug, run the script again, and repeat. Python shows errors one at a time.

| File | Bug type | Number of bugs |
|------|----------|----------------|
| `lab3_bug1_syntax_error.py` | Syntax errors | 4 |
| `lab3_bug2_key_error.py` | Runtime - `KeyError` | 2 |
| `lab3_bug3_type_error.py` | Runtime - `TypeError` | 3 |
| `lab3_bug4_logic_error.py` | Logic errors (no crash) | 3 |
| `lab3_bug5_oop_error.py` (bonus) | OOP mistakes | 3 |

Each starter file shows the **expected output** in its docstring.

### Bug explanations (trainer reference - try first!)

<details>
<summary><b>Bug file 1 - Syntax errors</b></summary>

| # | Faulty code | Python message | Fix |
|---|-------------|----------------|-----|
| 1 | `print("Window availability check"` | `SyntaxError: invalid syntax` reported on a **later** line (the `if` line) | Add the closing `)`. **Lesson:** the real mistake can be on a line *above* the reported one. |
| 2 | `for window in expected_windows` | `SyntaxError: expected ':'` | Add `:` at the end of the line. |
| 3 | `print(f"{window}: MISSING)` | `SyntaxError: unterminated f-string literal` | Close the string: `MISSING")` |
| 4 | `if missing_count = 0:` | `invalid syntax. Maybe you meant '==' or ':=' instead of '='?` | Use `==` to compare. `=` is for assignment. |

Syntax errors stop the **whole** file from running. Not even the first line runs.
</details>

<details>
<summary><b>Bug file 2 - KeyError</b></summary>

1. `KeyError: 'password'` - the third test-data row has the key `"pasword"` (a typo). This is a **test data bug**. Fix the data.
2. `KeyError: 'guest'` - `registered_users[username]` crashes when the user does not exist. Testing an unknown user is a valid negative test, so the **code** must handle it. Use `registered_users.get(username)`, which returns `None` instead of raising an error.

**Lesson:** a failure is not always a code bug. Check the test data too.
</details>

<details>
<summary><b>Bug file 3 - TypeError</b></summary>

1. `can only concatenate str (not "int") to str` - `"Suite " + ... + passed` joins text and a number. Use an f-string.
2. `unsupported operand type(s) for /: 'str' and 'str'` - the Billing values are text (`"7"`, `"2"`). `"7" + "2"` gives `"72"`: the strings are joined, not added. Convert them with `int()`.
3. `build_summary() missing 1 required positional argument: 'failed'` - the Reports call passes only 2 arguments. Pass `0` for `failed`.

**Lesson:** values read from files, screens and text boxes are **strings**. Convert them before you do maths.
</details>

<details>
<summary><b>Bug file 4 - Logic errors</b></summary>

1. `classify_response(4.5)` returns `SLOW`. The conditions are in the wrong order: `4.5 > 1` is already True, so `> 3` is never checked. Check the biggest limit first.
2. `count_failures(["FAIL","PASS","FAIL"])` returns 1. `range(1, len(results))` skips index 0. This is an **off-by-one** error. Loop over the list directly.
3. `all_passed(["PASS","FAIL"])` returns True. The function returns at the first `PASS`. Instead, return `False` at the first non-PASS, and return `True` only after the loop has finished.

**Debugger tip:** put a breakpoint inside `count_failures`, press F5, then F10. Watch `i` - it starts at 1.
</details>

<details>
<summary><b>Bug file 5 (bonus) - OOP mistakes</b></summary>

1. `TypeError: ... takes 1 positional argument but 2 were given` - `def enter_username(username)` is missing `self`.
2. `AttributeError: 'LoginWindow' object has no attribute 'title'` - the child `__init__` does not call `super().__init__(title)`.
3. No error, but the output shows `open=False`. `window.open` without `()` does not call the method. Use `window.open()`.
</details>

### Stretch goals

1. Choose any working script from `examples/`. Add one bug of your own and swap files with a partner. Time how long each of you takes to find the other's bug.
2. For bug file 4, write one extra check that would have caught each bug even earlier (for example, a response time of exactly 3 seconds).

---

## Lab 4 (Extra) - Test Result Analyzer

**Objective:** Practise lists, dictionaries, loops and functions on realistic test execution data.

**Estimated time:** 30 minutes

### Steps

1. Run the starter. The report prints, but the counts are 0 and the module table is empty.
2. Complete `count_by_status` using `counts[status] = counts.get(status, 0) + 1`.
3. Complete `pass_percentage`. Use only executed tests (PASS + FAIL), and protect against division by zero.
4. Complete `failed_test_ids`. A list comprehension is fine here.
5. Complete `slowest_test` by looping and keeping the biggest `duration`.
6. Complete `module_summary`. It is a dictionary of dictionaries.

### Expected output

```
 Total tests : 8
 PASS        : 5
 FAIL        : 2
 SKIP        : 1
 Pass %      : 71.4%
 Failed      : TC_202, TC_206
 Slowest     : TC_206 (9.6s)
--------------------------------------------------
 Module      PASS  FAIL  SKIP  Health
 Login          1     1     0  ATTENTION
 Billing        2     0     1  OK
 Reports        1     1     0  ATTENTION
 Settings       1     0     0  OK
==================================================
 Build status (needs >= 80% pass): REJECTED
```

### Hints

- `dict.get(key, default)` returns the default value when the key is missing.
- `", ".join(list_of_strings)` joins a list into one string.

### Stretch goals

- Print the average duration of executed tests.
- Sort the failed tests by duration, slowest first. Use `sorted(..., key=lambda r: r["duration"], reverse=True)`.

---

## Lab 5 (Extra) - Safe Test Data Loader

**Objective:** Use `try / except / else / finally` and custom exceptions. A test-data loader should not crash because of one bad row.

**Estimated time:** 30 minutes

### Steps

1. Run the starter. It **crashes** with `ValueError: invalid literal for int() ... 'ten'`.
   (The starter also leaves a temporary file in your TEMP folder. TODO 6 fixes that.)
2. TODO 1-3: in `parse_row`, raise `InvalidTestDataError` for a wrong column count, an empty username and a wait time that is not positive.
3. TODO 4: in `load_test_data`, catch `FileNotFoundError` around `open()`.
4. TODO 5: wrap `parse_row(...)` in `try / except ValueError / except InvalidTestDataError / else`.
5. TODO 6: in `main`, use `try / finally` so that the temporary file is **always** deleted.

### Expected output

```
VALID ROWS:
  TC_301  user=admin    wait=5s
  TC_306  user=viewer   wait=8s

REJECTED ROWS:
  - line 3: not a number -> invalid literal for int() with base 10: 'ten'
  - line 4: expected 4 columns, got 2
  - line 5: username is empty
  - line 7: wait_seconds must be positive, got -2

Loaded 2 valid rows, rejected 4.

Missing file check:
  - File not found: no_such_file.csv

Cleanup: temporary data file deleted.
```

### Hints

- The `else` block runs only when the `try` block raised **no** exception. That is the right place to append a valid row.
- The order of the checks matters. Check the column count **before** you unpack `parts` into 4 variables.

### Stretch goals

- Save the rejected rows into a `rejected_rows.log` file in the TEMP folder.
- Add a rule that the password must be at least 6 characters long.

---

## End-of-day checklist

- [ ] I can run a Python file from the VS Code terminal.
- [ ] I can write a function with parameters and a return value.
- [ ] I can create a class with `__init__`, attributes and methods, and make objects from it.
- [ ] I can make a child class with `super().__init__()` and override a method.
- [ ] I can read a traceback and name the error type.
- [ ] I can set a breakpoint, step over (F10) and step into (F11).
- [ ] I can use `try / except / finally`.
