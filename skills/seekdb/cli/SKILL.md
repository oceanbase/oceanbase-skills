---
name: seekdb-cli
description: "Use seekdb-cli to interact with seekdb/OceanBase databases via shell commands. Use when: (1) querying databases with SQL, (2) exploring table schemas and structure, (3) profiling table data distributions, (4) inferring table relationships, (5) managing vector collections and semantic search, (6) adding/exporting collection data, (7) managing AI models , (8) checking database connection status, or (9) performing any database operation via command line."
license: MIT
---

# seekdb-cli — AI-Agent Database CLI

A command-line client designed for AI Agents. All output is JSON-structured, stateless, with built-in safety guardrails.

## Prerequisites

Check if seekdb-cli is installed (either command works—they share the same entry point):


```bash
seekdb --version
# or, aligned with PyPI package name / for `which`-style checks:
seekdb-cli --version
```

If not installed, choose the method that matches your environment:

**Recommended — pipx (works globally without polluting system Python):**

```bash
# Install pipx first if needed (Ubuntu/Debian)
sudo apt install pipx && pipx ensurepath
# Then install seekdb-cli
pipx install seekdb-cli
```

**Alternative — pip (when inside a project venv or on systems without PEP 668):**

```bash
pip install seekdb-cli
```

> **Note for Ubuntu 23.04+ / Debian 12+:** Direct `pip install` at the system level is blocked by PEP 668.
> Use `pipx` instead — it creates an isolated environment while keeping **`seekdb`** and **`seekdb-cli`** on your PATH (same program).

Throughout this skill, examples use `seekdb`; you may substitute `seekdb-cli` everywhere.

**Embedded vs remote:** The default local store uses **embedded** mode (pyseekdb). That requires **Linux (glibc ≥ 2.28) or macOS 15+**; on other OSes, connect with a remote DSN: `seekdb --dsn "seekdb://user:pass@host:port/db" ...`.

## Connection

**DSN resolution** (highest priority wins):

1. `--dsn` on the CLI (must appear **before** the subcommand)
2. `SEEKDB_DSN` environment variable
3. `.env` in the **current working directory** (`SEEKDB_DSN=...` line)
4. `~/.seekdb/config.env`
5. Default `embedded:~/.seekdb/seekdb.db`

With no config, the default embedded path applies — you can run commands directly. If the user gives a specific DSN, pass it with `--dsn`:

```bash
# Remote mode
seekdb --dsn "seekdb://user:pass@host:port/db" schema tables

# Remote with TLS (query string on the URL; encode special characters in user/password)
# tls=skip-verify — encrypted, no certificate verification (common for self-signed servers)
seekdb --dsn "seekdb://user:pass@host:2881/db?tls=skip-verify" status
# tls=required — encrypted with default OS CA verification
seekdb --dsn "seekdb://user:pass@host:2881/db?tls=required" sql "SELECT 1"

# Embedded mode (path is a data directory, created if missing; not a single SQLite file)
seekdb --dsn "embedded:./seekdb.db" status
seekdb --dsn "embedded:~/.seekdb/seekdb.db?database=mydb" sql "SELECT 1"
```

DSN formats:
- **Remote:** `seekdb://user:pass@host:port/db`
- **Remote + TLS:** append `?tls=skip-verify|required|verify-ca|verify-identity` (or the same values via MySQL-style `sslmode=`, e.g. `REQUIRED`, `VERIFY_CA`). Optional query params: `ssl_ca`, `ssl_cert`, `ssl_key`, `ssl_key_password`.
- **Embedded:** `embedded:<path>[?database=<db>]` (default logical database name: `test`)

## Self-Description for AI Agents

Run `seekdb ai-guide` to get a structured JSON guide of all commands, recommended workflow, safety features, and output format. Execute this once to learn the full CLI.

```bash
seekdb ai-guide
```

## Recommended Workflow

### SQL Database Exploration

```
1. seekdb schema tables              → list all tables (name, column count, row count)
2. seekdb schema describe <table>    → get column names, types, indexes, comments
3. seekdb table profile <table>      → get data statistics (null ratios, distinct, min/max, top values)
4. seekdb relations infer            → infer JOIN relationships between tables
5. seekdb sql "SELECT ... LIMIT N"   → execute SQL with explicit LIMIT
```

### Vector Collection Workflow

```
1. seekdb collection list            → list all collections
2. seekdb collection info <name>     → get collection details and preview
3. seekdb query <collection> --text "..." → search (default: hybrid = semantic + fulltext)
```

## Command Reference

### seekdb sql

Execute SQL statements. Default is read-only mode.

```bash
# Read query
seekdb sql "SELECT id, name FROM users LIMIT 10"

# Read from file
seekdb sql --file query.sql

# Pipe or redirect (stdin read automatically when not a TTY; --stdin is optional)
echo "SELECT 1" | seekdb sql
# Explicit stdin (e.g. redirect into the command)
seekdb sql --stdin < query.sql

# Include table schema in output
seekdb sql "SELECT * FROM orders LIMIT 5" --with-schema

# Disable large-field truncation
seekdb sql "SELECT content FROM articles LIMIT 1" --no-truncate

# Write operation (requires --write flag)
seekdb sql --write "INSERT INTO users (name) VALUES ('Alice')"
seekdb sql --write "UPDATE users SET name = 'Bob' WHERE id = 1"
seekdb sql --write "DELETE FROM users WHERE id = 3"
```

**Output format:**

```json
{"ok": true, "columns": ["id", "name"], "rows": [{"id": 1, "name": "Alice"}], "affected": 0, "time_ms": 12}
```

### seekdb schema tables

```bash
seekdb schema tables
```

```json
{"ok": true, "data": [{"name": "users", "columns": 5, "rows": 1200}, {"name": "orders", "columns": 8, "rows": 50000}]}
```

### seekdb schema describe

```bash
seekdb schema describe orders
```

```json
{"ok": true, "data": {"table": "orders", "comment": "Order table", "columns": [{"name": "id", "type": "int", "comment": "Order ID"}, {"name": "status", "type": "varchar(20)", "comment": "0=pending, 1=paid"}], "indexes": ["PRIMARY(id)", "idx_status(status)"]}}
```

### seekdb schema dump

```bash
seekdb schema dump
```

Returns all `CREATE TABLE` DDL statements.

### seekdb table profile

Generate statistical summary of a table without returning raw data. Helps understand data distribution before writing SQL.

```bash
seekdb table profile <table>
```

```json
{"ok": true, "data": {
  "table": "orders",
  "row_count": 50000,
  "columns": [
    {"name": "id", "type": "int", "null_ratio": 0, "distinct": 50000, "min": 1, "max": 50000},
    {"name": "user_id", "type": "int", "null_ratio": 0, "distinct": 1200, "min": 1, "max": 1500},
    {"name": "amount", "type": "decimal(10,2)", "null_ratio": 0.02, "min": 0.5, "max": 9999.99},
    {"name": "status", "type": "varchar(20)", "null_ratio": 0, "distinct": 4, "top_values": ["paid", "pending", "refunded", "cancelled"]},
    {"name": "created_at", "type": "datetime", "null_ratio": 0, "min": "2024-01-01", "max": "2026-03-10"}
  ],
  "candidate_join_keys": ["user_id"],
  "candidate_time_columns": ["created_at"]
}}
```

### seekdb relations infer

Infer JOIN relationships between tables by analyzing column name patterns (e.g., `user_id` → `users.id`) and type compatibility.

```bash
# Infer all table relationships
seekdb relations infer

# Infer for a specific table only
seekdb relations infer --table orders
```

```json
{"ok": true, "data": [
  {"from": "orders.user_id", "to": "users.id", "confidence": "high"},
  {"from": "orders.product_id", "to": "products.id", "confidence": "high"},
  {"from": "order_items.order_id", "to": "orders.id", "confidence": "high"}
]}
```

### seekdb collection list

```bash
seekdb collection list
```

```json
{"ok": true, "data": [{"name": "docs", "count": 1500}, {"name": "faq", "count": 200}]}
```

### seekdb collection create

```bash
seekdb collection create my_docs --dimension 384 --distance cosine
seekdb collection create my_docs -d 768 --distance l2
```

Options: `--dimension` / `-d` (default: 384), `--distance` cosine | l2 | ip (default: cosine).

### seekdb collection delete

```bash
seekdb collection delete my_docs
```

### seekdb collection info

```bash
seekdb collection info my_docs
```

```json
{"ok": true, "data": {"name": "my_docs", "count": 1500, "dimension": 384, "distance": "cosine", "preview": {"ids": ["doc1", "doc2"], "documents": ["Hello world", "Test doc"], "metadatas": [{"category": "test"}, {}]}}}
```

`dimension` and `distance` are included when available from the collection metadata.

### seekdb query

Search a collection using hybrid (default), semantic (vector), or fulltext mode.

```bash
# Hybrid search (default: semantic + fulltext, RRF ranking)
seekdb query my_docs --text "how to deploy seekdb"

# Semantic (vector) only
seekdb query my_docs --text "how to deploy seekdb" --mode semantic

# Fulltext search
seekdb query my_docs --text "deployment guide" --mode fulltext

# With metadata filter
seekdb query my_docs --text "performance tuning" --where '{"category": "tech"}'

# Limit results (--limit or -n, default: 10)
seekdb query my_docs --text "seekdb" -n 5
```

```json
{"ok": true, "data": {"results": [
  {"id": "doc1", "score": 0.92, "document": "How to deploy seekdb...", "metadata": {"category": "tech"}},
  {"id": "doc2", "score": 0.85, "document": "seekdb performance tuning...", "metadata": {"category": "tech"}}
], "count": 2}, "time_ms": 35}
```

### seekdb get

Retrieve documents from a collection by IDs or metadata filter.

```bash
# Get by IDs
seekdb get my_docs --ids "doc1,doc2"

# Get by metadata filter (--limit or -n, default: 10)
seekdb get my_docs --where '{"category": "tech"}' -n 20
```

### seekdb add

Add data to a collection. Exactly one source is required: `--file`, `--stdin`, or `--data`. The collection is auto-created if it does not exist.

```bash
# From file (JSON array, JSONL, or CSV)
seekdb add my_docs --file data.jsonl
seekdb add my_docs --file articles.csv --vectorize-column content

# Inline: single object or array
seekdb add my_docs --data '{"id":"1","document":"Hello world","metadata":{"source":"cli"}}'
seekdb add my_docs --data '[{"id":"a","document":"Doc A"},{"id":"b","document":"Doc B"}]'

# From stdin (JSON array or JSONL; use with pipes)
echo '{"id":"1","document":"from pipe"}' | seekdb add my_docs --stdin
some_script | seekdb add my_docs --stdin
```

**Record format**: Each record may have `id` (optional), `document`/`text`/`content` (text to vectorize), and any other fields become metadata. If `embedding` is present, it is used directly.

### seekdb export

Export collection data to a file.

```bash
seekdb export my_docs --output backup.json
seekdb export my_docs --output backup.jsonl -n 5000
```

Options: `--output` (required), `--limit` / `-n` (default: 10000).

### seekdb ai model list

List AI models registered in the database (from `DBA_OB_AI_MODELS` / DBMS_AI_SERVICE). Works in both remote and embedded mode.

```bash
seekdb ai model list
```

```json
{"ok": true, "data": [{"name": "my_llm", "type": "completion", "model_name": "THUDM/GLM-4-9B-0414", "model_id": 1}]}
```

### seekdb ai model create

Register an AI model via `DBMS_AI_SERVICE.CREATE_AI_MODEL`. Create an endpoint separately to use it for completion.

```bash
seekdb ai model create my_llm --type completion --model "THUDM/GLM-4-9B-0414"
seekdb ai model create my_embed --type dense_embedding --model "BAAI/bge-m3"
seekdb ai model create my_rerank --type rerank --model "<rerank_model>"
```

Types: `completion`, `dense_embedding`, `rerank`.

### seekdb ai model delete

Drop an AI model. Drop any endpoints that use it first.

```bash
seekdb ai model delete my_llm
```

### seekdb ai model endpoint create / delete

Create or drop an endpoint that binds an AI model to a URL and API key (so the database can call the model).

```bash
seekdb ai model endpoint create my_ep my_llm \
  --url "https://api.siliconflow.cn/v1/chat/completions" \
  --access-key "<YOUR_API_KEY>" \
  --provider siliconflow

seekdb ai model endpoint delete my_ep
```

**Supported `--provider` values:**

| Provider | Vendor |
|----------|--------|
| `siliconflow` | SiliconFlow (OpenAI-compatible) |
| `openAI` | OpenAI |
| `deepseek` | DeepSeek (OpenAI-compatible) |
| `aliyun-openAI` | Alibaba Cloud (OpenAI-compatible) |
| `aliyun-dashscope` | Alibaba Cloud DashScope |
| `hunyuan-openAI` | Tencent Hunyuan (OpenAI-compatible) |

**Common `--url` values (use the specific interface URL, not the base URL):**

| Vendor | completion | embedding | rerank |
|--------|-----------|-----------|--------|
| SiliconFlow | `https://api.siliconflow.cn/v1/chat/completions` | `https://api.siliconflow.cn/v1/embeddings` | `https://api.siliconflow.cn/v1/rerank` |
| DeepSeek | `https://api.deepseek.com/chat/completions` | — | — |
| Alibaba (OpenAI) | `https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions` | `https://dashscope.aliyuncs.com/compatible-mode/v1/embeddings` | — |
| Tencent Hunyuan | `https://api.hunyuan.cloud.tencent.com/v1/chat/completions` | `https://api.hunyuan.cloud.tencent.com/v1/embeddings` | — |

> Full parameter spec: [CREATE_AI_MODEL_ENDPOINT](references/create-ai-model-endpoint.md)

### seekdb ai complete

Run text completion using the database `AI_COMPLETE` function. Requires a registered **completion** model and an endpoint. Supported in both remote and embedded mode.

```bash
seekdb ai complete "Summarize this table structure" --model my_llm
```

```json
{"ok": true, "data": {"model": "my_llm", "response": "The table has..."}, "time_ms": 1200}
```

### seekdb ai-guide

Output a structured JSON guide for AI Agents containing all commands, parameters, workflow, and safety rules. Execute once to learn the full CLI.

```bash
seekdb ai-guide
```

### seekdb status

```bash
seekdb status
```

Returns CLI version, server version, database name, and connectivity.

## Safety Features

### Row Protection

Queries without `LIMIT` are automatically probed. If result exceeds 100 rows, execution is blocked:

```json
{"ok": false, "error": {"code": "LIMIT_REQUIRED", "message": "Query returns more than 100 rows. Please add LIMIT to your SQL."}}
```

**Action**: Add an explicit `LIMIT` clause and retry.

### Write Protection

Write operations (INSERT/UPDATE/DELETE) are blocked by default:

```json
{"ok": false, "error": {"code": "WRITE_NOT_ALLOWED", "message": "Write operations require --write flag."}}
```

**Action**: Add `--write` flag to enable write operations.

Even with `--write`, `DELETE` / `UPDATE` without a `WHERE` clause are blocked.

### Error Auto-Correction

On SQL errors, the CLI automatically attaches schema hints:

**Column not found** → returns the table's column list and indexes:
```json
{"ok": false, "error": {"code": "SQL_ERROR", "message": "Unknown column 'username'"}, "schema": {"table": "users", "columns": ["id", "name", "email"], "indexes": ["PRIMARY(id)"]}}
```

**Table not found** → returns available table names:
```json
{"ok": false, "error": {"code": "SQL_ERROR", "message": "Table 'user' does not exist"}, "schema": {"tables": ["users", "orders", "products"]}}
```

**Action**: Use the schema info to correct the SQL and retry.

### Large Field Truncation

TEXT/BLOB fields are truncated to 200 characters by default, with original length noted:

```json
{"content": "First 200 characters of content...(truncated, 8520 chars)"}
```

Use `--no-truncate` to get full content when needed.

### Sensitive Field Masking

Columns matching sensitive patterns are automatically masked:

| Pattern | Example Output |
|---------|---------------|
| phone/mobile/tel | `138****5678` |
| email | `z***@gmail.com` |
| password/secret/api_key | `******` |
| id_card / national_id / similar | `110***********1234` |

## Output Formats

Default is JSON. Switch with `--format` (global option; must appear **before** the subcommand):

```bash
seekdb --format table sql "SELECT id, name FROM users LIMIT 5"
seekdb --format csv sql "SELECT id, name FROM users LIMIT 5"
seekdb --format jsonl sql "SELECT id, name FROM users LIMIT 5"
```

All formats now work with non-row data (e.g., `schema tables`, `collection list`). CSV and JSONL will auto-detect list-of-dict data in the `data` field.

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Business error (SQL error, connection error, etc.) |
| 2 | Usage error (missing arguments, invalid options) |

## Operation Logging

All commands are logged to `~/.seekdb/sql-history.jsonl` for audit (SQL invocations include a redacted `sql` field when applicable):

```json
{"ts": "2026-03-12T14:23:01", "command": "sql", "sql": "SELECT id FROM users LIMIT 10", "ok": true, "rows": 10, "time_ms": 12}
```
