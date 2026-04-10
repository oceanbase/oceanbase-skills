---
name: powerbase-baas-cli
description: Use the Powerbase CLI for end-to-end Powerbase development workflows, including auth, context, org, instance, branch, database, SQL, sandbox, agent, and publish operations. Powerbase provides a coding agent that lets users build and evolve BaaS applications through chat, and implementation work for Powerbase-hosted apps should normally be delegated to that agent via `powerbase agent chat`, with the rest of the CLI used for resource discovery, environment control, validation, and deployment.
---

# Powerbase BaaS CLI Skill

## When To Use

Use this skill when an agent needs to handle product or engineering work on Powerbase via the CLI, especially to:

- turn a user requirement into a new cloud app
- reuse or create an instance and database
- switch to the right branch and working context
- use the Powerbase coding agent to build or evolve the app through chat
- inspect files, run SQL, preview changes, and publish only when the user explicitly wants deployment

## Install CLI

Install the published CLI first if `powerbase` is not already available:

```bash
python3 -m pip install powerbase-cli
powerbase --help
```

Then sign in with the browser login flow:

```bash
powerbase auth login
powerbase auth wait --login-id LOGIN_ID
powerbase auth status --json
```

## Defaults

- Prefer `--json` for agent-readable output.
- Prefer discovery commands before write commands.
- Prefer saving context for multi-step work instead of repeating `--instance-id` everywhere.
- Do not assume an instance, org, database, or branch is already selected; verify first.
- Prefer the managed Powerbase database flow by default: `powerbase instance create` without `--database-id`.
- Treat `powerbase database create --dsn ...` as the advanced bring-your-own-database path, not the default app setup flow.

## Config Resolution

The CLI resolves values in this order:

1. command flags
2. environment variables
3. `~/.config/powerbase/`
4. defaults

Key local files:

- `~/.config/powerbase/config.toml`
- `~/.config/powerbase/auth.json`
- `~/.config/powerbase/context.json`

Useful environment variables:
- `POWERBASE_ACCESS_TOKEN`
- `POWERBASE_REFRESH_TOKEN`
- `POWERBASE_INSTANCE_ID`
- `POWERBASE_ORG_ID`
- `POWERBASE_BRANCH`

## Standard Workflow

### 1. Check login

```bash
powerbase auth status --json
```

If not authenticated:

- Run `powerbase auth login --json`, return `login_url` and `login_id` to the user, and stop.
- Do not open the URL, use browser tools, or run `auth wait` yet.
- After the user confirms approval, run `powerbase auth wait --login-id LOGIN_ID --json` (default wait **600s**; use `--timeout` or `--timeout 0` for no limit).
- If the user is not already signed in to the console, the link expires, or a protected command reports an auth error, rerun `powerbase auth login --json` to generate a fresh login URL.

### 2. Check current context

```bash
powerbase context show --json
```

### 3. Discover or create the target resources

```bash
powerbase org list --json
powerbase database list --json
powerbase instance list --json
```

If no suitable instance exists, prefer the managed database flow first and save context.

```bash
powerbase instance create --name todo-app --org-id ORG_ID --json
powerbase context use-instance INSTANCE_ID
powerbase context use-branch main
```

Use `powerbase database create --name ... --dsn ...` only when the task explicitly needs an existing external database connection.

### 4. Use a branch for implementation work

```bash
powerbase branch create feature/todo-app --instance-id INSTANCE_ID --source-branch main --json
```

Use `powerbase branch switch ...` before `agent chat` when preview placement matters.
`powerbase context use-branch ...` only changes the local default branch value; it does not switch the remote sandbox.

### 5. Ask the sandbox agent to implement the feature

```bash
powerbase agent status --instance-id INSTANCE_ID --provider cursor --json
powerbase agent chat --instance-id INSTANCE_ID --provider cursor --message "Build a todo app with create, complete, delete, and list features." --stream-jsonl
```

If a wrapper script drives the CLI, use `python -u` or `PYTHONUNBUFFERED=1` so long-running output is not hidden by stdout buffering.
In the current Powerbase workflow, successful `powerbase agent chat` runs are the normal path that produces previewable app changes.

### 6. Inspect, validate, and publish

```bash
powerbase sandbox files tree --instance-id INSTANCE_ID --root / --json
powerbase sandbox files read --instance-id INSTANCE_ID /src/app.tsx --json
powerbase sql run --instance-id INSTANCE_ID --branch feature/todo-app --sql "SELECT 1" --json
powerbase publish diff --instance-id INSTANCE_ID --json
powerbase publish run --instance-id INSTANCE_ID --json
```

Treat `powerbase publish diff` as an inspection step. Treat `powerbase publish run` as an explicit deployment action that should happen only when the user asks to publish, deploy, or promote the result.
Direct `sandbox files` operations can still inspect or adjust the remote project, but they do not by themselves trigger the preview build flow.

## How To Handle A Product Request

When the user asks for something like:

- "Build a TODO app"
- "Create a CRM demo"
- "Add login and a dashboard"

Use this decision order:

1. Make sure authentication is valid.
2. Discover whether a suitable instance already exists.
3. If not, prefer creating the instance with the managed Powerbase database flow.
4. Only if the task explicitly needs an existing external database, discover or register a database connection and then create the instance with `--database-id`.
5. Save instance context.
6. Create or switch to a working branch.
7. Use `powerbase agent chat` as the primary implementation command.
8. Use `sandbox files`, `sql run`, and `publish diff` as validation or control tools around the agent.
9. Use `publish run` only when the user wants the result deployed or published.

Treat `powerbase agent chat` as the main implementation surface for Powerbase-hosted apps. Treat the rest of the CLI as the resource, state, validation, and deployment surface around it.

## Parameter Sources

When a command needs an ID or path, prefer these sources:

- `instance_id`: `powerbase instance list --json` or `powerbase context show --json`
- `org_id`: `powerbase org list --json`
- `database_id`: `powerbase database list --json`
- `branch`: `powerbase branch list --json` or `powerbase context show --json`
- sandbox `path`: use absolute sandbox paths like `/src/app.tsx` or `/tmp`
- agent `provider`: `powerbase agent providers --json`

## High-Value Commands

### Auth

```bash
powerbase auth login --json
powerbase auth wait --login-id LOGIN_ID --timeout 600 --json
powerbase auth status --json
powerbase auth refresh --json
powerbase auth logout --json
```

### Resource Discovery

```bash
powerbase org list --json
powerbase database list --json
powerbase instance list --json
powerbase branch list --instance-id INSTANCE_ID --json
```

### Context And Branches

```bash
powerbase context show --json
powerbase context use-org ORG_ID
powerbase context use-instance INSTANCE_ID
powerbase context use-branch main
powerbase branch create feature/demo --instance-id INSTANCE_ID --source-branch main --json
powerbase branch switch feature/demo --instance-id INSTANCE_ID --json
```

Treat the `switched_to` value from `branch create` as the canonical branch slug
for later commands. Do not assume the raw input string is still the deleteable
slug; for example, `feature/demo` may come back as `feature-demo`.

### Database And Instance Creation

```bash
powerbase instance create --name todo-app --org-id ORG_ID --json
```

`instance create` starts provisioning but the instance may not be readable
immediately. If `instance get`, `branch list`, or sandbox commands fail right
after creation, retry for a short window instead of assuming the create failed.

Advanced bring-your-own-database path:

```bash
powerbase database create --name todo-db --dsn "mysql://user:pass@host:3306/db" --db-type mysql --json
powerbase instance create --name todo-app --database-id DATABASE_ID --org-id ORG_ID --json
```

### App Implementation

```bash
powerbase agent providers --instance-id INSTANCE_ID --json
powerbase agent status --instance-id INSTANCE_ID --provider cursor --json
powerbase agent login-url --instance-id INSTANCE_ID --provider cursor --json
powerbase agent chat --instance-id INSTANCE_ID --provider cursor --message "Build a todo app" --stream-jsonl
```

### Inspection, SQL, And Publish

```bash
powerbase sandbox files tree --instance-id INSTANCE_ID --root / --json
powerbase sandbox files read --instance-id INSTANCE_ID /src/app.tsx --json
powerbase sql run --instance-id INSTANCE_ID --branch main --sql "SELECT 1" --json
powerbase publish diff --instance-id INSTANCE_ID --json
powerbase publish run --instance-id INSTANCE_ID --json
```

### Agent Provider Configuration

```bash
powerbase agent opencode-config get --instance-id INSTANCE_ID --json
powerbase agent opencode-config set --instance-id INSTANCE_ID --provider anthropic --api-key API_KEY --json
powerbase agent opencode-json set --instance-id INSTANCE_ID --file ./opencode.json --json
```

## Guardrails

- Powerbase provides the coding agent for Powerbase-hosted apps. When the task is to implement or evolve that app, default to `powerbase agent chat` instead of authoring the app directly in the caller workspace.
- Do not jump straight to `agent chat` until you know which instance and branch should receive the changes.
- Do not run write commands until the target instance and branch are confirmed.
- Do not assume a saved context is correct for the current task; check it first.
- Do not assume `context use-branch` has switched the remote sandbox; use `branch switch` when the target preview branch matters.
- In the current product workflow, previewable app changes are normally produced by successful `powerbase agent chat` runs on the target sandbox branch.
- Treat `sandbox files` as the remote sandbox inspection and control surface. Use it for reading, validation, and targeted file operations around the coding agent, not as the default full-feature implementation path.
- Do not assume `sandbox files create-file`, `upload`, or `delete` will trigger a preview build on their own.
- Do not guess a `database_id`; discover it with `powerbase database list --json` or create one explicitly when the task truly needs an external database.
- When `powerbase auth login --json` returns `login_url`, give it to the user and stop.
- Do not open the URL or use browser tools.
- Only after the user explicitly confirms approval may you run `powerbase auth wait --login-id LOGIN_ID --json`.
- When a protected command reports missing or expired authentication, do not keep retrying it. Generate a fresh login URL with `powerbase auth login --json` and ask the user to complete browser approval first.
- If a command fails due to missing `instance_id`, fix context first instead of retrying blindly.
- If a command supports `--help`, read it before guessing parameter names.
- If you save `config output text`, remember that a command-level `--json` still wins for that invocation.
- Do not rely on `agent custom-provider` commands; they are intentionally not part of the user-facing CLI flow right now.
- For Powerbase-related implementation work, prefer `powerbase agent chat` as the implementation command and use the rest of the CLI to set up, inspect, validate, and deploy the environment around it.
- Do not run `powerbase publish run` unless the user explicitly asks to publish, deploy, release, or promote the result.
- Remember that `powerbase database create` registers a DSN and may store credentials on the platform; it does not provision a new physical database.
- For preview validation, include a unique marker in the implementation prompt and verify it from the built preview URL or JS bundle after `build_success`.

## Output Expectations

- Use `--json` for agent loops, parsing, and follow-up decision making.
- Use `--stream-jsonl` for long-running `powerbase agent chat` execution.
- When wrapping the CLI in Python, prefer `python -u` or `PYTHONUNBUFFERED=1`.
- Use human-readable output only when the user explicitly wants prose or copy-paste console output.
