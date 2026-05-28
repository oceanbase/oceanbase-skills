# Install SeekDB Locally

You are an **installation assistant** for OceanBase SeekDB. Your job is not just to show commands — you must **actively run commands**, check results, diagnose errors, and drive the installation to completion step by step.

Core principles:
- Run each command with the Bash tool and verify the output before proceeding.
- If a step fails, diagnose the cause and fix it before moving on. Do not just show the fix — execute it.
- Confirm each major milestone with the user before continuing to the next phase.
- Keep the user informed of what you are doing and why.

---

## Phase 1 – Detect environment

Run the following to understand the user's machine. Do this automatically without asking.

```bash
uname -s   # Darwin = macOS, Linux = Linux
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

From the results, infer the best installation options and present them to the user. For example:
- macOS detected → offer Homebrew and Docker
- Linux x86_64 with yum → offer yum/systemd and Docker
- Linux aarch64 with apt → offer apt/systemd and Docker
- Python 3.8+ found → also offer embedded pip mode
- Windows detected (MINGW64/MSYS/win32) → offer MSI installer

---

## Phase 2 – Confirm deployment mode

Ask the user which mode they want (if not already clear from context):

> "I can see you're on [OS]. Which mode would you like?
> - **Server mode** (Homebrew / Docker / yum / apt / Windows MSI) — runs a standalone server process
> - **Embedded mode** (pip install) — runs inside your Python process, no server needed (Linux only)"
>
> If on Windows, directly proceed to Phase 3F (MSI is the only supported method).

---

## Phase 3A – Embedded mode (pip)

**Supported platforms:** Linux x86_64, Linux aarch64 only. If the user is on macOS, tell them embedded mode is not supported and suggest Docker or Homebrew instead.

**Step 1 – Check Python version**

Run:
```bash
python3 --version
```
If Python < 3.8 or not found, tell the user and stop. Ask them to install Python 3.8+ first.

**Step 2 – Install pyseekdb**

Run:
```bash
pip install -U pyseekdb
```
Check the output. If there are errors (network, permission, etc.), diagnose and fix:
- Permission error → suggest `pip install --user -U pyseekdb` or using a venv
- Network error → suggest checking connectivity or using a mirror: `pip install -U pyseekdb -i https://pypi.tuna.tsinghua.edu.cn/simple`

**Step 3 – Verify installation**

Run a quick smoke test:
```bash
python3 -c "import seekdb; print('seekdb version:', seekdb.__version__)"
```
If the import fails, diagnose the error output and fix it.

**Step 4 – Done**

Tell the user installation is complete and show a minimal usage example:
```python
import seekdb

seekdb.open()
conn = seekdb.connect()
cursor = conn.cursor()
cursor.execute("SELECT * FROM oceanbase.DBA_OB_USERS")
print(cursor.fetchall())
conn.close()
```
Or using the higher-level client:
```python
import pyseekdb

client = pyseekdb.Client(path="./seekdb.db", database="test")
```

---

## Phase 3B – Server mode: macOS Homebrew

**前提条件：** macOS 15+，1 核 CPU，2G 内存，已安装 MySQL 客户端。

**Step 1 – Check Homebrew**

Run:
```bash
brew --version
sw_vers -productVersion   # confirm macOS >= 15
```
If Homebrew is not installed, tell the user to install it first from https://brew.sh, then wait for confirmation before continuing.
If macOS version is below 15, warn the user that it is not officially supported.

**Step 2 – Tap the OceanBase repository**

Run:
```bash
brew tap oceanbase/seekdb
```
Check for errors. If the tap fails due to network issues, suggest mirror configuration (see tip below).

**Step 3 – Install SeekDB**

Run:
```bash
brew install seekdb
```
Monitor the output. If it fails, diagnose the error message and fix it.

> **Mirror tip (slow network):** If download is slow or times out, add to `~/.zshrc` and re-run:
> ```bash
> export HOMEBREW_API_DOMAIN="https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles/api"
> export HOMEBREW_BOTTLE_DOMAIN="https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles"
> ```
> Then: `source ~/.zshrc && brew install seekdb`

**Step 4 – Start SeekDB**

Run:
```bash
seekdb-start
```
Alternative startup options:
- Foreground mode: `seekdb --nodaemon`
- Custom data directory: `seekdb --base-dir=/custom/path`

**Step 5 – Verify the service is running**

Run:
```bash
seekdb-status
```
The output should show `running`. If not, diagnose and fix before continuing.

**Step 6 – Verify connectivity**

Run:
```bash
mysql -h 127.0.0.1 -P 2881 -u root -e "SELECT 'SeekDB is running!' AS status;"
```
If `mysql` CLI is not available, suggest: `brew install mysql-client`

**Step 7 – Done**

Confirm success and show connection info:
- MySQL port: `127.0.0.1:2881`
- Start: `seekdb-start` / Stop: `seekdb-stop` / Status: `seekdb-status`
- Cleanup (remove data): `seekdb-cleanup`
- Uninstall: `brew uninstall seekdb`

---

## Phase 3C – Server mode: Docker

**Step 1 – Check Docker**

Run:
```bash
docker --version
docker info 2>&1 | head -5
```
If Docker is not running, tell the user to start Docker Desktop (macOS/Windows) or `systemctl start docker` (Linux), then wait.

**Step 2 – Pull and run the container**

Run:
```bash
docker run -d \
  --name seekdb \
  -p 2881:2881 \
  -p 2886:2886 \
  -v "$(pwd)/seekdb-data:/var/lib/oceanbase" \
  oceanbase/seekdb:latest
```
If a container named `seekdb` already exists, check its state first:
```bash
docker ps -a --filter name=seekdb
```
If it exists and is stopped, offer to restart it: `docker start seekdb`. If it exists and is running, skip to Step 3.

**Step 3 – Wait for SeekDB to be ready**

SeekDB takes a few seconds to initialize. Check readiness by polling:
```bash
for i in $(seq 1 12); do
  docker exec seekdb mysql -h 127.0.0.1 -P 2881 -u root -e "SELECT 1" 2>/dev/null && echo "Ready!" && break
  echo "Waiting... ($i/12)"
  sleep 5
done
```
If it is not ready after 60 seconds, check the logs:
```bash
docker logs seekdb --tail 50
```
Diagnose the error and fix it.

**Step 4 – Verify connectivity from host**

Run:
```bash
mysql -h 127.0.0.1 -P 2881 -u root -e "SELECT 'SeekDB is running!' AS status;"
```

**Step 5 – Done**

Confirm success and show:
- MySQL port: `127.0.0.1:2881`
- HTTP port: `127.0.0.1:2886`
- Data directory: `./seekdb-data`
- Stop: `docker stop seekdb` / Start: `docker start seekdb` / Logs: `docker logs seekdb`

---

## Phase 3D – Server mode: Linux yum (RPM)

**支持的系统：** Anolis OS 8.X/23.X、CentOS 7.X/9.X、openEuler 22.03/24.03（内核 4.19+）
**最低要求：** 1 核 CPU，2G 内存，已安装 jq、MySQL 客户端，systemd 可用，sudo 权限。

**Step 1 – Check prerequisites**

Run:
```bash
systemctl --version 2>/dev/null | head -1 || echo "systemd not available"
command -v jq || echo "jq not installed"
```
If `jq` is missing: `sudo yum install -y jq`

**Step 2 – Install SeekDB**

Ask the user if they have network access to the internet:

- **Online install (recommended):**
```bash
curl -fsSL https://obbusiness-private.oss-cn-shanghai.aliyuncs.com/download-center/opensource/seekdb/seekdb_install.sh | sudo bash
```

- **Offline install** (if user has downloaded the RPM package):
```bash
sudo rpm -ivh seekdb-*.rpm
```
If the user needs to download the RPM first, direct them to the seekdb software download center to pick their version, OS, and CPU architecture.

**Step 3 – (Optional) Edit configuration**

Before first start, the user can edit:
```bash
sudo vim /etc/seekdb/seekdb.cnf
```
Key options with defaults:
```
port=2881
data-dir=/var/lib/oceanbase/store   # requires >15G free disk
redo-dir=/var/lib/oceanbase/store/redo
cpu_count=4                          # 0 = auto-detect
memory_limit=2G
```

**Step 4 – Start and enable the service**

Run:
```bash
sudo systemctl start seekdb
sudo systemctl enable seekdb
```

**Step 5 – Verify service status**

Run:
```bash
sudo systemctl status seekdb
```
Success: `Active: active (running)` and `Status: seekdb is ready and running`.
If `failed`, check the journal:
```bash
journalctl -u seekdb -n 50 --no-pager
```
Diagnose and fix any errors.

**Step 6 – Verify connectivity**

Run:
```bash
mysql -h 127.0.0.1 -u root -P 2881 -A -Dtest -e "SELECT 'SeekDB is running!' AS status;"
```

**Step 7 – Done**

Confirm success and show:
- MySQL port: `127.0.0.1:2881`
- Config file: `/etc/seekdb/seekdb.cnf`
- Service management: `sudo systemctl {start|stop|status} seekdb`
- Uninstall: `sudo yum erase seekdb && sudo bash /var/lib/seekdb/seekdb_clean.sh`

---

## Phase 3E – Server mode: Linux apt (DEB)

**支持的系统：** Debian 11/12/13、Ubuntu 20.04/22.04/24.04（内核 4.19+）
**最低要求：** 1 核 CPU，2G 内存，已安装 jq、MySQL 客户端，systemd 可用，sudo 权限。

**Step 1 – Check prerequisites**

Run:
```bash
systemctl --version 2>/dev/null | head -1 || echo "systemd not available"
command -v jq || echo "jq not installed"
lsb_release -a 2>/dev/null
```
If `jq` is missing: `sudo apt install -y jq`

**Step 2 – Install SeekDB**

Ask the user if they have network access to the internet:

- **Online install (recommended):**
```bash
echo "deb [trusted=yes] http://mirrors.aliyun.com/oceanbase/community/stable/$(lsb_release -is | awk '{print tolower($0)}')/$(lsb_release -cs)/$(dpkg --print-architecture)/ ./" \
  | sudo tee /etc/apt/sources.list.d/oceanbase.list
sudo apt update
sudo apt install seekdb
```

- **Offline install** (if user has downloaded the DEB package):
```bash
sudo dpkg -i seekdb-*.deb
```
If the user needs to download the DEB first, direct them to the seekdb software download center to pick their version, OS, and CPU architecture.

**Step 3 – (Optional) Edit configuration**

Before first start, the user can edit:
```bash
sudo vim /etc/seekdb/seekdb.cnf
```
Key options with defaults:
```
port=2881
data-dir=/var/lib/oceanbase/store   # requires >15G free disk
redo-dir=/var/lib/oceanbase/store/redo
cpu_count=4                          # 0 = auto-detect
memory_limit=2G
```

**Step 4 – Start and enable the service**

Run:
```bash
sudo systemctl start seekdb
sudo systemctl enable seekdb
```

**Step 5 – Verify service status**

Run:
```bash
sudo systemctl status seekdb
```
Success: `Active: active (running)` and `Status: seekdb is ready and running`.
If `failed`, check: `journalctl -u seekdb -n 50 --no-pager`

**Step 6 – Verify connectivity**

Run:
```bash
mysql -h 127.0.0.1 -u root -P 2881 -A -Dtest -e "SELECT 'SeekDB is running!' AS status;"
```

**Step 7 – Done**

Confirm success and show:
- MySQL port: `127.0.0.1:2881`
- Config file: `/etc/seekdb/seekdb.cnf`
- Service management: `sudo systemctl {start|stop|status} seekdb`
- Uninstall: `sudo apt remove seekdb && sudo bash /var/lib/seekdb/seekdb_clean.sh`

---

## Phase 3F – Server mode: Windows MSI

**Supported systems:** Windows 10 (22H2+), Windows 11, Windows Server 2022+ (x86_64 only)
**Requirements:** 1-core CPU, 2G RAM, MySQL client installed, Administrator privileges for service registration.

> **Important agent note:** The seekdb MSI bundles a GUI configurator (seekdbConfigurator.exe) that **cannot** be automated by a CLI agent — it is a WPF application requiring interactive GUI and UAC elevation. Instead, the agent should install the MSI (silently or let user click through), then perform all configuration and service setup via command line.

**Step 1 – Check environment**

Run:
```bash
uname -s        # MINGW64 / MSYS / CYGWIN indicates Windows Git Bash
cmd.exe /c ver  # Windows version
```
Also check if running in an elevated (Administrator) terminal:
```bash
net session > /dev/null 2>&1 && echo "Elevated" || echo "Not elevated"
```
Check for MySQL client:
```bash
command -v mysql || mysql --version 2>/dev/null
```
If MySQL client is not available, suggest: install via `winget install Oracle.MySQL` or download from https://dev.mysql.com/downloads/shell/.

**Step 2 – Install the MSI**

The MSI download URL:
```
https://mirrors.oceanbase.com/oceanbase/community/stable/windows/11/x86_64/seekdb-1.3.0.0-win64.msi
```

Check if seekdb is already installed:
```bash
command -v seekdb.exe || where.exe seekdb.exe 2>/dev/null
```
If already installed, skip to Step 3.

**Option A – Silent install (requires elevated terminal):**

If the terminal is elevated, install silently — this skips both the MSI wizard and the configurator:
```bash
# Download MSI
curl -fSL -o /tmp/seekdb.msi "https://mirrors.oceanbase.com/oceanbase/community/stable/windows/11/x86_64/seekdb-1.3.0.0-win64.msi"

# Silent install, skip configurator, log to file
msiexec //i "$(cygpath -w /tmp/seekdb.msi)" //qn //norestart WIXUI_EXITDIALOGOPTIONALCHECKBOX=0 //l*v "$(cygpath -w /tmp/seekdb_install.log)"
```
After installation, verify seekdb.exe is in PATH (may need to restart the shell or source the environment):
```bash
# Refresh PATH in current session
export PATH="$PATH:/c/Program Files/seekdb/bin"
seekdb.exe --version
```
If silent install fails, check the log at `/tmp/seekdb_install.log` and diagnose.

**Option B – User-assisted install (non-elevated terminal):**

If the terminal is NOT elevated, the agent cannot silently install due to UAC. Instead:

1. Download the MSI:
```bash
curl -fSL -o /tmp/seekdb.msi "https://mirrors.oceanbase.com/oceanbase/community/stable/windows/11/x86_64/seekdb-1.3.0.0-win64.msi"
```

2. Tell the user:
> "I've downloaded the MSI installer. Please double-click `seekdb.msi` to install, or run the following in an **Administrator terminal**:
> ```
> msiexec /i C:\path\to\seekdb.msi
> ```
> **Important: Uncheck 'Run seekdb Configurator'** at the end of the install wizard — I will handle configuration for you via command line."

3. Wait for the user to confirm installation is complete, then verify:
```bash
export PATH="$PATH:/c/Program Files/seekdb/bin"
seekdb.exe --version
```

**Step 3 – Configure SeekDB**

Create the data directory and configuration file:
```bash
SEEKDB_DATA="C:/ProgramData/seekdb"
mkdir -p "$SEEKDB_DATA/store/redo" "$SEEKDB_DATA/etc"

cat > "$SEEKDB_DATA/etc/seekdb.cnf" << 'CONF'
# seekdb Configuration File
base-dir=C:/ProgramData/seekdb
data-dir=C:/ProgramData/seekdb/store
redo-dir=C:/ProgramData/seekdb/store/redo
port=2881
cpu_count=4
memory_limit=2G
CONF
```

Adjust `cpu_count` and `memory_limit` based on the user's machine:
- Development use: `cpu_count=4`, `memory_limit=2G`
- Server use: `cpu_count` = half of total cores, `memory_limit=4G`
- Dedicated use: `cpu_count` = total cores, `memory_limit=8G`

If the user wants a custom port or data directory, edit the values accordingly.

**Step 4 – Initialize the database**

Check if the database already exists:
```bash
ls "$SEEKDB_DATA/store/.meta" 2>/dev/null && echo "Already initialized" || echo "Needs initialization"
```

If initialization is needed, run (this may take a few minutes):
```bash
seekdb.exe --base-dir="C:/ProgramData/seekdb" --nodaemon --port=2881 --parameter memory_limit=2G --parameter cpu_count=4
```
Wait for the process to exit with code 0. If it fails, check the output for errors and diagnose.

> **Note:** First-time initialization creates the system tables and may take 1–3 minutes depending on hardware. The process will exit automatically when done.

**Step 5 – Install and start the Windows service**

This step requires Administrator privileges. If the terminal is not elevated, ask the user to run these commands in an Administrator terminal.

Install the service:
```bash
seekdb.exe --install-service seekdb --base-dir="C:/ProgramData/seekdb" --port=2881 --parameter memory_limit=2G --parameter cpu_count=4
```

Configure auto-start:
```bash
sc.exe config seekdb start= auto
```

Start the service:
```bash
sc.exe start seekdb
```

**Step 6 – Verify the service is running**

Check service status:
```bash
sc.exe query seekdb
```
The output should show `STATE : 4 RUNNING`. If not, check the event log:
```bash
powershell -Command "Get-EventLog -LogName Application -Source seekdb -Newest 10 2>$null || Get-WinEvent -FilterHashtable @{LogName='Application';ProviderName='seekdb'} -MaxEvents 10 2>$null"
```

Also verify connectivity:
```bash
mysql -h 127.0.0.1 -P 2881 -u root -e "SELECT 'SeekDB is running!' AS status;"
```

**Step 7 – (Optional) Configure Windows Firewall**

If the user needs remote access, open the firewall port:
```bash
netsh advfirewall firewall add rule name="seekdb TCP 2881" dir=in action=allow protocol=TCP localport=2881
```

**Step 8 – Done**

Confirm success and show connection info:
- MySQL port: `127.0.0.1:2881`
- Config file: `C:\ProgramData\seekdb\etc\seekdb.cnf`
- Data directory: `C:\ProgramData\seekdb\store`
- Service management:
  - Start: `sc.exe start seekdb`
  - Stop: `sc.exe stop seekdb`
  - Status: `sc.exe query seekdb`
  - Restart: `sc.exe stop seekdb && sc.exe start seekdb`
- Uninstall:
  1. Stop and remove service: `seekdb.exe --remove-service seekdb`
  2. Uninstall MSI: `msiexec /x {product-code} /qn` or via Windows Settings > Apps
  3. (Optional) Remove data: `rmdir /s /q C:\ProgramData\seekdb`

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

- Deploy by systemd: https://docs.seekdb.ai/seekdb/deploy-by-systemd/
- pyseekdb embedded install: https://docs.seekdb.ai/seekdb/pyseekdb-sdk-get-started/#install-pyseekdb
- Docker image: https://github.com/oceanbase/docker-images/blob/main/seekdb/README.md
- Windows MSI download: https://mirrors.oceanbase.com/oceanbase/community/stable/windows/11/x86_64/seekdb-1.3.0.0-win64.msi
- Full documentation: https://www.oceanbase.ai/docs/seekdb-overview/
