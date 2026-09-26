#!/usr/bin/env bash
# =============================================================================
# linux_commands_practice.sh
# Day 3 - Linux basics for automation engineers
#
# Runs every command from the slides, with comments, inside a throw-away
# sandbox folder:  examples/sandbox/linux_practice/
#
# How to run:
#   Linux / WSL / macOS :  chmod +x linux_commands_practice.sh && ./linux_commands_practice.sh
#   Windows Git Bash    :  bash linux_commands_practice.sh
#
# Tip: read each block, then type the commands yourself in a terminal.
# =============================================================================

set -e          # stop at the first command that fails (like an exception)
set -u          # using an undefined variable is an error

# $(...) runs a command and captures its output. dirname "$0" = folder of this script
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SANDBOX="$SCRIPT_DIR/sandbox/linux_practice"

step() { echo; echo "=================== $1 ==================="; }

step "0. Prepare sandbox"
rm -rf "$SANDBOX"          # only ever removes OUR sandbox folder
mkdir -p "$SANDBOX"        # -p = create parents, no error if it exists
cd "$SANDBOX"

step "1. pwd - print working directory (where am I?)"
pwd

step "2. mkdir / touch - create folders and empty files"
mkdir -p project/logs project/data project/scripts
touch project/logs/app.log project/data/users.csv
echo "created project/ tree"

step "3. ls - list files"
ls project                 # names only
ls -l project              # long format: permissions, owner, size, date
ls -la project             # -a also shows hidden files (names starting with .)
ls -R project              # recursive

step "4. cd - change directory"
cd project/logs
pwd
cd ..                      # one level up
pwd
cd - > /dev/null           # back to previous directory (output hidden)
cd "$SANDBOX"              # absolute path always works

step "5. echo + redirection: > (overwrite)  >> (append)"
echo "2026-09-26 10:00:01 INFO  Application started"   >  project/logs/app.log
echo "2026-09-26 10:00:05 ERROR Could not connect to DB" >> project/logs/app.log
echo "2026-09-26 10:00:09 INFO  Retrying connection"   >> project/logs/app.log
echo "2026-09-26 10:00:12 error timeout after 30s"      >> project/logs/app.log
printf "id,name,role\n1,alice,admin\n2,bob,tester\n" > project/data/users.csv

step "6. cat - print file contents (head/tail/wc are useful friends)"
cat project/logs/app.log
echo "--- head -n 2 ---"; head -n 2 project/logs/app.log
echo "--- tail -n 1 ---"; tail -n 1 project/logs/app.log
echo "--- wc -l (line count) ---"; wc -l < project/logs/app.log

step "7. grep - search text"
grep "ERROR" project/logs/app.log            # case-sensitive
echo "--- grep -i (ignore case) ---"
grep -i "error" project/logs/app.log
echo "--- grep -c (count) ---"
grep -ci "error" project/logs/app.log
echo "--- grep -n (line numbers) ---"
grep -n "INFO" project/logs/app.log
echo "--- grep -r (recursive in folder) ---"
grep -r "alice" project
echo "--- pipe | : output of one command becomes input of the next ---"
cat project/logs/app.log | grep -i error | wc -l
# grep exit code: 0 = found, 1 = not found. '|| ...' keeps set -e from stopping the script
grep -q "FATAL" project/logs/app.log || echo "no FATAL lines (grep exit code 1)"

step "8. cp - copy"
cp project/data/users.csv project/data/users_backup.csv
cp -r project/data project/data_copy         # -r = recursive for folders
ls project project/data

step "9. mv - move / rename"
mv project/data/users_backup.csv project/data/users_old.csv    # rename
mv project/data_copy project/archive                          # rename folder
ls project project/data

step "10. find - locate files"
find project -name "*.csv"                   # by name pattern
find project -type d                          # only directories
find project -type f -name "*.log"            # only files
find project -type f -mtime -1                # modified in the last 1 day
find project -type f -size -1k                # smaller than 1 KB

step "11. rm - remove (NO recycle bin in Linux - be careful!)"
rm project/data/users_old.csv
rm -r project/archive                         # -r needed for folders
ls project project/data
# NEVER run: rm -rf /   or   rm -rf $UNSET_VAR/*

step "12. Permissions: chmod, rwx and octal"
cat > project/scripts/hello.sh <<'EOF'
#!/usr/bin/env bash
echo "Hello from a shell script! Args: $*"
EOF
ls -l project/scripts/hello.sh
chmod +x project/scripts/hello.sh             # add execute permission
ls -l project/scripts/hello.sh
chmod 755 project/scripts/hello.sh            # rwx r-x r-x
chmod 644 project/data/users.csv              # rw- r-- r--
ls -l project/scripts/hello.sh project/data/users.csv
./project/scripts/hello.sh one two            # run it (needs x + shebang)
# NOTE: on Windows Git Bash, NTFS does not store Linux permissions, so ls -l
# may not change after chmod. Try this section in WSL or a Linux VM to see it.

step "13. Running a Python script in Linux"
cat > project/scripts/check_env.py <<'EOF'
#!/usr/bin/env python3
import platform, sys
print(f"Python {platform.python_version()} on {platform.system()}; args={sys.argv[1:]}")
EOF
chmod +x project/scripts/check_env.py
# Pick whichever python exists: python3 on Linux, python on Windows
PY=$(command -v python3 || command -v python)
# python3 may be the Microsoft Store stub on Windows; verify it really runs
"$PY" --version > /dev/null 2>&1 || PY=$(command -v python)
"$PY" project/scripts/check_env.py --env qa
echo "On Linux you can also run it directly: ./project/scripts/check_env.py --env qa"

step "14. Environment variables and exit codes"
export TEST_ENV=qa
echo "TEST_ENV is $TEST_ENV"
true;  echo "exit code of 'true'  = $?"
false || echo "exit code of 'false' = 1 (non-zero means failure)"

step "15. Disk usage and processes"
du -sh project                                # size of a folder
df -h . | head -n 2                           # free space on this drive
ps | head -n 5                                # running processes (ps aux on Linux)

step "DONE"
echo "Sandbox left at: $SANDBOX  (safe to delete)"
