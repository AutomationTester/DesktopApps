"""
Day 4 - Example 05: Self-healing locator (concept, simulated)
=============================================================
UI elements change between builds: an automation_id is renamed, a title
gets translated, a button moves. A "self-healing" locator keeps a LIST of
fallback locators and tries them in order. When a fallback works it logs a
WARNING so a human can update the primary locator later.

Commercial AI tools go further (they score candidates by similarity of
text, type, position). Here we implement the simple, explainable version
plus a tiny "similarity" fallback to show the idea.

In pywinauto the same idea looks like:
    for criteria in [dict(auto_id="num7Button"), dict(title="Seven", control_type="Button")]:
        try:
            return window.child_window(**criteria).wait("visible", timeout=2)
        except Exception:
            continue

Run:
    python 05_self_healing_locator_concept.py
"""
import difflib
import logging
import sys

logging.basicConfig(level=logging.INFO, format="%(levelname)-7s | %(message)s", stream=sys.stdout)
log = logging.getLogger("self_healing")


class ElementNotFound(Exception):
    pass


# Simulated window "tree" of the NEW build. Developers renamed a few ids.
FAKE_WINDOW_ELEMENTS = [
    {"auto_id": "num7Button", "title": "Seven", "control_type": "Button"},
    {"auto_id": "plusBtn", "title": "Plus", "control_type": "Button"},       # was plusButton
    {"auto_id": "equalButton", "title": "Equals", "control_type": "Button"},
    {"auto_id": "CalculatorResult", "title": "Display is 0", "control_type": "Text"},  # was CalculatorResults
]


def find(**criteria):
    """Pretend pywinauto child_window(): all given properties must match exactly."""
    for el in FAKE_WINDOW_ELEMENTS:
        if all(el.get(k) == v for k, v in criteria.items()):
            return el
    raise ElementNotFound(criteria)


def find_with_healing(name, locators, similarity_key="auto_id", threshold=0.6):
    """Try each locator in order; finally try a fuzzy match on the first locator's id."""
    for index, criteria in enumerate(locators):
        try:
            element = find(**criteria)
            if index == 0:
                log.info("[%s] found with primary locator %s", name, criteria)
            else:
                log.warning("[%s] primary locator failed; HEALED with fallback #%d %s "
                            "-> please update the page object", name, index, criteria)
            return element
        except ElementNotFound:
            log.debug("[%s] locator %s not found", name, criteria)

    # Last resort: closest id by string similarity (the 'AI-like' part)
    wanted = locators[0].get(similarity_key, "")
    candidates = [el[similarity_key] for el in FAKE_WINDOW_ELEMENTS]
    best = difflib.get_close_matches(wanted, candidates, n=1, cutoff=threshold)
    if best:
        element = find(**{similarity_key: best[0]})
        score = difflib.SequenceMatcher(None, wanted, best[0]).ratio()
        log.warning("[%s] HEALED by similarity: '%s' -> '%s' (score %.2f). Verify manually!",
                    name, wanted, best[0], score)
        return element
    log.error("[%s] could not be located with %d locators", name, len(locators))
    raise ElementNotFound(name)


# Locator repository (as a page object would hold it)
LOCATORS = {
    "seven": [{"auto_id": "num7Button"}, {"title": "Seven", "control_type": "Button"}],
    "plus": [{"auto_id": "plusButton"}, {"title": "Plus", "control_type": "Button"}],
    "result": [{"auto_id": "CalculatorResults"}, {"auto_id": "ResultDisplay"}],
    "memory": [{"auto_id": "MemoryButton"}, {"title": "Memory"}],
}

if __name__ == "__main__":
    for name, locs in LOCATORS.items():
        try:
            el = find_with_healing(name, locs)
            print(f"  -> {name:<7} resolved to {el}")
        except ElementNotFound:
            print(f"  -> {name:<7} NOT FOUND - the test should fail with a clear message")
    print("\nNOTE: 'memory' was 'healed' to the Seven button - a WRONG heal (this app has no")
    print("      memory button at all). This is exactly why healing needs human review.")
    print("\nTakeaways:")
    print(" * Healing must be LOGGED as a warning - silent healing hides real UI changes.")
    print(" * Similarity healing can pick the WRONG element; keep a human in the loop.")
