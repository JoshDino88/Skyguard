"""Load the organizer-provided simulated dataset into plain Python structures.

Field names below mirror the original (Chinese) headers of each sheet so the
mapping is auditable.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

import openpyxl

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "Track 3 Data.xlsx"

SHEET_BASELINE = "01_机场月度运行基线"
SHEET_SCALE = "02_机场年度规模"
SHEET_WEATHER = "03_机场天气月度"
SHEET_EVENTS = "04_模拟事件"
SHEET_RULES = "05_运营规则"
SHEET_FEEDBACK = "07_人工反馈"
SHEET_TESTS = "08_测试问题"
SHEET_DATA_QUALITY = "11_数据质量问题"


def _load_sheet(wb, name: str) -> list[dict[str, Any]]:
    ws = wb[name]
    rows = list(ws.iter_rows(values_only=True))
    if not rows:
        return []
    header = ["" if h is None else str(h) for h in rows[0]]
    out: list[dict[str, Any]] = []
    for r in rows[1:]:
        if r is None or all(c is None or str(c).strip() == "" for c in r):
            continue
        out.append(dict(zip(header, r)))
    return out


class Dataset:
    """A thin, read-only view over the organizer's workbook."""

    def __init__(self, path: str | Path = DATA_PATH):
        self.path = Path(path)
        self.wb = openpyxl.load_workbook(self.path, data_only=True)

    def table(self, name: str) -> list[dict[str, Any]]:
        return _load_sheet(self.wb, name)

    @property
    def baseline(self) -> list[dict[str, Any]]:
        return self.table(SHEET_BASELINE)

    @property
    def scale(self) -> list[dict[str, Any]]:
        return self.table(SHEET_SCALE)

    @property
    def weather(self) -> list[dict[str, Any]]:
        return self.table(SHEET_WEATHER)

    @property
    def events(self) -> list[dict[str, Any]]:
        return self.table(SHEET_EVENTS)

    @property
    def rules(self) -> list[dict[str, Any]]:
        return self.table(SHEET_RULES)

    @property
    def feedback(self) -> list[dict[str, Any]]:
        return self.table(SHEET_FEEDBACK)

    @property
    def tests(self) -> list[dict[str, Any]]:
        return self.table(SHEET_TESTS)

    @property
    def data_quality(self) -> list[dict[str, Any]]:
        return self.table(SHEET_DATA_QUALITY)
