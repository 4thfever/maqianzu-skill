# 人物 Fact 检索工作流

本文件用于补充“观点型材料”之外的另一类整理任务：为人物建立可考证、可回溯、可分级的公开 fact 层。

这里的重点不是多收集几个有趣说法，而是尽量避免把玩笑、印象、粉丝共识和断章取义混成“事实”。

## 适用场景

- 想整理马前卒的公开偏好、履历、自我叙述和稳定表达
- 想补充“人物画像”所需的硬信息，而不只是主题观点
- 想把人物相关说法分成“直接事实”“稳定倾向”“单次表达”和“待核实线索”

## 不适用场景

- 不要用本流程整理未公开隐私
- 不要把他人转述直接写成确定事实
- 不要把弹幕、梗图、评论区共识直接入库
- 不要为了搜集人物 fact 而跳过本地材料，直接做全网漫灌搜索

## 核心原则

1. 先确认命题，再搜索材料
2. 先找一手来源，再看二手整理
3. 先做证据分级，再写结论
4. 先找支持证据，再主动找反证
5. 不把高风险标签写成硬事实

## 推荐的 Fact 类型

### 1. 身份与履历类

- 出生年份
- 教育经历
- 工作经历
- 平台迁移
- 栏目沿革

### 2. 文化偏好类

- 喜欢或长期关注的演员、导演、作家、电影、游戏、历史题材
- 反复推荐的作品
- 明确表达过反感的作品类型或文化产品

### 3. 自我叙述类

- “我出生于……”
- “我小时候……”
- “我以前在……”
- “我做媒体这些年……”
- “我为什么做这个节目……”

### 4. 稳定表达类

- 长期重复引用的书、作者、案例、比喻
- 反复出现的审美标准、批评标准
- 长期关注的传播题材或社会对象

### 5. 公开互动类

- 与哪些学者、媒体人、UP 主、机构有明确公开互动
- 是否有长期合作、公开争论或持续引用

### 6. 争议与澄清类

- 外界长期流传的说法
- 他本人是否公开承认、否认或修正

## 证据等级

### A 级：本人一手材料

- 节目原文
- 直播记录
- 本人动态
- 采访原视频或原文
- 公开演讲原文

说明：
这类材料可以作为定案依据，但仍要保留时间和出处。

### B 级：本人材料的整理版

- 知识库中的 `meta.md` 和 `chunk-*.md`
- 字幕稿
- 粉丝整理笔记
- 采访摘要

说明：
这类材料适合当检索入口和证据指针。重要结论应尽量回查 A 级材料。

### C 级：第三方报道

- 媒体报道
- 百科条目
- 第三方评论视频

说明：
这类材料只提供线索，不单独用于落硬结论。

### D 级：梗与评论区共识

- 弹幕
- 评论区戏称
- 粉丝圈内说法
- 对立面剪辑后的标签

说明：
这类信息默认不可信，只用于反向寻找原始出处。

## 事实表述分级

### 硬事实

适用条件：

- 有明确一手来源
- 时间、对象、表达都可定位

推荐写法：

- 某年某月某日，他在某节目中明确提到……

### 稳定倾向

适用条件：

- 有多个时期、多个来源重复支持
- 不是一次节目效果

推荐写法：

- 从多期节目和公开表达看，他长期对……有明显偏好

### 单次表达

适用条件：

- 只有一次明确表达
- 尚不能外推为稳定特征

推荐写法：

- 他曾在某期节目中公开表示……

### 待核实线索

适用条件：

- 目前只有二手材料或梗
- 没找到一手来源

推荐写法：

- 外界曾流传……，当前尚未回查到可定案的一手依据

## 搜索顺序

### 第一轮：本地候选池

目标：
先从仓库内找到“值得搜”的对象和命题，不急着定案。

优先入口：

- `knowledge/topics/*.md`
- `knowledge/episodes/.../meta.md`
- 少量高相关 `chunk-*.md`

建议动作：

- 从标题和摘要里抽人名、作品名、平台名、机构名
- 记录反复出现的文化对象和自我叙述句型
- 先形成 50 到 100 条候选命题

### 第二轮：本人材料定点搜索

目标：
把候选命题回收到本人公开表达中。

优先来源：

- 节目原文
- 直播记录
- 本人动态
- 演讲与访谈

建议动作：

- 针对每条命题拆分成更小的验证问题
- 查询是否为单次提及还是长期重复
- 区分认真评价、顺手举例和节目效果

### 第三轮：外部补证与反证

目标：
确认有没有误传、断章取义或反向证据。

优先来源：

- 外部报道
- 转载整理
- 评论区高频说法

建议动作：

- 主动搜索相反证据
- 查明说法最早出现在哪里
- 确认是不是别人替他下的标签

## 高产搜索句型

优先检索以下类型的表达：

- 我出生于
- 我小时候
- 我大学
- 我以前在
- 我做媒体这些年
- 我做睡前消息以来
- 我一直喜欢
- 我很喜欢
- 我推荐
- 我买了……的书
- 我看过
- 我最讨厌
- 我不是第一次说
- 这个题材我一直关注

这些句型更接近“事实陈述”，比抽象价值判断更适合做人物 fact。

## 搜索词模板

每个候选命题至少准备三组搜索词。

### 1. 精确组

格式：

- `马前卒 + 对象`
- `马督工 + 对象`
- `睡前消息 + 对象`

示例：

- `马前卒 刘亦菲`
- `马督工 冯玮`
- `睡前消息 李焕英`

### 2. 动词组

格式：

- `马前卒 + 动词 + 对象`

常用动词：

- 喜欢
- 推荐
- 夸
- 批评
- 买了
- 看过
- 提过
- 回应

示例：

- `马前卒 喜欢 刘亦菲`
- `马前卒 买了 冯玮的书`
- `马前卒 推荐 李焕英`

### 3. 反证组

格式：

- `马前卒 + 对象 + 原话`
- `马前卒 + 对象 + 断章取义`
- `马前卒 + 对象 + 直播`

示例：

- `马前卒 刘亦菲 原话`
- `马前卒 刘亦菲 断章取义`
- `马前卒 刘亦菲 直播`

## 证据卡模板

每条候选 fact 先写成卡片，不要直接进主知识。

```md
## fact_id

- `claim`: 
- `category`: 
- `candidate_query`: 
- `why_it_matters`: 
- `evidence_level`: 
- `first_seen_in`: 
- `primary_source`: 
- `source_date`: 
- `source_type`: 
- `quote_or_summary`: 
- `counter_evidence`: 
- `recommended_wording`: 
- `status`: candidate / verified / downgraded / rejected
```

## 表格字段模板

如果需要批量管理，建议使用统一字段：

```text
fact_id
claim
category
subject
object
confidence
evidence_level
source_date
source_type
source_path
quote_or_summary
counter_evidence
recommended_wording
status
```

## 推荐的信心等级

- `high`: 有一手来源，且结论表述保守
- `medium`: 有较强支持，但还缺一手回查或存在表述外推
- `low`: 只有二手线索，暂不建议直接用于回答

## 五条示范样本

以下示例用于说明“怎么写”，不是都已经完成最终核验。

### 示例 1

```md
## fact_birth_1981

- `claim`: 马前卒出生于 1981 年
- `category`: 身份与履历
- `candidate_query`: 马前卒 1981；马督工 生于1981
- `why_it_matters`: 属于高价值基础画像信息
- `evidence_level`: B
- `first_seen_in`: `knowledge/topics/media.md`
- `primary_source`: `knowledge/episodes/main/main-201-300-236/meta.md`
- `source_date`: 2021-02-16
- `source_type`: main/meta
- `quote_or_summary`: 节目摘要中出现“生于1981，我带着回忆看李焕英”
- `counter_evidence`: 暂未检出
- `recommended_wording`: 他在 2021-02-16 的节目中明确以“生于1981”为切入谈《李焕英》
- `status`: verified
```

### 示例 2

```md
## fact_liuyifei_interest

- `claim`: 马前卒对刘亦菲有明显正面兴趣
- `category`: 文化偏好
- `candidate_query`: 马前卒 刘亦菲；马督工 喜欢 刘亦菲
- `why_it_matters`: 有助于补充人物文化偏好层
- `evidence_level`: B
- `first_seen_in`: `knowledge/topics/media.md`
- `primary_source`: `knowledge/episodes/main/main-501-600-548/meta.md`
- `source_date`: 2022-02-07
- `source_type`: main/meta
- `quote_or_summary`: 他专门围绕“刘亦菲推荐《围棋少女》”做过一期节目
- `counter_evidence`: 仅凭标题和摘要尚不足以支持“死忠粉丝”这种高强度标签
- `recommended_wording`: 他曾专门围绕刘亦菲与《围棋少女》的争议做节目；若需上升为稳定偏好，还应继续回查 chunk 和其他公开表达
- `status`: candidate
```

### 示例 3

```md
## fact_bought_fengwei_book

- `claim`: 马前卒曾公开表示购买冯玮的书
- `category`: 公开互动
- `candidate_query`: 马前卒 冯玮 买书；马督工 冯玮
- `why_it_matters`: 说明其处理同业争议时的行动方式
- `evidence_level`: B
- `first_seen_in`: `knowledge/topics/media.md`
- `primary_source`: `knowledge/episodes/main/main-201-300-255/meta.md`
- `source_date`: 2021-03-30
- `source_type`: main/meta
- `quote_or_summary`: 标题与摘要均明确写到“我果断买下冯教授的书”
- `counter_evidence`: 需回查节目正文确认是字面购买，还是节目包装措辞
- `recommended_wording`: 他曾在 2021-03-30 的节目中表示，为调查相关争议买了冯玮的书
- `status`: candidate
```

### 示例 4

```md
## fact_recommended_hi_mom

- `claim`: 马前卒曾公开推荐观众全家去看《你好，李焕英》
- `category`: 文化偏好
- `candidate_query`: 马前卒 李焕英 推荐；马督工 李焕英
- `why_it_matters`: 能补充人物的文化消费判断
- `evidence_level`: B
- `first_seen_in`: `knowledge/topics/media.md`
- `primary_source`: `knowledge/episodes/main/main-201-300-236/meta.md`
- `source_date`: 2021-02-16
- `source_type`: main/meta
- `quote_or_summary`: 摘要中有“推荐全家去看看李焕英同志”
- `counter_evidence`: 这更接近单次推荐，不宜直接外推为长期电影口味
- `recommended_wording`: 他曾在谈《你好，李焕英》的节目里明确给出正面推荐
- `status`: candidate
```

### 示例 5

```md
## fact_media_platform_ideal

- `claim`: 马前卒曾系统总结自己对媒体平台的判断标准
- `category`: 自我叙述
- `candidate_query`: 马前卒 平台梦想 8条标准；马督工 复旦 演讲
- `why_it_matters`: 有助于区分其一般观点与自我方法论
- `evidence_level`: B
- `first_seen_in`: `knowledge/topics/media.md`
- `primary_source`: `knowledge/episodes/main/main-301-400-374/meta.md`
- `source_date`: 2021-12-16
- `source_type`: main/meta
- `quote_or_summary`: 节目摘要提到回顾 10 年媒体工作经验和 20 年社交平台用户体会
- `counter_evidence`: 需回查 chunk 或原讲稿，确认哪些属于自我经历，哪些属于一般方法总结
- `recommended_wording`: 他曾在复旦演讲中把自己的媒体实践经验总结为一套平台判断标准
- `status`: candidate
```

## 最小执行流程

如果只想快速跑一轮，可以压缩成下面六步：

1. 从主题页和 `meta.md` 先列 20 条候选 fact
2. 过滤掉明显带情绪的标签词
3. 为每条候选 fact 准备三组搜索词
4. 回查本人一手来源
5. 主动查找反证和误传
6. 用保守措辞写入 fact 卡，不把外推写成定论

## 常见错误

- 把标题党标签当作人物稳定特征
- 只看二手整理，不回查原始材料
- 一次玩笑就上升为长期偏好
- 把外界评价写成本人自述
- 把“可能如此”写成“就是如此”

## 结论

人物 fact 整理的关键，不是搜得更猛，而是把“证据等级”和“表述强度”匹配起来。

搜集阶段可以大胆，定案阶段必须保守。
