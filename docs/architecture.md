# 项目结构说明

## 目标

本项目采用“bootstrap 层 + prompt 层 + knowledge 层 + tools 层”的分层结构，目的是让 OpenClaw 在一个可读、可查、可维护的本地 workspace 内完成检索和回答。

## 分层总览

- `AGENTS.md` / `SOUL.md` / `TOOLS.md`：workspace bootstrap
- `skills/maqianzu/SKILL.md`：skill 入口
- `prompts/`：详细分析规则
- `knowledge/`：本地知识库
- `tools/`：构建脚本

## 分层说明

### bootstrap

workspace 根目录下的 bootstrap 文件用于提供全局上下文：

- `AGENTS.md`：总规则
- `SOUL.md`：高层人格与表达气质
- `TOOLS.md`：工具偏好与检索流程

### prompts

`prompts/` 用于定义 skill 的行为规则。

其中包括：

- `persona.md`：公开表达风格与说话习惯
- `analysis_framework.md`：常见分析路径与推理框架
- `response_policy.md`：回答边界与输出约束
- `retrieval_workflow.md`：读取知识库的顺序与检索方式

### knowledge

`knowledge/` 用于存放可被 OpenClaw 读取的知识库文件。

设计目标：

- 按来源类型区分 `main` 与 `livestream`
- 通过 `knowledge/episodes/<source_type>/<episode_id>/` 组织正式节目目录
- 通过 `topics/` 与 `index.md` 提供索引入口
- 最终通过 chunk 文件支持按需精读

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

1. 先由 workspace 注入 `AGENTS.md`、`SOUL.md`、`TOOLS.md`
2. 再按需读取 `skills/maqianzu/SKILL.md`
3. 先读 `knowledge/quickstart.md`
4. 再按需回到 `knowledge/index.md`
5. 再读主题索引
6. 最后读取具体 chunk

## 开发档案

如果需要了解本仓库的研究记录、执行计划和开发过程，见 [docs/dev/README.md](dev/README.md)。
