# SkyGuard

An **explainable AI assistant for flight disruptions at key airports**.

> HackSHSID 2026 · Track 3 (Sustainability) · Problem setter: Accenture

SkyGuard helps aviation professionals at a fictional Chinese domestic airline
decide how to respond when weather changes or operational disruptions occur at
key airports. It identifies problems, explains its reasoning (traceable to data
and rules), recommends prioritized actions, and drafts audience-specific
messages — while keeping every safety-critical decision with a human.

## What it does

- Detects operational signals from an event's text and the airport's own
  baseline: weather risk, sustained pressure, data-source conflicts, human veto,
  privacy exposure, and major operational decisions.
- Produces a structured brief: risk level, rationale, likely impacts,
  assumptions to verify, information gaps, first/next steps, escalation
  conditions, and human-decision points.
- Drafts three messages for operations staff, airport coordination teams and
  passengers — passenger wording carefully avoids claiming a delay.
- Every conclusion carries a citation (a `SIM-*` source id or a `RULE*` id).

## Installation

Requires Python 3.10+.

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py --event EVT001     # assess one simulated event
python main.py --all              # assess all five events
python main.py --all --json       # also dump machine-readable JSON
```

Reports are written to `outputs/`.

Run the test suite:

```bash
python tests/test_assistant.py
```

## Data sources and assumptions

- **Data**: the organizer-provided *simulated* dataset `data/Track 3 Data.xlsx`
  (SIM-BASE monthly baselines, SIM-SCALE annual airport size, SIM-WEATHER
  monthly weather). All airports, cities, events, rules and numbers are
  fictional and do not correspond to any real institution or operation.
- **Disruption definition**: an airport is "disrupted" when its share of flights
  completed as planned falls at least 5 percentage points below its own
  trailing 12-month average (traceable to RULE003 and the dataset's own derived
  field).
- **Reasoning model**: an auditable rule-and-baseline engine (RULE001–RULE012)
  rather than a black box, so every conclusion can be explained and traced.

## Project structure

```text
skyguard/
├── main.py                 # CLI entry point
├── skyguard/               # the assistant package
│   ├── data_loader.py      # reads the xlsx dataset
│   ├── baseline.py         # baseline stats + disruption definition
│   ├── rules.py            # rule book + signal detection
│   ├── assistant.py        # event -> structured brief
│   └── report.py           # Markdown rendering
├── tests/test_assistant.py # 15 test questions + 5 events + edge cases
├── data/Track 3 Data.xlsx  # organizer's simulated dataset
├── outputs/                # generated briefs + test report
└── docs/                   # AI usage, project description, citations
```

## AI use statement

See [`docs/AI_USAGE.md`](docs/AI_USAGE.md).

## License

Simulated dataset © HackSHSID 2026 organizers. Application code for educational
use.
