#!/usr/bin/env bash
set -euo pipefail

# ============================================================
# publish-skills.sh
# Validate and push skills to GitHub for skills.sh indexing.
#
# skills.sh auto-indexes public GitHub repos — no manual
# submission needed. This script validates the repo structure,
# pushes to GitHub, and verifies the skill is discoverable.
#
# Usage:
#   ./scripts/publish-skills.sh              # push current branch
#   ./scripts/publish-skills.sh --branch main  # push to specific branch
# ============================================================

REPO_ROOT="$(git rev-parse --show-toplevel)"
GITHUB_REMOTE="github"
GITHUB_REPO="oceanbase/oceanbase-skills"
BRANCH="${1:-}"

if [[ "$BRANCH" == "--branch" ]]; then
  BRANCH="${2:?Usage: $0 --branch <branch-name>}"
elif [[ -z "$BRANCH" ]]; then
  BRANCH="$(git rev-parse --abbrev-ref HEAD)"
fi

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

pass() { echo -e "${GREEN}[PASS]${NC} $1"; }
fail() { echo -e "${RED}[FAIL]${NC} $1"; ERRORS=$((ERRORS + 1)); }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }

ERRORS=0

echo "========================================="
echo " OceanBase Skills — Publish Validation"
echo "========================================="
echo ""

# --- Step 1: Validate directory structure ---
echo "Step 1: Validating directory structure..."

SKILLS_DIR="${REPO_ROOT}/skills"
if [[ ! -d "$SKILLS_DIR" ]]; then
  fail "skills/ directory not found"
else
  pass "skills/ directory exists"
fi

SKILL_DIRS=()
for dir in "$SKILLS_DIR"/*/; do
  [[ -d "$dir" ]] && SKILL_DIRS+=("$dir")
done

if [[ ${#SKILL_DIRS[@]} -eq 0 ]]; then
  fail "No skill subdirectories found in skills/"
else
  pass "Found ${#SKILL_DIRS[@]} skill(s)"
fi

# --- Step 2: Validate each skill ---
echo ""
echo "Step 2: Validating skills..."

for dir in "${SKILL_DIRS[@]}"; do
  skill_name="$(basename "$dir")"
  skill_md="${dir}SKILL.md"

  if [[ ! -f "$skill_md" ]]; then
    fail "${skill_name}: SKILL.md not found"
    continue
  fi

  # Check frontmatter has name and description
  has_name=$(head -20 "$skill_md" | grep -c "^name:" || true)
  has_desc=$(head -20 "$skill_md" | grep -c "^description:" || true)

  if [[ "$has_name" -eq 0 ]]; then
    fail "${skill_name}: SKILL.md missing 'name' in frontmatter"
  else
    pass "${skill_name}: SKILL.md has name"
  fi

  if [[ "$has_desc" -eq 0 ]]; then
    fail "${skill_name}: SKILL.md missing 'description' in frontmatter"
  else
    pass "${skill_name}: SKILL.md has description"
  fi

  # Check sub-skills
  for sub_skill_md in "${dir}"*/SKILL.md; do
    [[ -f "$sub_skill_md" ]] || continue
    sub_name="$(basename "$(dirname "$sub_skill_md")")"
    pass "${skill_name}/${sub_name}: SKILL.md exists"
  done
done

# --- Step 3: Validate package.json ---
echo ""
echo "Step 3: Validating package.json..."

root_pkg="${REPO_ROOT}/package.json"
if [[ ! -f "$root_pkg" ]]; then
  fail "Root package.json not found"
else
  main_field=$(python3 -c "import json; print(json.load(open('$root_pkg')).get('main',''))" 2>/dev/null || echo "")
  if [[ "$main_field" == skills/* ]]; then
    pass "package.json main points to skills/"
  else
    warn "package.json main='${main_field}' — expected skills/..."
  fi
fi

# --- Step 4: Check for uncommitted changes ---
echo ""
echo "Step 4: Checking git status..."

if [[ -n "$(git -C "$REPO_ROOT" status --porcelain)" ]]; then
  warn "Uncommitted changes detected — commit before publishing"
  git -C "$REPO_ROOT" status --short
else
  pass "Working tree is clean"
fi

# --- Step 5: Abort if errors ---
echo ""
if [[ $ERRORS -gt 0 ]]; then
  echo -e "${RED}Validation failed with $ERRORS error(s). Fix before publishing.${NC}"
  exit 1
fi

echo -e "${GREEN}All validations passed.${NC}"
echo ""

# --- Step 6: Check GitHub remote ---
echo "Step 5: Checking GitHub remote..."

if ! git -C "$REPO_ROOT" remote get-url "$GITHUB_REMOTE" &>/dev/null; then
  fail "Git remote '${GITHUB_REMOTE}' not found"
  echo ""
  echo "Add it with:"
  echo "  git remote add ${GITHUB_REMOTE} git@github.com:${GITHUB_REPO}.git"
  exit 1
fi
pass "Remote '${GITHUB_REMOTE}' configured"

# --- Step 7: Push to GitHub ---
echo ""
echo "Step 6: Pushing branch '${BRANCH}' to GitHub (${GITHUB_REMOTE})..."

git -C "$REPO_ROOT" push "${GITHUB_REMOTE}" "${BRANCH}" -u

echo ""
pass "Pushed to GitHub successfully"

# --- Step 8: Verify on skills.sh ---
echo ""
echo "========================================="
echo " Post-publish verification"
echo "========================================="
echo ""
echo "skills.sh indexes GitHub repos automatically."
echo "It may take a few minutes for changes to appear."
echo ""
echo "Check your skills at:"
echo "  https://www.skills.sh/${GITHUB_REPO}"
echo ""
echo "Install commands:"
for dir in "${SKILL_DIRS[@]}"; do
  skill_name="$(basename "$dir")"
  echo "  npx skills add ${GITHUB_REPO}/${skill_name}"
done
echo ""
echo "Search:"
for dir in "${SKILL_DIRS[@]}"; do
  skill_name="$(basename "$dir")"
  echo "  https://www.skills.sh/?q=${skill_name}"
done
echo ""
echo "Done."
