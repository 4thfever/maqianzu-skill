# 马前卒人物 Fact 索引

本页提供给 Codex 和维护者的轻量入口。详细人读说明见 `docs/dev/maqianzu-person-facts.md`，结构化检索层见 `facts/maqianzu/*.jsonl`。

## 文件

- `facts/maqianzu/verified.jsonl`：可优先引用的已核实事实
- `facts/maqianzu/candidate.jsonl`：可继续核实的候选事实
- `facts/maqianzu/avoid.jsonl`：敏感或默认不引用的事实

## 高频主题

- 履历：出生年份、毕业时间、观察者网经历、创业时间
- 平台：天涯、知乎、微博、B站、新闻列表
- 成长：农村、矿区、小山沟、河北平泉
- 方法：好问题、新闻筛选、媒体孵化器、社区训练
- 偏好：流浪地球2、李焕英、香港市民文化、天空之城

## 检索建议

- 先按 `predicate`、`object`、`keywords` 检索
- 默认只引用 `verified.jsonl` 中 `citation_safe=true` 的条目
- `candidate.jsonl` 只用于补线索，不直接当硬事实输出
- `avoid.jsonl` 默认不进入普通 persona 输出
