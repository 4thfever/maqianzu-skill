# TOOLS

本 workspace 主要是本地知识检索与分析型使用场景。

## 默认工具偏好

- 回答问题时优先使用 `read`
- 只在必要时使用 `exec`
- 不为了“多看一点”而读取大量无关文件

## 推荐读取路径

1. 先读 `skills/maqianzu/SKILL.md`
2. 再读 `prompts/analysis_framework.md`
3. 再读 `prompts/response_policy.md`
4. 再读 `knowledge/quickstart.md`
5. 再进入相关 `knowledge/topics/*.md`
6. 最后按需读取 `knowledge/episodes/...`

## 何时使用 exec

只有在以下情况才建议使用：

- 用户明确要求更新知识库
- 用户明确要求重建数据
- 需要运行 `python tools/build_all.py`
- 需要执行单独的构建、校验脚本

## 不推荐的行为

- 不要在问答阶段无端修改知识文件
- 不要在没有缩小主题范围前扫描大量 chunk
- 不要把构建脚本当作日常回答流程的一部分
