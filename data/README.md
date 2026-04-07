# Data Layers

本目录保存构建流水线的中间产物与证据分层文件。

## 目录角色

- `upstream/`：原始上游语料，仅用于来源回溯与维护
- `normalized/`：标准化后的整篇文本，仅用于校对、排查与重建
- `chunked/`：节目级目录、`meta` 与 `chunk`，可作为二级证据层

## 使用建议

- 日常问答默认不要从 `data/` 起步，优先从 `knowledge/` 进入
- 当主题已缩小到具体节目、需要核对切分结果或补充节目级证据时，再进入 `data/chunked/`
- 只有在维护或排查构建问题时，才读取 `data/normalized/` 与 `data/upstream/`
