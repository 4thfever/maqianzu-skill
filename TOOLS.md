# TOOLS

本仓库主要服务于本地知识检索与分析型使用场景。

## 默认工具偏好

- 回答问题时优先读取本地文件
- 只在必要时运行脚本
- 不为了“多看一点”而读取大量无关文件
- 如问题是人物公开 fact 检索，优先读取 `facts/` 结构化层

## 推荐读取路径

1. 先读 `skills/maqianzu/SKILL.md`
2. 再读 `prompts/analysis_framework.md`
3. 再读 `prompts/response_policy.md`
4. 如果是人物 fact 问题，先读 `facts/maqianzu/verified.jsonl`
5. 再按需读 `docs/dev/maqianzu-person-facts-index.md`
6. 再读 `knowledge/quickstart.md`
7. 再进入相关 `knowledge/topics/*.md`
8. 最后按需读取 `knowledge/episodes/...`

`data/` 的默认使用方式：

- `data/chunked/`：证据层与构建结果层，可在需要节目级核对时读取
- `data/normalized/`：标准化中间层，主要用于维护和排查
- `data/upstream/`：原始语料层，主要用于回溯来源

## 何时运行脚本

只有在以下情况才建议运行 `tools/` 下脚本：

- 用户明确要求更新知识库
- 用户明确要求重建数据或索引
- 需要运行 `python tools/build_all.py`
- 需要执行单独的构建、校验脚本

## 不推荐的行为

- 不要在问答阶段无端修改知识文件
- 不要在没有缩小主题范围前扫描大量 chunk
- 不要把构建脚本当作日常回答流程的一部分
- 不要把 `data/normalized/` 或 `data/upstream/` 当作日常问答起点
- 不要在已有 `verified.jsonl` 可用时，跳过结构化层直接从候选 fact 或评论性材料起步
