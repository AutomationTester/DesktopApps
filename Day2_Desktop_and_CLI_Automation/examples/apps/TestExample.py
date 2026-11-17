# Beginner example: open Notepad, type text, then File -> Save as -> type name -> Save.
# Install the library first:  pip install pywinauto

import time
from pywinauto import Application, Desktop
from pywinauto.keyboard import send_keys

# 1. Open Notepad
Application(backend="uia").start("notepad.exe")
time.sleep(2)

# 2. Find the Notepad window (new Notepad starts via a launcher, so search by title)
notepad = Desktop(backend="uia").window(title_re=".*Notepad", found_index=0)
notepad.wait("visible", timeout=10)
notepad.set_focus()
time.sleep(1)

# 3. Type some text
send_keys("Hello, World!", with_spaces=True)

# 4. Click the File menu, then the "Save as" option
notepad.child_window(title="File", control_type="MenuItem").click_input()
time.sleep(3)
notepad.child_window(title_re="Save as.*", control_type="MenuItem").click_input()

# 5. In the Save dialog, type the file name and click Save
save_dialog = notepad.child_window(title="Save as", control_type="Window")
save_dialog.wait("visible", timeout=10)
file_box = save_dialog.child_window(auto_id="1001", control_type="Edit")
file_box.click_input()
send_keys("^a")  # select any existing text
send_keys("example.txt")
time.sleep(1)
save_dialog.child_window(title="Save", auto_id="1", control_type="Button").invoke()
confirm = save_dialog.child_window(title="Confirm Save As", control_type="Window")
if confirm.exists(timeout=5):
    confirm.child_window(title="Yes", auto_id="CommandButton_6", control_type="Button").click_input()
print("Done: saved as example.txt")

notepad.close()
