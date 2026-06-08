# OceanBase Skills

A collection of **AI Agent Skills** for OceanBase products — designed for use with Claude Code, Cursor, Windsurf, and any other agent that supports the **Agent Skills Specification**.

Each skill is a self-contained directory with a `SKILL.md` file (plus optional `references/`) that gives AI agents the domain knowledge needed to help you operate OceanBase products correctly and safely.

---

## Available Skills

### oceanbase-deploy — OceanBase Deployment & Operations (via obd)

| Skill | Description |
|-------|-------------|
| [`oceanbase-deploy`](./skills/oceanbase-deploy/) | Overview & routing — start here if unsure which skill to use |
| [`cluster-management`](./skills/oceanbase-deploy/cluster-management/) | Cluster lifecycle: deploy, start, stop, upgrade, scale out, OCP CE takeover, monitoring |
| [`tenant-management`](./skills/oceanbase-deploy/tenant-management/) | Tenant CRUD, backup, restore, workload optimization |
| [`seekdb (obd)`](./skills/oceanbase-deploy/seekdb/) | obd-managed SeekDB: primary-standby HA (switchover / failover / decouple) |
| [`testing-and-benchmark`](./skills/oceanbase-deploy/testing-and-benchmark/) | Sysbench, TPC-H, TPC-C, mysqltest benchmarks |

### seekdb — SeekDB 全生命周期技能（安装 / 编译 / 文档 / CLI / 导入 / 查询）

| Skill | Description |
|-------|-------------|
| [`seekdb`](./skills/seekdb/) | Overview & routing for standalone SeekDB |
| [`seekdb/install`](./skills/seekdb/install/) | Install/deploy SeekDB via Homebrew, Docker, yum, apt, pip, Windows MSI |
| [`seekdb/build`](./skills/seekdb/build/) | Build SeekDB from source for macOS, Linux, Android, Windows, Python wheel |
| [`seekdb/docs`](./skills/seekdb/docs/) | 文档检索 — SQL 语法、向量/混合检索、SDK、集成、部署等 ~1000 条文档目录检索 |
| [`seekdb/cli`](./skills/seekdb/cli/) | `seekdb-cli` — SQL/schema/表数据画像/向量集合/AI 模型，全 JSON 输出，AI Agent 友好 |
| [`seekdb/importing`](./skills/seekdb/importing/) | 导入 CSV/Excel 数据到 SeekDB，支持指定列向量化 |
| [`seekdb/querying`](./skills/seekdb/querying/) | 查询/导出 — 标量过滤、混合检索（全文+语义），结果导出 CSV/Excel |

> More skills are on the way. Planned areas include OceanBase kernel tuning, SQL diagnostics, migration, and more.

---

## Quick Start

### Install via skills.sh (recommended)

```bash
# Install the oceanbase-deploy skill (includes all sub-skills)
npx skills add oceanbase/oceanbase-skills --skill oceanbase-deploy

# Install the seekdb standalone skill (install / build from source)
npx skills add oceanbase/oceanbase-skills --skill seekdb

# Or install all skills from this repo
npx skills add oceanbase/oceanbase-skills
```

### Manual install — Claude Code

```bash
mkdir -p .claude/skills/oceanbase-deploy
curl -sL "https://raw.githubusercontent.com/oceanbase/oceanbase-skills/main/skills/oceanbase-deploy/SKILL.md" \
  -o .claude/skills/oceanbase-deploy/SKILL.md
for s in cluster-management tenant-management seekdb testing-and-benchmark; do
  mkdir -p .claude/skills/oceanbase-deploy/$s
  curl -sL "https://raw.githubusercontent.com/oceanbase/oceanbase-skills/main/skills/oceanbase-deploy/$s/SKILL.md" \
    -o .claude/skills/oceanbase-deploy/$s/SKILL.md
done

# SeekDB skill bundle (install + build + docs + cli + importing + querying)
mkdir -p .claude/skills/seekdb
curl -sL "https://raw.githubusercontent.com/oceanbase/oceanbase-skills/main/skills/seekdb/SKILL.md" \
  -o .claude/skills/seekdb/SKILL.md
for s in install build docs cli importing querying; do
  mkdir -p .claude/skills/seekdb/$s
  curl -sL "https://raw.githubusercontent.com/oceanbase/oceanbase-skills/main/skills/seekdb/$s/SKILL.md" \
    -o .claude/skills/seekdb/$s/SKILL.md
done
```

### Load a single skill from GitHub URL

```
https://raw.githubusercontent.com/oceanbase/oceanbase-skills/main/skills/oceanbase-deploy/<skill-name>/SKILL.md
```

---

## Agent Integration

### Claude Code / Cursor / Windsurf (via skills.sh)

```bash
npx skills add oceanbase/oceanbase-skills --skill oceanbase-deploy
```

`npx skills add` automatically detects your IDE (Claude Code, Cursor, Windsurf, etc.) and installs to the right directory.

### Claude Code (manual)

Use the curl commands in [Quick Start](#manual-install--claude-code) above, or manually place `SKILL.md` files into `.claude/skills/oceanbase-deploy/`.

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

### SeekDB (obd-managed HA)

```text
部署并启动一个 SeekDB 实例
```

```text
创建一个 SeekDB 主备集群，并告诉我主库和备库分别怎么部署
```

```text
查看 seekdb-test 的拓扑，如果主库挂了该用 switchover 还是 failover
```

### SeekDB (standalone install / build)

```text
在我的 Mac 上安装 SeekDB
```

```text
用 Docker 部署一个 SeekDB 实例
```

```text
帮我从源码编译 SeekDB 的 Linux rpm 包
```

### SeekDB (docs / cli / import / query)

```text
seekdb 的混合检索（hybrid search）SQL 语法是什么样的？
```

```text
用 seekdb-cli 列出所有表，并把 orders 表的字段画像跑一下
```

```text
把这个 Excel 导入 seekdb，把 Description 列做向量化
```

```text
从 my_docs 集合里搜「部署最佳实践」，导出前 20 条到 results.xlsx
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
├── .claude-plugin/
│   └── marketplace.json               # skills.sh discovery manifest
├── README.md
├── AGENTS.md
├── package.json
├── LICENSE
└── skills/
    ├── oceanbase-deploy/              # OceanBase obd deployment & ops
    │   ├── SKILL.md                   # Overview & routing
    │   ├── README.md
    │   ├── package.json
    │   ├── cluster-management/        # Cluster lifecycle
    │   │   ├── SKILL.md
    │   │   └── references/
    │   ├── tenant-management/         # Tenant ops
    │   │   ├── SKILL.md
    │   │   └── references/
    │   ├── seekdb/                    # obd-managed SeekDB HA
    │   │   ├── SKILL.md
    │   │   └── references/
    │   └── testing-and-benchmark/     # Benchmarks
    │       ├── SKILL.md
    │       └── references/
    └── seekdb/                        # Standalone SeekDB — full lifecycle
        ├── SKILL.md                   # Overview & routing (6 sub-skills)
        ├── package.json
        ├── install/                   # Install via Homebrew/Docker/yum/apt/pip/MSI
        │   ├── SKILL.md
        │   └── references/
        ├── build/                     # Build from source (macOS/Linux/Android/Windows)
        │   ├── SKILL.md
        │   └── references/
        ├── docs/                      # Documentation catalog (~1000 entries)
        │   ├── SKILL.md
        │   ├── references/            # seekdb-docs-catalog.jsonl + examples
        │   ├── seekdb-docs/           # Mirrored doc tree (optional, refreshable)
        │   └── scripts/               # Maintainer scripts (update_docs.sh, generate_catalog.py)
        ├── cli/                       # seekdb-cli usage guide
        │   ├── SKILL.md
        │   └── references/
        ├── importing/                 # CSV/Excel import + vectorization
        │   ├── SKILL.md
        │   ├── scripts/               # import_to_seekdb.py, read_excel.py
        │   └── example-data/          # sample_products.csv / .xlsx
        └── querying/                  # Scalar + hybrid search, CSV/Excel export
            ├── SKILL.md
            └── scripts/               # query_from_seekdb.py
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
