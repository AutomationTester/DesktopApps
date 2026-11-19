"""
Lab 3 - the FLAKY test script you will improve with the help of an AI assistant.

It tests backup_tool.py. Run it from THIS folder 3-4 times:
    python flaky_backup_test.py
You will see different results: 'Backup FAILED', 'error', or a crash.

Do NOT fix it yet - first follow Lab 3 in Lab_Guide.md
(find the problems yourself, then write a prompt, then review the AI answer).
"""
import os, time, json, subprocess

SRC = "lab3_work/source_files"
DST = "lab3_work/backup"

def make_source():
    os.makedirs(SRC)
    for i in range(3):
        f = open(SRC + "/file" + str(i) + ".txt", "w")
        f.write("data " + str(i))

def test_backup():
    make_source()
    subprocess.Popen("python backup_tool.py " + SRC + " " + DST, shell=True)
    time.sleep(2)
    try:
        status = json.load(open(DST + "/status.json"))
        if status["status"] == "done" and status["files"] == "3":
            print("Backup OK")
        else:
            print("Backup FAILED")
        for f in os.listdir(SRC):
            if f not in os.listdir(DST):
                print("missing " + f)
    except:
        print("error")

test_backup()
