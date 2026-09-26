"""
Example 15 - IDE Debugging Walkthrough (breakpoints, step over, step into)
===========================================================================
Day 1 | Topic: IDE debugging

How to use this file (VS Code):
    1. Open this file in VS Code.
    2. Click in the left margin (gutter) next to the line marked
       "BREAKPOINT 1" - a red dot appears.
    3. Press F5 -> choose "Python Debugger: Current File".
    4. The program pauses at the red dot. Look at the VARIABLES panel.
    5. Use the debug toolbar:
         F10  Step Over  -> run the current line, do NOT go inside functions
         F11  Step Into  -> go INSIDE the function called on this line
         Shift+F11 Step Out -> finish the current function, go back to caller
         F5   Continue   -> run until the next breakpoint
         Shift+F5 Stop
    6. Add "invoice_total" to the WATCH panel and watch it change.
    7. Try a CONDITIONAL breakpoint: right-click the red dot on
       "BREAKPOINT 2" -> Edit Breakpoint -> Expression: qty > 5

PyCharm: same idea - click the gutter, then Debug (Shift+F9);
         F8 = Step Over, F7 = Step Into, Shift+F8 = Step Out, F9 = Resume.

You can also run it normally:
    python 15_ide_debugging_walkthrough.py
"""


def line_total(price, qty, discount_percent):
    """Return the total for one invoice line after discount."""
    gross = price * qty                                   # BREAKPOINT 2 (conditional: qty > 5)
    discount = gross * discount_percent / 100
    net = gross - discount
    return round(net, 2)


def calculate_invoice(items):
    """Add up all line totals. Step INTO line_total() from here with F11."""
    invoice_total = 0
    for item in items:
        total = line_total(item["price"], item["qty"], item["discount"])   # BREAKPOINT 1
        invoice_total += total
        print(f"{item['name']:10} qty={item['qty']:<3} line total = {total:>8.2f}")
    return round(invoice_total, 2)


def main():
    # Test data for a billing desktop app (simulated)
    items = [
        {"name": "Keyboard", "price": 750.0, "qty": 2, "discount": 0},
        {"name": "Mouse", "price": 399.0, "qty": 10, "discount": 10},
        {"name": "Monitor", "price": 8999.0, "qty": 1, "discount": 5},
    ]
    expected_total = 1500.0 + 3591.0 + 8549.05
    actual_total = calculate_invoice(items)

    print(f"\nExpected total : {expected_total:.2f}")
    print(f"Actual total   : {actual_total:.2f}")
    print("Result         :", "PASS" if abs(expected_total - actual_total) < 0.01 else "FAIL")

    # Tip: instead of clicking the gutter you can also write breakpoint()
    # on any line - Python pauses there (in the terminal it opens pdb,
    # type 'n' = next, 's' = step, 'p variable' = print, 'c' = continue).
    # breakpoint()


if __name__ == "__main__":
    main()
