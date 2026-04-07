# Facts Layer

本目录用于存放适合 Codex 检索、筛选和引用的结构化事实层。

和 `docs/dev/` 下的人读研究笔记不同，这里的重点不是展开论证，而是提供：

- 稳定字段
- 低成本检索
- 可控引用边界

## 当前内容

- `maqianzu/verified.jsonl`：已核实且默认可优先引用的事实
- `maqianzu/candidate.jsonl`：候选事实与待核实线索
- `maqianzu/avoid.jsonl`：敏感或默认不建议引用的事实

## 建议用法

1. 先查 `verified.jsonl`
2. 优先筛选 `citation_safe=true`
3. 再按 `predicate`、`object`、`keywords` 缩小范围
4. 需要上下文时回到 `docs/dev/maqianzu-person-facts.md`
5. 需要节目级核对时再进入 `knowledge/episodes/...`

如果需要一个固定的检索顺序模板，可直接参考 `query-template.md`。

## 字段说明

- `fact_id`：稳定 ID
- `status`：`verified` / `candidate` / `avoid`
- `confidence`：当前整理信心
- `evidence_level`：证据强度
- `claim`：原始命题
- `normalized_claim`：更适合引用的保守表述
- `recommended_wording`：输出时优先采用的措辞
- `source_path`：原始来源路径
- `source_excerpt`：用于快速人工复核的摘录
- `predicate` / `object` / `keywords`：检索辅助字段
- `citation_safe`：是否默认适合直接进入普通回答
- `quote_strength`：`direct` / `summarized`

## 维护原则

- 不要让 `candidate` 和 `verified` 混用
- 不要把 `avoid` 层内容喂回普通 persona
- 更新结构化层时，尽量同时更新对应的人读说明文件
