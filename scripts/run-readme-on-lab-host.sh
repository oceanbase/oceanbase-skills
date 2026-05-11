#!/usr/bin/env bash
# Lab host used for README case runs.
# Set README_TEST_SSH to your own test host before running, e.g.:
#   export README_TEST_SSH=root@your-test-host
if [[ -z "${README_TEST_SSH:-}" ]]; then
  echo "ERROR: README_TEST_SSH is not set. Example: export README_TEST_SSH=root@your-test-host" >&2
  exit 1
fi
exec "$(dirname "$0")/run-readme-cases.sh" "$@"
