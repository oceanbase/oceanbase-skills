---
name: seekdb-docs
description: seekdb database documentation lookup. Use when users ask about seekdb features, SQL syntax, vector search, hybrid search, integrations, deployment, or any seekdb-related topics. Automatically locates relevant docs via catalog-based semantic search.
---

# seekdb Documentation

Provides access to ~1000 seekdb documentation entries through a catalog-based search system.

## Version Info

<!-- AUTO-UPDATED by update_docs.sh — do not edit manually -->
- **Documentation versions covered**: V1.0.0, V1.1.0 (merged, latest takes priority)
- **Latest version**: V1.1.0
<!-- END AUTO-UPDATED -->
- The `branch` field in catalog entries indicates which Git branch hosts the file (used for remote fallback URLs only). It does NOT indicate which seekdb version the content applies to — many docs apply to all versions.
- If the user asks about a specific seekdb version, note that this documentation set reflects the latest available content and may not distinguish version-specific differences.

## Path Resolution (Do First)

All resource paths are relative to this SKILL.md's location. Resolve the skill directory first:

1. Read this SKILL.md to get its absolute path
2. Extract the parent directory as `<skill_dir>`
3. Catalog: `<skill_dir>references/seekdb-docs-catalog.jsonl`
4. Docs base: `<skill_dir>seekdb-docs/`

## Workflow

### Step 1: Search Catalog

**Grep search (preferred for ~90% of queries)**:
```bash
grep -i "keyword" <skill_dir>references/seekdb-docs-catalog.jsonl
```

**Full catalog load** (only when grep returns no results or semantic matching is needed):
- Local: `<skill_dir>references/seekdb-docs-catalog.jsonl`
- Remote fallback: `https://raw.githubusercontent.com/oceanbase/seekdb-ecology-plugins/main/agent-skills/skills/seekdb/references/seekdb-docs-catalog.jsonl`
- Format: JSONL — one `{"path": "...", "description": "...", "branch": "..."}` per line (~1000 entries)

### Step 2: Match Query

- Extract `path`, `description`, and `branch` from search results
- Select entries whose descriptions best match the query semantically (match by meaning, not just keywords)
- Consider multiple matches for comprehensive answers

### Step 3: Read Document

Local-first with remote fallback:
1. Try local: `<skill_dir>seekdb-docs/[path]`
2. Fallback: `https://raw.githubusercontent.com/oceanbase/seekdb-doc/[branch]/en-US/[path]`
   - `[branch]` comes from the catalog entry's `branch` field (e.g. `V1.0.0`, `V1.1.0`)
   - Docs span multiple version branches; some files only exist in a specific branch

## Example

```
Query: "How to integrate with Claude Code?"

1. grep -i "claude code" <skill_dir>references/seekdb-docs-catalog.jsonl
2. Match: {"path": "300.integrations/300.developer-tools/700.claude-code.md",
           "description": "This guide explains how to use the seekdb plugin with Claude Code...",
           "branch": "V1.0.0"}
3. Read: <skill_dir>seekdb-docs/300.integrations/300.developer-tools/700.claude-code.md
   Fallback: https://raw.githubusercontent.com/oceanbase/seekdb-doc/V1.0.0/en-US/300.integrations/300.developer-tools/700.claude-code.md
```

See [examples.md](references/examples.md) for more complete workflow examples.

## Notes

- **Optional local docs**: Run `scripts/update_docs.sh` to download and merge docs from all version branches locally
- **Multi-version**: Docs span multiple branches; the update script merges them and records each file's source branch in the catalog
- **Offline capable**: With local docs and catalog present, works completely offline

## Category Overview

- **Get Started**: Quick start, basic operations, overview
- **Development**: Vector search, hybrid search, AI functions, MCP, multi-model
- **Integrations**: Frameworks, model platforms, developer tools, workflows
- **Guides**: Deployment, management, security, OBShell, performance
- **Reference**: SQL syntax, PL, error codes, SDK APIs
- **Tutorials**: Step-by-step scenarios
