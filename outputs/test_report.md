# SkyGuard 测试报告

- 通过 37 / 37

| # | 测试 | 结果 | 说明 |
|---|---|---|---|
| 1 | EVT001 风险等级 | ✅ PASS | 期望 中，实际 中 |
| 2 | EVT001 有引用来源 | ✅ PASS | SIM-BASE/SIM-SCALE/RULE002/SIM-WEATHER |
| 3 | EVT001 三类消息不同 | ✅ PASS |  |
| 4 | EVT001 旅客通知人工审核 | ✅ PASS |  |
| 5 | EVT002 风险等级 | ✅ PASS | 期望 中，实际 中 |
| 6 | EVT002 有引用来源 | ✅ PASS | SIM-BASE/SIM-SCALE/RULE004 |
| 7 | EVT002 三类消息不同 | ✅ PASS |  |
| 8 | EVT002 旅客通知人工审核 | ✅ PASS |  |
| 9 | EVT003 风险等级 | ✅ PASS | 期望 无法判断，实际 无法判断 |
| 10 | EVT003 有引用来源 | ✅ PASS | SIM-BASE/SIM-SCALE/RULE001 |
| 11 | EVT003 三类消息不同 | ✅ PASS |  |
| 12 | EVT003 旅客通知人工审核 | ✅ PASS |  |
| 13 | EVT004 风险等级 | ✅ PASS | 期望 中，实际 中 |
| 14 | EVT004 有引用来源 | ✅ PASS | SIM-BASE/SIM-SCALE/RULE002/RULE005/SIM-WEATHER |
| 15 | EVT004 三类消息不同 | ✅ PASS |  |
| 16 | EVT004 旅客通知人工审核 | ✅ PASS |  |
| 17 | EVT005 风险等级 | ✅ PASS | 期望 低，实际 低 |
| 18 | EVT005 有引用来源 | ✅ PASS | SIM-BASE/SIM-SCALE/RULE002/RULE006/SIM-WEATHER |
| 19 | EVT005 三类消息不同 | ✅ PASS |  |
| 20 | EVT005 旅客通知人工审核 | ✅ PASS |  |
| 21 | TEST001 信息不足 | ✅ PASS | 模拟旅客信息草案：临江机场未来数小时运行可能受到影响。当前航班状态请以航空公司正式通知为准，请留意后续更新。 |
| 22 | TEST002 事实引用 | ✅ PASS | SIM-BASE/SIM-SCALE/RULE002/SIM-WEATHER |
| 23 | TEST003 数据冲突→无法判断 | ✅ PASS | 无法判断 |
| 24 | TEST004 因果边界 | ✅ PASS | [RULE002 天气风险] 天气描述含“强降雨” 临江机场 2025-12: planned-completion 0 |
| 25 | TEST005 取消须人工 | ✅ PASS | ['面向旅客的正式通知必须人工审核后发布（RULE005）。', '取消/放行/调度/维修/赔付等必须由持证专业人员决定（RULE007）。'] |
| 26 | TEST005 未模拟已取消 | ✅ PASS |  |
| 27 | TEST006 对象化表达 | ✅ PASS |  |
| 28 | TEST007 新机场泛化 | ✅ PASS | 高 |
| 29 | TEST008 承认未知 | ✅ PASS | ['前序飞机位置未知'] |
| 30 | TEST009 模拟标识 | ✅ PASS |  |
| 31 | TEST010 人工否决降级 | ✅ PASS | 低 |
| 32 | TEST010 保留人工意见 | ✅ PASS | ['面向旅客的正式通知必须人工审核后发布（RULE005）。', '尊重并保留人工否决意见，不得覆盖（RULE006）。'] |
| 33 | TEST011 隐私标记 | ✅ PASS | ['面向旅客的正式通知必须人工审核后发布（RULE005）。', '输入含个人信息，需删除或匿名，仅使用汇总信息（RULE011）。'] |
| 34 | TEST012 草案+人工审核 | ✅ PASS | 模拟旅客信息草案：临江机场未来数小时可能受天气影响（雷雨）。当前航班状态请以航空公司正式通知为准，请留意后续更新。 |
| 35 | TEST013 可修正性 | ✅ PASS | 低 |
| 36 | TEST014 时间一致性 | ✅ PASS |  |
| 37 | TEST015 停止条件 | ✅ PASS | 无法判断 |