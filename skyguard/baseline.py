"""Baseline statistics and the quantitative definition of a *disruption*.

Definition (traceable to RULE003 and the dataset's own derived field):
an airport is "disrupted" in a month when its share of flights completed as
planned ("按计划完成航班的比例") falls at least DISRUPTION_THRESHOLD_PP
percentage points below that airport's own trailing 12-month average —
i.e. its "与自身平均差（百分点）" is <= -5.0.
"""
from __future__ import annotations

from typing import Any

DISRUPTION_THRESHOLD_PP = 5.0  # percentage points


def airport_records(baseline: list[dict[str, Any]], airport: str) -> list[dict[str, Any]]:
    return [r for r in baseline if r.get("机场名称") == airport]


def latest_record(baseline: list[dict[str, Any]], airport: str) -> dict[str, Any] | None:
    rows = airport_records(baseline, airport)
    return rows[-1] if rows else None


def latest_delta_pp(baseline: list[dict[str, Any]], airport: str) -> float | None:
    """Latest "与自身平均差（百分点）" for an airport, or None if unknown."""
    rec = latest_record(baseline, airport)
    if rec is None:
        return None
    v = rec.get("与自身平均差（百分点）")
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def is_disrupted(delta_pp: float | None, threshold: float = DISRUPTION_THRESHOLD_PP) -> bool:
    return delta_pp is not None and delta_pp <= -threshold


def describe_baseline(baseline: list[dict[str, Any]], airport: str) -> str:
    """A human-readable snapshot of the airport's latest baseline row."""
    rec = latest_record(baseline, airport)
    if rec is None:
        return f"{airport}: no baseline record available"
    y, m = rec.get("年份"), rec.get("月份")
    planned = rec.get("按计划完成航班的比例")
    delta = rec.get("与自身平均差（百分点）")
    return (
        f"{airport} {y}-{m:02d}: planned-completion {planned}, "
        f"delta vs 12-mo self-average {delta} pp"
    )
