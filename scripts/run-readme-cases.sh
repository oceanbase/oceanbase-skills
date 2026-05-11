#!/usr/bin/env bash
# Map root README.md "Example prompts" to obd checks on a machine where obd is installed.
#
# Default: non-destructive (list/display only). Skips cases that need YAML, interact, or new clusters.
#
# Usage on your test machine:
#   bash scripts/run-readme-cases.sh
#
# Remote (e.g. root@your-test-host):
#   README_TEST_SSH=root@your-test-host bash scripts/run-readme-cases.sh
#
# Optional env:
#   OBD_DEPLOY_NAME=         # empty or "auto" = first name from `obd cluster list` (else test-cluster)
#   SEEKDB_DEPLOY=           # empty or "auto" = first from `obd seekdb list`
#   OBD_CONFIG=config.yaml
#   MYSQL_TENANT=mysql
#   SYSBENCH_SCRIPT=oltp_read_write.lua
#   README_TEST_SSH=user@host
#   README_AUTO_DEMO=1       # if no cluster registered, run `obd demo -c oceanbase-ce` first
#   RUN_DEMO=1               # always run obd demo (even if clusters exist; use with care)
#   RUN_DEPLOY=1
#   RUN_SYSBENCH=1           # only runs if tenant exists on deploy
#   README_TRY_TENANT=1      # try `obd cluster tenant create` before sysbench (may fail on small demo)

set -u

# When piped to `ssh ... bash -s`, BASH_SOURCE may be unset.
REPO_ROOT="."
if [[ -n "${BASH_SOURCE[0]:-}" ]]; then
  REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)" || REPO_ROOT="."
fi

pass() { echo "[PASS] $*"; }
skip() { echo "[SKIP] $*"; }
fail() { echo "[FAIL] $*"; }

# First data row of obd table: | name | ...
obd_first_table_name() {
  local out
  out=$(obd cluster list 2>/dev/null || true)
  if echo "$out" | grep -qi "empty"; then
    echo ""
    return 0
  fi
  echo "$out" | grep -E '^\|[[:space:]]+[a-zA-Z0-9_.-]+[[:space:]]+\|' | grep -v Name | grep -v '^|[[:space:]]*-' | head -1 | awk -F'|' '{gsub(/^[ \t]+|[ \t]+$/,"",$2); print $2}'
}

seekdb_first_name() {
  local out
  out=$(obd seekdb list 2>/dev/null || true)
  if echo "$out" | grep -qi "No deploy"; then
    echo ""
    return 0
  fi
  echo "$out" | grep -E '^\|[[:space:]]+[a-zA-Z0-9_.-]+[[:space:]]+\|' | grep -v Name | grep -v '^|[[:space:]]*-' | head -1 | awk -F'|' '{gsub(/^[ \t]+|[ \t]+$/,"",$2); print $2}'
}

tenant_exists() {
  local deploy="$1" tenant="$2"
  obd cluster tenant show "$deploy" 2>/dev/null | grep -E "^\|[[:space:]]*${tenant}[[:space:]]*\|" -q
}

resolve_deploy_name() {
  local explicit="${OBD_DEPLOY_NAME:-}"
  if [[ -z "$explicit" || "$explicit" == "auto" ]]; then
    local d
    d=$(obd_first_table_name)
    if [[ -n "$d" ]]; then
      echo "$d"
    else
      echo "test-cluster"
    fi
  else
    echo "$explicit"
  fi
}

resolve_seekdb_name() {
  local explicit="${SEEKDB_DEPLOY:-}"
  if [[ -z "$explicit" || "$explicit" == "auto" ]]; then
    seekdb_first_name
  else
    echo "$explicit"
  fi
}

run_remote() {
  if [[ -n "${README_TEST_SSH:-}" ]]; then
    ssh -o BatchMode=yes -o StrictHostKeyChecking=accept-new "${README_TEST_SSH}" "bash -s" <"$0"
    exit $?
  fi
}

run_remote

if ! command -v obd >/dev/null 2>&1; then
  echo "obd not found in PATH. Run this script on the test machine where OceanBase Deployer is installed."
  exit 1
fi

OBD_CONFIG="${OBD_CONFIG:-config.yaml}"
MYSQL_TENANT="${MYSQL_TENANT:-mysql}"
SYSBENCH_SCRIPT="${SYSBENCH_SCRIPT:-oltp_read_write.lua}"

obd --version || true
echo "---"

# Optional: bootstrap demo when list is empty
if [[ "${README_AUTO_DEMO:-}" == "1" ]]; then
  if [[ -z "$(obd_first_table_name)" ]]; then
    echo "=== README_AUTO_DEMO: no cluster, running obd demo ==="
    obd env set IO_DEFAULT_CONFIRM 1 >/dev/null 2>&1 || true
    if obd demo -c oceanbase-ce; then pass "obd demo (auto)"; else fail "obd demo (auto)"; fi
  else
    skip "README_AUTO_DEMO: cluster already present"
  fi
fi

# README: obd demo
if [[ "${RUN_DEMO:-}" == "1" ]]; then
  echo "=== Case: obd demo (README quick local / demo prompts) ==="
  obd env set IO_DEFAULT_CONFIRM 1 >/dev/null 2>&1 || true
  if obd demo -c oceanbase-ce; then pass "obd demo"; else fail "obd demo"; fi
else
  skip "obd demo — set RUN_DEMO=1 to run (creates/changes demo environment)"
fi

# README: config deploy
if [[ "${RUN_DEPLOY:-}" == "1" ]]; then
  echo "=== Case: obd cluster deploy (README config deploy) ==="
  OBD_DEPLOY_NAME_RESOLVED=$(resolve_deploy_name)
  if [[ ! -f "${OBD_CONFIG}" ]]; then
    fail "RUN_DEPLOY=1 but OBD_CONFIG not found: ${OBD_CONFIG}"
  else
    if obd cluster deploy "${OBD_DEPLOY_NAME_RESOLVED}" -c "${OBD_CONFIG}"; then
      pass "obd cluster deploy ${OBD_DEPLOY_NAME_RESOLVED}"
    else
      fail "obd cluster deploy ${OBD_DEPLOY_NAME_RESOLVED}"
    fi
  fi
else
  skip "cluster deploy from config — set RUN_DEPLOY=1 and OBD_CONFIG"
fi

# OCP sanity: cluster list should succeed when obd works
echo "=== Case: OCP prompts (README) — sanity ==="
if obd cluster list >/dev/null 2>&1; then
  pass "obd cluster list"
else
  fail "obd cluster list"
fi

# SeekDB
echo "=== Case: SeekDB prompts (README) ==="
seekdb_out=$(obd seekdb list 2>&1) || true
if echo "$seekdb_out" | grep -qi "No deploy with component"; then
  pass "obd seekdb list (no seekdb deploy on host — expected for many OB-only machines)"
elif obd seekdb list >/dev/null 2>&1; then
  pass "obd seekdb list"
  SEEKDB_DEPLOY_RESOLVED=$(resolve_seekdb_name)
  if [[ -n "${SEEKDB_DEPLOY_RESOLVED}" ]]; then
    if obd seekdb display "${SEEKDB_DEPLOY_RESOLVED}" -g; then
      pass "obd seekdb display ${SEEKDB_DEPLOY_RESOLVED} -g"
    else
      fail "obd seekdb display ${SEEKDB_DEPLOY_RESOLVED} -g"
    fi
  else
    skip "no SeekDB deploy name in list — install/primary/standby is interactive; see SKILL.md"
  fi
else
  skip "obd seekdb list unexpected output"
fi

# Start + display (README uses test-cluster; auto uses e.g. demo)
OBD_DEPLOY_NAME_RESOLVED=$(resolve_deploy_name)
echo "=== Case: start + display (resolved deploy: ${OBD_DEPLOY_NAME_RESOLVED}) ==="
if obd cluster list 2>/dev/null | grep -qE "\|[[:space:]]*${OBD_DEPLOY_NAME_RESOLVED}[[:space:]]*\|"; then
  if obd cluster start "${OBD_DEPLOY_NAME_RESOLVED}"; then
    pass "obd cluster start ${OBD_DEPLOY_NAME_RESOLVED}"
  else
    fail "obd cluster start ${OBD_DEPLOY_NAME_RESOLVED}"
  fi
  if obd cluster display "${OBD_DEPLOY_NAME_RESOLVED}"; then
    pass "obd cluster display ${OBD_DEPLOY_NAME_RESOLVED}"
  else
    fail "obd cluster display ${OBD_DEPLOY_NAME_RESOLVED}"
  fi
else
  skip "deploy ${OBD_DEPLOY_NAME_RESOLVED} not registered — set README_AUTO_DEMO=1 or RUN_DEMO=1, or OBD_DEPLOY_NAME"
fi

# Sysbench
if [[ "${RUN_SYSBENCH:-}" == "1" ]]; then
  echo "=== Case: obd test sysbench (README) ==="
  obd env set IO_DEFAULT_CONFIRM 1 >/dev/null 2>&1 || true
  OBD_DEPLOY_NAME_RESOLVED=$(resolve_deploy_name)
  if ! obd cluster list 2>/dev/null | grep -qE "\|[[:space:]]*${OBD_DEPLOY_NAME_RESOLVED}[[:space:]]*\|"; then
    skip "sysbench — deploy ${OBD_DEPLOY_NAME_RESOLVED} not registered"
  elif [[ "${README_TRY_TENANT:-}" == "1" ]] && ! tenant_exists "${OBD_DEPLOY_NAME_RESOLVED}" "${MYSQL_TENANT}"; then
    obd cluster tenant create "${OBD_DEPLOY_NAME_RESOLVED}" -n "${MYSQL_TENANT}" --memory-size=1G --log-disk-size=2G >/dev/null 2>&1 || true
  fi
  if tenant_exists "${OBD_DEPLOY_NAME_RESOLVED}" "${MYSQL_TENANT}"; then
    if obd test sysbench "${OBD_DEPLOY_NAME_RESOLVED}" --tenant="${MYSQL_TENANT}" --script-name="${SYSBENCH_SCRIPT}"; then
      pass "obd test sysbench"
    else
      fail "obd test sysbench"
    fi
  else
    skip "sysbench — no tenant ${MYSQL_TENANT} on ${OBD_DEPLOY_NAME_RESOLVED} (demo may only have sys; create failed or skipped)"
  fi
else
  skip "sysbench — set RUN_SYSBENCH=1 (needs ${MYSQL_TENANT} tenant)"
fi

echo "---"
echo "Done. Deploy used: $(resolve_deploy_name). Re-run with RUN_DEMO=1 / README_AUTO_DEMO=1 / RUN_SYSBENCH=1 as needed."
