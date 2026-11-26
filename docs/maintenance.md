# 维护说明

本页描述的是维护者更新本地知识库时使用的维护动作，不属于日常问答路径的一部分。

## 何时需要维护

以下情况才建议运行维护脚本：

- 同步上游最新语料
- 修改了切分、索引或校验逻辑
- 需要重新生成 `knowledge/` 下的索引文件

## 常用命令

一键重建：

```bash
python tools/build_all.py
```

一键重建会先验证 `data/upstream/bedtimenews-archive-contents/` 是独立的上游
Git 检出，然后备份 `data/normalized/`、`data/chunked/` 和 `knowledge/`。
任一步骤失败都会自动恢复旧产物；全部校验通过后才删除临时备份。

分步执行：

```bash
python tools/fetch_sources.py
python tools/normalize_archive.py
python tools/split_chunks.py
python tools/build_index.py
python tools/validate_knowledge.py
```

各生成脚本默认拒绝覆盖非空输出目录。确需单独重建时，在确认目标路径无误后显式加入
`--replace`，例如：

```bash
python tools/normalize_archive.py --replace
python tools/split_chunks.py --replace
python tools/build_index.py --replace
```

## 维护原则

- 日常问答和维护动作分离
- 维护脚本只在明确需要时运行
- 修改生成文案时同步修改源脚本，避免下次重建回滚
- `data/chunked/` 可以作为节目级证据层保留
- `data/normalized/` 和 `data/upstream/` 主要服务于维护、校对与回溯
- 不得把位于主仓库中的普通子目录当作独立上游 Git 仓库
- 空语料、输入输出目录重叠或已有产物未显式授权覆盖时，应立即终止构建
