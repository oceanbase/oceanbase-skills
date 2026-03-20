# oceanbase-deploy

OceanBase OBD 部署与运维说明，供**任意 AI Agent**（Cursor、Claude Code、Windsurf、自定义 Agent 等）加载使用。内容为纯 Markdown，与具体产品解耦。

源码与版本管理：[oceanbase/oceanbase-skills](https://github.com/oceanbase/oceanbase-skills) 仓库内 **`oceanbase-deploy/`** 目录。

## 安装

```bash
npm install oceanbase-deploy
```

## 在不同 Agent 中使用

### 任意支持「从文件/URL 加载说明」的 Agent

**方式一：从 npm 包路径加载**

安装后，说明文件在：

- `node_modules/oceanbase-deploy/SKILL.md`

在 Agent 的「自定义指令 / Rules / System prompt」中配置为该文件路径，或对话时让 Agent 读取该文件即可。

**方式二：从 URL 加载（无需 npm）**

若你的 Agent 支持从 URL 加载说明，可使用仓库原始文件地址，例如：

- `https://raw.githubusercontent.com/oceanbase/oceanbase-skills/main/oceanbase-deploy/SKILL.md`

### Cursor

1. **项目内使用**：把本包中的说明复制到 Cursor 技能目录。
   ```bash
   mkdir -p .cursor/skills/oceanbase-deploy
   cp node_modules/oceanbase-deploy/SKILL.md .cursor/skills/oceanbase-deploy/SKILL.md
   ```
2. 或在 Cursor 设置中指定「额外说明」指向 `node_modules/oceanbase-deploy/SKILL.md`。

### Claude Code / Claude for VS Code

在项目根或工作区中创建 `.claude/instructions.md`（或产品支持的说明路径），将 `SKILL.md` 的内容粘贴进去，或写入：

```
See instructions in node_modules/oceanbase-deploy/SKILL.md
```

具体以当前产品的「自定义指令」文档为准。

### Windsurf

在 Windsurf 的 Rules / 项目规则中，添加对 `node_modules/oceanbase-deploy/SKILL.md` 的引用，或将其内容粘贴到规则文件。详见 Windsurf 的「规则/上下文」配置说明。

### 其他 Agent（通用）

- 若 Agent 支持「系统提示词 / 规则文件」：把 `SKILL.md` 的路径或内容配置进去。
- 若 Agent 支持「读取 URL」：使用上述 raw GitHub 链接。
- 若 Agent 仅支持「对话中给上下文」：在对话开始时发送「请按以下说明操作」，并粘贴或附上 `SKILL.md` 内容。

## 包内文件

| 文件 | 说明 |
|------|------|
| `SKILL.md` | 供任意 Agent 使用的 OBD 部署与运维说明（主内容） |
| `README.md` | 本说明（安装与多 Agent 使用方式） |

## License

MIT
