# Facts Query Template

本文件提供人物公开 fact 的默认查询顺序，目标是让 Codex 在检索、筛选和引用时尽量走同一套稳定流程。

## 默认顺序

1. 先查 `facts/maqianzu/verified.jsonl`
2. 先筛 `citation_safe=true`
3. 再按问题类型筛 `predicate`
4. 再用 `object` 和 `keywords` 缩小范围
5. 命中后优先输出 `recommended_wording`
6. 需要更保守表述时，退回 `normalized_claim`
7. 需要人工复核时，再看 `source_excerpt` 与 `source_path`
8. 如果 `verified` 不够，再把 `candidate.jsonl` 当线索层使用
9. `avoid.jsonl` 默认不进入普通 persona 输出

## 常见检索入口

- 问生平履历：优先查 `predicate=出生年份`、`毕业年份`、`职业经历`、`职业转型`、`加入机构`、`离开机构`、`创业经历`
- 问平台经历：优先查 `predicate=使用过平台`、`运营栏目`、`平台影响`、`产品起点`、`发布渠道`
- 问公开偏好：优先查 `predicate=公开评价`、`公开推荐`、`公开偏好`、`阅读偏好`
- 问方法和工作流：优先查 `predicate=工作方法`、`产品定位`、`信息来源类型`、`信息来源声明`、`方法论观点`
- 问成长背景：优先查 `predicate=成长经历`、`家乡`、`家庭公开信息`

## 输出约定

- 默认把 `verified + citation_safe=true` 视为可优先引用层
- `candidate` 只能写成“有迹象”“节目包装曾出现”“可保守表述为”，不能写成硬事实
- `quote_strength=direct` 时可更放心做近义转述，`summarized` 时要保守
- 如果 `recommended_wording` 已经足够回答，尽量不要自行扩写
- 如果结构化层与节目原文不一致，以节目原文为准

## 最小检索模式

如果只想快速回答一个人物 fact 问题，默认执行下面四步：

1. 打开 `verified.jsonl`
2. 找 `citation_safe=true`
3. 用 `predicate/object/keywords` 找最接近的 1 到 3 条
4. 直接采用对应的 `recommended_wording`
