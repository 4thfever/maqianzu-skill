<div align="center">

# 马前卒 Skill

<p>
  <img src="./ma_claw.png" alt="马前卒 Skill cover" width="360" />
</p>

<table>
<tr>
  <td>
    <blockquote>
      <h2>保卫我们的现代生活</h2>
    </blockquote>
  </td>
</tr>
</table>

<p>
  <img src="https://img.shields.io/badge/OpenClaw-Workspace-2F6FEB?style=for-the-badge" alt="OpenClaw Workspace" />
  <img src="https://img.shields.io/badge/Knowledge-Local%20First-0A7F5A?style=for-the-badge" alt="Local First" />
  <img src="https://img.shields.io/badge/Mode-Structured%20Analysis-8B5CF6?style=for-the-badge" alt="Structured Analysis" />
  <img src="https://img.shields.io/badge/License-MIT-F2C94C?style=for-the-badge" alt="MIT License" />
</p>

<p>
  <a href="#快速开始">快速开始</a> ·
  <a href="#适用场景">适用场景</a> ·
  <a href="#仓库结构">仓库结构</a> ·
  <a href="#工作流">工作流</a> ·
  <a href="#更新知识库">更新知识库</a> ·
  <a href="#声明">声明</a>
</p>

</div>

一个尽可能还原马前卒/睡前消息的问题分析方式、观点、态度、口吻和记忆的Skill。以 OpenClaw 为主要运行平台。

## 快速开始

如果你只是想把这个 skill 跑起来，最短路径如下：

```bash
git clone https://github.com/4thfever/maqianzu-skill ~/openclaw-workspaces/maqianzu
openclaw --workspace ~/openclaw-workspaces/maqianzu
```

进入 OpenClaw 后可以直接提问；如果想先确认 workspace 上下文是否正常，再检查：

```text
/context list
```

正常情况下，你应该能看到：

- `AGENTS.md`
- `SOUL.md`
- `TOOLS.md`

如果还想确认显式 skill 入口已经被识别，可以执行：

```bash
openclaw skills list --workspace ~/openclaw-workspaces/maqianzu
```

看到 `maqianzu` 后，说明 skill 入口已经被 OpenClaw 识别。

在这个 workspace 里，日常提问默认就应按本仓库定义的分析路径回答，不需要每次显式写“请用马前卒式分析”。例如：

```text
地方债问题的核心矛盾是什么？
```

<details>
<summary>展开查看完整上手流程</summary>

### 1. 安装 OpenClaw

先确保你已经能在终端里运行：

```bash
openclaw --help
```

如果这条命令能执行，说明 OpenClaw 已经装好了。

### 2. 把仓库 clone 到本地

```bash
git clone https://github.com/4thfever/maqianzu-skill ~/openclaw-workspaces/maqianzu
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
地方债问题的核心矛盾是什么？
```

正常情况下，OpenClaw 会先利用：

- `AGENTS.md`
- `SOUL.md`
- `TOOLS.md`
- `skills/maqianzu/SKILL.md`

也就是说，`skills/maqianzu/SKILL.md` 是一个显式的 skill 入口，但这个 workspace 本身也已经默认按“马前卒式分析”的方向组织回答。

再按需进入：

- `knowledge/quickstart.md`
- `knowledge/topics/*.md`
- `knowledge/episodes/...`

### 7. 如果只想更新知识库，再运行构建脚本

平时问答不用跑构建。只有你想同步上游语料时，才运行：

```bash
python tools/build_all.py
```

</details>

## 适用场景

适合：

- 本地分析、可追溯、带材料依据的问答
- 复用“结构分析 -> 现实约束 -> 结论判断”的回答路径
- 优先依赖本地知识文件，而不是外部向量库
- 先缩小主题范围，再逐层进入节目材料

不太适合：

- 联网实时问答
- 通用闲聊人格包
- 零维护使用

## 项目定位

- 以 OpenClaw 为主要支持平台
- 以本地文件知识库为基础，不依赖外部向量库
- 重点放在分析框架、论证习惯和表达风格
- 回答时优先缩小主题范围，再按需读取具体节目材料

## 仓库结构

如果你第一次看这个仓库，优先关注下面这几个入口文件：

```text
maqianzu-skill/
├─ AGENTS.md                  # workspace 总规则
├─ SOUL.md                    # 高层人格与表达气质
├─ TOOLS.md                   # 工具使用与检索工作流
├─ skills/
│  └─ maqianzu/
│     └─ SKILL.md             # OpenClaw skill 入口
├─ prompts/                   # 分析、人格、边界与检索规则
├─ knowledge/
│  ├─ quickstart.md           # 高频主题与快速入口
│  ├─ index.md                # 知识总入口
│  ├─ topics/                 # 主题索引
│  └─ episodes/               # 节目级元数据与 chunk
├─ tools/                     # 语料抓取、标准化、切分、建索引、校验脚本
└─ docs/                      # 补充文档与开发记录
```

## 集成方式

本仓库既可以作为独立 workspace 直接运行，也保留了 `skills/maqianzu/SKILL.md` 作为显式 skill 入口。

在 OpenClaw 以该目录作为 workspace 运行时，可优先配合以下文件使用：

- `AGENTS.md`
- `SOUL.md`
- `TOOLS.md`

而 `skills/maqianzu/SKILL.md` 会作为额外的显式入口提供给 agent。

## 工作流

> 这个 workspace 的核心不是“全库搜索”，而是“先判断主题，再逐层下钻”。

1. 先由 OpenClaw 注入 `AGENTS.md`、`SOUL.md`、`TOOLS.md`
2. 再按需读取 `skills/maqianzu/SKILL.md`
3. 先看 `knowledge/quickstart.md`
4. 再看 `knowledge/topics/*.md`
5. 最后按需进入 `knowledge/episodes/.../meta.md` 与具体 chunk

仓库已包含可直接使用的 `prompts/` 和 `knowledge/`。如果只是使用 skill，通常不需要先重建知识库。

## 更新知识库

平时问答不用跑构建。只有你想同步上游最新语料时，才运行：

```bash
python tools/build_all.py
```

如需查看构建细节，见 [docs/build-process.md](docs/build-process.md)。

## 声明

> [!IMPORTANT]
> 本项目是一个基于公开材料整理的非官方 skill/workspace，不代表马前卒本人当前或未来的真实立场。
>
> 本项目主要基于公开节目材料整理，目标是构建一种“马前卒式分析框架”的 OpenClaw skill。
>
> 本项目基于公开数据提供 AI 能力，仅供学习交流使用；如果在使用过程中涉及违法行为，由使用者本人负责，开发者对此不承担任何责任。
>
> 若马督工本人或睡前消息官方认为本 repo 不合适，本人会将其下架。

## 延伸阅读

- [构建过程](docs/build-process.md)
- [致谢说明](docs/acknowledgements.md)
- [开发档案](docs/dev/README.md)

## 致谢

感谢以下项目为本仓库提供基础结构或语料来源：

- `therealXiaomanChu/ex-skill`
- `bedtimenews/bedtimenews-archive-contents`
- 马督工与睡前消息团队
