"""SkyGuard — an explainable AI assistant for flight disruptions at key airports.

HackSHSID 2026 · Track 3 (Sustainability) · Problem setter: Accenture.

The assistant reads the organizer-provided *simulated* airport dataset and,
for a given operational event, produces a traceable decision-support brief:
risk level, reasoning (tied to data/rules), prioritized actions, escalation
conditions, human-decision points, and audience-specific draft messages for
operations staff, airport coordination teams and passengers.

Design principle: every conclusion must be traceable to a data source or a
rule, and every safety-critical decision stays with a human.
"""

__version__ = "0.1.0"
