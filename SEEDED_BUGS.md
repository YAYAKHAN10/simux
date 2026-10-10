# Seeded bugs: ground truth for the SimUX test app

Pre-registered list of the issues planted in `test-app/`. Detection precision
and recall (proposal §2.2.11) are scored against this table: a finding that
matches a row is a TP, a missed row is an FN, and anything else reported on
these pages is an FP. The grounding stub maps each ID to its WCAG criterion
text.

**Scripted task (all pages):** reach and activate the submit control using only
Tab, Enter, Space and arrow keys. **Success** = the browser lands on
`success.html` (heading "Submission received").

| ID | Page | Element | Bug | WCAG SC (primary) | Also relevant | What the a11y tree shows | Expected task outcome |
|----|------|---------|-----|-------------------|---------------|--------------------------|-----------------------|
| SB-01 | `p1-newsletter.html` | `img.banner` | Promo image has no `alt`; its text ("20% off… code WELCOME20") appears nowhere else | **1.1.1 Non-text Content** (A) | n/a | `- img` with no name | **Pass**: task completes, but the offer is never perceived |
| SB-02 | `p2-search.html` | `button[type=submit]` | Icon-only submit button with no accessible name (SVG is `aria-hidden`, no label) | **4.1.2 Name, Role, Value** (A) | 2.4.6 Headings and Labels | `- button` with no name | **Pass with hesitation**: agent has to guess which button submits |
| SB-03 | `p3-contact.html` | `input[name=email]` | Email field has a visible "Email address" text but no `<label for>` / `aria-label` | **1.3.1 Info and Relationships** (A) | 4.1.2, 3.3.2 | `- textbox` with no name; "Email address" is loose text | **Pass**: field is reachable, but unidentified |
| SB-04 | `p4-checkout.html` | `#promo` (promo code widget) | Keyboard focus trap: script cycles Tab/Shift+Tab between the promo field and Apply, so focus never reaches "Place order" | **2.1.2 No Keyboard Trap** (A) | 2.1.1 | Tree looks normal; the trap is only visible behaviourally (focus repeats) | **Fail**: submit unreachable. *Edge case for testing* |
| SB-05 | `p5-booking.html` | `div#confirm` | "Confirm booking" is a `<div>` with a click handler only: not focusable, no role, no key handler | **2.1.1 Keyboard** (A) | 4.1.2 | `- text: Confirm booking` (no button exists) | **Fail**: submit control does not exist for a keyboard user. *Edge case for testing* |

**Control page:** `control.html` (Create account) has **no seeded bugs**. The
expected result is a pass with **zero findings**; anything reported there
counts as a false positive.

**Not test targets:** `index.html` (hub page, neutral link text so it leaks no
hints) and `success.html` (success marker).

### Notes for the agent and the grounding stub
- The ground truth is kept **only in this file**. The pages carry no comments or
  attributes that name a bug, so a model reading the page can't be tipped off.
- SB-01/02/03 show up in the tree as nodes **with no name**. If the snapshot is
  pruned (e.g. `interesting_only`), unnamed nodes may be dropped. Use
  `locator.aria_snapshot()`, which keeps them.
- SB-04 is invisible in any single snapshot. It can only be detected from the
  **step history** (the same two elements repeating). This is why the agent
  loop logs every step.
- Everything else on the pages is intended to pass WCAG 2.2 A/AA (labelled
  fields, 4.5:1 contrast, 44 px targets, visible focus), so unplanned FPs stay
  rare.
- `python test-app/check_seeds.py` re-verifies every row above (scripted
  keyboard user + a11y-tree checks). Run it after any change to `test-app/`.
