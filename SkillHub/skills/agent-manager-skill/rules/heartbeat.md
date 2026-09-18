# agent-manager / heartbeat rules

仅在当前 heartbeat 需要推进 `agent-manager-skill` 相关 OKR 时读取本文件。

## 目标范围
- `fractalmind-ai/agent-manager-skill` 的 Phase 2 / inbound queue / replay / rescue-sweep / heartbeat 相关工作
- 只补 skill-specific 规则；全局升级、审批、静默窗口仍以根级 `HEARTBEAT.md` 为准

## 心跳执行规则
1. 先 `cd projects/fractalmind-ai/agent-manager-skill`
2. 先核对 **当前 canonical tracker**，不要直接复用旧 issue 编号：
   - `gh issue list -R fractalmind-ai/agent-manager-skill --state open`
   - `gh pr list -R fractalmind-ai/agent-manager-skill --state open`
3. `#138 / #141 / PR #142` 现在都只算**历史证据**；若 heartbeat 里仍把它们写成当前 tracker，必须先纠偏再汇报
4. 若现有 Phase 2 切片都已 merge/closed，则先判断：
   - 是 Phase 2 已实质收口，可转 COMPLETE / observe
   - 还是出现了新的剩余缺口，需要**新建 issue** 继续追踪
5. 汇报必须给出可复核证据：issue/PR URL、commit、测试命令、tmux/CLI 输出、文件路径
6. routine review/merge gate 继续 owner 推进；只有触发根级 `HEARTBEAT.md` 的审批项 / 卡点条件时，才升级给 Elliot

## 当前已知提醒（2026-03-20）
- `Issue #141` 已 closed，不能再当作当前 freshest tracker
- open issue 当前主要是 `#117 / #114 / #109`；是否与 Phase 2 直接相关，需每轮 fresh 判断
- 如果本轮只是做 HEARTBEAT / memory 重构，先把 tracker 口径纠偏，再决定是否继续追 agent-manager 代码线
