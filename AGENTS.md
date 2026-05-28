# AGENTS.md — OceanBase Skills Repository

This file provides context for AI agents (Claude Code, Cursor, Windsurf, GitHub Copilot, etc.) working inside this repository.

---

## Repository Purpose

`oceanbase-skills` is a monorepo of **AI Agent Skills** for OceanBase products. Each skill is a directory containing a `SKILL.md` (with YAML frontmatter) and optional `references/` for supplemental documentation, following the **Agent Skills Specification**.

Skills are published as a single npm package (`oceanbase-skills`) so they can be installed into any project and loaded by any AI agent.

---

## Repository Structure

```
oceanbase-skills/
├── README.md
├── AGENTS.md             # This file
├── package.json          # npm: oceanbase-skills
├── LICENSE
├── skills/
│   └── oceanbase-deploy/         # obd-based skill family
│       ├── SKILL.md              # Overview & routing
│       ├── README.md
│       ├── package.json          # npm: oceanbase-deploy (legacy)
│       ├── cluster-management/   # Cluster lifecycle
│       │   ├── SKILL.md
│       │   └── references/
│       ├── tenant-management/    # Tenant ops
│       │   ├── SKILL.md
│       │   └── references/
│       ├── seekdb/               # obd-managed SeekDB: lifecycle & HA
│       │   ├── SKILL.md
│       │   └── references/
│       └── testing-and-benchmark/ # Benchmarks
│           ├── SKILL.md
│           └── references/
└── seekdb/                       # SeekDB product skill family (standalone)
    ├── SKILL.md                  # Overview & routing
    ├── install/                  # Install on Linux/macOS/Windows
    │   ├── SKILL.md
    │   └── references/
    └── build/                    # Build from source
        ├── SKILL.md
        └── references/
```

### Conventions

- **One skill per directory** under `skills/`.
- **`SKILL.md` is the primary artifact.** It uses YAML frontmatter (`name`, `description`, `compatibility`, `metadata`) and is written for AI agents to read and follow.
- **`references/*.md`** contains supplemental documentation loaded on demand — keeps `SKILL.md` under 500 lines.
- **`README.md`** (where present) explains how end-users install and integrate the skill. It is human-facing.

---

## Current Skills

| Directory | Skill Name | Domain |
|-----------|------------|--------|
| `skills/oceanbase-deploy` | `oceanbase-deploy` | Overview and routing to specialized skills |
| `skills/oceanbase-deploy/cluster-management` | `cluster-management` | Cluster deploy, start, stop, upgrade, OCP CE, monitoring |
| `skills/oceanbase-deploy/tenant-management` | `tenant-management` | Tenant CRUD, backup, restore |
| `skills/oceanbase-deploy/seekdb` | `seekdb` | obd-managed SeekDB lifecycle, primary-standby HA |
| `skills/oceanbase-deploy/testing-and-benchmark` | `testing-and-benchmark` | Sysbench, TPC-H, TPC-C, mysqltest |
| `seekdb` | `seekdb` (product) | Standalone SeekDB product: overview and routing |
| `seekdb/install` | `seekdb-install` | Install SeekDB on Linux/macOS/Windows (Homebrew / Docker / yum / apt / MSI / pip) |
| `seekdb/build` | `seekdb-build` | Build SeekDB from source: macOS, Linux, Android cross, Windows, Python wheel |

---

## How to Work in This Repository

### Adding a New Skill

1. Create `skills/oceanbase-deploy/<new-skill-name>/`.
2. Write `SKILL.md` with YAML frontmatter (`name`, `description`, `compatibility`, `metadata`) and clear instructions.
3. Add `references/` for detailed content that should be loaded on demand.
4. Keep `SKILL.md` under 500 lines — move details to `references/`.

### Editing an Existing Skill

- The source of truth for skill content is `skills/oceanbase-deploy/<skill-name>/SKILL.md`.
- When updating commands, flags, or behaviors, verify against official OceanBase documentation.
- Preserve safety rules — do not weaken or remove confirmation requirements for destructive operations.

### What NOT to Do

- Do not add application source code (this repo is documentation only).
- Do not remove or soften safety warnings (e.g., confirmation before `destroy`, `redeploy`, `failover`).
- Do not invent undocumented commands or flags.
- Do not commit secrets, credentials, or environment-specific configuration.

---

## Skill Quality Guidelines

A high-quality `SKILL.md` should:

- **Be accurate**: commands must match actual CLI behavior.
- **Be safe**: destructive operations must have explicit safety warnings and require user confirmation.
- **Be agent-friendly**: clear, imperative language an LLM can follow without ambiguity.
- **Include examples**: realistic usage patterns for common and edge-case scenarios.
- **Define terminology**: overlapping or confusing terms (e.g., OCP CE vs. OCP Express) must be defined clearly.
- **Stay focused**: only cover the domain of that specific skill; cross-skill concerns belong in separate skills.
- **Cross-reference**: link to related skills for adjacent functionality.
