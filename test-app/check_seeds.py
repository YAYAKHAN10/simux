"""Sanity-check that every seeded bug in SEEDED_BUGS.md is actually present.

This is not the SimUX agent. It is a scripted keyboard user that
presses Tab (max 25 times) looking for each page's submit control, then
presses Enter on it, and also checks the accessibility-tree evidence for
each seeded bug. It exists so the ground truth used for precision/recall
is verified rather than assumed.

Usage:
    pip install playwright && playwright install chromium
    python test-app/check_seeds.py            # prints a table
    python test-app/check_seeds.py --json     # machine-readable
"""

import functools
import http.server
import json
import re
import sys
import threading
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeout
from playwright.sync_api import sync_playwright

APP_DIR = Path(__file__).resolve().parent
PORT = 8765
MAX_TABS = 25

# page -> (selector of the submit control, seeded bug id or None)
PAGES = {
    "control.html": ("button[type=submit]", None),
    "p1-newsletter.html": ("button[type=submit]", "SB-01"),
    "p2-search.html": ("button[type=submit]", "SB-02"),
    "p3-contact.html": ("button[type=submit]", "SB-03"),
    "p4-checkout.html": ("button[type=submit]", "SB-04"),
    "p5-booking.html": ("#confirm", "SB-05"),
}


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def serve():
    handler = functools.partial(QuietHandler, directory=str(APP_DIR))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", PORT), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


def keyboard_run(page, target_selector):
    """Tab towards the target; press Enter if reached. Returns details."""
    target = page.locator(target_selector)
    focus_trail = []
    for _ in range(MAX_TABS):
        page.keyboard.press("Tab")
        focused = page.evaluate(
            "() => { const e = document.activeElement;"
            " return e ? (e.id || e.tagName.toLowerCase()) : null; }"
        )
        focus_trail.append(focused)
        if target.evaluate("el => el === document.activeElement"):
            page.keyboard.press("Enter")
            try:
                page.wait_for_url("**/success.html*", timeout=3000)
                submitted = True
            except PlaywrightTimeout:
                submitted = False
            return {
                "reached": True,
                "submitted": submitted,
                "tabs": len(focus_trail),
                "trail": focus_trail,
            }
    return {"reached": False, "submitted": False, "tabs": MAX_TABS,
            "trail": focus_trail}


def seed_evidence(page, bug):
    """Return (present: bool, note) for the seeded bug on this page."""
    tree = page.locator("body").aria_snapshot()
    if bug is None:
        return None, "control page: no seeded bug"
    if bug == "SB-01":
        unnamed_img = re.search(r"^\s*- img\s*$", tree, re.M) is not None
        return unnamed_img, "unnamed `img` node in a11y tree"
    if bug == "SB-02":
        unnamed_btn = re.search(r"^\s*- button\s*$", tree, re.M) is not None
        return unnamed_btn, "unnamed `button` node in a11y tree"
    if bug == "SB-03":
        unnamed_box = re.search(r"^\s*- textbox\s*$", tree, re.M) is not None
        return unnamed_box, "unnamed `textbox` node in a11y tree"
    if bug == "SB-04":
        return None, "behavioural: see keyboard run (focus should cycle)"
    if bug == "SB-05":
        no_button = "Confirm booking" in tree and \
            'button "Confirm booking"' not in tree
        return no_button, "'Confirm booking' is text, not a button"
    raise ValueError(bug)


def main():
    server = serve()
    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for name, (selector, bug) in PAGES.items():
            page = browser.new_page()
            page.goto(f"http://127.0.0.1:{PORT}/{name}")
            present, note = seed_evidence(page, bug)
            run = keyboard_run(page, selector)
            if bug == "SB-04":
                trail = run["trail"]
                present = not run["reached"] and set(trail[-4:]) <= {
                    "promo-code", "promo-apply"}
            results.append({"page": name, "bug": bug, "seed_present": present,
                            "note": note, **run})
            page.close()
        browser.close()
    server.shutdown()

    if "--json" in sys.argv:
        print(json.dumps(results, indent=2))
        return

    print(f"{'page':<20} {'bug':<6} {'seed ok':<8} {'reached':<8} "
          f"{'submitted':<10} tabs")
    for r in results:
        seed = "-" if r["seed_present"] is None else str(r["seed_present"])
        print(f"{r['page']:<20} {str(r['bug'] or '-'):<6} {seed:<8} "
              f"{str(r['reached']):<8} {str(r['submitted']):<10} {r['tabs']}")


if __name__ == "__main__":
    main()
