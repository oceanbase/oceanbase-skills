# OceanBase Skills

A collection of **AI Agent Skills** for OceanBase products — designed for use with Claude Code, Cursor, Windsurf, and any other agent that supports the **Agent Skills Specification**.

Each skill is a self-contained directory with a `SKILL.md` file (plus optional `references/`) that gives AI agents the domain knowledge needed to help you operate OceanBase products correctly and safely.

---

## Available Skills

| Skill | Description |
|-------|-------------|
| [`oceanbase-deploy`](./skills/oceanbase-deploy/) | Overview & routing — start here if unsure which skill to use |
| [`cluster-management`](./skills/oceanbase-deploy/cluster-management/) | Cluster lifecycle: deploy, start, stop, upgrade, scale out, OCP CE takeover, monitoring |
| [`tenant-management`](./skills/oceanbase-deploy/tenant-management/) | Tenant CRUD, backup, restore, workload optimization |
| [`seekdb`](./skills/oceanbase-deploy/seekdb/) | obd-managed SeekDB: lifecycle and primary-standby HA (switchover / failover / decouple) |
| [`testing-and-benchmark`](./skills/oceanbase-deploy/testing-and-benchmark/) | Sysbench, TPC-H, TPC-C, mysqltest benchmarks |
| [`seekdb` (product)](./seekdb/) | SeekDB product skill: install on Linux/macOS/Windows (Homebrew / Docker / yum / apt / MSI / pip) and build from source |

> More skills are on the way. Planned areas include OceanBase kernel tuning, SQL diagnostics, migration, and more.

---

## Quick Start

### Claude Code — One-line install (all skills)

```bash
# Copy all skills into your project at once
mkdir -p .claude/skills/oceanbase-deploy
curl -sL "https://raw.githubusercontent.com/oceanbase/oceanbase-skills/main/skills/oceanbase-deploy/SKILL.md" \
  -o .claude/skills/oceanbase-deploy/SKILL.md
for s in cluster-management tenant-management seekdb testing-and-benchmark; do
  mkdir -p .claude/skills/oceanbase-deploy/$s
  curl -sL "https://raw.githubusercontent.com/oceanbase/oceanbase-skills/main/skills/oceanbase-deploy/$s/SKILL.md" \
    -o .claude/skills/oceanbase-deploy/$s/SKILL.md
done

# SeekDB product skill (install + build) — separate top-level skill
mkdir -p .claude/skills/seekdb
curl -sL "https://raw.githubusercontent.com/oceanbase/oceanbase-skills/main/seekdb/SKILL.md" \
  -o .claude/skills/seekdb/SKILL.md
for s in install build; do
  mkdir -p .claude/skills/seekdb/$s/references
  curl -sL "https://raw.githubusercontent.com/oceanbase/oceanbase-skills/main/seekdb/$s/SKILL.md" \
    -o .claude/skills/seekdb/$s/SKILL.md
done
# Optional: pull reference files on demand from seekdb/{install,build}/references/
```

Claude Code will automatically discover all skills under `.claude/skills/` and offer them when relevant.

### Load a single skill from GitHub URL

```
https://raw.githubusercontent.com/oceanbase/oceanbase-skills/main/skills/oceanbase-deploy/<skill-name>/SKILL.md
```

---

## Agent Integration

### Claude Code

Use the one-liner in [Quick Start](#claude-code--one-line-install-all-skills) above, or manually place `SKILL.md` files into `.claude/skills/oceanbase-deploy/`.

### Cursor

```bash
mkdir -p .cursor/skills/oceanbase-deploy
curl -sL "https://raw.githubusercontent.com/oceanbase/oceanbase-skills/main/skills/oceanbase-deploy/SKILL.md" \
  -o .cursor/skills/oceanbase-deploy/SKILL.md
for s in cluster-management tenant-management seekdb testing-and-benchmark; do
  mkdir -p .cursor/skills/oceanbase-deploy/$s
  curl -sL "https://raw.githubusercontent.com/oceanbase/oceanbase-skills/main/skills/oceanbase-deploy/$s/SKILL.md" \
    -o .cursor/skills/oceanbase-deploy/$s/SKILL.md
done

# SeekDB product skill
mkdir -p .cursor/skills/seekdb
curl -sL "https://raw.githubusercontent.com/oceanbase/oceanbase-skills/main/seekdb/SKILL.md" \
  -o .cursor/skills/seekdb/SKILL.md
for s in install build; do
  mkdir -p .cursor/skills/seekdb/$s
  curl -sL "https://raw.githubusercontent.com/oceanbase/oceanbase-skills/main/seekdb/$s/SKILL.md" \
    -o .cursor/skills/seekdb/$s/SKILL.md
done
```

### Windsurf

In Windsurf's Rules or project context configuration, add the path to the skill file or paste its contents.

### Other Agents

- **System prompt / rules file**: paste the content of `SKILL.md`.
- **URL-based loading**: use the raw GitHub link above.
- **In-conversation context**: paste the `SKILL.md` content at the start of your session.

---

## Example Prompts

After loading the skills, ask your agent for concrete tasks. Below are examples grouped by skill.

### Cluster Management

```text
部署一个本机 OceanBase 开源版本，能快速跑起来就行
```

```text
用 config.yaml 部署一个名为 test-cluster 的 OceanBase 社区版集群
```

```text
帮我部署 OCP
```

```text
帮我直接启动 test-cluster，并检查启动后状态
```

```text
如何给 ob-test 添加 Prometheus 和 Grafana 监控
```

### Tenant Management

```text
在 test-cluster 上创建一个名为 mysql 的租户
```

```text
给 test-cluster 上的 mysql 租户配置备份路径并执行一次备份
```

### SeekDB (obd-managed)

```text
部署并启动一个 SeekDB 实例
```

```text
创建一个 SeekDB 主备集群，并告诉我主库和备库分别怎么部署
```

```text
查看 seekdb-test 的拓扑，如果主库挂了该用 switchover 还是 failover
```

### SeekDB (product — install & build)

```text
在我的 macOS 上装一个 SeekDB
```

```text
用 Docker 跑一个 SeekDB，并打通 2881 端口
```

```text
帮我从源码编出一个 release 版 SeekDB，再打成 rpm 包
```

### Testing & Benchmark

```text
对 test-cluster 的 mysql 租户跑一个 sysbench 测试
```

```text
给我跑 TPC-H 的完整命令和参数
```

### Tips

- Want the agent to execute directly? Say **"帮我执行"**.
- Want a plan first? Say **"先不要执行，只给我命令和步骤"**.
- For destructive operations, say **"我确认允许高风险操作"** or **"先不要执行破坏性命令"**.

---

## Repository Structure

```
oceanbase-skills/
├── README.md
├── AGENTS.md
├── package.json
├── LICENSE
├── skills/
│   └── oceanbase-deploy/              # obd-based skills
│       ├── SKILL.md                   # Overview & routing
│       ├── README.md
│       ├── package.json
│       ├── cluster-management/        # Cluster lifecycle
│       │   ├── SKILL.md
│       │   └── references/
│       │       ├── config-deployment.md
│       │       ├── ocp-ce.md
│       │       ├── monitoring.md
│       │       └── mirror-management.md
│       ├── tenant-management/         # Tenant ops
│       │   ├── SKILL.md
│       │   └── references/
│       │       └── backup-restore.md
│       ├── seekdb/                    # obd-managed SeekDB: lifecycle & HA
│       │   ├── SKILL.md
│       │   └── references/
│       │       ├── install-modes.md
│       │       └── ha-operations.md
│       └── testing-and-benchmark/     # Benchmarks
│           ├── SKILL.md
│           └── references/
│               └── test-commands.md
└── seekdb/                            # SeekDB product skill (standalone)
    ├── SKILL.md                       # Overview & routing
    ├── install/                       # Install on Linux/macOS/Windows
    │   ├── SKILL.md
    │   └── references/
    │       ├── pip-embedded.md
    │       ├── macos-homebrew.md
    │       ├── docker.md
    │       ├── linux-yum.md
    │       ├── linux-apt.md
    │       └── windows-msi.md
    └── build/                         # Build from source
        ├── SKILL.md
        └── references/
            ├── build-macos.md
            ├── build-linux.md
            ├── build-android.md
            ├── build-windows.md
            └── build-python-wheel.md
```

Each skill follows the **Agent Skills Specification**:

| File | Purpose |
|------|---------|
| `SKILL.md` | Main skill content with YAML frontmatter — consumed by AI agents |
| `references/*.md` | Supplemental documentation, loaded on demand to save context |

---

## Contributing

Contributions are welcome. To add a new skill:

1. Create `skills/<your-skill-name>/`.
2. Write `SKILL.md` with YAML frontmatter (`name`, `description`, `compatibility`, `metadata`) and clear, agent-friendly instructions.
3. Add `references/` for detailed supplemental content (loaded on demand, not always in context).
4. Keep `SKILL.md` under 500 lines; move details to `references/`.
5. Test your skill by loading it into Claude Code and running representative prompts.

Please keep skill content factual, concise, and safe — especially for destructive or irreversible operations.

---

## License

[MIT](./LICENSE)
