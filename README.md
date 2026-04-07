<div align="left">

# 马前卒.Skill

<tr>
  <td>
    <blockquote>
      <h3>保卫我们的现代生活</h3>
    </blockquote>
  </td>
</tr>

<p>
  <img src="https://img.shields.io/badge/Codex-Ready-2F6FEB?style=for-the-badge" alt="Codex Ready" />
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

一个面向 Codex 的本地分析知识库仓库，目标是尽可能复用马前卒 / 睡前消息常见的结构化分析路径、论证习惯和材料组织方式。

## 快速开始

如果你只是想直接使用这套分析能力，最短路径如下：

```powershell
git clone https://github.com/4thfever/maqianzu-skill
cd maqianzu-skill
```

然后在 Codex 中打开该仓库，直接提问即可。例如：

```text
地方债问题的核心矛盾是什么？
```

正常情况下，Codex 会先遵循以下仓库入口：

- `AGENTS.md`
- `TOOLS.md`
- `SOUL.md`
- `skills/maqianzu/SKILL.md`

再按需进入：

- `prompts/analysis_framework.md`
- `prompts/response_policy.md`
- `prompts/retrieval_workflow.md`
- `prompts/topic_router.md`
- `knowledge/quickstart.md`
- `knowledge/topics/*.md`
- `knowledge/episodes/...`

如果想看更完整的上手说明，见 [GETTING_STARTED.md](GETTING_STARTED.md)。

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

- 面向 Codex 使用
- 以本地文件知识库为基础，不依赖外部向量库
- 重点放在分析框架、论证习惯和表达风格
- 回答时优先缩小主题范围，再按需读取具体节目材料

## 仓库结构

如果你第一次看这个仓库，优先关注下面这几个入口文件：

```text
maqianzu-skill/
├─ AGENTS.md                  # Codex 顶层执行协议
├─ SOUL.md                    # 高层气质与稳定倾向
├─ TOOLS.md                   # 读取与工具使用纪律
├─ skills/
│  └─ maqianzu/
│     └─ SKILL.md             # 仓库内部分析模式入口
├─ prompts/                   # 分析、人格、边界与检索规则
├─ knowledge/
│  ├─ quickstart.md           # 高频主题与快速入口
│  ├─ index.md                # 知识总入口
│  ├─ topics/                 # 主题索引
│  └─ episodes/               # 节目级元数据与 chunk
├─ tools/                     # 语料抓取、标准化、切分、建索引、校验脚本
└─ docs/                      # 补充文档与开发记录
```

## 工作流

> 这个仓库的核心不是“全库搜索”，而是“先判断主题，再逐层下钻”。

默认流程：

1. 先由 `AGENTS.md` 规定读取顺序和工作边界
2. 再由 `TOOLS.md`、`SOUL.md`、`skills/maqianzu/SKILL.md` 建立行为框架
3. 先看 `knowledge/quickstart.md`
4. 再看 `knowledge/topics/*.md`
5. 最后按需进入 `knowledge/episodes/.../meta.md` 与具体 chunk

仓库已包含可直接使用的 `prompts/` 和 `knowledge/`。如果只是日常问答，通常不需要先重建知识库。

## 更新知识库

平时问答不用跑构建。只有你想同步上游最新语料时，才运行：

```bash
python tools/build_all.py
```

如需查看构建细节，见 [docs/build-process.md](docs/build-process.md)。

## 声明

> [!IMPORTANT]
> 本项目是一个基于公开材料整理的非官方本地分析仓库，不代表马前卒本人当前或未来的真实立场。
>
> 本项目主要基于公开节目材料整理，目标是构建一种“马前卒式分析框架”的可复用能力。
>
> 本项目基于公开数据提供 AI 能力，仅供学习交流使用；如果在使用过程中涉及违法行为，由使用者本人负责，开发者对此不承担任何责任。
>
> 若马督工本人或睡前消息官方认为本 repo 不合适，维护者会评估并处理下架请求。

## 延伸阅读

- [快速开始](GETTING_STARTED.md)
- [Codex 使用说明](docs/codex-usage.md)
- [构建过程](docs/build-process.md)
- [架构说明](docs/architecture.md)
- [开发档案](docs/dev/README.md)

## 致谢

感谢以下项目为本仓库提供基础结构或语料来源：

- `therealXiaomanChu/ex-skill`
- `bedtimenews/bedtimenews-archive-contents`
- 马督工与睡前消息团队
