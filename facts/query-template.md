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

补充规则：

- 如果用户在问“怎么看某人”“喜不喜欢某演员”“对某作品/人物有没有偏好”这类公开偏好问题，`verified` 没命中时，默认继续查 `candidate.jsonl`
- 查 `candidate` 时，优先继续用 `predicate=公开评价/公开偏好/公开推荐` 配合 `object`、`keywords` 缩小范围
- 命中 `candidate` 后，优先采用其中的 `recommended_wording`，并明确这是保守表述，不上升为硬事实

## 常见检索入口

- 问生平履历：优先查 `predicate=出生年份`、`毕业年份`、`职业经历`、`职业转型`、`加入机构`、`离开机构`、`创业经历`
- 问平台经历：优先查 `predicate=使用过平台`、`运营栏目`、`平台影响`、`产品起点`、`发布渠道`
- 问公开偏好：优先查 `predicate=公开评价`、`公开推荐`、`公开偏好`、`阅读偏好`
- 问方法和工作流：优先查 `predicate=工作方法`、`产品定位`、`信息来源类型`、`信息来源声明`、`方法论观点`
- 问成长背景：优先查 `predicate=成长经历`、`家乡`、`家庭公开信息`

其中“你怎么看刘亦菲”“你喜不喜欢某演员”“你怎么评价某部作品”这类问题，通常同时需要：

- 先查 `verified`
- 未命中再查 `candidate`
- 再回到相关 `knowledge/topics/*.md` 或少量 `knowledge/episodes/...`

## 输出约定

- 默认把 `verified + citation_safe=true` 视为可优先引用层
- `candidate` 只能写成“有迹象”“节目包装曾出现”“可保守表述为”，不能写成硬事实
- `quote_strength=direct` 时可更放心做近义转述，`summarized` 时要保守
- 如果 `recommended_wording` 已经足够回答，尽量不要自行扩写
- 如果结构化层与节目原文不一致，以节目原文为准
- 最终回答不要暴露“我刚查了 candidate”这类后台过程，而应把保守措辞自然融进 persona 输出。

## 最小检索模式

如果只想快速回答一个人物 fact 问题，默认执行下面五步：

1. 打开 `verified.jsonl`
2. 找 `citation_safe=true`
3. 用 `predicate/object/keywords` 找最接近的 1 到 3 条
4. 如果是公开偏好类问题且 `verified` 不足，再查 `candidate.jsonl`
5. 直接采用最稳妥的 `recommended_wording`
