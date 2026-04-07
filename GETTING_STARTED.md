# 快速开始

本仓库面向 Codex 使用，不需要安装额外的平台插件或导入专用工作空间。

## 1. 获取仓库

```powershell
git clone https://github.com/4thfever/maqianzu-skill
cd maqianzu-skill
```

## 2. 在 Codex 中打开仓库

打开该仓库后，Codex 会默认以 `AGENTS.md` 作为顶层执行协议，再按需读取：

- `TOOLS.md`
- `SOUL.md`
- `skills/maqianzu/SKILL.md`
- `prompts/*`
- `knowledge/*`

## 3. 直接提问

日常使用时，直接提问即可。例如：

```text
地方债问题的核心矛盾是什么？
```

```text
中国制造业升级为什么总是卡在组织能力上？
```

## 4. 如果希望答案说明依据

可以直接要求：

```text
请说明你主要依据了哪些主题页或节目材料。
```

## 5. 如果希望更新知识库

只有在你明确想同步上游语料、重建索引或执行校验时，才运行维护脚本：

```bash
python tools/build_all.py
```

或按需执行：

```bash
python tools/fetch_sources.py
python tools/normalize_archive.py
python tools/split_chunks.py
python tools/build_index.py
python tools/validate_knowledge.py
```

## 6. 建议的使用习惯

- 单一主题问题优先从 `knowledge/quickstart.md` 和 `knowledge/topics/*.md` 进入
- 只有在问题跨主题时，再回到 `knowledge/index.md`
- 日常问答默认只读，不主动修改知识文件
