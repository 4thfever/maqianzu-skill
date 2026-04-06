# 构建流程

本页描述的是维护者更新本地知识库时使用的构建链路，不属于 OpenClaw 日常问答路径的一部分。

本项目的构建流程分为四步：

1. 获取上游语料
2. 标准化文本
3. 切分知识块
4. 生成主题索引与总索引

## 构建步骤

### 1. 获取上游语料

脚本：

- `tools/fetch_sources.py`

职责：

- 从 `bedtimenews/bedtimenews-archive-contents` 拉取语料
- 使用稀疏检出，只保留 `main` 与 `livestream`
- 将上游仓库存放到 `data/upstream/bedtimenews-archive-contents/`

运行方式：

```bash
python tools/fetch_sources.py
```

### 2. 标准化文本

脚本：

- `tools/normalize_archive.py`

职责：

- 只处理 `main` 与 `livestream`
- 保留目录结构
- 将文本统一转换为 UTF-8
- 统一换行与行尾空白
- 输出标准化清单 `data/normalized/manifest.json`

运行方式：

```bash
python tools/normalize_archive.py
```

### 3. 切分知识块

脚本：

- `tools/split_chunks.py`

职责：

- 按页面类型区分 `main` 与 `livestream`
- 过滤 `livestream` 年度索引页
- 跳过只有嵌入模板、没有正文的空页面
- 输出节目级目录、`meta.md`、`meta.json` 与 chunk 文件

运行方式：

```bash
python tools/split_chunks.py
```

## 目录约定

- `data/upstream/`：上游稀疏检出
- `data/normalized/`：标准化后的中间文本
- `data/chunked/`：切分后的节目目录与 chunk

`data/` 属于构建中间产物，默认不提交到仓库。

### 4. 生成主题索引与总索引

脚本：

- `tools/build_index.py`
- `tools/validate_knowledge.py`
- `tools/build_all.py`

职责：

- 从 `data/chunked/` 读取节目级元数据
- 将节目目录同步到 `knowledge/episodes/`
- 生成 `knowledge/index.md`
- 生成 `knowledge/topics/*.md`
- 生成 `knowledge/catalog.json`
- 校验索引引用是否完整、主题是否有效

运行方式：

```bash
python tools/build_index.py
python tools/validate_knowledge.py
```

一键运行：

```bash
python tools/build_all.py
```

## 构建结果

当前构建链路已经可以完整跑通：

1. 稀疏拉取上游 `main` 与 `livestream`
2. 标准化文本
3. 切分节目和 chunk
4. 生成知识总索引与主题索引
5. 执行知识校验
