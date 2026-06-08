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

### seekdb — SeekDB Full Lifecycle Skills (install / build / docs / CLI / import / query)

| Skill | Description |
|-------|-------------|
| [`seekdb`](./skills/seekdb/) | Overview & routing for standalone SeekDB |
| [`seekdb/install`](./skills/seekdb/install/) | Install/deploy SeekDB via Homebrew, Docker, yum, apt, pip, Windows MSI |
| [`seekdb/build`](./skills/seekdb/build/) | Build SeekDB from source for macOS, Linux, Android, Windows, Python wheel |
| [`seekdb/docs`](./skills/seekdb/docs/) | Documentation search — SQL syntax, vector/hybrid search, SDK, integration, deployment; ~1000 doc catalog entries |
| [`seekdb/cli`](./skills/seekdb/cli/) | `seekdb-cli` — SQL / schema / table data profiling / vector collections / AI models, all JSON output, AI-Agent friendly |
| [`seekdb/importing`](./skills/seekdb/importing/) | Import CSV/Excel data into SeekDB, with per-column vectorization |
| [`seekdb/querying`](./skills/seekdb/querying/) | Query/export — scalar filters, hybrid search (full-text + semantic), export results to CSV/Excel |

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
Deploy a local OceanBase community edition — just get it running quickly
```

```text
Use config.yaml to deploy an OceanBase community edition cluster named test-cluster
```

```text
Help me deploy OCP
```

```text
Start test-cluster directly and check its status after startup
```

```text
How do I add Prometheus and Grafana monitoring to ob-test
```

### Tenant Management

```text
Create a tenant named mysql on test-cluster
```

```text
Configure the backup path for the mysql tenant on test-cluster and run a backup
```

### SeekDB (obd-managed HA)

```text
Deploy and start a SeekDB instance
```

```text
Create a SeekDB primary-standby cluster and tell me how to deploy the primary and standby separately
```

```text
Show the topology of seekdb-test — if the primary goes down, should I use switchover or failover
```

### SeekDB (standalone install / build)

```text
Install SeekDB on my Mac
```

```text
Deploy a SeekDB instance with Docker
```

```text
Build the Linux rpm package of SeekDB from source
```

### SeekDB (docs / cli / import / query)

```text
What does the hybrid search SQL syntax look like in seekdb?
```

```text
Use seekdb-cli to list all tables and run the column profile for the orders table
```

```text
Import this Excel file into seekdb and vectorize the Description column
```

```text
Search "deployment best practices" in the my_docs collection and export the top 20 results to results.xlsx
```

### Testing & Benchmark

```text
Run a sysbench test against the mysql tenant on test-cluster
```

```text
Give me the full TPC-H command and parameters
```

### Tips

- Want the agent to execute directly? Say **"go ahead and run it"**.
- Want a plan first? Say **"don't run anything yet, just give me the commands and steps"**.
- For destructive operations, say **"I confirm high-risk operations are allowed"** or **"don't run destructive commands yet"**.

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
