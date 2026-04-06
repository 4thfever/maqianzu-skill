# 马前卒 Skill

*"战无不胜的马督工降临在他忠诚的赛博临高"*

一个以 OpenClaw 为主要运行平台的 `maqianzu` 本地分析型 skill/workspace。

本仓库基于公开节目材料整理马前卒常见的分析路径、表达风格和知识索引，让 OpenClaw 能优先按“结构分析 -> 现实约束 -> 结论判断”的方式组织回答。

## 项目定位

- 以 OpenClaw 为主要支持平台
- 以本地文件知识库为基础，不依赖外部向量库
- 重点放在分析框架、论证习惯和表达风格
- 回答时优先缩小主题范围，再按需读取具体节目材料

## 仓库结构

- `AGENTS.md`：workspace 总规则
- `SOUL.md`：高层人格与表达气质
- `TOOLS.md`：工具使用与检索工作流
- `skills/maqianzu/SKILL.md`：OpenClaw skill 入口
- `prompts/`：更细的分析、人格、边界与检索规则
- `knowledge/quickstart.md`：高频主题与快速入口
- `knowledge/index.md`：知识总入口
- `knowledge/topics/*.md`：主题索引
- `knowledge/episodes/...`：节目级元数据与 chunk
- `tools/`：语料抓取、标准化、切分、建索引、校验脚本

## OpenClaw 使用

推荐把本仓库作为一个独立 workspace 使用。下面是一种常见示例：

```bash
git clone <your-repo-url> ~/.openclaw/workspaces/maqianzu
openclaw --workspace ~/.openclaw/workspaces/maqianzu
```

在 OpenClaw 以该目录作为 workspace 运行时，可优先配合以下文件使用：

- `AGENTS.md`
- `SOUL.md`
- `TOOLS.md`

而 `skills/maqianzu/SKILL.md` 会作为 skill 入口提供给 agent。

## 傻瓜版指南

如果你只是想把这个 skill 跑起来，不想研究 OpenClaw 配置，可以直接按下面做：

### 1. 安装 OpenClaw

先确保你已经能在终端里运行：

```bash
openclaw --help
```

如果这条命令能执行，说明 OpenClaw 已经装好了。

### 2. 把仓库 clone 到本地

```bash
git clone <your-repo-url> ~/openclaw-workspaces/maqianzu
```

### 3. 直接把这个仓库当成 workspace 启动

```bash
openclaw --workspace ~/openclaw-workspaces/maqianzu
```

这一步最省事，不需要你再手动把 skill 拆到别的目录里。

### 4. 进会话后先检查上下文

在 OpenClaw 里执行：

```text
/context list
```

正常情况下，你应该能看到这几个文件已经进入 workspace 上下文：

- `AGENTS.md`
- `SOUL.md`
- `TOOLS.md`

### 5. 再检查 skill 是否可见

在终端里执行：

```bash
openclaw skills list --workspace ~/openclaw-workspaces/maqianzu
```

如果你看到了 `maqianzu`，说明 skill 入口已经被 OpenClaw 识别。

### 6. 然后就可以直接提问

例如：

```text
请用马前卒式分析，谈谈地方债问题。
```

正常情况下，OpenClaw 会先利用：

- `AGENTS.md`
- `SOUL.md`
- `TOOLS.md`
- `skills/maqianzu/SKILL.md`

再按需进入：

- `knowledge/quickstart.md`
- `knowledge/topics/*.md`
- `knowledge/episodes/...`

### 7. 如果只想更新知识库，再运行构建脚本

平时问答不用跑构建。只有你想同步上游语料时，才运行：

```bash
python tools/build_all.py
```

## 推荐读取顺序

1. 先由 OpenClaw 注入 `AGENTS.md`、`SOUL.md`、`TOOLS.md`
2. 再按需读取 `skills/maqianzu/SKILL.md`
3. 先看 `knowledge/quickstart.md`
4. 再看 `knowledge/topics/*.md`
5. 最后按需进入 `knowledge/episodes/.../meta.md` 与具体 chunk

仓库已包含可直接使用的 `prompts/` 和 `knowledge/`。如果只是使用 skill，通常不需要先重建知识库。

## 更新知识库

如果你想同步上游最新语料，可以运行：

```bash
python tools/build_all.py
```

如需查看构建细节，见 [docs/build-process.md](docs/build-process.md)。

## 声明

本项目是一个基于公开材料整理的非官方 skill/workspace，不代表马前卒本人当前或未来的真实立场。

本项目主要基于公开节目材料整理，目标是构建一种“马前卒式分析框架”的 OpenClaw skill。
若马督工本人或睡前消息官方认为本repo不合适，本人会将其下架。

## 致谢

感谢以下项目为本仓库提供基础结构或语料来源：

- `therealXiaomanChu/ex-skill`
- `bedtimenews/bedtimenews-archive-contents`
- 马督工与睡前消息团队

更完整的说明见 [docs/acknowledgements.md](docs/acknowledgements.md)。

## 开发档案

如需了解研究记录和开发过程，见 [docs/dev/README.md](docs/dev/README.md)。
