# Install SeekDB — Linux yum (RPM)

**Supported systems:** Anolis OS 8.X/23.X, CentOS 7.X/9.X, openEuler 22.03/24.03 (kernel 4.19+)
**Minimum requirements:** 1-core CPU, 2 GB RAM, `jq` and MySQL client installed, systemd available, sudo privileges.

---

## Step 1 — Check prerequisites

```bash
systemctl --version 2>/dev/null | head -1 || echo "systemd not available"
command -v jq || echo "jq not installed"
```
If `jq` is missing: `sudo yum install -y jq`

## Step 2 — Install SeekDB

Ask the user if they have network access to the internet:

- **Online install — yum repo (recommended):**
```bash
yum-config-manager --add-repo https://mirrors.oceanbase.com/oceanbase/community/stable/el/\$releasever/\$basearch/
sudo yum install -y seekdb
```

- **Online install — script (alternative):**

> **Security requirement:** Prefer the yum repo method above. Only use the script when its SHA-256 digest has been obtained from an official OceanBase release channel independently of the download URL. Do not continue when no official digest is available.

```bash
: "${SEEKDB_INSTALL_SHA256:?Set this to the SHA-256 published by an official OceanBase release channel}"
SEEKDB_INSTALL_SCRIPT="$(mktemp)"
trap 'rm -f "$SEEKDB_INSTALL_SCRIPT"' EXIT
curl --proto '=https' --tlsv1.2 -fL \
  https://obbusiness-private.oss-cn-shanghai.aliyuncs.com/download-center/opensource/seekdb/seekdb_install.sh \
  -o "$SEEKDB_INSTALL_SCRIPT"
printf '%s  %s\n' "$SEEKDB_INSTALL_SHA256" "$SEEKDB_INSTALL_SCRIPT" | sha256sum --check --strict
less "$SEEKDB_INSTALL_SCRIPT"
sudo bash "$SEEKDB_INSTALL_SCRIPT"
```

Stop if checksum verification fails. Visual review is additional defense, not a substitute for the checksum.

- **Offline install** (if user has downloaded the RPM package):
```bash
sudo rpm -ivh seekdb-*.rpm
```
If the user needs to download the RPM first, direct them to the seekdb software download center to pick their version, OS, and CPU architecture.

## Step 3 — (Optional) Edit configuration

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

## Step 4 — Start and enable the service

```bash
sudo systemctl start seekdb
sudo systemctl enable seekdb
```

## Step 5 — Verify service status

```bash
sudo systemctl status seekdb
```
Success: `Active: active (running)` and `Status: seekdb is ready and running`.
If `failed`, check the journal:
```bash
journalctl -u seekdb -n 50 --no-pager
```
Diagnose and fix any errors; do not stop merely because the first start failed. If the log reports an address/port conflict or port 2881 is already listening (for example, an existing OceanBase observer), leave the existing service unchanged. Follow the startup-recovery procedure in `../SKILL.md` to select a free port, update `/etc/seekdb/seekdb.cnf`, restart SeekDB, and verify on the new port.

## Step 6 — Verify connectivity

Use port 2881 unless startup recovery selected another port:
```bash
mysql -h 127.0.0.1 -u root -P "${SEEKDB_PORT:-2881}" -A -Dtest -e "SELECT 'SeekDB is running!' AS status;"
```

## Step 7 — Done

Confirm success and show:
- MySQL port: `127.0.0.1:${SEEKDB_PORT:-2881}` (report the resolved numeric port)
- Config file: `/etc/seekdb/seekdb.cnf`
- Service management: `sudo systemctl {start|stop|status} seekdb`
- Uninstall: `sudo yum erase seekdb && sudo bash /var/lib/seekdb/seekdb_clean.sh`

---

## References

- Deploy by systemd: <https://docs.seekdb.ai/seekdb/deploy-by-systemd/>
