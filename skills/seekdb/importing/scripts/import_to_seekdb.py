#!/usr/bin/env python3
"""
Import CSV/Excel files to seekdb vector database and manage collections.

Usage:
    python import_to_seekdb.py import <file_path> [--vectorize-column <column_name>] [--collection <name>]
    python import_to_seekdb.py delete <collection_name>

Examples:
    # Import with vectorization on Details column
    python import_to_seekdb.py import products.csv --vectorize-column Details
    
    # Import without vectorization
    python import_to_seekdb.py import products.csv
    
    # Import Excel file with custom collection name
    python import_to_seekdb.py import products.xlsx --vectorize-column Description --collection my_products
    
    # Delete a collection
    python import_to_seekdb.py delete my_collection

Note: To list all collections, use query_from_seekdb.py list command.

This script is designed for use in Claude Code (non-interactive environment).
"""

import argparse
import os
import uuid
import sys
from pathlib import Path
from typing import Optional

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv is optional, will use environment variables directly

try:
    import pandas as pd
except ImportError:
    print("Error: pandas is required. Install with: pip install pandas openpyxl")
    sys.exit(1)

try:
    import pyseekdb
except ImportError:
    print("Error: pyseekdb is required. Install with: pip install pyseekdb")
    sys.exit(1)
host = os.getenv("SEEKDB_HOST")
if host:
    # Server mode
    client = pyseekdb.Client(
        host=host,
        port=int(os.getenv("SEEKDB_PORT", "2881")),
        database=os.getenv("SEEKDB_DATABASE", "test"),
        user=os.getenv("SEEKDB_USER", "root"),
        password=os.getenv("SEEKDB_PASSWORD", "")
    )
else:
    # Embedded mode
    seekdb_path = os.path.expanduser("~/.seekdb")
    # Ensure directory exists
    os.makedirs(seekdb_path, exist_ok=True)
    client = pyseekdb.Client(path=seekdb_path)

def read_file(file_path: str) -> pd.DataFrame:
    """Read CSV or Excel file into DataFrame."""
    path = Path(file_path)
    
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    suffix = path.suffix.lower()
    
    if suffix == '.csv':
        return pd.read_csv(file_path)
    elif suffix in ['.xlsx', '.xls']:
        return pd.read_excel(file_path)
    else:
        raise ValueError(f"Unsupported file format: {suffix}. Use .csv or .xlsx")


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Clean DataFrame for import."""
    # Convert numpy types to Python types
    for col in df.columns:
        if df[col].dtype == 'int64':
            df[col] = df[col].astype(object).where(df[col].notna(), None)
        elif df[col].dtype == 'float64':
            df[col] = df[col].astype(object).where(df[col].notna(), None)
    
    # Fill NaN with empty string for string columns
    df.infer_objects(copy=False).fillna('')
    
    return df


def import_to_seekdb(
    file_path: str,
    vectorize_column: Optional[str] = None,
    collection_name: Optional[str] = None,
    batch_size: int = 100
):
    """
    Import CSV/Excel file to seekdb.
    
    Args:
        file_path: Path to CSV or Excel file
        vectorize_column: Column name to vectorize for semantic search (optional)
        collection_name: Name of the collection (default: derived from filename)
        batch_size: Number of records per batch insert
    
    Environment Variables (from .env):
        SEEKDB_HOST: seekdb server host (for server mode)
        SEEKDB_PORT: seekdb server port (default: 2881)
        SEEKDB_DATABASE: Database name (default: test)
        SEEKDB_USER: Username (default: root)
        SEEKDB_PASSWORD: Password
    """
    # Step 1: Read file
    print(f"Reading file: {file_path}")
    df = read_file(file_path)
    df = clean_dataframe(df)
    print(f"Loaded {len(df)} records with columns: {df.columns.tolist()}")
    
    # Validate vectorize column
    if vectorize_column and vectorize_column not in df.columns:
        raise ValueError(f"Column '{vectorize_column}' not found. Available columns: {df.columns.tolist()}")
    
    # Step 2: Connect to seekdb (read connection params from environment)
    print("Connecting to seekdb...")

    
    # Step 3: Determine collection name
    if not collection_name:
        collection_name = Path(file_path).stem.replace(' ', '_').replace('-', '_')
    
    print(f"Collection name: {collection_name}")
    
    # Step 4: Create collection
    if vectorize_column:
        print(f"Creating collection with vectorization on column: {vectorize_column}")
        print("Using DefaultEmbeddingFunction (all-MiniLM-L6-v2, 384 dimensions)")
        # Use default embedding function (auto-calculates dimension)
        collection = client.get_or_create_collection(name=collection_name)
    else:
        print("Creating collection without vectorization")
        # Without embedding function, must specify dimension
        collection = client.get_or_create_collection(
            name=collection_name,
            embedding_function=None
        )
    
    # Step 5: Prepare data
    ids = [str(uuid.uuid4()) for _ in range(len(df))]
    
    documents: Optional[list[str]] = None
    metadatas: list[dict]
    
    if vectorize_column:
        documents = df[vectorize_column].astype(str).tolist()
        metadata_columns:list[str] = [col for col in df.columns if col != vectorize_column]
        metadatas = df[metadata_columns].to_dict("records")  # type: ignore[call-overload]
    else:
        metadatas = df.to_dict("records")  # type: ignore[call-overload]
    
    # Step 6: Import in batches
    print(f"Importing {len(ids)} records in batches of {batch_size}...")
    total_imported = 0
    
    for i in range(0, len(ids), batch_size):
        batch_ids = ids[i:i+batch_size]
        batch_meta = metadatas[i:i+batch_size]
        
        if vectorize_column and documents is not None:
            batch_docs = documents[i:i+batch_size]
            collection.add(
                ids=batch_ids,
                documents=batch_docs,
                metadatas=batch_meta
            )
        else:
            # Without vectorization, need to provide embeddings
            # Using dummy embeddings (in real use, generate proper embeddings or skip)
            import random
            batch_embeddings = [[random.random() for _ in range(384)] for _ in range(len(batch_ids))]
            collection.add(
                ids=batch_ids,
                embeddings=batch_embeddings,
                metadatas=batch_meta
            )
        
        total_imported += len(batch_ids)
        print(f"  Imported {total_imported}/{len(ids)} records")
    
    # Step 7: Verify
    count = collection.count()
    print(f"\nImport complete!")
    print(f"Total records in collection '{collection_name}': {count}")
    
    # Preview
    preview = collection.peek(limit=2)
    print("\nPreview of imported data:")
    for i in range(len(preview['ids'])):
        print(f"  ID: {preview['ids'][i][:8]}...")
        if preview['documents'] and preview['documents'][i]:
            doc_preview = preview['documents'][i][:80] if len(preview['documents'][i]) > 80 else preview['documents'][i]
            print(f"  Document: {doc_preview}...")
        print(f"  Metadata keys: {list(preview['metadatas'][i].keys())}")
        print()
    
    return collection_name, count


def delete_collection(collection_name: str):
    """
    Delete a collection from seekdb.
    
    Args:
        collection_name: Name of the collection to delete
    """
    print("Connecting to seekdb...")
    
    # Check if collection exists
    collections = client.list_collections()
    collection_names = [c.name for c in collections]
    
    if collection_name not in collection_names:
        print(f"Error: Collection '{collection_name}' not found.")
        print(f"Available collections: {collection_names}")
        return False
    
    # Delete collection
    print(f"Deleting collection '{collection_name}'...")
    client.delete_collection(collection_name)
    print(f"Collection '{collection_name}' has been deleted successfully.")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Import CSV/Excel files to seekdb vector database and manage collections",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Import subcommand
    import_parser = subparsers.add_parser(
        "import", 
        help="Import CSV/Excel file to seekdb",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    import_parser.add_argument("file_path", help="Path to CSV or Excel file")
    import_parser.add_argument("--vectorize-column", "-v", 
                               help="Column name to vectorize for semantic search")
    import_parser.add_argument("--collection", "-c",
                               help="Collection name (default: derived from filename)")
    import_parser.add_argument("--batch-size", "-b", type=int, default=100,
                               help="Batch size for import (default: 100)")
    
    # Delete subcommand
    delete_parser = subparsers.add_parser(
        "delete",
        help="Delete a collection from seekdb"
    )
    delete_parser.add_argument("collection_name", help="Name of the collection to delete")
    
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        sys.exit(1)
    
    try:
        if args.command == "import":
            collection_name, count = import_to_seekdb(
                file_path=args.file_path,
                vectorize_column=args.vectorize_column,
                collection_name=args.collection,
                batch_size=args.batch_size
            )
            print(f"\nSuccess! Collection '{collection_name}' now has {count} records.")
        
        elif args.command == "delete":
            success = delete_collection(collection_name=args.collection_name)
            if not success:
                sys.exit(1)
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
