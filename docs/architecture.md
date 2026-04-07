# 项目结构说明

## 目标

本项目采用“控制层 + prompt 层 + knowledge 层 + tools 层”的分层结构，目的是让 Codex 在一个可读、可查、可维护的本地仓库内完成检索和回答。

## 分层总览

- `AGENTS.md`：Codex 顶层执行协议
- `SOUL.md`：高层人格与表达气质
- `TOOLS.md`：工具偏好与检索纪律
- `skills/maqianzu/SKILL.md`：分析模式入口
- `prompts/`：详细分析规则
- `knowledge/`：本地知识库
- `facts/`：适合检索与引用的结构化事实层
- `tools/`：构建脚本
- `data/`：构建中间产物与证据分层

## 分层说明

### 控制层

仓库根目录下的控制文件用于提供全局上下文：

- `AGENTS.md`：总规则与默认执行顺序
- `SOUL.md`：高层人格与表达气质
- `TOOLS.md`：工具偏好与检索流程

### prompts

`prompts/` 用于定义分析和回答细则。

其中包括：

- `persona.md`：公开表达风格与说话习惯
- `analysis_framework.md`：常见分析路径与推理框架
- `response_policy.md`：回答边界与输出约束
- `retrieval_workflow.md`：读取知识库的顺序与检索方式
- `topic_router.md`：主题判断与跨主题路由规则

### knowledge

`knowledge/` 用于存放可被 Codex 按需读取的知识库文件。

设计目标：

- 按来源类型区分 `main` 与 `livestream`
- 通过 `knowledge/episodes/<source_type>/<episode_id>/` 组织正式节目目录
- 通过 `topics/` 与 `index.md` 提供索引入口
- 最终通过 chunk 文件支持按需精读

### facts

`facts/` 用于存放从知识库和公开材料中提炼出的结构化事实层。

设计目标：

- 给 Codex 提供低成本、可筛选、可分级的事实检索入口
- 把 `verified`、`candidate`、`avoid` 三类材料分开
- 让模型先命中结构化字段，再按需回到 `docs/dev/` 和 `knowledge/`

### data

`data/` 用于存放构建流水线的中间层与证据层文件。

其中：

- `data/upstream/`：原始上游材料
- `data/normalized/`：标准化后的整篇文本
- `data/chunked/`：节目级目录、`meta` 与 `chunk`，适合作为二级证据层

### tools

`tools/` 用于存放知识库构建流程脚本。

包括：

- 抓取上游材料
- 清洗和标准化文本
- 切分 chunk
- 生成索引
- 校验知识库结构

## 检索策略

本项目默认采用“先索引、后精读”的方式，而不是假设存在自动向量检索层。

推荐路径：

1. 先由 `AGENTS.md` 建立默认工作边界
2. 再按需读取 `TOOLS.md`、`SOUL.md`、`skills/maqianzu/SKILL.md`
3. 先读 `knowledge/quickstart.md`
4. 再按需回到 `knowledge/index.md`
5. 再读主题索引
6. 最后读取具体 chunk

其中 `data/chunked/` 不是主入口，而是当主题已经缩小、需要节目级核对时再进入的证据层。

## 开发档案

如果需要了解本仓库的研究记录、执行计划和开发过程，见 [docs/dev/README.md](dev/README.md)。
