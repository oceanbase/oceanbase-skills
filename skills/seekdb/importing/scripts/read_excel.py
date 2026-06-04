#!/usr/bin/env python3
"""
Read and preview Excel files with detailed information.

Usage:
    python read_excel.py <file_path> [options]

Examples:
    # Show basic file info and preview first 5 rows
    python read_excel.py data.xlsx
    
    # Preview specific sheet
    python read_excel.py data.xlsx --sheet "Sheet2"
    
    # Show more rows
    python read_excel.py data.xlsx --rows 20
    
    # List all sheets only
    python read_excel.py data.xlsx --list-sheets
    
    # Export to CSV
    python read_excel.py data.xlsx --to-csv output.csv
    
    # Show column statistics
    python read_excel.py data.xlsx --stats

This script is designed for use in Claude Code (non-interactive environment).
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

try:
    import pandas as pd
except ImportError:
    print("Error: pandas is required. Install with: pip install pandas openpyxl")
    sys.exit(1)

try:
    import openpyxl
except ImportError:
    print("Warning: openpyxl is recommended for .xlsx files. Install with: pip install openpyxl")


def list_sheets(file_path: str) -> list[str]:
    """List all sheet names in an Excel file."""
    path = Path(file_path)
    
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    suffix = path.suffix.lower()
    if suffix not in ['.xlsx', '.xls']:
        raise ValueError(f"Not an Excel file: {suffix}. Use .xlsx or .xls")
    
    xl = pd.ExcelFile(file_path)
    return xl.sheet_names


def read_excel(
    file_path: str,
    sheet_name: Optional[str] = None,
    nrows: Optional[int] = None
) -> pd.DataFrame:
    """
    Read an Excel file into a DataFrame.
    
    Args:
        file_path: Path to Excel file
        sheet_name: Name of sheet to read (default: first sheet)
        nrows: Number of rows to read (default: all)
    
    Returns:
        DataFrame with Excel data
    """
    path = Path(file_path)
    
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    suffix = path.suffix.lower()
    if suffix not in ['.xlsx', '.xls']:
        raise ValueError(f"Not an Excel file: {suffix}. Use .xlsx or .xls")
    
    # Read the Excel file
    if sheet_name:
        df = pd.read_excel(file_path, sheet_name=sheet_name, nrows=nrows)
    else:
        df = pd.read_excel(file_path, nrows=nrows)
    
    return df


def print_file_info(file_path: str):
    """Print basic file information."""
    path = Path(file_path)
    file_size = path.stat().st_size
    
    # Human readable file size
    if file_size < 1024:
        size_str = f"{file_size} B"
    elif file_size < 1024 * 1024:
        size_str = f"{file_size / 1024:.1f} KB"
    else:
        size_str = f"{file_size / (1024 * 1024):.1f} MB"
    
    print(f"\n{'='*60}")
    print(f"File: {path.name}")
    print(f"Path: {path.absolute()}")
    print(f"Size: {size_str}")
    print(f"{'='*60}")


def print_sheet_info(file_path: str):
    """Print information about all sheets in the file."""
    sheets = list_sheets(file_path)
    print(f"\nSheets ({len(sheets)} total):")
    
    xl = pd.ExcelFile(file_path)
    for i, sheet in enumerate(sheets, 1):
        df = xl.parse(sheet)
        print(f"  {i}. {sheet} - {len(df)} rows x {len(df.columns)} columns")


def print_data_preview(df: pd.DataFrame, max_rows: int = 5):
    """Print a preview of the DataFrame."""
    print(f"\nData Preview (showing {min(len(df), max_rows)} of {len(df)} rows):")
    print("-" * 60)
    
    # Set pandas display options for better output
    with pd.option_context(
        'display.max_columns', None,
        'display.width', None,
        'display.max_colwidth', 50
    ):
        print(df.head(max_rows).to_string(index=True))


def print_column_info(df: pd.DataFrame):
    """Print column information."""
    print(f"\nColumns ({len(df.columns)} total):")
    print("-" * 60)
    
    for col in df.columns:
        dtype = df[col].dtype
        non_null = df[col].notna().sum()
        null = df[col].isna().sum()
        print(f"  - {col}")
        print(f"      Type: {dtype}, Non-null: {non_null}, Null: {null}")


def print_statistics(df: pd.DataFrame):
    """Print statistical summary for numeric columns."""
    numeric_cols = df.select_dtypes(include=['number']).columns
    
    if len(numeric_cols) == 0:
        print("\nNo numeric columns found for statistics.")
        return
    
    print(f"\nStatistics (numeric columns only):")
    print("-" * 60)
    
    with pd.option_context(
        'display.max_columns', None,
        'display.width', None,
        'display.float_format', '{:.2f}'.format
    ):
        print(df[numeric_cols].describe().to_string())


def export_to_csv(df: pd.DataFrame, output_path: str):
    """Export DataFrame to CSV file."""
    df.to_csv(output_path, index=False)
    print(f"\nExported to CSV: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Read and preview Excel files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument("file_path", help="Path to Excel file (.xlsx or .xls)")
    parser.add_argument("--sheet", "-s",
                        help="Sheet name to read (default: first sheet)")
    parser.add_argument("--rows", "-r", type=int, default=5,
                        help="Number of rows to preview (default: 5)")
    parser.add_argument("--list-sheets", "-l", action="store_true",
                        help="List all sheets and exit")
    parser.add_argument("--columns", "-c", action="store_true",
                        help="Show detailed column information")
    parser.add_argument("--stats", action="store_true",
                        help="Show statistics for numeric columns")
    parser.add_argument("--to-csv", metavar="OUTPUT",
                        help="Export sheet to CSV file")
    parser.add_argument("--all-rows", "-a", action="store_true",
                        help="Read and display all rows (use with caution for large files)")
    
    args = parser.parse_args()
    
    try:
        # Print file info
        print_file_info(args.file_path)
        
        # List sheets
        if args.list_sheets:
            print_sheet_info(args.file_path)
            return
        
        # Print sheet info
        print_sheet_info(args.file_path)
        
        # Read the data
        if args.sheet:
            print(f"\nReading sheet: {args.sheet}")
        else:
            sheets = list_sheets(args.file_path)
            print(f"\nReading sheet: {sheets[0]} (first sheet)")
        
        # Read all rows or limited rows based on options
        nrows = None if args.all_rows or args.to_csv else None
        df = read_excel(args.file_path, sheet_name=args.sheet, nrows=nrows)
        
        print(f"Total: {len(df)} rows x {len(df.columns)} columns")
        
        # Show column info if requested
        if args.columns:
            print_column_info(df)
        
        # Print preview
        preview_rows = len(df) if args.all_rows else args.rows
        print_data_preview(df, max_rows=preview_rows)
        
        # Show statistics if requested
        if args.stats:
            print_statistics(df)
        
        # Export to CSV if requested
        if args.to_csv:
            export_to_csv(df, args.to_csv)
        
        print()
        
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
