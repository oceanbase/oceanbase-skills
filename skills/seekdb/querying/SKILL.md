---
name: querying-from-seekdb
description: "Query and export data from seekdb vector database. Supports two search modes: (1) Scalar search - metadata filtering only, (2) Hybrid search - fulltext + semantic search combined. The --query-text parameter is used for BOTH fulltext ($contains) and semantic (query_texts) search simultaneously. Can export results to CSV/Excel."
license: MIT
---

# Query and Export Data from seekdb

Query data from seekdb vector database with support for scalar search, hybrid search (fulltext + semantic), and export to CSV/Excel files.

## Path Convention

> **Note**: All paths in this document (e.g., `scripts/`) are relative to THIS skill directory, not the project root.

## Prerequisites

- Python 3.10+ installed
- Data imported into seekdb collection
- Required packages:

```bash
pip install pyseekdb pandas openpyxl
```

## ⚠️ CRITICAL: Execution Workflow

**MUST FOLLOW this workflow when handling user search requests:**

### Step 1: Get Collection Information (If Not Already Known)

Before constructing any query, you MUST understand the data structure. **However, you should cache this information within the conversation.**

**Caching Rules:**
- ✅ **First query for a collection**: Execute `--info` to get metadata structure
- ✅ **Subsequent queries for the SAME collection**: Use cached info from earlier in conversation, skip `--info`
- ✅ **Query for a DIFFERENT collection**: Execute `--info` for the new collection
- ✅ **User explicitly asks for collection info**: Execute `--info`

```bash
# Get collection info to see metadata fields (only if not already known)
python scripts/query_from_seekdb.py <collection_name> --info
```

This shows:
- Total record count
- Available metadata field names (e.g., `source`, `year`, `category`)
- Sample documents

**Example conversation flow:**
```
User: "找 seekdb_demo 中 2023 年的教程"
→ Claude Code: 执行 --info (第一次查询此 collection)
→ 发现 metadata 有 source, year 字段
→ 执行搜索

User: "再找一下 notion 来源的"
→ Claude Code: 不需要再执行 --info (同一 collection，结构已知)
→ 直接执行搜索

User: "查一下 another_collection 中的数据"
→ Claude Code: 执行 --info (不同 collection)
→ 了解新 collection 的结构
→ 执行搜索
```

### Step 2: Analyze User Request

Parse the user's natural language request to identify:

| Component | Look For | Maps To |
|-----------|----------|---------|
| **Metadata conditions** | Field-value pairs like "2023年", "来自notion", "价格<100" | `--where` filter |
| **Content/Semantic search** | Keywords, concepts, descriptions, questions | `--query-text` (used for BOTH fulltext and semantic) |

**Important**: `--query-text` is used for **BOTH** fulltext search (`$contains`) and semantic search (`query_texts`) simultaneously. The same text is used for both.

### Step 3: Choose Search Method

```
User Request Analysis
       │
       ▼
┌─────────────────────────────────────────────────────────────┐
│ Does the request involve ONLY metadata field conditions?    │
│ (e.g., "year=2023", "source=notion", no content search)     │
└─────────────────────────────────────────────────────────────┘
       │
       ├── YES ──► Scalar Search: --where only
       │
       └── NO ───► Does it involve content/semantic search?
                          │
                          ├── YES (no metadata) ──► Hybrid Search: --query-text only
                          │
                          └── YES (with metadata) ──► Scalar + Hybrid: --where + --query-text
```

## Two Search Modes

### Mode 1: Scalar Search (Metadata Only)

**When to use**: User wants to filter by metadata fields ONLY, no content/semantic search needed.

```bash
# Filter by metadata fields only
python scripts/query_from_seekdb.py seekdb_demo --where '{"source": "notion", "year": 2023}'
```

**Example requests**:
- "找出所有来自 notion 的文档"
- "显示 2023 年的记录"
- "source 是 google-docs 的数据"

### Mode 2: Hybrid Search (Fulltext + Semantic)

**When to use**: User wants to search by content - the query text is used for BOTH fulltext matching AND semantic similarity.

```bash
# Hybrid search: query text used for both fulltext ($contains) and semantic (query_texts)
python scripts/query_from_seekdb.py seekdb_demo --query-text "seekdb 教程"
```

**How it works**:
- `--query-text "seekdb 教程"` → Fulltext: `where_document: {"$contains": "seekdb 教程"}` + Semantic: `query_texts: "seekdb 教程"`
- Results are ranked using RRF (Reciprocal Rank Fusion)

**Example requests**:
- "找 seekdb 教程" → `--query-text "seekdb 教程"`
- "搜索 python 技术文档" → `--query-text "python 技术文档"`

### Mode 3: Scalar + Hybrid Search

**When to use**: User wants metadata filtering + content/semantic search.

```bash
# Metadata filter + Hybrid search
python scripts/query_from_seekdb.py seekdb_demo --query-text "seekdb 教程" --where '{"year": 2023}'
```

**Example requests**:
- "请找出 seekdb_demo 集合中 2023 年写的 seekdb 教程" → `--query-text "seekdb 教程" --where '{"year": 2023}'`
- "找 notion 来源的编程指南" → `--query-text "编程指南" --where '{"source": "notion"}'`

## 🎯 Real-World Example Analysis

**User request**: "请找出 seekdb_demo 集合中 2023 年写的 seekdb 教程"

**Step 1**: Run `--info` to get metadata structure:
```bash
python scripts/query_from_seekdb.py seekdb_demo --info
# Output shows metadata fields: source, year
```

**Step 2**: Analyze request:
| Part | Type | Filter |
|------|------|--------|
| "2023 年" | Metadata field `year` | `--where '{"year": 2023}'` |
| "seekdb 教程" | Content/Semantic search | `--query-text "seekdb 教程"` |

**Step 3**: Execute:
```bash
python scripts/query_from_seekdb.py seekdb_demo --query-text "seekdb 教程" --where '{"year": 2023}'
```

## CLI Reference

### Commands

```bash
# List all collections
python scripts/query_from_seekdb.py --list-collections

# Show collection info (run this first to understand data structure!)
python scripts/query_from_seekdb.py <collection_name> --info

# Scalar search (metadata filter only)
python scripts/query_from_seekdb.py <collection_name> --where '<json_filter>'

# Hybrid search (fulltext + semantic, using same query text for both)
python scripts/query_from_seekdb.py <collection_name> --query-text "<text>" [-n <count>]

# Scalar + Hybrid search (metadata filter + fulltext + semantic)
python scripts/query_from_seekdb.py <collection_name> --query-text "<text>" --where '<json>'

# Export to CSV/Excel
python scripts/query_from_seekdb.py <collection_name> <search_options> --output results.csv
python scripts/query_from_seekdb.py <collection_name> <search_options> --output results.xlsx
```

### Options

| Option | Short | Description |
|--------|-------|-------------|
| `--query-text` | `-q` | Text for hybrid search (fulltext + semantic) |
| `--where` | `-w` | Metadata filter as JSON string |
| `--n-results` | `-n` | Number of results (default: 5) |
| `--output` | `-o` | Export to file (.csv or .xlsx) |
| `--json` | `-j` | Output as JSON |
| `--info` | | Show collection info |
| `--list-collections` | `-l` | List all collections |
| `--include` | | Fields to include: documents,metadatas,embeddings |
| `--sheet-name` | `-s` | Sheet name for Excel export |

## Filter Operators

### How to Construct --where Parameter

**Step 1**: Run `--info` to see available metadata fields:
```bash
python scripts/query_from_seekdb.py seekdb_demo --info

# Example output:
# Collection: seekdb_demo
#   Total records: 2
# Preview (first 3 records):
#   ID: doc1...
#     Document: python tutorial...
#     Metadata keys: ['source', 'year']    ← These are the metadata field names!
```

**Step 2**: Use the metadata field names to construct `--where`:
```bash
# From the output above, we know the collection has 'source' and 'year' fields
# So we can filter by these fields:

--where '{"source": "notion"}'           # source equals "notion"
--where '{"year": 2023}'                 # year equals 2023
--where '{"source": "notion", "year": 2023}'  # both conditions (implicit AND)
```

**Step 3**: Match user request to metadata fields:
| User says | Metadata field | --where value |
|-----------|----------------|---------------|
| "2023 年的" | `year` | `'{"year": 2023}'` |
| "来自 notion 的" | `source` | `'{"source": "notion"}'` |
| "价格低于 100 的" | `price` | `'{"price": {"$lt": 100}}'` |
| "品牌是三星或苹果的" | `brand` | `'{"brand": {"$in": ["Samsung", "Apple"]}}'` |

### Metadata Filter Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `$eq` | Equal to | `{"year": {"$eq": 2023}}` or `{"year": 2023}` |
| `$ne` | Not equal to | `{"status": {"$ne": "deleted"}}` |
| `$gt` | Greater than | `{"score": {"$gt": 90}}` |
| `$gte` | Greater than or equal | `{"score": {"$gte": 90}}` |
| `$lt` | Less than | `{"score": {"$lt": 50}}` |
| `$lte` | Less than or equal | `{"score": {"$lte": 50}}` |
| `$in` | In list | `{"tag": {"$in": ["ml", "ai"]}}` |
| `$nin` | Not in list | `{"tag": {"$nin": ["old"]}}` |
| `$and` | Logical AND | `{"$and": [{"year": 2023}, {"source": "notion"}]}` |
| `$or` | Logical OR | `{"$or": [{"year": 2023}, {"year": 2024}]}` |

### Complex Filter Examples

```bash
# Multiple conditions with implicit AND (both must be true)
--where '{"source": "notion", "year": 2023}'

# Explicit AND
--where '{"$and": [{"source": "notion"}, {"year": {"$gte": 2023}}]}'

# OR condition
--where '{"$or": [{"source": "notion"}, {"source": "google-docs"}]}'

# Range condition (year between 2022 and 2024)
--where '{"$and": [{"year": {"$gte": 2022}}, {"year": {"$lte": 2024}}]}'

# Combined AND + OR
--where '{"$and": [{"year": 2023}, {"$or": [{"source": "notion"}, {"source": "obsidian"}]}]}'
```

## Export to CSV/Excel

```bash
# Export scalar search results to CSV
python scripts/query_from_seekdb.py mobiles --where '{"Brand": "SAMSUNG"}' --output samsung.csv

# Export hybrid search results to Excel
python scripts/query_from_seekdb.py mobiles --query-text "good camera" --output results.xlsx

# Export with custom sheet name
python scripts/query_from_seekdb.py mobiles --query-text "phone" --output phones.xlsx --sheet-name "Search Results"
```

### Supported Export Formats

| Format | Extension | Description |
|--------|-----------|-------------|
| CSV | `.csv` | Comma-separated values, UTF-8 encoded with BOM |
| Excel | `.xlsx` | Excel workbook format |

## Data Structure in seekdb

seekdb stores data in two distinct locations:

| Storage | Description | Filter Method | Example |
|---------|-------------|---------------|---------|
| **Metadata** | Structured key-value fields | `--where` | `{"source": "notion", "year": 2023}` |
| **Document** | Text content | `--query-text` (hybrid search) | Fulltext + Semantic search |

## Connection Configuration

Set environment variables for server mode:

| Variable | Description | Default |
|----------|-------------|---------|
| `SEEKDB_HOST` | Server host (if set, uses server mode) | - |
| `SEEKDB_PORT` | Server port | 2881 |
| `SEEKDB_DATABASE` | Database name | test |
| `SEEKDB_USER` | Username | root |
| `SEEKDB_PASSWORD` | Password | - |

## References

- [pyseekdb SDK Getting Started](https://github.com/oceanbase/seekdb-doc/blob/V1.0.0/en-US/450.reference/900.sdk/10.pyseekdb-sdk/10.pyseekdb-sdk-get-started.md)
- [hybrid_search API](https://github.com/oceanbase/seekdb-doc/blob/V1.0.0/en-US/450.reference/900.sdk/10.pyseekdb-sdk/50.apis/400.dql/400.hybrid-search-of-api.md)
- [get API](https://github.com/oceanbase/seekdb-doc/blob/V1.0.0/en-US/450.reference/900.sdk/10.pyseekdb-sdk/50.apis/400.dql/300.get-interfaces-of-api.md)
- [Filter Operators](https://github.com/oceanbase/seekdb-doc/blob/V1.0.0/en-US/450.reference/900.sdk/10.pyseekdb-sdk/50.apis/400.dql/500.filter-operators-of-api.md)
