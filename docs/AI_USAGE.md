# AI Use Statement

*This is a draft — the team should review and finalize it so it truthfully
reflects how this project was built.*

## Tools used

- **DeepSeek Harness (dsh)** — a large-language-model coding assistant used to
  draft, structure and debug the Python source code, tests and documentation.

## What the tool helped produce

- Initial structure and code for the data loader, baseline module, rule book,
  assistant, report renderer and test suite.
- Drafts of this README, this statement, and the supporting documents.

## How the team checked and revised the output

- Every module was executed end-to-end against the organizer's dataset and test
  questions; the test suite passes 37/37 (see `outputs/test_report.md`).
- The disruption definition and risk rules were verified against RULE001–RULE012
  and the official EVT001 example output (risk level "medium").
- Generated messages were reviewed and adjusted where they diverged from the
  expected behaviour (e.g. risk-level mapping and passenger wording).

## Attribution

- External libraries: `openpyxl` (MIT) and `matplotlib`/Pillow for data
  loading and chart rendering.
- The dataset is provided by the HackSHSID 2026 organizers (simulated).
- All other logic is original work, described and understood by the team.
