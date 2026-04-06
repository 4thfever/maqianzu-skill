# 安装说明

## OpenClaw

本仓库以 OpenClaw 为主要运行平台。

推荐把它作为一个独立 workspace 使用。下面是一种常见示例：

```bash
git clone <your-repo-url> ~/.openclaw/workspaces/maqianzu
openclaw --workspace ~/.openclaw/workspaces/maqianzu
```

说明：

- 将 `<your-repo-url>` 替换为你自己的 GitHub 仓库地址
- workspace 根目录下的 `AGENTS.md`、`SOUL.md`、`TOOLS.md` 应作为 bootstrap 文件使用
- `skills/maqianzu/SKILL.md` 应作为 skill 入口供 agent 按需读取

## 安装后可直接使用的部分

安装完成后，仓库已经具备：

- OpenClaw bootstrap 文件
- 正式 skill 入口 `skills/maqianzu/SKILL.md`
- prompts
- 高频入口 `knowledge/quickstart.md`
- 知识总索引
- 主题索引
- 正式节目目录 `knowledge/episodes/`
- 构建与校验脚本

如果只是使用 skill，可以直接读取现有索引和规则文件。

## 如需重新构建本地知识库

只有在你准备同步上游最新内容，或者你修改了切分/索引脚本时，才需要执行这一步。

```bash
python tools/build_all.py
```

如需逐步执行，也可以使用：

```bash
python tools/fetch_sources.py
python tools/normalize_archive.py
python tools/split_chunks.py
python tools/build_index.py
python tools/validate_knowledge.py
```

## 目录约定

- `skills/maqianzu/`：OpenClaw skill 入口
- `AGENTS.md` / `SOUL.md` / `TOOLS.md`：workspace bootstrap
- `knowledge/`：对 OpenClaw 友好的总索引、主题索引与正式节目目录
- `data/chunked/`：节目级元数据与 chunk 中间层
- `data/normalized/`：标准化文本
- `data/upstream/`：上游语料稀疏检出

`data/` 属于本地构建中间产物，默认不提交到仓库。
