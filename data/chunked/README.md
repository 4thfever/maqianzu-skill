# Chunked Evidence Layer

本目录保存切分后的节目级目录、`meta` 和 `chunk` 文件。

## 适用场景

- 主题已经缩小到具体节目，需要进一步精读
- 需要核对节目级元数据
- 需要验证切分边界或 chunk 内容
- 需要为回答补充更细的节目级证据

## 不适合的场景

- 作为日常问答的主入口
- 在没有缩小问题范围前盲目扫描全部目录

## 推荐读取方式

1. 先通过 `knowledge/quickstart.md` 与 `knowledge/topics/*.md` 缩小范围
2. 再读取本目录下对应节目 `meta.md` 或 `meta.json`
3. 最后按需进入少量 `chunk-*.md`

## 可用索引

- `catalog.json`：全量节目目录与路径索引
- `topics/*.json`：按主题聚合后的节目索引
