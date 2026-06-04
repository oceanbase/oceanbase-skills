---
name: seekdb
description: Overview skill for OceanBase SeekDB. Routes to specialized sub-skills covering the full SeekDB lifecycle — install/deploy on a target machine, build from source, look up documentation, use the seekdb-cli for SQL/schema/vector ops, import CSV/Excel data, and query/export results. Use as a starting point when the user mentions seekdb, pyseekdb, "install seekdb", "build seekdb", "seekdb docs", "seekdb-cli", "import to seekdb", "query seekdb", or wants a lightweight standalone OceanBase-compatible database. For obd-managed seekdb deployments and primary-standby HA, see the separate oceanbase-deploy/seekdb skill instead.
compatibility: Standalone product skill. Each sub-skill has its own platform requirements — see the sub-skill SKILL.md for details.
metadata:
  author: oceanbase
  version: "2.0"
---

# SeekDB

SeekDB is a lightweight OceanBase-compatible database that can run as a standalone server (Homebrew / Docker / yum / apt / Windows MSI) or as an embedded Python module (`pyseekdb`). It also supports vector search, hybrid search, and AI functions.

This is the entry point. Pick the sub-skill that matches the user's task.

## Skill Index

| Sub-skill | Use When |
|-----------|----------|
| [install](install/SKILL.md) | Install / deploy SeekDB on a target machine — Homebrew, Docker, yum, apt, Windows MSI, or pip embedded. |
| [build](build/SKILL.md) | Build SeekDB binaries and packages from source — macOS, Linux, Android (cross), Windows, Python wheel. |
| [docs](docs/SKILL.md) | Look up SeekDB documentation (SQL syntax, vector/hybrid search, integrations, SDK APIs, deployment guides) via catalog-based search. |
| [cli](cli/SKILL.md) | Use `seekdb-cli` to interact with a SeekDB/OceanBase instance from the shell — SQL, schema exploration, table profiling, vector collections, AI models. |
| [importing](importing/SKILL.md) | Import CSV / Excel files into SeekDB, with optional column vectorization for semantic search. |
| [querying](querying/SKILL.md) | Query a SeekDB collection — scalar (metadata) search, hybrid (fulltext + semantic) search, export to CSV / Excel. |

## When to Use Which Sub-skill

| User says... | Go to |
|--------------|-------|
| "Install seekdb on my Mac / Linux / Windows" | [install](install/SKILL.md) |
| "I want to use seekdb from Python" | [install](install/SKILL.md) — pip embedded mode |
| "Build seekdb from source" / "make a release rpm/deb/tgz/apk/installer" | [build](build/SKILL.md) |
| "How does seekdb's hybrid search / vector index / SQL function X work?" | [docs](docs/SKILL.md) |
| "Connect to seekdb from shell" / "run SQL via CLI" / "list tables" / "profile this table" | [cli](cli/SKILL.md) |
| "Import this CSV / Excel into seekdb" / "vectorize a column" | [importing](importing/SKILL.md) |
| "Search this collection" / "filter by metadata" / "export search results to Excel" | [querying](querying/SKILL.md) |
| "Deploy seekdb primary-standby with obd, do switchover/failover" | use the separate **`oceanbase-deploy/seekdb`** skill at [`../oceanbase-deploy/seekdb/SKILL.md`](../oceanbase-deploy/seekdb/SKILL.md). That skill is for obd-managed HA clusters; this skill is for the SeekDB product itself. |

## Two Directions Under This Skill

The sub-skills naturally split into two directions — pick by what the user wants to do:

- **Provisioning** (`install`, `build`) — get SeekDB running on a machine, or produce a build artifact.
- **Data plane** (`docs`, `cli`, `importing`, `querying`) — interact with a running SeekDB: look up documentation, run SQL, ingest data, search.

## Default Ports

| Port | Purpose |
|------|---------|
| 2881 | MySQL protocol |
| 2886 | HTTP / obshell |

## References

- Product documentation: <https://www.oceanbase.ai/docs/seekdb-overview/>
- Software download center: <https://mirrors.oceanbase.com/oceanbase/community/stable/>
- Upstream ecology plugins (catalog source for `docs/`): <https://github.com/oceanbase/seekdb-ecology-plugins>
