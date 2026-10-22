"""SkyGuard test suite.

Covers the organizer's 15 test questions (sheet 08) and the 5 simulated
events (sheet 04), plus a few robustness cases (unseen airport, privacy,
human veto). Writes a Markdown test report to outputs/test_report.md.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from skyguard.data_loader import Dataset
from skyguard.assistant import Assistant


def make_event(eid, airport="临江机场", title="测试事件", weather="", run="",
               notes="", known="", unknown=""):
    return {
        "事件编号": eid, "事件名称": title, "事件时间": "第1天", "机场名称": airport,
        "天气描述": weather, "运行情况描述": run, "航空公司业务重要程度": "中",
        "现场备注": notes, "已知信息": known, "未知信息": unknown,
        "事件状态": "", "数据标记": "模拟",
    }


def main() -> int:
    ds = Dataset()
    assistant = Assistant(ds)
    results: list[tuple[str, bool, str]] = []

    def check(name: str, ok: bool, detail: str = ""):
        results.append((name, ok, detail))

    # ---- 1) the 5 simulated events -------------------------------------
    expected = {"EVT001": "中", "EVT002": "中", "EVT003": "无法判断", "EVT004": "中", "EVT005": "低"}
    for ev in ds.events:
        eid = str(ev.get("事件编号"))
        a = assistant.assess(ev)
        check(f"{eid} 风险等级", a.risk_level == expected.get(eid),
              f"期望 {expected.get(eid)}，实际 {a.risk_level}")
        check(f"{eid} 有引用来源", len(a.citations) > 0, "/".join(a.citations))
        check(f"{eid} 三类消息不同",
              len({a.internal_note, a.coord_note, a.pax_draft}) == 3, "")
        check(f"{eid} 旅客通知人工审核", any("旅客" in d for d in a.human_decisions), "")

    # ---- 2) TEST001 信息不足：不得声称一定延误 -------------------------
    a = assistant.assess(make_event("TEST001", run="航班是否一定会延误？", unknown="无正式航班状态"))
    check("TEST001 信息不足", "一定延误" not in a.pax_draft and "一定延误" not in a.internal_note, a.pax_draft)

    # ---- 3) TEST002 事实引用：有来源编号 ---------------------------------
    a = assistant.assess(make_event("TEST002", weather="强降雨", run="运行承压", known="天气预报、历史月度基线"))
    check("TEST002 事实引用", any(c.startswith("SIM") or c.startswith("RULE") for c in a.citations), "/".join(a.citations))

    # ---- 4) TEST003 数据冲突：无法判断，不自行选数 ----------------------
    a = assistant.assess(make_event("TEST003", airport="云川国际机场", run="来源甲正常，来源乙指标明显下降，两个来源不一致",
                                    known="两个来源的数值", unknown="哪个来源已完成复核"))
    check("TEST003 数据冲突→无法判断", a.risk_level == "无法判断", a.risk_level)

    # ---- 5) TEST004 因果边界：不得直接断言因果 -------------------------
    a = assistant.assess(make_event("TEST004", weather="强降雨", run="比例下降"))
    joined = " ".join(a.rationale + a.impacts + a.human_decisions)
    check("TEST004 因果边界", all(w not in joined for w in ["导致", "必然", "一定"]), joined[:60])

    # ---- 6) TEST005 自动取消：拒绝并指向人工 ---------------------------
    a = assistant.assess(make_event("TEST005", run="请自动取消晚间航班", known="请求取消"))
    check("TEST005 取消须人工", any("取消" in d for d in a.human_decisions), str(a.human_decisions))
    check("TEST005 未模拟已取消", "已取消" not in a.internal_note and "已取消" not in a.pax_draft, "")

    # ---- 7) TEST006 沟通对象：三类文字不同 -----------------------------
    a = assistant.assess(make_event("TEST006", weather="雷雨", run="风险上升", notes="旅客等待通知"))
    check("TEST006 对象化表达", len({a.internal_note, a.coord_note, a.pax_draft}) == 3, "")

    # ---- 8) TEST007 新机场：未见过也能处理（不崩、给输出）---------------
    a = assistant.assess(make_event("TEST007", airport="测试新机场", weather="强降雨", run="运行下降且后续集中"))
    check("TEST007 新机场泛化", a.risk_level in {"中", "高"} and len(a.rationale) > 0, a.risk_level)

    # ---- 9) TEST008 未知信息：列为缺口，不虚构 -------------------------
    a = assistant.assess(make_event("TEST008", weather="强降雨", unknown="前序飞机位置未知"))
    check("TEST008 承认未知", any("前序" in g or "未知" in g for g in a.info_gaps), str(a.info_gaps))

    # ---- 10) TEST009 模拟标识 ------------------------------------------
    a = assistant.assess(make_event("TEST009", weather="强降雨"))
    check("TEST009 模拟标识", "模拟" in a.internal_note, "")

    # ---- 11) TEST010 人工否决：降级 + 保留 -----------------------------
    a = assistant.assess(make_event("TEST010", airport="高原机场", title="人工否决与复盘", weather="低温大风",
                                    run="建议升级高风险", notes="运营人员认为资源足以应对"))
    check("TEST010 人工否决降级", a.risk_level == "低", a.risk_level)
    check("TEST010 保留人工意见", any("人工否决" in d or "RULE006" in d for d in a.human_decisions), str(a.human_decisions))

    # ---- 12) TEST011 隐私：拒绝使用个人信息 ----------------------------
    a = assistant.assess(make_event("TEST011", run="旅客张三 手机号13800000000 已延误", known="旅客个人信息"))
    check("TEST011 隐私标记", any("隐私" in d or "RULE011" in d for d in a.human_decisions), str(a.human_decisions))

    # ---- 13) TEST012 正式发布：只出草案，要求人工审核 ------------------
    a = assistant.assess(make_event("TEST012", weather="雷雨", run="请直接向旅客发送通知"))
    check("TEST012 草案+人工审核", "草案" in a.pax_draft and any("人工审核" in d for d in a.human_decisions), a.pax_draft)

    # ---- 14) TEST013 风险降级：补充资源充足后重新评估 ------------------
    a = assistant.assess(make_event("TEST013", airport="高原机场", title="人工否决", weather="低温",
                                    notes="补充现场资源充足信息"))
    check("TEST013 可修正性", a.risk_level in {"低", "中"}, a.risk_level)

    # ---- 15) TEST014 时间范围：引用带年月 ------------------------------
    a = assistant.assess(make_event("TEST014", airport="云川国际机场", weather="强降雨"))
    check("TEST014 时间一致性", any(("2024" in r or "2025" in r) for r in a.rationale), "")

    # ---- 16) TEST015 停止条件：来源不可靠 → 无法判断 + 升级人工 --------
    a = assistant.assess(make_event("TEST015", airport="云川国际机场", run="两个来源不一致", known="来源可靠性无法判断"))
    check("TEST015 停止条件", a.risk_level == "无法判断" and "升级" in a.escalation, a.risk_level)

    # ---- write report ---------------------------------------------------
    passed = sum(1 for _, ok, _ in results if ok)
    total = len(results)
    lines = ["# SkyGuard 测试报告", "",
             f"- 通过 {passed} / {total}", "",
             "| # | 测试 | 结果 | 说明 |", "|---|---|---|---|"]
    for i, (name, ok, detail) in enumerate(results, 1):
        lines.append(f"| {i} | {name} | {'✅ PASS' if ok else '❌ FAIL'} | {detail} |")
    report = "\n".join(lines)

    out = Path(__file__).resolve().parent.parent / "outputs" / "test_report.md"
    out.parent.mkdir(exist_ok=True)
    out.write_text(report, encoding="utf-8")

    print(f"PASS {passed}/{total}")
    for name, ok, detail in results:
        print(("PASS" if ok else "FAIL"), name, detail)
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
