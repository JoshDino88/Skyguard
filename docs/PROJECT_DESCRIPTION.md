# Project description (for the submission form)

## Interpretation of the problem

Flight disruptions force airlines to act on incomplete or even contradictory
information. The problem is not to "predict the future", but to **help a human
operator decide what to verify, in what order, when to escalate, and what can
and cannot be said to passengers** — safely and transparently.

## Approach

SkyGuard models the assistant as an **auditable rule-and-baseline engine**:

1. It defines a *disruption* quantitatively — an airport whose planned-completion
   rate falls 5+ percentage points below its own 12-month average (RULE003).
2. It detects operational signals from event text with explicit keywords and
   maps each to one of the 12 operational rules (RULE001–RULE012).
3. It emits a structured brief (risk level, reasoning, information gaps,
   prioritized actions, escalation conditions, human-decision points) and three
   audience-specific draft messages.

## Why this is unique

- **Every conclusion is traceable** to a source id (`SIM-*`) or a rule id
  (`RULE*`) — no black box.
- **Safety stays with humans**: cancellations, releases, scheduling, maintenance
  and passenger notices are flagged for human approval, never auto-executed.
- **It generalizes**: the engine reads events and rules from data, so an unseen
  airport or a new scenario is handled the same way (verified by test cases).
