#!/bin/bash
# Update seekdb-docs from GitHub repository (multi-version merge)
# This script downloads documentation from multiple version branches,
# merges them (newer versions override older), and tracks which branch
# each file comes from for correct remote fallback URLs.

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# agent-skills/ (pyproject.toml) — used so `uv run python` resolves the project env
AGENT_SKILLS_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
TARGET_DIR="$SKILL_DIR/seekdb-docs"
REFERENCES_DIR="$SKILL_DIR/references"
CATALOG_FILE="$REFERENCES_DIR/seekdb-docs-catalog.jsonl"
BRANCH_MAP_FILE="$REFERENCES_DIR/_branch_map.tsv"

# Version branches to merge, ordered from oldest to newest.
# Newer versions override older ones for files that exist in both.
# Files unique to older branches (e.g. showInAllVersions) are preserved.
VERSIONS=("V1.0.0" "V1.1.0")

REPO_URL="https://github.com/oceanbase/seekdb-doc.git"
TEMP_DIR="/tmp/seekdb-doc-update"

echo -e "${GREEN}=== seekdb-docs Multi-Version Update Script ===${NC}"
echo "Versions to merge (in order): ${VERSIONS[*]}"
echo ""

# Step 1: Prepare directories
echo -e "${YELLOW}[1/5] Preparing directories...${NC}"
rm -rf "$TEMP_DIR"
mkdir -p "$TEMP_DIR"
rm -rf "$TARGET_DIR"
mkdir -p "$TARGET_DIR"

# Temporary raw branch map (may have duplicates)
RAW_MAP="$TEMP_DIR/_raw_branch_map.tsv"
> "$RAW_MAP"

# Step 2: Clone and merge each version (oldest first)
echo -e "${YELLOW}[2/5] Cloning and merging version branches...${NC}"
for VERSION in "${VERSIONS[@]}"; do
    echo "  Processing $VERSION..."
    CLONE_DIR="$TEMP_DIR/$VERSION"

    git clone --depth 1 --branch "$VERSION" --single-branch "$REPO_URL" "$CLONE_DIR" 2>/dev/null || {
        echo -e "${RED}  Error: Failed to clone branch $VERSION${NC}"
        echo "  Please check your internet connection and try again."
        continue
    }

    if [ ! -d "$CLONE_DIR/en-US" ]; then
        echo -e "${RED}  Warning: No en-US directory in $VERSION, skipping${NC}"
        continue
    fi

    # Copy files into merged directory (newer version overwrites older)
    cp -r "$CLONE_DIR/en-US/"* "$TARGET_DIR/"

    # Record branch mapping for every .md file in this version
    (cd "$CLONE_DIR/en-US" && find . -name "*.md" -type f | sed 's|^\./||') | while read -r filepath; do
        printf '%s\t%s\n' "$filepath" "$VERSION" >> "$RAW_MAP"
    done

    echo -e "  ${GREEN}✓${NC} $VERSION merged"
done

# Step 3: Deduplicate branch map — keep the latest version for each path
echo -e "${YELLOW}[3/5] Resolving file-to-branch mapping...${NC}"
mkdir -p "$REFERENCES_DIR"
# tac reverses lines so awk '!seen[...]++' keeps the LAST (newest) version per path
tac "$RAW_MAP" | awk -F'\t' '!seen[$1]++' | sort > "$BRANCH_MAP_FILE"

MAPPED_COUNT=$(wc -l < "$BRANCH_MAP_FILE")
echo "  Mapped $MAPPED_COUNT files to their source branches"

# Step 4: Enrich catalog with branch info
echo -e "${YELLOW}[4/5] Updating catalog with branch info...${NC}"
if [ -f "$CATALOG_FILE" ]; then
    export BRANCH_MAP_FILE CATALOG_FILE
    uv run --project "$AGENT_SKILLS_ROOT" python << 'PYEOF'
import json, os

branch_map_file = os.environ["BRANCH_MAP_FILE"]
catalog_file = os.environ["CATALOG_FILE"]

# Load branch map: path -> branch
branch_map = {}
with open(branch_map_file, "r") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        parts = line.split("\t")
        if len(parts) == 2:
            branch_map[parts[0]] = parts[1]

# Read and update catalog entries
updated = 0
entries = []
with open(catalog_file, "r") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        entry = json.loads(line)
        path = entry.get("path", "")
        if path in branch_map:
            entry["branch"] = branch_map[path]
            updated += 1
        entries.append(entry)

# Write back
with open(catalog_file, "w") as f:
    for entry in entries:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

print(f"  Updated {updated}/{len(entries)} catalog entries with branch info")
PYEOF
else
    echo "  No catalog file found at $CATALOG_FILE, skipping catalog update"
    echo "  You can generate a catalog later and re-run this script to add branch info"
fi

# Step 5: Update version info in SKILL.md
echo -e "${YELLOW}[5/6] Updating version info in SKILL.md...${NC}"
SKILL_FILE="$SKILL_DIR/SKILL.md"
if [ -f "$SKILL_FILE" ]; then
    export SKILL_FILE
    export VERSIONS_STR="${VERSIONS[*]}"
    uv run --project "$AGENT_SKILLS_ROOT" python << 'PYEOF'
import os, re

skill_file = os.environ["SKILL_FILE"]
versions_str = os.environ["VERSIONS_STR"]
versions = versions_str.split()
all_versions = ", ".join(versions)
latest = versions[-1]

with open(skill_file, "r", encoding="utf-8") as f:
    content = f.read()

# Replace the block between AUTO-UPDATED markers
new_block = (
    "<!-- AUTO-UPDATED by update_docs.sh — do not edit manually -->\n"
    f"- **Documentation versions covered**: {all_versions} (merged, latest takes priority)\n"
    f"- **Latest version**: {latest}\n"
    "<!-- END AUTO-UPDATED -->"
)
pattern = r"<!-- AUTO-UPDATED by update_docs\.sh.*?-->.*?<!-- END AUTO-UPDATED -->"
updated = re.sub(pattern, new_block, content, flags=re.DOTALL)

with open(skill_file, "w", encoding="utf-8") as f:
    f.write(updated)

print(f"  Updated SKILL.md: versions={all_versions}, latest={latest}")
PYEOF
else
    echo "  SKILL.md not found, skipping version info update"
fi

# Step 6: Stats & cleanup
echo -e "${YELLOW}[6/6] Cleaning up...${NC}"
FILE_COUNT=$(find "$TARGET_DIR" -type f -name "*.md" | wc -l)
DIR_SIZE=$(du -sh "$TARGET_DIR" | cut -f1)
BRANCH_COUNT=$(awk -F'\t' '{print $2}' "$BRANCH_MAP_FILE" | sort -u | wc -l)

rm -rf "$TEMP_DIR"

echo ""
echo -e "${GREEN}Update complete!${NC}"
echo ""
echo "Summary:"
echo "  - Location:        $TARGET_DIR"
echo "  - Versions merged: ${VERSIONS[*]}"
echo "  - Source branches: $BRANCH_COUNT"
echo "  - Files:           $FILE_COUNT markdown files"
echo "  - Size:            $DIR_SIZE"
echo "  - Branch map:      $BRANCH_MAP_FILE"
echo ""
echo -e "${GREEN}✓ Documentation updated successfully${NC}"
echo ""
echo "Next step: regenerate the catalog with LLM-generated descriptions:"
echo "  cd \"$AGENT_SKILLS_ROOT\" && uv run python \"$SCRIPT_DIR/generate_catalog.py\" --incremental"
echo ""
echo "Or full regeneration (ignore cache):"
echo "  cd \"$AGENT_SKILLS_ROOT\" && uv run python \"$SCRIPT_DIR/generate_catalog.py\""
