# Powerbase CLI Skill README

这个 Skill 适合用在 Powerbase 的完整 CLI 工作流中：登录、确认上下文、选择实例和分支、通过 `powerbase agent chat` 完成功能开发，再按需做检查、SQL 验证和发布。

如果你只想快速上手，可以直接参考下面这些提示词。

## 提示词示例

### 1. 从零创建一个应用

```text
请使用 Powerbase CLI 帮我创建一个新的 todo app。
先检查我是否已登录，如果没有登录就给我登录链接并暂停。
然后列出 org，选择合适的 org 创建实例，默认使用 Powerbase 托管数据库。
创建完成后切到 main 或合适的新分支，并通过 powerbase agent chat 实现一个支持新增、完成、删除、列表查看的 todo 应用。
除非我明确要求，否则不要直接 publish。
```

### 2. 在现有实例上继续开发功能

```text
请用 Powerbase CLI 帮我继续开发现有应用。
先检查当前 auth status 和 context show，确认我当前使用的 instance 和 branch。
如果没有合适的工作分支，就从 main 创建一个 feature/auth-dashboard 分支并切换过去。
然后使用 powerbase agent chat，为这个应用增加登录功能和一个简单 dashboard。
完成后读取关键文件并告诉我这次改了什么，但先不要发布。
```

### 3. 做验证和准备发布

```text
请使用 Powerbase CLI 帮我检查当前实例是否可以发布。
先确认当前 instance 和 branch，再运行 publish diff 查看待发布内容。
如有需要，使用 sandbox files read 检查关键文件，并执行一条 SQL 做基本验证。
把检查结果总结给我；只有在我明确说“发布”之后，再执行 powerbase publish run。
```

## 使用建议

- 描述清楚你是想“新建应用”、“继续改现有实例”还是“检查并发布”。
- 最好在提示词里明确是否允许创建实例、创建分支、运行 SQL、发布上线。
- 如果你知道目标 `org`、`instance` 或 `branch`，直接写出来会更高效。
- 如果尚未登录，Skill 会优先引导你完成 `powerbase auth login`，而不是直接继续执行后续命令。
