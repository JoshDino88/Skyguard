"""Render an Assessment into a Markdown brief aligned with the template."""
from __future__ import annotations

from .assistant import Assessment


def _bullet(title: str, items: list[str]) -> list[str]:
    out = [f"## {title}"]
    out += [f"- {i}" for i in items]
    out.append("")
    return out


def render_markdown(a: Assessment) -> str:
    L: list[str] = []
    L.append(f"# SkyGuard 决策支持简报 — {a.event_id}")
    L.append("")
    L.append(f"- **机场 / 时间**：{a.scope}")
    L.append(f"- **风险等级**：{a.risk_level}")
    L.append("")
    L += _bullet("判断依据", a.rationale)
    L += _bullet("可能影响", a.impacts)
    L += _bullet("待核查假设", a.assumptions)
    L += _bullet("信息缺口", a.info_gaps)
    L.append("## 行动建议")
    L.append(f"- **第一步**：{a.first_step}")
    L += [f"- {s}" for s in a.next_steps]
    L.append("")
    L.append("## 升级条件")
    L.append(f"- {a.escalation}")
    L.append("")
    L += _bullet("必须人工决定事项", a.human_decisions)
    L += _bullet("引用来源", a.citations)
    L.append("## 三类受众草案消息（发布前均须人工审核）")
    L.append(f"- **内部运营提示**：{a.internal_note}")
    L.append(f"- **机场协调信息**：{a.coord_note}")
    L.append(f"- **旅客信息草案**：{a.pax_draft}")
    L.append("")
    L.append("> 本输出基于赛事方模拟数据（SIM-BASE / SIM-SCALE / SIM-WEATHER），不对应真实机构或真实运行。")
    return "\n".join(L)
