---
name: importing-to-seekdb
description: "Import CSV or Excel files into seekdb vector database and manage collections. Supports automatic vectorization of specified columns using embedding functions. When users need to: (1) Read and preview Excel files, (2) Import CSV/Excel data into seekdb, (3) Create vector collections from tabular data, (4) Vectorize specific text columns for semantic search, (5) Batch insert product/document data with embeddings, (6) Delete collections, or (7) Access sample data files (sample_products.csv/xlsx) for testing - IMPORTANT: sample files are located in this skill's example-data/ directory, you MUST read this skill file first to get the correct path."
license: MIT
---

# Import Data Files to seekdb

Read, preview, and import CSV or Excel files into seekdb vector database with optional column vectorization for semantic search. Also provides collection delete functionality.

## Path Convention

> **Note**: All paths in this document (e.g., `scripts/`, `example-data/`) are relative to THIS skill directory, not the project root.

## Prerequisites

- Python 3.10+ installed
- Required packages:

```bash
pip install pyseekdb pandas openpyxl
```

## Sample Data

Sample data files are provided in the `example-data/` directory:

| File | Description |
|------|-------------|
| `sample_products.csv` | Sample product data in CSV format |
| `sample_products.xlsx` | Sample product data in Excel format |

## Quick Start

Use the provided `scripts/import_to_seekdb.py` script:

```bash
# Import with vectorization on Details column
python scripts/import_to_seekdb.py import example-data/sample_products.csv --vectorize-column Details

# Import without vectorization
python scripts/import_to_seekdb.py import example-data/sample_products.csv

# Import Excel with custom collection name
python scripts/import_to_seekdb.py import example-data/sample_products.xlsx -v Description -c my_products

# Delete a collection
python scripts/import_to_seekdb.py delete my_collection
```

> **Note**: To list all collections, use `query_from_seekdb.py list` from the `querying-from-seekdb` skill.

## Scripts

This skill provides the following scripts in the `scripts/` directory:

| Script | Description |
|--------|-------------|
| `import_to_seekdb.py` | Main script with CLI interface for importing data and managing collections |
| `read_excel.py` | Read and preview Excel files with detailed information |

### Available Commands

#### import_to_seekdb.py

| Command | Description |
|---------|-------------|
| `import <file>` | Import CSV/Excel file to seekdb with optional vectorization |
| `delete <name>` | Delete a collection from seekdb |

#### read_excel.py

Read and preview Excel files before importing:

```bash
# Basic preview (show file info and first 5 rows)
python scripts/read_excel.py example-data/sample_products.xlsx

# List all sheets
python scripts/read_excel.py example-data/sample_products.xlsx --list-sheets

# Preview specific sheet with more rows
python scripts/read_excel.py data.xlsx --sheet "Sheet2" --rows 20

# Show column information and statistics
python scripts/read_excel.py example-data/sample_products.xlsx --columns --stats

# Export to CSV
python scripts/read_excel.py example-data/sample_products.xlsx --to-csv output.csv
```

| Option | Description |
|--------|-------------|
| `--sheet, -s` | Sheet name to read (default: first sheet) |
| `--rows, -r` | Number of rows to preview (default: 5) |
| `--list-sheets, -l` | List all sheets and exit |
| `--columns, -c` | Show detailed column information |
| `--stats` | Show statistics for numeric columns |
| `--to-csv` | Export sheet to CSV file |
| `--all-rows, -a` | Display all rows |

## Workflow

The `import_to_seekdb.py` script automatically handles the following steps:

1. **Read Data File** - Supports CSV (.csv) and Excel (.xlsx, .xls) formats
2. **Connect to seekdb** - Uses environment variables for server mode, or embedded mode by default
3. **Create Collection** - With optional vectorization using default embedding function (all-MiniLM-L6-v2, 384 dimensions)
4. **Import Data** - Batch processing with configurable batch size
5. **Verify** - Displays record count and data preview after import

## User Interaction Guide

### For Reading Excel Files

When user wants to preview or inspect an Excel file before importing:

```bash
# Preview file structure and data
python scripts/read_excel.py <file_path>

# With column details and statistics
python scripts/read_excel.py <file_path> --columns --stats
```

This helps users:
- Understand the file structure (sheets, columns, row count)
- Identify which column to vectorize
- Check data quality before importing

### For Data Import

When user requests data import, ask:

1. **File path**: "Please provide the path to your CSV or Excel file."
   - If user needs sample data, use files from the `example-data/` directory
   - Suggest using `read_excel.py` to preview the file first
2. **Vectorization**: "Would you like to enable vector search by vectorizing a column? (yes/no)"
3. **Column selection** (if yes): "Which column to vectorize? (e.g., 'Details', 'Description')"
4. **Collection name**: "Collection name? (default: derived from filename)"
5. **Connection mode**: "Embedded (local) or server mode?"

### For Collection Management

- **List collections**: Use `query_from_seekdb.py list` from the `querying-from-seekdb` skill
- **Delete collection**: Run `python scripts/import_to_seekdb.py delete <collection_name>`

## Embedding Functions

The script uses the default embedding function (all-MiniLM-L6-v2, 384 dimensions) when vectorization is enabled via `--vectorize-column`.

## Handling Large Files

For files with >10,000 rows, the `import_to_seekdb.py` script uses batch processing automatically. You can configure batch size:

```bash
python scripts/import_to_seekdb.py import large_file.csv -v Details --batch-size 500
```

## References

- [pyseekdb SDK Getting Started](https://github.com/oceanbase/seekdb-doc/blob/V1.0.0/en-US/450.reference/900.sdk/10.pyseekdb-sdk/10.pyseekdb-sdk-get-started.md)
- [create_collection API](https://github.com/oceanbase/seekdb-doc/blob/V1.0.0/en-US/450.reference/900.sdk/10.pyseekdb-sdk/50.apis/200.collection/100.create-collection-of-api.md)
- [delete_collection API](https://github.com/oceanbase/seekdb-doc/blob/V1.0.0/en-US/450.reference/900.sdk/10.pyseekdb-sdk/50.apis/200.collection/400.delete-collection-of-api.md)
- [add API](https://github.com/oceanbase/seekdb-doc/blob/V1.0.0/en-US/450.reference/900.sdk/10.pyseekdb-sdk/50.apis/300.dml/200.add-data-of-api.md)
