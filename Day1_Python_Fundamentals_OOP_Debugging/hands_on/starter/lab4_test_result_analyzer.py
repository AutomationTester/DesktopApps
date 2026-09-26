"""
Lab 4 (Extra practice) - Test Result Analyzer (STARTER)
========================================================
How to run:
    python lab4_test_result_analyzer.py

Practises: variables, lists, dictionaries, loops, conditions, functions.

Complete each "# TODO" function. print_report() is already written and
uses your functions. The script runs from the start, but the numbers
stay wrong until you complete the TODOs.
Expected final values are listed in hands_on/Lab_Guide.md (Lab 4).
"""

EXECUTION_RECORDS = [
    {"id": "TC_201", "module": "Login", "status": "PASS", "duration": 2.4},
    {"id": "TC_202", "module": "Login", "status": "FAIL", "duration": 5.1},
    {"id": "TC_203", "module": "Billing", "status": "PASS", "duration": 3.3},
    {"id": "TC_204", "module": "Billing", "status": "PASS", "duration": 7.8},
    {"id": "TC_205", "module": "Billing", "status": "SKIP", "duration": 0.0},
    {"id": "TC_206", "module": "Reports", "status": "FAIL", "duration": 9.6},
    {"id": "TC_207", "module": "Reports", "status": "PASS", "duration": 4.0},
    {"id": "TC_208", "module": "Settings", "status": "PASS", "duration": 1.2},
]


def count_by_status(records):
    """Return a dict like {'PASS': 5, 'FAIL': 2, 'SKIP': 1}."""
    counts = {}
    # TODO: loop over records; for each record add 1 to counts[record["status"]]
    #   hint: counts[status] = counts.get(status, 0) + 1
    return counts


def pass_percentage(counts):
    """Pass % based on EXECUTED tests only (PASS + FAIL). 0.0 if nothing executed."""
    # TODO: executed = PASS count + FAIL count (use counts.get(key, 0))
    # TODO: if executed is 0 return 0.0, else return PASS / executed * 100
    return 0.0


def failed_test_ids(records):
    """Return the list of ids whose status is FAIL."""
    # TODO: build and return a list of record["id"] where status is "FAIL"
    return []


def slowest_test(records):
    """Return the record with the biggest duration."""
    slowest = records[0]
    # TODO: loop over the remaining records and keep the one with the biggest "duration"
    return slowest


def module_summary(records):
    """Return {'Login': {'PASS': 1, 'FAIL': 1, 'SKIP': 0}, ...}."""
    summary = {}
    # TODO: for each record:
    #   - if its module is not yet in summary, add {"PASS": 0, "FAIL": 0, "SKIP": 0}
    #   - add 1 to summary[module][status]
    return summary


def print_report(records):
    counts = count_by_status(records)
    print("=" * 50)
    print(" TEST EXECUTION SUMMARY")
    print("=" * 50)
    print(f" Total tests : {len(records)}")
    for status in ("PASS", "FAIL", "SKIP"):
        print(f" {status:11} : {counts.get(status, 0)}")
    print(f" Pass %      : {pass_percentage(counts):.1f}%")
    print(f" Failed      : {', '.join(failed_test_ids(records)) or 'none'}")
    slow = slowest_test(records)
    print(f" Slowest     : {slow['id']} ({slow['duration']}s)")
    print("-" * 50)
    print(f" {'Module':10} {'PASS':>5} {'FAIL':>5} {'SKIP':>5}  Health")
    for module, c in module_summary(records).items():
        health = "OK" if c["FAIL"] == 0 else "ATTENTION"
        print(f" {module:10} {c['PASS']:>5} {c['FAIL']:>5} {c['SKIP']:>5}  {health}")
    print("=" * 50)
    build = "ACCEPTED" if pass_percentage(counts) >= 80 else "REJECTED"
    print(f" Build status (needs >= 80% pass): {build}")


if __name__ == "__main__":
    print_report(EXECUTION_RECORDS)
