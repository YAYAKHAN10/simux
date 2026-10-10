# Live demo script (draft)

> Draft written before the agent runs. Fill the TODOs from `logs/runs.csv`
> after the weekend runs, then rehearse once end-to-end with a timer.

**Target length:** ~6 minutes. **Presenter:** Person A drives, Person B takes
"how does the agent work" questions.

## Before the panel arrives
- [ ] `python -m http.server 8000 -d test-app` running; `localhost:8000` open
- [ ] API key loaded; one warm-up call made (cold first calls are slow)
- [ ] `python test-app/check_seeds.py` passes (proves the bugs are still in place)
- [ ] Fallback log + screen recording open in a background tab (see below)
- [ ] Terminal font large enough to read from the back of the room

## Running order

**1. Setup (30 s): `index.html`, then `SEEDED_BUGS.md`**
> "This is our test app: six small pages, each ending in a submit button. We
> planted five known accessibility bugs and wrote them down *before* running
> anything. That list is our ground truth."

**2. Control page (45 s): `control.html`**
> "First, a page with no bugs. Our accessibility persona sees only the
> accessibility tree, the same information a screen reader gets: no
> screenshot, no HTML. It can only press Tab, Enter, Space and arrow keys."
- Show the tree the agent receives, then the run. Expected: **pass, no findings.**
- TODO: steps taken = __

**3. Detectable-but-passable bug (1 min): `p2-search.html`**
> "Here the search button is just an icon. Sighted users see a magnifying
> glass; the persona sees `button` with no name."
- Point at the unnamed `button` node in the tree. Show the finding with the
  WCAG 4.1.2 citation the grounding stub attached.
- TODO: agent output / hesitation observed = __

**4. The edge case, a clear failure (1.5 min): `p4-checkout.html`**
> "This checkout looks fine with a mouse. But the promo-code box traps keyboard
> focus. Watch the focus go back and forth."
- Show the step log: the same two elements repeating until the step cap.
- Outcome: **fail**, 2.1.2 No Keyboard Trap cited.
> "A static scanner can't see this, because the page markup is valid. You only
> find it by actually trying to use the page. That's the point of SimUX."
- TODO: run_id = __ , steps = __

**5. (If time) `p5-booking.html`**: the "button" is a div, so there is nothing
to Tab to. Fail, 2.1.1.

**6. Wrap-up (45 s)**
> "Built so far: the restricted persona, the execution loop and grounded
> findings on a seeded target. Next: the fix-and-verify loop, where the same
> agent re-runs on the patched page to confirm the fix actually works."
- Show the architecture figure (built vs planned).

## Fallback if the API is down
1. Say so plainly: "The inference API is down, so I'll replay a recorded run."
2. Replay the saved run log for p4 (TODO: path `logs/runs/<run_id>.jsonl`) and
   the screen recording.
3. Still show the pages and the a11y tree live. Those don't need the API.

The fallback is a backup, not the main demo. Always try live first.

## Likely questions (Person A)
- *How do you know the bugs are real?* Pre-registered in `SEEDED_BUGS.md`;
  `check_seeds.py` verifies each one with a scripted keyboard user.
- *Why a control page?* To count false positives; without it we could only
  measure recall.
- *Why not just run axe-core?* axe catches SB-01/02/03 from markup but can't
  see SB-04 (the trap is runtime behaviour). TODO: confirm by running axe on
  p4 before the demo.
