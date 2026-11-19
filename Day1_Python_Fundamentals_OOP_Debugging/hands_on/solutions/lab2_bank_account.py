"""
Lab 2 - OOP-based Business Logic: Bank Accounts (SOLUTION)
===========================================================
How to run:
    python lab2_bank_account.py

Business rules (the "requirements" a tester would get):
    R1  An account is created with an account number, holder name and
        an opening balance (default 0). Opening balance cannot be negative.
    R2  deposit(amount): amount must be > 0, otherwise raise ValueError.
    R3  withdraw(amount): amount must be > 0; cannot withdraw more than the
        available balance -> raise InsufficientFundsError.
    R4  Balance must NOT be changeable directly from outside (encapsulation).
        It is read-only through the 'balance' property.
    R5  Every successful deposit/withdrawal is recorded in a transaction history.
    R6  SavingsAccount (child of Account) must keep a minimum balance of 1000
        and can add interest (4% per year by default).
    R7  CurrentAccount (child of Account) allows an overdraft up to a limit
        (default 5000), i.e. balance may go down to -overdraft_limit.

At the bottom, a set of CHECKS verifies each rule like automated test cases.
"""


class InsufficientFundsError(Exception):
    """Raised when a withdrawal would break the balance rules."""


class Account:
    """Parent class with the common banking behaviour."""

    bank_name = "PyBank"                  # class attribute shared by all accounts

    def __init__(self, account_no, holder, opening_balance=0):
        if opening_balance < 0:                                     # R1
            raise ValueError("Opening balance cannot be negative")
        self.account_no = account_no
        self.holder = holder
        self._balance = opening_balance    # protected - use the property  (R4)
        self._transactions = []            # history                        (R5)
        if opening_balance:
            self._record("OPEN", opening_balance)

    # ------------ encapsulation: read-only balance ------------
    @property
    def balance(self):
        return self._balance

    @property
    def transactions(self):
        return list(self._transactions)   # return a COPY so callers cannot edit history

    # ------------ helper methods ------------
    def _record(self, kind, amount):
        self._transactions.append((kind, amount, self._balance))

    @staticmethod
    def _validate_amount(amount):
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise ValueError(f"Amount must be a positive number, got {amount!r}")

    def available_to_withdraw(self):
        """How much can be withdrawn right now (child classes change this)."""
        return self._balance

    # ------------ business methods ------------
    def deposit(self, amount):                                      # R2
        self._validate_amount(amount)
        self._balance += amount
        self._record("DEPOSIT", amount)
        return self._balance

    def withdraw(self, amount):                                     # R3
        self._validate_amount(amount)
        if amount > self.available_to_withdraw():
            raise InsufficientFundsError(
                f"Cannot withdraw {amount}; available {self.available_to_withdraw()}")
        self._balance -= amount
        self._record("WITHDRAW", amount)
        return self._balance

    def statement(self):
        print(f"\n{self.bank_name} statement - {self.account_no} ({self.holder})")
        for kind, amount, balance_after in self._transactions:
            print(f"   {kind:9} {amount:>10.2f}   balance {balance_after:>10.2f}")
        print(f"   Closing balance: {self._balance:.2f}")

    def __str__(self):
        return f"{type(self).__name__}({self.account_no}, {self.holder}, balance={self._balance:.2f})"


class SavingsAccount(Account):                                      # R6
    MIN_BALANCE = 1000

    def __init__(self, account_no, holder, opening_balance=0, interest_rate=4.0):
        super().__init__(account_no, holder, opening_balance)
        self.interest_rate = interest_rate

    def available_to_withdraw(self):          # override: keep the minimum balance
        return max(0, self._balance - self.MIN_BALANCE)

    def add_interest(self, years=1):
        interest = round(self._balance * self.interest_rate / 100 * years, 2)
        if interest > 0:
            self.deposit(interest)
        return interest


class CurrentAccount(Account):                                      # R7
    def __init__(self, account_no, holder, opening_balance=0, overdraft_limit=5000):
        super().__init__(account_no, holder, opening_balance)
        self.overdraft_limit = overdraft_limit

    def available_to_withdraw(self):          # override: balance + overdraft
        return self._balance + self.overdraft_limit


# ======================================================================
# Automated checks - each one is like a test case for a business rule
# ======================================================================
results = []


def check(test_id, description, test):
    """Run test() (a lambda). PASS if it returns True; ERROR if it crashes."""
    try:
        status = "PASS" if test() else "FAIL"
    except Exception as error:               # an unexpected crash is also a result
        status = f"ERROR ({type(error).__name__})"
    results.append(status)
    print(f" {test_id:6} {description:55} {status}")


def raises(error_type, func, *args):
    """Return True if func(*args) raises error_type."""
    try:
        func(*args)
    except error_type:
        return True
    return False


if __name__ == "__main__":
    print("=" * 72)
    print(" BUSINESS RULE CHECKS - PyBank")
    print("=" * 72)

    acc = Account("AC001", "Anita", 500)
    check("BR_01", "Opening balance is stored", lambda: acc.balance == 500)
    check("BR_02", "Negative opening balance is rejected",
          lambda: raises(ValueError, Account, "AC002", "Ravi", -10))
    check("BR_03", "Deposit 1500 -> balance 2000", lambda: acc.deposit(1500) == 2000)
    check("BR_04", "Deposit 0 is rejected", lambda: raises(ValueError, acc.deposit, 0))
    check("BR_05", "Deposit of text '100' is rejected", lambda: raises(ValueError, acc.deposit, "100"))
    check("BR_06", "Withdraw 700 -> balance 1300", lambda: acc.withdraw(700) == 1300)
    check("BR_07", "Withdraw more than balance is rejected",
          lambda: raises(InsufficientFundsError, acc.withdraw, 5000))
    check("BR_08", "Balance unchanged after rejected withdrawal", lambda: acc.balance == 1300)
    check("BR_09", "Balance cannot be set directly",
          lambda: raises(AttributeError, setattr, acc, "balance", 1_000_000))
    check("BR_10", "History has OPEN, DEPOSIT, WITHDRAW",
          lambda: [t[0] for t in acc.transactions] == ["OPEN", "DEPOSIT", "WITHDRAW"])

    sav = SavingsAccount("SB001", "Kiran", 5000)
    check("BR_11", "Savings: withdraw 4000 is OK (1000 stays)", lambda: sav.withdraw(4000) == 1000)
    check("BR_12", "Savings: cannot go below minimum 1000",
          lambda: raises(InsufficientFundsError, sav.withdraw, 1))
    check("BR_13", "Savings: 4% interest on 1000 = 40", lambda: sav.add_interest() == 40)
    check("BR_14", "SavingsAccount is an Account (inheritance)", lambda: isinstance(sav, Account))

    cur = CurrentAccount("CA001", "Meera", 1000, overdraft_limit=2000)
    check("BR_15", "Current: overdraft withdraw 2500 -> -1500", lambda: cur.withdraw(2500) == -1500)
    check("BR_16", "Current: cannot exceed overdraft limit",
          lambda: raises(InsufficientFundsError, cur.withdraw, 600))

    print("-" * 72)
    print(f" Passed {results.count('PASS')}/{len(results)}")

    acc.statement()
    print("\nObjects:", acc, sav, cur, sep="\n  ")
