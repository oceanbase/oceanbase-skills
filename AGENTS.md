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
│   ├── oceanbase-deploy/         # obd-based skill family
│   │   ├── SKILL.md              # Overview & routing
│   │   ├── README.md
│   │   ├── package.json          # npm: oceanbase-deploy (legacy)
│   │   ├── references/           # shared safety and capability gates
│   │   ├── cluster-management/   # Cluster lifecycle
│   │   │   ├── SKILL.md
│   │   │   └── references/
│   │   ├── obd-administration/   # OBD controller administration
│   │   │   ├── SKILL.md
│   │   │   └── references/
│   │   ├── obdiag-diagnostics/   # Diagnostics through obd obdiag
│   │   │   ├── SKILL.md
│   │   │   └── references/
│   │   ├── tenant-management/    # Tenant ops
│   │   │   ├── SKILL.md
│   │   │   └── references/
│   │   └── testing-and-benchmark/ # Benchmarks
│   │       ├── SKILL.md
│   │       └── references/
│   └── seekdb/                   # SeekDB product skill family (standalone)
│       ├── SKILL.md              # Overview & routing
│       ├── install/              # Install on Linux/macOS/Windows
│       ├── build/                # Build from source
│       ├── docs/                 # Documentation lookup
│       ├── cli/                  # seekdb-cli operations
│       ├── importing/            # CSV/Excel import
│       └── querying/             # Query and export
```

### Conventions

- **One skill per directory** under `skills/`.
- **`SKILL.md` is the primary artifact.** It uses YAML frontmatter (`name`, `description`, `compatibility`, `metadata`) and is written for AI agents to read and follow.
- **`references/*.md`** contains supplemental documentation loaded on demand — keeps `SKILL.md` under 500 lines.
- **`README.md`** (where present) explains how end-users install and integrate the skill. It is human-facing.
- **`oceanbase-deploy` is a complete routed bundle.** Packaging and manual-install instructions must retain its root entrypoint, shared references, and child skill directories; do not instruct users to paste only the root `SKILL.md`.
- **The root `package.json` is the published npm package authority.** Keep its release version and SPDX license synchronized with the intended release and root `LICENSE`; the nested legacy package is not a substitute.

---

## Current Skills

| Directory | Skill Name | Domain |
|-----------|------------|--------|
| `skills/oceanbase-deploy` | `oceanbase-deploy` | Overview and routing to specialized skills |
| `skills/oceanbase-deploy/cluster-management` | `cluster-management` | Community Edition cluster deploy, multi-node maximum-utilization sizing, lifecycle, upgrade, retained components, and monitoring |
| `skills/oceanbase-deploy/obd-administration` | `obd-administration` | Tested OBD controller installation, update/rollback, repositories, exact tool provisioning, traces, and runtime identity |
| `skills/oceanbase-deploy/obdiag-diagnostics` | `obdiag-diagnostics` | Diagnostic collection, checks, analysis, scenes, ASH, and RCA through OBD |
| `skills/oceanbase-deploy/tenant-management` | `tenant-management` | Tenant CRUD, backup, restore |
| `skills/oceanbase-deploy/testing-and-benchmark` | `testing-and-benchmark` | Sysbench, TPC-H, TPC-C, mysqltest |
| `skills/seekdb` | `seekdb` (product) | Standalone SeekDB product: overview and routing |
| `skills/seekdb/install` | `seekdb-install` | Install SeekDB on Linux/macOS/Windows (Homebrew / Docker / yum / apt / MSI / pip) |
| `skills/seekdb/build` | `seekdb-build` | Build SeekDB from source: macOS, Linux, Android cross, Windows, Python wheel |
| `skills/seekdb/docs` | `seekdb-docs` | SeekDB documentation lookup |
| `skills/seekdb/cli` | `seekdb-cli` | SQL, schema, vector, and AI operations through seekdb-cli |
| `skills/seekdb/importing` | `importing-to-seekdb` | CSV/Excel import and vectorization |
| `skills/seekdb/querying` | `querying-from-seekdb` | Collection querying and export |

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
- Do not remove or soften safety warnings for retained destructive operations, or the current-Skill-version unsupported boundary for removed workflows such as `redeploy`.
- Do not invent undocumented commands or flags.
- Do not commit secrets, credentials, or environment-specific configuration.

---

## Skill Quality Guidelines

A high-quality `SKILL.md` should:

- **Be accurate**: commands must match actual CLI behavior.
- **Be safe**: destructive operations must have explicit safety warnings and require user confirmation.
- **Be agent-friendly**: clear, imperative language an LLM can follow without ambiguity.
- **Include examples**: realistic usage patterns for common and edge-case scenarios.
- **Define terminology**: overlapping or confusing retained terms must be defined clearly.
- **Stay focused**: only cover the domain of that specific skill; cross-skill concerns belong in separate skills.
- **Cross-reference**: link to related skills for adjacent functionality.
