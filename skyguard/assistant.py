"""The SkyGuard assistant: event + baselines -> structured, traceable brief.

The output shape mirrors the organizer's standard template (sheet 06): risk
level, rationale, likely impacts, assumptions to verify, information gaps,
first/next steps, escalation conditions, human-decision points, citations,
and three audience-specific draft messages.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .data_loader import Dataset
from .baseline import latest_delta_pp, describe_baseline
from .rules import RuleBook, Signal, detect_signals


@dataclass
class Assessment:
    event_id: str
    airport: str
    risk_level: str
    scope: str
    rationale: list[str] = field(default_factory=list)
    impacts: list[str] = field(default_factory=list)
    assumptions: list[str] = field(default_factory=list)
    info_gaps: list[str] = field(default_factory=list)
    first_step: str = ""
    next_steps: list[str] = field(default_factory=list)
    escalation: str = ""
    human_decisions: list[str] = field(default_factory=list)
    citations: list[str] = field(default_factory=list)
    internal_note: str = ""
    coord_note: str = ""
    pax_draft: str = ""


class Assistant:
    def __init__(self, dataset: Dataset):
        self.dataset = dataset
        self.rules = RuleBook(dataset.rules)

    def assess(self, event: dict[str, Any]) -> Assessment:
        airport = str(event.get("机场名称") or "")
        event_id = str(event.get("事件编号") or "EVT??")
        delta = latest_delta_pp(self.dataset.baseline, airport)
        signals = detect_signals(event, delta)

        a = Assessment(
            event_id=event_id,
            airport=airport,
            risk_level=self._risk_level(signals, event),
            scope=self._scope(event),
        )
        a.rationale = self._rationale(event, signals, delta)
        a.impacts = self._impacts(signals)
        a.assumptions = self._assumptions(event, signals)
        a.info_gaps = self._info_gaps(event)
        a.first_step, a.next_steps = self._actions(signals)
        a.escalation = self._escalation(signals, event)
        a.human_decisions = self._human_decisions(event, signals)
        a.citations = self._citations(signals)
        a.internal_note, a.coord_note, a.pax_draft = self._messages(event, signals, delta)
        return a

    # -- components ---------------------------------------------------------
    def _risk_level(self, signals: list[Signal], event: dict) -> str:
        labels = {s.label for s in signals}
        if "数据来源冲突" in labels:
            return "无法判断"
        if "人工否决" in labels:
            return "低"
        independent = labels & {"天气风险", "运行压力", "异常波动"}
        if len(independent) >= 2:
            return "高"
        if independent or "旅客沟通" in labels:
            return "中"
        return "低"

    def _scope(self, event: dict) -> str:
        airport = event.get("机场名称")
        t = event.get("事件时间")
        return f"{airport}，{t}" if t else str(airport)

    def _rationale(self, event, signals, delta) -> list[str]:
        out = []
        for s in signals:
            rule = self.rules.get(s.rule_id)
            theme = rule.get("规则主题") if rule else ""
            out.append(f"[{s.rule_id} {theme}] {s.reason}")
        if delta is not None:
            out.append(describe_baseline(self.dataset.baseline, str(event.get("机场名称"))))
        if event.get("航空公司业务重要程度"):
            out.append(f"航空公司业务重要程度：{event.get('航空公司业务重要程度')}")
        if not out:
            out.append("未识别到明显风险信号；按常规监测处理。")
        return out

    def _impacts(self, signals) -> list[str]:
        out = []
        if any(s.label == "天气风险" for s in signals):
            out.append("地面保障与后续运行可能承压，但当前无正式延误状态。")
        if any(s.label in ("运行压力", "异常波动") for s in signals):
            out.append("按计划完成航班比例低于自身基线，放行/登机口资源可能趋紧。")
        if any(s.label == "数据来源冲突" for s in signals):
            out.append("指标读数不可靠，暂不能给出确定性结论。")
        if any(s.label == "旅客沟通" for s in signals):
            out.append("存在面向旅客的信息沟通需求，需谨慎措辞。")
        return out or ["无明显不利影响，继续常规监测。"]

    def _assumptions(self, event, signals) -> list[str]:
        out = []
        for s in signals:
            if s.label == "天气风险":
                out.append("假设天气提示准确且会持续到所覆盖时段。")
            if s.label == "运行压力":
                out.append("假设“下降”指按计划完成比例相对自身基线下降。")
        out.append("上述均为假设，需人工核查后方可作为行动依据。")
        return out

    def _info_gaps(self, event) -> list[str]:
        unknown = event.get("未知信息")
        if unknown:
            return [str(unknown)]
        return ["（事件未提供未知信息字段）"]

    def _actions(self, signals) -> tuple[str, list[str]]:
        steps: list[str] = []
        for s in signals:
            rule = self.rules.get(s.rule_id)
            if not rule:
                continue
            verify = rule.get("建议核查事项")
            action = rule.get("建议行动")
            if verify:
                steps.append(f"核查：{verify}")
            if action:
                steps.append(f"行动：{action}")
        seen, ordered = set(), []
        for s in steps:
            if s not in seen:
                seen.add(s)
                ordered.append(s)
        first = ordered[0] if ordered else "按常规监测清单逐项核查。"
        return first, ordered[1:]

    def _escalation(self, signals, event) -> str:
        labels = {s.label for s in signals}
        independent = labels & {"天气风险", "运行压力", "异常波动"}
        if len(independent) >= 2 or "数据来源冲突" in labels:
            return "升级运营负责人（RULE008 / RULE001），等待人工复核后再推进。"
        if "人工否决" in labels:
            return "尊重人工否决，不升级为高风险，改为持续监测（RULE006）。"
        if independent:
            return "若机场保障能力下降并出现正式运行异常，升级运营负责人。"
        return "暂不升级，持续监测。"

    def _human_decisions(self, event, signals) -> list[str]:
        out = []
        out.append("面向旅客的正式通知必须人工审核后发布（RULE005）。")
        labels = {s.label for s in signals}
        if any(s.label == "重大运行决定" for s in signals):
            out.append("取消/放行/调度/维修/赔付等必须由持证专业人员决定（RULE007）。")
        if any(s.label == "数据来源冲突" for s in signals):
            out.append("不得自行选定更有利的来源；需人工复核口径与更新时间（RULE001）。")
        if any(s.label == "人工否决" for s in signals):
            out.append("尊重并保留人工否决意见，不得覆盖（RULE006）。")
        if any(s.label == "隐私信息" for s in signals):
            out.append("输入含个人信息，需删除或匿名，仅使用汇总信息（RULE011）。")
        return out

    def _citations(self, signals) -> list[str]:
        cited = ["SIM-BASE", "SIM-SCALE"]
        ids = [s.rule_id for s in signals]
        for rid in ids:
            if rid not in cited:
                cited.append(rid)
        if any(s.label == "天气风险" for s in signals):
            if "SIM-WEATHER" not in cited:
                cited.append("SIM-WEATHER")
        return cited

    def _messages(self, event, signals, delta):
        airport = event.get("机场名称")
        weather = event.get("天气描述")
        risk = self._risk_level(signals, event)
        if risk == "无法判断":
            internal = (
                f"模拟运营提示：{airport}风险暂无法判断（数据来源冲突），"
                "请先复核数据来源、更新时间与统计口径，再下结论。"
            )
        else:
            internal = (
                f"模拟运营提示：{airport}存在{risk}风险信号，暂无正式延误结论。"
                "请优先核查机场保障能力、前序运行与后续任务集中程度。"
            )
        coord = (
            f"模拟协调信息：请确认{airport}的最新天气/运行更新、地面保障能力"
            "及需要重点协调的时段。"
        )
        pax = (
            f"模拟旅客信息草案：{airport}未来数小时运行可能受到影响。"
            "当前航班状态请以航空公司正式通知为准，请留意后续更新。"
        )
        has_weather_signal = any(s.label == "天气风险" for s in signals)
        if has_weather_signal and weather:
            pax = pax.replace("运行可能受到影响", f"可能受天气影响（{weather}）")
        return internal, coord, pax
