# Codex 使用说明

本仓库的默认使用方式是：在 Codex 中打开仓库后直接提问，由仓库内部规则引导读取和回答。

## 控制链

默认控制链如下：

1. `AGENTS.md`
2. `TOOLS.md`
3. `SOUL.md`
4. `skills/maqianzu/SKILL.md`
5. `prompts/analysis_framework.md`
6. `prompts/response_policy.md`
7. `prompts/retrieval_workflow.md`
8. `prompts/topic_router.md`
9. `knowledge/quickstart.md`
10. `knowledge/topics/*.md`
11. `knowledge/episodes/...`

`data/` 的使用层级：

- `data/chunked/`：二级证据层，可在需要节目级核对时读取
- `data/normalized/`：维护中间层
- `data/upstream/`：原始来源层

## 日常问答

日常问答默认只读分析，不主动运行维护脚本，不主动修改知识文件。

优先做的事情：

- 判断问题属于哪个主题
- 读取最少量、最相关的材料
- 区分直接依据和框架推演
- 给出结构分析、现实约束和结论判断

如果问题主要是在问人物公开 fact，默认先走：

1. `facts/maqianzu/verified.jsonl`
2. `facts/query-template.md`
3. `docs/dev/maqianzu-person-facts-index.md`
4. 必要时再回到 `knowledge/episodes/...`

## 何时进入节目级材料

只有在以下情况才建议读取 `knowledge/episodes/...`：

- 需要更具体的节目材料支撑判断
- 需要核对节目级元数据或片段
- 主题页无法提供足够细节

如果需要核对切分结果、chunk 元数据或构建中间层，可进一步读取 `data/chunked/...`。

## 何时回到总索引

以下情况适合读取 `knowledge/index.md`：

- 主题不明确
- 问题明显跨越多个主题
- 需要查看最近节目
- 需要判断整体分布
