# AGENTS.md — OceanBase Skills Repository

This file provides context for AI agents (Claude Code, Cursor, Windsurf, GitHub Copilot, etc.) working inside this repository.

---

## Repository Purpose

`oceanbase-skills` is a monorepo of **AI Agent Skills** for OceanBase products. Each skill is a standalone Markdown document (`SKILL.md`) that gives AI agents accurate domain knowledge to help users operate OceanBase software correctly and safely.

Skills are published as npm packages so they can be installed into any project and loaded by any AI agent.

---

## Repository Structure

```
oceanbase-skills/
├── README.md             # Repository overview and usage guide
├── AGENTS.md             # This file — context for AI agents
├── LICENSE
└── skills/
    └── <skill-name>/     # One directory per skill
        ├── SKILL.md      # The skill content (consumed by AI agents)
        ├── README.md     # Installation and integration guide
        └── package.json  # npm package metadata
```

### Conventions

- **One skill per directory** under `skills/`. Each directory is also an npm package.
- **`SKILL.md` is the primary artifact.** It is written for AI agents to read and follow, not for humans to skim. Keep it precise, imperative, and unambiguous.
- **`README.md`** explains how end-users install and integrate the skill into their agent environment. It is human-facing.
- **`package.json`** uses the skill directory name as the npm package name. The `main` field points to `SKILL.md`.

---

## Current Skills

| Directory | npm Package | Domain |
|-----------|-------------|--------|
| `skills/oceanbase-deploy` | `oceanbase-deploy` | OceanBase cluster deployment and operations using `obd` |

---

## How to Work in This Repository

### Adding a New Skill

1. Create `skills/<new-skill-name>/`.
2. Write `SKILL.md` — focus on correctness, safety warnings for destructive operations, and concrete command examples.
3. Write `README.md` — explain installation and how to load the skill in Cursor, Claude Code, Windsurf, and generic agents.
4. Write `package.json` — set `name`, `version`, `description`, `main: "SKILL.md"`, `files: ["SKILL.md", "README.md"]`, and `repository.directory`.

### Editing an Existing Skill

- The source of truth for skill content is `skills/<skill-name>/SKILL.md`.
- When updating commands, flags, or behaviors, verify against official OceanBase documentation before making changes.
- Preserve existing safety rules sections — do not weaken or remove confirmation requirements for destructive operations.

### What NOT to Do

- Do not add code that is not documentation (no application source code belongs here).
- Do not remove or soften safety warnings (e.g., confirmation requirements before `destroy`, `redeploy`, `failover`).
- Do not invent undocumented commands or flags.
- Do not commit secrets, credentials, or environment-specific configuration.

---

## Skill Quality Guidelines

A high-quality `SKILL.md` in this repository should:

- **Be accurate**: commands must match the actual CLI behavior of the tool.
- **Be safe**: destructive or irreversible operations must have explicit safety warnings and require user confirmation before execution.
- **Be agent-friendly**: written in clear, imperative language that an LLM can follow without ambiguity.
- **Include examples**: show realistic usage patterns for common and edge-case scenarios.
- **Define terminology**: if the product has overlapping or easily confused terms (e.g., OCP CE vs. OCP Express), define them clearly at the top of the skill.
- **Stay focused**: only cover the domain of that specific skill; cross-skill concerns belong in separate skills.
