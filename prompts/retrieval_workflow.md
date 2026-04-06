# Retrieval Workflow

## 目标

本 workspace / skill 采用“先索引、后精读”的读取方式。

不要在一开始盲目扫描大量文件。应先缩小范围，再读取最相关的材料。

## 基本读取顺序

### 1. 先读行为规则

优先读取：

- `prompts/analysis_framework.md`
- `prompts/response_policy.md`

作用：

- 确定回答方式
- 确定边界
- 确定基本分析重心

### 2. 再读快速入口

优先读取：

- `knowledge/quickstart.md`
- `knowledge/index.md`

作用：

- 快速把问题归到少数几个主题入口
- 判断知识库中有哪些主题
- 判断应该从 `main` 还是 `livestream` 入手
- 判断是否已有可直接对应的主题入口

### 3. 再读主题索引

根据问题主题读取相关文件，例如：

- `knowledge/topics/economy.md`
- `knowledge/topics/industry.md`
- `knowledge/topics/governance.md`
- `knowledge/topics/society.md`
- `knowledge/topics/international.md`
- `knowledge/topics/media.md`

作用：

- 缩小相关材料范围
- 确认关键词和高频问题
- 找到值得精读的节目目录或 chunk

### 4. 最后读具体材料

只在需要时读取：

- 节目 `meta.md`
- 具体 chunk 文件

优先读取最相关、最少量、最能支撑回答的材料，不要为了“读得多”而读无关文件。

## 读取策略

- 问题越具体，读取越精确。
- 问题越宽泛，越要先用主题索引缩小范围。
- 如果已有足够材料支持判断，就不要继续扩张读取范围。
- 如果没有直接材料，就停止盲找，转入“信息不足 + 框架性推演”的回答模式。

## 主题判断提示

可优先按以下方向判断用户问题：

- 财政、增长、消费、收入分配：偏 `economy`
- 制造业、技术路线、产业升级：偏 `industry`
- 政策执行、地方治理、制度安排：偏 `governance`
- 教育、医疗、社会现象、日常生活结构：偏 `society`
- 国际关系、地缘、全球产业链：偏 `international`
- 舆论、平台、媒体传播、节目本身：偏 `media`

## 输出前复核

在回答前至少检查一次：

- 当前判断是否有材料支持
- 哪些部分是直接依据
- 哪些部分是风格化推演
- 是否需要在答案中说明依据边界
