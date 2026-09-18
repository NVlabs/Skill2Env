---
name: grill
description: |
  Calibrated interrogation of a fuzzy idea before it becomes a spec. Asks one
  question at a time, recommends an answer, and lands each answer in §G (goal)
  or §C (constraints) — unknowns parked as `?` items, never guessed. The
  cheapest place to kill a bad idea is before §T exists. Triggers when the user
  has a vague idea, says "grill me", "stress-test this", "challenge my plan",
  "interview me before I spec", or invokes /ck:grill. Defers the actual write to
  the spec skill.
---

# grill — sharpen idea before spec

**One question at a time. Every answer lands in a § or gets parked `?`. Never guess a constraint into existence.**

Plan-then-execute guesses the fuzzy parts & builds the wrong thing.
Grill drags the fuzz into §G/§C *before* a single §T row exists.
A bad assumption caught here costs one question. Caught in §B it costs a bug.

## WHEN TO GRILL

- Idea is one sentence & you can feel the holes.
- Multiple readings of the goal exist & you are about to pick one silently.
- Before `/spec new` on anything non-trivial.
- User asks to be challenged / stress-tested.

Skip for a typo or a one-line fix. Grill scales to uncertainty, ⊥ to ego.

## CALIBRATE FIRST

One opening read, not a quiz:
1. How well does user know this domain? (sets question depth)
2. How locked is the idea? (exploring vs committed)
3. Pressure wanted: light / normal / brutal.

Match it. Brutal grilling on a half-formed idea just demoralizes. Light
grilling on a committed plan misses the load-bearing flaw.

## QUESTION LADDER

Climb in order. Each rung, ask **one** question, **recommend** an answer, wait.

1. **Goal** — what must the code *do*, in one line? (→ §G)
2. **Done** — how do we know it works? name the observable. (→ §C / future §V)
3. **Boundary** — what is explicitly out of scope? (→ §C)
4. **Lock** — what tech/lib/pattern is non-negotiable? what is forbidden? (→ §C)
5. **Surface** — what does the outside world touch — cmd, api, file, env? (→ §I)
6. **Edge** — the one input that breaks the happy path? (→ future §V)
7. **Unknown** — what do we *not* know yet? (→ park as `?` §C bullet)

Stop climbing the moment the spec would be unambiguous. Do not ask all seven by reflex.

## ANSWER FORMAT

Each question carries a recommended answer so the user can grunt "yes" & move:

> Q: auth — session cookie or JWT?
> rec: JWT — stateless, you named horizontal scaling as a §C.
> (a) JWT  (b) cookie  (c) something else?

## HANDOFF

When done, emit a compact block — goal line, constraint bullets, surfaced
unknowns as `?` — and hand to the **spec** skill to write §G/§C. Grill proposes;
spec is the sole mutator. Never write SPEC.md directly.

## WHEN TO STOP

Done when ALL hold:
- §G is one line, one reading, zero "or maybe".
- §C covers every non-negotiable the user stated or implied.
- Every blocking unknown is either answered or parked as an explicit `?`.

Unresolved blocking unknown that needs the outside world → recommend `/research`, not a guess.

## BOUNDARIES

- ⊥ make product decisions for the user. Recommend, never decide.
- ⊥ write SPEC.md. Hand structured answers to spec.
- ⊥ ask in bulk. One question, one recommendation, wait.
- ⊥ grill a trivial change. Right-size or skip.
