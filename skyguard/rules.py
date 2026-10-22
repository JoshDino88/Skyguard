"""Operational rule book and signal detection.

The 12 rules (RULE001-RULE012) are loaded from the dataset, and *signals*
are detected from an event's text through explicit keyword patterns plus a
baseline check, so every conclusion stays traceable instead of being a black
box.
"""
from __future__ import annotations

from dataclasses import dataclass

from .baseline import is_disrupted


@dataclass
class Signal:
    label: str        # human-readable signal name
    rule_id: str      # governing rule
    reason: str       # why it fired (traceability)


# --- keyword lexicons (kept small and auditable) ---------------------------
WEATHER_KW = ["强降雨", "阵风", "雷雨", "雷暴", "低温", "大风", "暴雨", "降雨"]
DECLINE_KW = ["下降"]
CONCENTRATION_KW = ["集中", "仍有", "后续"]
CONFLICT_KW = ["冲突", "不一致", "两个来源"]
PAX_KW = ["旅客", "通知", "延误"]
REJECT_KW = ["否决", "拒绝", "足以应对"]
MAJOR_DECISION_KW = ["取消", "放行", "调度", "维修", "赔付"]
PRIVACY_KW = ["姓名", "手机号", "身份证", "电话", "邮箱", "护照", "住址"]


def _has(text: str, kws: list[str]) -> str | None:
    for kw in kws:
        if kw in text:
            return kw
    return None


def detect_signals(event: dict, delta_pp: float | None) -> list[Signal]:
    """Detect which operational signals are present in an event.

    The event title is included so signals carried only by the title
    (e.g. "人工否决") are still caught.
    """
    title = str(event.get("事件名称") or "")
    weather = str(event.get("天气描述") or "")
    run = str(event.get("运行情况描述") or "")
    notes = str(event.get("现场备注") or "")
    known = str(event.get("已知信息") or "")
    unknown = str(event.get("未知信息") or "")
    full = " ".join([title, weather, run, notes, known, unknown])
    run_note = run + notes

    signals: list[Signal] = []

    hit = _has(weather, WEATHER_KW)
    if hit:
        signals.append(Signal("天气风险", "RULE002", f"天气描述含“{hit}”"))

    # sustained pressure = a decline AND still-concentrated upcoming tasks
    if _has(run_note, DECLINE_KW) and _has(run_note, CONCENTRATION_KW):
        signals.append(Signal("运行压力", "RULE004", "运行描述含“下降”且后续任务仍集中"))

    if _has(full, CONFLICT_KW):
        signals.append(Signal("数据来源冲突", "RULE001", "文本含“冲突/不一致/两个来源”"))

    if is_disrupted(delta_pp):
        signals.append(Signal(
            "异常波动",
            "RULE003",
            f"该机场与自身12月平均差 {delta_pp} pp ≤ -5 pp 阈值",
        ))

    if _has(full, PAX_KW):
        signals.append(Signal("旅客沟通", "RULE005", "文本含“旅客/通知/延误”"))

    if _has(full, REJECT_KW):
        signals.append(Signal("人工否决", "RULE006", "文本含“否决/拒绝/足以应对”"))

    if _has(full, MAJOR_DECISION_KW):
        signals.append(Signal("重大运行决定", "RULE007", "文本含“取消/放行/调度/维修/赔付”"))

    if _has(full, PRIVACY_KW):
        signals.append(Signal("隐私信息", "RULE011", "文本含个人信息（姓名/手机号/身份证等）"))

    return signals


class RuleBook:
    """Indexed view of the 12 operational rules."""

    def __init__(self, rules: list[dict]):
        self._by_id = {str(r.get("规则编号")): r for r in rules}

    def get(self, rule_id: str) -> dict | None:
        return self._by_id.get(rule_id)

    def all(self) -> list[dict]:
        return list(self._by_id.values())
