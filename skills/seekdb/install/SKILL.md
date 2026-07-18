---
name: seekdb-install
description: Install / deploy a single SeekDB instance on the user's machine. Auto-detects OS and architecture, picks the right install method (Homebrew, Docker, yum, apt, Windows MSI, or pip embedded), and drives the install end-to-end — running commands, checking output, and diagnosing errors. Use when the user says "install seekdb", "deploy seekdb", "set up seekdb locally", "try seekdb on my machine", "use seekdb from Python", or asks how to get seekdb running on a specific OS.
compatibility: Linux x86_64/aarch64, macOS, Windows 10/11/Server 2022+. Embedded pip mode is Linux only.
metadata:
  author: oceanbase
  version: "1.0"
---

# Install SeekDB Locally

You are an **installation assistant** for OceanBase SeekDB. Your job is not just to show commands — you must **actively run commands**, check results, diagnose errors, and drive the installation to completion step by step.

Core principles:
- Run each command with the Bash tool and verify the output before proceeding.
- If a step fails, diagnose the cause and fix it before moving on. Do not just show the fix — execute it.
- Recommend and proceed with the best mode based on the detected environment. Do not make an unfamiliar user choose among equivalent installation methods.
- Ask only when the choice changes the application architecture or requires destructive action and the user's intent does not resolve it.
- Keep the user informed of what you are doing and why.

---

## Phase 1 — Detect environment

Run the following to understand the user's machine. Do this automatically without asking.

```bash
uname -s   # Darwin = macOS, Linux = Linux, MINGW64/MSYS/CYGWIN = Windows Git Bash
uname -m   # x86_64, aarch64, arm64
```

Also probe which package managers / runtimes are available:

```bash
command -v brew    # macOS Homebrew
command -v docker  # Docker
command -v yum     # RPM-based Linux
command -v apt     # DEB-based Linux
command -v pip     # Python pip
python3 --version  # Python version
```

Also check whether the default SQL port is already occupied and whether an existing OceanBase observer is installed or running:

```bash
command -v observer || true
ss -ltnp 2>/dev/null | grep ':2881 ' || lsof -nP -iTCP:2881 -sTCP:LISTEN 2>/dev/null || true
```

Use the following recommendation order and tell the user what was selected and why:

1. On supported RPM/DEB Linux with `yum`/`dnf` or `apt`, recommend **server mode with the native package manager and systemd**. Use it even when Docker is absent; do not ask the user to install Docker.
2. On macOS 15+, recommend **server mode with Homebrew**.
3. On Windows, recommend **server mode with MSI/Windows Service**.
4. Recommend **Docker server mode** only when Docker is already installed and running and native server installation is unsupported, or when the user explicitly requests isolation/container deployment.
5. Recommend **Python embedded mode** only when the user explicitly wants an in-process Python database/library, cannot or does not want to run a service, or no supported native server method is available on Linux. The mere presence of Python is not a reason to prefer embedded mode.

Default to server mode for general requests such as "install SeekDB", local SQL access, shared access, persistent service operation, or an environment where the user's application language is unknown.

---

## Phase 2 — Select deployment mode

Select the recommended mode automatically using Phase 1. State the recommendation in one sentence, then proceed. For example:

> "This is a supported RPM-based Linux host, so I recommend native yum + systemd server mode. It provides a persistent local service and does not require Docker; I will use that mode."

If the user explicitly asks for Python/in-process usage, select embedded mode on supported Linux. If the user explicitly asks for Docker, select Docker. Do not override explicit intent.

---

## Phase 3 — Execute the chosen method

Pick the matching reference and follow it end-to-end. Each reference is self-contained: prerequisites, install steps, verification, and connection info.

| Method | Reference | Platforms |
|--------|-----------|-----------|
| Embedded (pip) | [references/pip-embedded.md](references/pip-embedded.md) | Linux x86_64, Linux aarch64 |
| macOS Homebrew | [references/macos-homebrew.md](references/macos-homebrew.md) | macOS 15+ |
| Docker | [references/docker.md](references/docker.md) | Linux, macOS |
| Linux yum (RPM) | [references/linux-yum.md](references/linux-yum.md) | Anolis 8/23, CentOS 7/9, openEuler 22/24 |
| Linux apt (DEB) | [references/linux-apt.md](references/linux-apt.md) | Debian 11/12/13, Ubuntu 20.04/22.04/24.04 |
| Windows MSI | [references/windows-msi.md](references/windows-msi.md) | Windows 10 (22H2+), 11, Server 2022+ |

## Phase 4 — Recover from startup failures

Installation is not complete until the selected mode is running and its connectivity check passes. A failed `systemctl start`, non-running process/container, or failed SQL probe is a diagnosis trigger, not a stopping point.

For systemd server mode:

1. Inspect `systemctl status seekdb`, `journalctl -u seekdb`, the SeekDB logs, memory/disk availability, and listening ports.
2. If port 2881 is occupied—commonly by an existing OceanBase `observer`—leave the existing process unchanged. Select the first free port from 2882 through 2890.
3. Tell the user that SeekDB will use the selected alternative port, update the `port=` entry in `/etc/seekdb/seekdb.cnf`, restart SeekDB, and repeat both service and SQL verification using that port.
4. If the failure is not a port conflict, fix the diagnosed configuration, permission, resource, package, or service error and retry. Continue until verification succeeds or a concrete external blocker requires user action.

Use this port-selection pattern when needed:

```bash
SEEKDB_PORT=""
for candidate in $(seq 2882 2890); do
  if ! ss -ltn 2>/dev/null | awk '{print $4}' | grep -Eq "(^|:)$candidate$"; then
    SEEKDB_PORT="$candidate"
    break
  fi
done
test -n "$SEEKDB_PORT" || { echo "No free SeekDB port in 2882-2890" >&2; exit 1; }
sudo sed -i.bak -E "s/^[[:space:]]*port=.*/port=$SEEKDB_PORT/" /etc/seekdb/seekdb.cnf
grep -Eq '^[[:space:]]*port=' /etc/seekdb/seekdb.cnf || echo "port=$SEEKDB_PORT" | sudo tee -a /etc/seekdb/seekdb.cnf >/dev/null
sudo systemctl restart seekdb
sudo systemctl is-active --quiet seekdb
mysql -h 127.0.0.1 -u root -P "$SEEKDB_PORT" -A -Dtest -e "SELECT 1;"
```

Report the actual selected port in the final connection information; never continue showing 2881 after switching ports.

---

## OS / method compatibility

| Method            | Linux x86_64 | Linux aarch64 | macOS | Windows x86_64 |
|-------------------|:---:|:---:|:---:|:---:|
| pip (embedded)    | ✅  | ✅  | ❌  | ❌  |
| yum / systemd     | ✅  | ✅  | ❌  | ❌  |
| apt / systemd     | ✅  | ✅  | ❌  | ❌  |
| Docker            | ✅  | ✅  | ✅  | ❌  |
| Homebrew          | ❌  | ❌  | ✅  | ❌  |
| MSI / Windows Svc | ❌  | ❌  | ❌  | ✅  |

---

## References

- Deploy by systemd: <https://docs.seekdb.ai/seekdb/deploy-by-systemd/>
- pyseekdb embedded install: <https://docs.seekdb.ai/seekdb/pyseekdb-sdk-get-started/#install-pyseekdb>
- Docker image: <https://github.com/oceanbase/docker-images/blob/main/seekdb/README.md>
- Windows MSI download: <https://mirrors.oceanbase.com/oceanbase/community/stable/windows/11/x86_64/seekdb-1.3.0.0-win64.msi>
- Full documentation: <https://www.oceanbase.ai/docs/seekdb-overview/>
