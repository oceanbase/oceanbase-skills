#!/usr/bin/env python3
"""
Generate seekdb-docs-catalog.jsonl from local documentation files.

Scans the seekdb-docs/ directory, sends each markdown file to an LLM
(OpenAI-compatible API) to generate a search-oriented description,
and outputs a JSONL catalog with branch info from _branch_map.tsv.

Usage:
    # Basic usage (requires OPENAI_API_KEY env var)
    python generate_catalog.py

    # Custom API endpoint and model
    python generate_catalog.py --base-url https://your-api.com/v1 --model gpt-4o-mini

    # Incremental update: only regenerate descriptions for new/changed files
    python generate_catalog.py --incremental

    # Dry run: show what would be processed without calling the API
    python generate_catalog.py --dry-run

    # Adjust concurrency and rate limiting
    python generate_catalog.py --concurrency 10 --max-chars 12000

Environment Variables:
    OPENAI_API_KEY      API key for the OpenAI-compatible service (required)
    OPENAI_BASE_URL     Base URL override (alternative to --base-url)
"""

import argparse
import asyncio
import hashlib
import json
import logging
import os
import sys
import time
from pathlib import Path

# ---------------------------------------------------------------------------
# Resolve paths relative to this script
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
DOCS_DIR = SKILL_DIR / "seekdb-docs"
REFERENCES_DIR = SKILL_DIR / "references"
CATALOG_FILE = REFERENCES_DIR / "seekdb-docs-catalog.jsonl"
BRANCH_MAP_FILE = REFERENCES_DIR / "_branch_map.tsv"
HASH_CACHE_FILE = REFERENCES_DIR / "_catalog_hash_cache.json"

# ---------------------------------------------------------------------------
# Prompt template
# ---------------------------------------------------------------------------
SYSTEM_PROMPT = """\
You are a technical documentation indexer. Your job is to write a concise, \
search-oriented description for a database documentation page.

Rules:
- Write exactly ONE sentence (two at most for complex topics).
- Start with "This document..." or a noun phrase describing the topic.
- Include key technical terms, feature names, and use cases so the description \
is useful for keyword and semantic search.
- Do NOT include the file path or document title in the description.
- Do NOT use marketing language or superlatives.
- Keep it under 300 characters when possible.
"""

USER_PROMPT_TEMPLATE = """\
Write a search-oriented description for the following seekdb documentation page.

File path: {path}

Content (may be truncated):
---
{content}
---

Description:"""

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("generate_catalog")

# Suppress noisy HTTP request logs from openai/httpx
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("openai").setLevel(logging.WARNING)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def file_md5(filepath: Path) -> str:
    """Return the MD5 hex digest of a file."""
    h = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def load_branch_map(path: Path) -> dict[str, str]:
    """Load _branch_map.tsv into a dict: relative_path -> branch."""
    mapping = {}
    if not path.exists():
        log.warning("Branch map not found: %s", path)
        return mapping
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split("\t")
            if len(parts) == 2:
                mapping[parts[0]] = parts[1]
    log.info("Loaded branch map: %d entries", len(mapping))
    return mapping


def load_hash_cache(path: Path) -> dict[str, str]:
    """Load the hash cache (path -> md5) from disk."""
    if not path.exists():
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def save_hash_cache(path: Path, cache: dict[str, str]) -> None:
    """Persist the hash cache to disk."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2)


def load_existing_catalog(path: Path) -> dict[str, dict]:
    """Load existing catalog as a dict keyed by path."""
    entries = {}
    if not path.exists():
        return entries
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
                entries[entry["path"]] = entry
            except (json.JSONDecodeError, KeyError):
                continue
    return entries


def collect_md_files(docs_dir: Path) -> list[Path]:
    """Collect all .md files under docs_dir, sorted by relative path."""
    files = sorted(docs_dir.rglob("*.md"))
    return files


def truncate_content(content: str, max_chars: int) -> str:
    """Truncate content to max_chars, keeping the beginning."""
    if len(content) <= max_chars:
        return content
    return content[:max_chars] + "\n\n[... content truncated ...]"


# ---------------------------------------------------------------------------
# LLM client (async, using openai SDK with semaphore for concurrency)
# ---------------------------------------------------------------------------
class LLMClient:
    """Async OpenAI-compatible chat completions client using the openai SDK."""

    def __init__(self, base_url: str, api_key: str, model: str, concurrency: int):
        self._base_url = base_url
        self._api_key = api_key
        self.model = model
        self.semaphore = asyncio.Semaphore(concurrency)
        self._client = None  # Lazy init — avoids importing openai in dry-run

    def _ensure_client(self):
        """Lazily create the AsyncOpenAI client on first real API call."""
        if self._client is None:
            try:
                from openai import AsyncOpenAI
            except ImportError:
                log.error("openai package is required. Install it with: pip install openai")
                sys.exit(1)
            self._client = AsyncOpenAI(
                api_key=self._api_key,
                base_url=self._base_url,
                timeout=60.0,
                max_retries=3,
            )

    async def generate_description(
        self, path: str, content: str, max_chars: int
    ) -> str:
        """Call the LLM to generate a description for a document."""
        truncated = truncate_content(content, max_chars)
        user_prompt = USER_PROMPT_TEMPLATE.format(path=path, content=truncated)

        async with self.semaphore:
            self._ensure_client()
            try:
                response = await self._client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": user_prompt},
                    ],
                    temperature=0.3,
                    max_tokens=256,
                )
                description = response.choices[0].message.content.strip()
                # Remove surrounding quotes if present
                if description.startswith('"') and description.endswith('"'):
                    description = description[1:-1]
                return description
            except Exception as e:
                log.error("Failed to generate description for %s: %s", path, e)
                return ""

    async def close(self):
        if self._client is not None:
            await self._client.close()


# ---------------------------------------------------------------------------
# Main logic
# ---------------------------------------------------------------------------
async def process_files(
    files: list[Path],
    docs_dir: Path,
    llm: LLMClient,
    max_chars: int,
    existing_catalog: dict[str, dict],
    hash_cache: dict[str, str],
    incremental: bool,
    dry_run: bool,
    branch_map: dict[str, str],
) -> list[dict]:
    """Process all files and return catalog entries."""
    entries = []
    tasks = []
    skipped = 0

    for filepath in files:
        rel_path = str(filepath.relative_to(docs_dir))
        current_hash = file_md5(filepath)

        # In incremental mode, skip files whose hash hasn't changed
        # and whose description already exists
        if incremental and rel_path in hash_cache and rel_path in existing_catalog:
            if hash_cache[rel_path] == current_hash:
                # Reuse existing entry, update branch if needed
                entry = existing_catalog[rel_path].copy()
                if rel_path in branch_map:
                    entry["branch"] = branch_map[rel_path]
                entries.append(entry)
                skipped += 1
                continue

        if dry_run:
            log.info("[DRY RUN] Would process: %s", rel_path)
            entries.append({
                "path": rel_path,
                "description": "(dry run - not generated)",
                **({"branch": branch_map[rel_path]} if rel_path in branch_map else {}),
            })
            continue

        # Read content
        content = filepath.read_text(encoding="utf-8", errors="replace")

        # Schedule async task
        tasks.append((rel_path, current_hash, content))

    if incremental and skipped > 0:
        log.info("Incremental mode: skipped %d unchanged files", skipped)

    if dry_run:
        log.info("[DRY RUN] Would process %d files total", len(files) - skipped)
        return entries

    # Process files concurrently with progress reporting
    if tasks:
        total = len(tasks)
        log.info("Generating descriptions for %d files...", total)

        completed = 0
        progress_lock = asyncio.Lock()

        async def _process_one(rel_path: str, current_hash: str, content: str):
            nonlocal completed
            description = await llm.generate_description(
                rel_path, content, max_chars
            )
            entry = {"path": rel_path, "description": description}
            if rel_path in branch_map:
                entry["branch"] = branch_map[rel_path]

            async with progress_lock:
                completed += 1
                if completed % 10 == 0 or completed == total:
                    log.info("Progress: %d/%d (%.0f%%)", completed, total, completed / total * 100)

            return rel_path, current_hash, entry

        results = await asyncio.gather(
            *[_process_one(rp, h, c) for rp, h, c in tasks]
        )

        new_hash_cache = dict(hash_cache)
        for rel_path, current_hash, entry in results:
            entries.append(entry)
            new_hash_cache[rel_path] = current_hash

        # Update hash cache
        hash_cache.update(new_hash_cache)

    # Sort entries by path for stable output
    entries.sort(key=lambda e: e["path"])
    return entries


def write_catalog(entries: list[dict], output_path: Path) -> None:
    """Write catalog entries to JSONL file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        for entry in entries:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    log.info("Wrote %d entries to %s", len(entries), output_path)


async def main():
    parser = argparse.ArgumentParser(
        description="Generate seekdb-docs-catalog.jsonl from documentation files using LLM"
    )
    parser.add_argument(
        "--base-url",
        default=os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1"),
        help="OpenAI-compatible API base URL (default: $OPENAI_BASE_URL or https://api.openai.com/v1)",
    )
    parser.add_argument(
        "--api-key",
        default=os.environ.get("OPENAI_API_KEY", ""),
        help="API key (default: $OPENAI_API_KEY)",
    )
    parser.add_argument(
        "--model",
        default=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
        help="Model name (default: $OPENAI_MODEL or gpt-4o-mini)",
    )
    parser.add_argument(
        "--docs-dir",
        type=Path,
        default=DOCS_DIR,
        help=f"Path to documentation directory (default: {DOCS_DIR})",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=CATALOG_FILE,
        help=f"Output JSONL path (default: {CATALOG_FILE})",
    )
    parser.add_argument(
        "--branch-map",
        type=Path,
        default=BRANCH_MAP_FILE,
        help=f"Branch map TSV path (default: {BRANCH_MAP_FILE})",
    )
    parser.add_argument(
        "--concurrency",
        type=int,
        default=5,
        help="Max concurrent API requests (default: 5)",
    )
    parser.add_argument(
        "--max-chars",
        type=int,
        default=8000,
        help="Max characters of document content sent to LLM (default: 8000)",
    )
    parser.add_argument(
        "--incremental",
        action="store_true",
        help="Only regenerate descriptions for new or changed files",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be processed without calling the API",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable debug logging",
    )
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Validate
    if not args.docs_dir.exists():
        log.error("Docs directory not found: %s", args.docs_dir)
        log.error("Run scripts/update_docs.sh first to download documentation.")
        sys.exit(1)

    if not args.api_key and not args.dry_run:
        log.error("API key required. Set OPENAI_API_KEY or use --api-key.")
        sys.exit(1)

    # Collect files
    md_files = collect_md_files(args.docs_dir)
    if not md_files:
        log.error("No .md files found in %s", args.docs_dir)
        sys.exit(1)
    log.info("Found %d markdown files in %s", len(md_files), args.docs_dir)

    # Load auxiliary data
    branch_map = load_branch_map(args.branch_map)
    existing_catalog = load_existing_catalog(args.output)
    hash_cache = load_hash_cache(HASH_CACHE_FILE)

    if existing_catalog:
        log.info("Loaded existing catalog: %d entries", len(existing_catalog))

    # Create LLM client
    llm = LLMClient(
        base_url=args.base_url,
        api_key=args.api_key,
        model=args.model,
        concurrency=args.concurrency,
    )

    start_time = time.time()

    try:
        entries = await process_files(
            files=md_files,
            docs_dir=args.docs_dir,
            llm=llm,
            max_chars=args.max_chars,
            existing_catalog=existing_catalog,
            hash_cache=hash_cache,
            incremental=args.incremental,
            dry_run=args.dry_run,
            branch_map=branch_map,
        )
    finally:
        await llm.close()

    elapsed = time.time() - start_time

    if not args.dry_run:
        # Write catalog
        write_catalog(entries, args.output)

        # Save hash cache for incremental mode
        save_hash_cache(HASH_CACHE_FILE, hash_cache)

        # Summary
        branch_counts = {}
        for e in entries:
            b = e.get("branch", "unknown")
            branch_counts[b] = branch_counts.get(b, 0) + 1

        print()
        print("=" * 50)
        print("Catalog generation complete!")
        print(f"  Entries:    {len(entries)}")
        print(f"  Output:     {args.output}")
        print(f"  Time:       {elapsed:.1f}s")
        print(f"  Model:      {args.model}")
        for branch, count in sorted(branch_counts.items()):
            print(f"  [{branch}]: {count} files")
        print("=" * 50)
    else:
        print(f"\n[DRY RUN] Would generate {len(entries)} entries in {args.output}")


if __name__ == "__main__":
    asyncio.run(main())
