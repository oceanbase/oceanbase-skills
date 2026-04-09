# OceanBase Skills

A collection of **AI Agent Skills** for OceanBase products — designed for use with Cursor, Claude Code, Windsurf, and any other agent that supports custom instructions or skill files.

Each skill is a self-contained Markdown document (`SKILL.md`) that gives AI agents the domain knowledge needed to help you operate OceanBase products correctly and safely.

---

## Available Skills

| Skill | npm Package | Description |
|-------|-------------|-------------|
| [oceanbase-deploy](./skills/oceanbase-deploy/) | `oceanbase-deploy` | Deploy and operate OceanBase clusters using `obd`. Covers cluster lifecycle, tenant management, backup/restore, SeekDB, OCP takeover, monitoring, and benchmarking. |

> More skills are on the way. Planned areas include OceanBase kernel tuning, SQL diagnostics, migration, and more.

---

## How to Use a Skill

Each skill can be loaded into your AI agent in several ways.

### Option 1 — Install via npm

```bash
npm install <skill-package-name>
# e.g.
npm install oceanbase-deploy
```

The skill file is then available at:

```
node_modules/<skill-package-name>/SKILL.md
```

### Option 2 — Load from URL (no npm required)

Use the raw GitHub URL directly if your agent supports loading from URLs:

```
https://raw.githubusercontent.com/oceanbase/oceanbase-skills/main/skills/oceanbase-deploy/SKILL.md
```

### Option 3 — Copy the file manually

Download or copy the `SKILL.md` content and paste it into your agent's system prompt, rules file, or custom instructions.

### Example prompts

After loading a skill, ask for concrete tasks instead of vague requests.

For `oceanbase-deploy`, examples include:

```text
部署一个本机 OceanBase 开源版本，能快速跑起来就行
```

```text
用 obd demo 快速部署一个本机演示环境
```

```text
用 config.yaml 部署一个名为 test-cluster 的 OceanBase 社区版集群
```

```text
帮我部署 OCP
```

```text
部署并启动一个 SeekDB 实例
```

```text
创建一个 SeekDB 主备集群，并告诉我主库和备库分别怎么部署
```

```text
帮我直接启动 test-cluster，并检查启动后状态
```

```text
对 test-cluster 的 mysql 租户跑一个 sysbench 测试
```

```text
帮我部署 OCP 社区版
```

## Agent Integration

### Cursor

Copy the skill into your project's Cursor skill directory:

```bash
mkdir -p .cursor/skills/oceanbase-deploy
cp node_modules/oceanbase-deploy/SKILL.md .cursor/skills/oceanbase-deploy/SKILL.md
```

Cursor will automatically detect and offer the skill when relevant tasks are requested.

### Claude Code

Create or update `AGENTS.md` (or `.claude/instructions.md`) in your project root and reference the skill:

```markdown
See OBD instructions in node_modules/oceanbase-deploy/SKILL.md
```

### Windsurf

In Windsurf's Rules or project context configuration, add the path to the skill file or paste its contents.

### Other Agents

- **System prompt / rules file**: paste the content of `SKILL.md`.
- **URL-based loading**: use the raw GitHub link above.
- **In-conversation context**: paste the `SKILL.md` content at the start of your session.

---

## Repository Structure

```
oceanbase-skills/
└── skills/
    └── oceanbase-deploy/     # OBD cluster deploy & ops skill
        ├── SKILL.md          # The skill content (loaded by AI agents)
        ├── README.md         # npm package usage guide
        └── package.json      # npm package metadata
```

Each skill lives under `skills/<skill-name>/` and follows the same layout:

| File | Purpose |
|------|---------|
| `SKILL.md` | Main skill content consumed by AI agents |
| `README.md` | Installation and integration guide |
| `package.json` | npm package metadata for publishing |

---

## Contributing

Contributions are welcome. To add a new skill:

1. Create a directory under `skills/<your-skill-name>/`.
2. Write `SKILL.md` with clear, accurate, and agent-friendly instructions.
3. Add a `README.md` explaining how to install and use the skill.
4. Add a `package.json` if the skill will be published to npm.

Please keep skill content factual, concise, and safe — especially for operations that are destructive or irreversible.

---

## License

[MIT](./LICENSE)
