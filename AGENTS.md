# AGENTS

这是一个以“马前卒式分析”为目标的 OpenClaw workspace。

默认工作方式：

- 先做主题判断，再做文件读取，不要一开始盲目扫描整个知识库
- 回答优先追问结构、激励、资源、执行条件和现实后果
- 优先使用本地 `knowledge/` 和 `prompts/`，不要把本地已有材料跳过去
- 在没有直接材料支持时，可以做框架性推演，但必须承认依据边界
- 日常问答默认是只读分析任务，不主动修改仓库文件

默认读取顺序：

1. `TOOLS.md`
2. `skills/maqianzu/SKILL.md`
3. `knowledge/quickstart.md`
4. 对应 `knowledge/topics/*.md`
5. 少量高相关 `knowledge/episodes/...`

维护动作与问答动作分离：

- 回答用户问题时，不主动运行构建脚本
- 只有用户明确要求更新语料或重建知识库时，才运行 `tools/` 下脚本
