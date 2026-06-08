#!/usr/bin/env python3
"""
Query data from seekdb vector database and optionally export to CSV/Excel.

Supports three search modes:
    1. Scalar search: metadata filtering only (uses collection.get)
    2. Fulltext + Semantic search: text query with document content filter (uses collection.query)
    3. Scalar + Fulltext + Semantic search: all filters combined (uses collection.query)

Usage:
    python query_from_seekdb.py <collection_name> --query-text <text> [--n-results <n>]
    python query_from_seekdb.py <collection_name> --where <filter>
    python query_from_seekdb.py <collection_name> --query-text <text> --output results.csv
    python query_from_seekdb.py --list-collections
    python query_from_seekdb.py <collection_name> --info

Examples:
    # 1. Scalar search (metadata filter only)
    python query_from_seekdb.py mobiles --where '{"Brand": {"$eq": "SAMSUNG"}}'
    
    # 2. Hybrid search (fulltext + semantic, using same query text for both)
    python query_from_seekdb.py mobiles --query-text "phone with good battery"
    
    # 3. Scalar + Hybrid search (metadata filter + fulltext + semantic)
    python query_from_seekdb.py mobiles --query-text "budget phone" --where '{"Brand": {"$eq": "SAMSUNG"}}'
    
    # Export query results to CSV
    python query_from_seekdb.py mobiles --query-text "phone with good battery" --output results.csv
    
    # Export query results to Excel
    python query_from_seekdb.py mobiles --query-text "phone" --n-results 100 --output results.xlsx
    
    # List all collections
    python query_from_seekdb.py --list-collections
    
    # Show collection info
    python query_from_seekdb.py mobiles --info
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Optional

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv is optional, will use environment variables directly

try:
    import pyseekdb
except ImportError:
    print("Error: pyseekdb is required. Install with: pip install pyseekdb")
    sys.exit(1)

# pandas is optional, only required for export
pandas_available = False
try:
    import pandas as pd
    pandas_available = True
except ImportError:
    pass


# Initialize client based on environment
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


def get_collection(collection_name: str):
    """Get a collection from seekdb."""
    if not client.has_collection(collection_name):
        raise ValueError(
            f"Collection '{collection_name}' not found. Available collections: {client.list_collections()}")
    return client.get_collection(name=collection_name)


def get_by_filter(
    collection_name: str,
    where: Optional[dict] = None,
    where_document: Optional[dict] = None,
    include: Optional[list] = None
) -> dict:
    """
    Perform scalar/metadata filter search using collection.get().

    Args:
        collection_name: Name of the collection to query
        where: Metadata filter conditions
        where_document: Document filter conditions (fulltext search)
        include: List of fields to include in results

    Returns:
        Query results dictionary with ids, documents, metadatas
    """
    collection = get_collection(collection_name)

    get_params = {}

    if where:
        get_params["where"] = where
    if where_document:
        get_params["where_document"] = where_document
    if include:
        get_params["include"] = include
    else:
        get_params["include"] = ["documents", "metadatas"]

    # collection.get() returns flat structure, convert to nested for consistency
    result = collection.get(**get_params)

    # Convert flat structure to nested structure (same as query results)
    return {
        "ids": [result.get("ids", [])],
        "documents": [result.get("documents", [])] if result.get("documents") else None,
        "metadatas": [result.get("metadatas", [])] if result.get("metadatas") else None,
        "distances": None  # get() doesn't return distances
    }


def hybrid_search(
    collection_name: str,
    query_text: str,
    n_results: int = 5,
    where: Optional[dict] = None,
    include: Optional[list] = None
) -> dict:
    """
    Perform hybrid search combining fulltext and semantic similarity search.

    The query_text is used for BOTH:
    - Fulltext search: where_document.$contains
    - Semantic search: knn.query_texts

    Args:
        collection_name: Name of the collection to query
        query_text: Text for both fulltext and semantic search
        n_results: Number of results to return
        where: Metadata filter conditions
        include: List of fields to include in results

    Returns:
        Query results dictionary with ids, documents, metadatas, distances
    """
    collection = get_collection(collection_name)

    # Build query part (fulltext search)
    query = {"where_document": {"$contains": query_text}}
    if where:
        query["where"] = where

    # Build knn part (semantic search)
    knn: dict = {"query_texts": query_text}
    if where:
        knn["where"] = where

    # Rank fusion
    rank = {"rrf": {}}

    # Include fields
    include_fields = include if include else ["documents", "metadatas"]

    return collection.hybrid_search(
        query=query,
        knn=knn,
        rank=rank,
        n_results=n_results,
        include=include_fields
    )


def results_to_dataframe(results: dict) -> "pd.DataFrame":
    """
    Convert query results to pandas DataFrame.

    Args:
        results: Query results dictionary

    Returns:
        DataFrame with all data flattened
    """
    if not pandas_available:
        raise ImportError(
            "pandas is required for export. Install with: pip install pandas openpyxl")

    import pandas as pd  # Import here since we've confirmed it's available

    rows = []

    # Query results have nested lists
    if not results.get("ids") or not results["ids"][0]:
        return pd.DataFrame()

    ids = results["ids"][0]
    distances = results.get("distances", [[]])[0]
    documents = results.get("documents", [[]])[
        0] if results.get("documents") else []
    metadatas = results.get("metadatas", [[]])[
        0] if results.get("metadatas") else []

    for i, id_ in enumerate(ids):
        row = {"id": id_}

        if distances and i < len(distances):
            row["distance"] = distances[i]

        if documents and i < len(documents) and documents[i]:
            row["document"] = documents[i]

        if metadatas and i < len(metadatas) and metadatas[i]:
            for key, value in metadatas[i].items():
                row[key] = value

        rows.append(row)

    return pd.DataFrame(rows)


def export_to_file(df, output_path: str, sheet_name: str = "Data") -> str:
    """
    Export DataFrame to CSV or Excel file.

    Args:
        df: DataFrame to export
        output_path: Output file path (.csv or .xlsx)
        sheet_name: Sheet name for Excel export

    Returns:
        Absolute path to the exported file
    """
    if not pandas_available:
        raise ImportError(
            "pandas is required for export. Install with: pip install pandas openpyxl")

    path = Path(output_path)
    suffix = path.suffix.lower()

    # Create parent directories if they don't exist
    path.parent.mkdir(parents=True, exist_ok=True)

    if suffix == '.csv':
        df.to_csv(output_path, index=False, encoding='utf-8-sig')
    elif suffix in ['.xlsx', '.xls']:
        df.to_excel(output_path, index=False,
                    sheet_name=sheet_name, engine='openpyxl')
    else:
        raise ValueError(
            f"Unsupported file format: {suffix}. Use .csv or .xlsx")

    return str(path.absolute())


def print_results(results: dict):
    """Pretty print query results."""
    # Query results have nested lists
    if not results.get("ids") or not results["ids"][0]:
        print("No results found.")
        return

    ids = results["ids"][0]
    distances = results.get("distances", [[]])[0]
    documents = results.get("documents", [[]])[
        0] if results.get("documents") else []
    metadatas = results.get("metadatas", [[]])[
        0] if results.get("metadatas") else []

    print(f"\nFound {len(ids)} results:\n")
    print("=" * 80)

    for i, id_ in enumerate(ids):
        print(f"\n[Result {i + 1}]")
        print(f"  ID: {id_}")
        if distances and i < len(distances):
            print(f"  Distance: {distances[i]:.4f}")
        if documents and i < len(documents) and documents[i]:
            doc = documents[i]
            if len(doc) > 200:
                doc = doc[:200] + "..."
            print(f"  Document: {doc}")
        if metadatas and i < len(metadatas) and metadatas[i]:
            print(f"  Metadata:")
            for key, value in metadatas[i].items():
                val_str = str(value)
                if len(val_str) > 100:
                    val_str = val_str[:100] + "..."
                print(f"    - {key}: {val_str}")


def list_collections():
    """List all available collections.
    
    Returns:
        List of collection objects
    """
    collections = client.list_collections()
    if not collections:
        print("No collections found.")
        return []

    print("\nAvailable collections:")
    for col in collections:
        if hasattr(col, 'name'):
            print(f"  - {col.name}")
        else:
            print(f"  - {col}")
    
    return collections


def collection_info(collection_name: str) -> dict:
    """Get information about a collection.
    
    Args:
        collection_name: Name of the collection
        
    Returns:
        Dictionary with collection info: name, count, preview
    """
    collection = get_collection(collection_name)
    count = collection.count()

    print(f"\nCollection: {collection_name}")
    print(f"  Total records: {count}")

    info = {
        "name": collection_name,
        "count": count,
        "preview": None
    }

    # Preview some data
    if count > 0:
        preview = collection.peek(limit=3)
        info["preview"] = preview
        print(f"\nPreview (first 3 records):")
        for i in range(len(preview['ids'])):
            print(f"  ID: {preview['ids'][i][:20]}...")
            if preview.get('documents') and preview['documents'][i]:
                doc = preview['documents'][i][:50] + "..." if len(
                    preview['documents'][i]) > 50 else preview['documents'][i]
                print(f"    Document: {doc}")
            if preview.get('metadatas') and preview['metadatas'][i]:
                print(
                    f"    Metadata keys: {list(preview['metadatas'][i].keys())}")
    
    return info


def output_results(results: dict, output_path: Optional[str],
                   as_json: bool, sheet_name: str = "Data"):
    """
    Output results to terminal, JSON, or file.

    Args:
        results: Query results dictionary
        output_path: Optional file path for export (.csv or .xlsx)
        as_json: Output as JSON to terminal
        sheet_name: Sheet name for Excel export
    """
    if output_path:
        # Export to file
        df = results_to_dataframe(results)
        if df.empty:
            print("No results found to export.")
            return

        abs_path = export_to_file(df, output_path, sheet_name=sheet_name)
        print(f"Exported {len(df)} records to: {abs_path}")
    elif as_json:
        print(json.dumps(results, indent=2, default=str))
    else:
        print_results(results)


def main():
    parser = argparse.ArgumentParser(
        description="Query data from seekdb vector database and optionally export to CSV/Excel",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    # Positional argument (optional for --list-collections)
    parser.add_argument("collection_name", nargs="?",
                        help="Name of the collection to query")

    # Query modes
    parser.add_argument("--query-text", "-q",
                        help="Text query for semantic similarity search")
    parser.add_argument("--list-collections", "-l", action="store_true",
                        help="List all available collections")
    parser.add_argument("--info", action="store_true",
                        help="Show collection info and preview")

    # Common options
    parser.add_argument("--n-results", "-n", type=int, default=5,
                        help="Number of results to return (default: 5)")
    parser.add_argument("--where", "-w",
                        help="Metadata filter as JSON string, e.g., '{\"Brand\": {\"$eq\": \"SAMSUNG\"}}'")
    parser.add_argument("--include",
                        help="Comma-separated fields to include: documents,metadatas,embeddings")
    parser.add_argument("--json", "-j", action="store_true",
                        help="Output results as JSON")

    # Export options
    parser.add_argument("--output", "-o",
                        help="Export results to file (.csv or .xlsx)")
    parser.add_argument("--sheet-name", "-s", default="Data",
                        help="Sheet name for Excel export (default: Data)")

    args = parser.parse_args()

    # Handle list-collections (no collection_name required)
    if args.list_collections:
        list_collections()
        return

    # All other modes require collection_name (except --list-collections)
    if not args.collection_name:
        parser.error(
            "collection_name is required (except for --list-collections)")

    # Parse where filter
    where_filter = None
    if args.where:
        try:
            where_filter = json.loads(args.where)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in --where: {e}", file=sys.stderr)
            sys.exit(1)

    # Parse include list
    include_list = None
    if args.include:
        include_list = [f.strip() for f in args.include.split(",")]

    try:
        if args.info:
            collection_info(args.collection_name)
        elif args.query_text:
            # Hybrid search: fulltext + semantic (with optional scalar filter)
            # query_text is used for BOTH fulltext ($contains) and semantic (query_texts)
            results = hybrid_search(
                collection_name=args.collection_name,
                query_text=args.query_text,
                n_results=args.n_results,
                where=where_filter,
                include=include_list
            )
            output_results(results, args.output, args.json, args.sheet_name)
        elif where_filter:
            # Pure scalar search (no semantic search)
            results = get_by_filter(
                collection_name=args.collection_name,
                where=where_filter,
                include=include_list
            )
            output_results(results, args.output, args.json, args.sheet_name)
        else:
            # Default: show collection info
            collection_info(args.collection_name)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
