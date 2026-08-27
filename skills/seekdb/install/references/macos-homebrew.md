# Install SeekDB — macOS Homebrew

**Prerequisites:** macOS 15+, 1-core CPU, 2 GB RAM, MySQL client installed.

---

## Step 1 — Check Homebrew

```bash
brew --version
sw_vers -productVersion   # confirm macOS >= 15
```
If Homebrew is not installed, tell the user to install it first from <https://brew.sh>, then wait for confirmation before continuing.
If macOS version is below 15, warn the user that it is not officially supported.

## Step 2 — Tap the OceanBase repository

```bash
brew tap oceanbase/seekdb
```
Check for errors. If the tap fails due to network issues, suggest mirror configuration (see tip below).

## Step 3 — Install SeekDB

```bash
brew install seekdb
```
Monitor the output. If it fails, diagnose the error message and fix it.

Record the installed formula and dependency versions so a later linkage failure is reproducible:

```bash
brew info oceanbase/seekdb/seekdb
brew list --versions seekdb thrift
```

> **Mirror tip (slow network):** If download is slow or times out, add to `~/.zshrc` and re-run:
> ```bash
> export HOMEBREW_API_DOMAIN="https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles/api"
> export HOMEBREW_BOTTLE_DOMAIN="https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles"
> ```
> Then: `source ~/.zshrc && brew install seekdb`

## Step 4 — Start SeekDB

```bash
seekdb-start
```
Alternative startup options:
- Foreground mode: `seekdb --nodaemon`
- Custom data directory: `seekdb --base-dir=/custom/path`

## Step 5 — Verify the service is running

```bash
seekdb-status
```
The output should show `running`. If not, diagnose and fix before continuing.

### Recover a Thrift dylib mismatch

Some older SeekDB bottles were linked to the exact path `libthrift-0.22.0.dylib`, while a newer Homebrew Thrift keg may provide only another versioned dylib. The current official formula carries a private compatibility shim and sets `DYLD_FALLBACK_LIBRARY_PATH` in `seekdb-start`; prefer that maintained fix over modifying Homebrew's shared Thrift keg.

If startup reports `Library not loaded` for `libthrift-0.22.0.dylib`:

```bash
brew update
brew reinstall oceanbase/seekdb/seekdb
brew list --versions seekdb thrift
otool -L "$(brew --prefix seekdb)/bin/seekdb" | grep thrift
seekdb-start
seekdb-status
```

Do not create a compatibility symlink under `$(brew --prefix thrift)/lib`, use `install_name_tool` on the signed SeekDB binary, or globally export a replacement library path. Those changes escape the SeekDB keg, can affect other Homebrew consumers, or invalidate the binary signature. If the current official formula still fails, preserve the error and report `brew info`, both package versions, `brew --prefix seekdb`, `brew --prefix thrift`, and the `otool -L` output as a packaging mismatch instead of improvising another binary change.

## Step 6 — Verify connectivity

```bash
mysql -h 127.0.0.1 -P 2881 -u root -e "SELECT 'SeekDB is running!' AS status;"
```
If `mysql` CLI is not available, suggest: `brew install mysql-client`

Verify the optional OBShell/dashboard separately:

```bash
lsof -nP -iTCP:2886 -sTCP:LISTEN || true
curl -sS -o /dev/null -w '%{http_code}\n' http://127.0.0.1:2886/ || true
```

An HTTP 500 does not invalidate a successful SQL probe. Report **SeekDB SQL ready; OBShell/dashboard degraded**, keep the database running, and diagnose only the management component. Do not report the whole stack as healthy until the dashboard check also passes.

## Step 7 — Done

Confirm success and show connection info:
- MySQL port: `127.0.0.1:2881`
- Start: `seekdb-start` / Stop: `seekdb-stop` / Status: `seekdb-status`
- Cleanup (remove data): `seekdb-cleanup`
- Uninstall: `brew uninstall seekdb`

---

## Sources

- [Official `oceanbase/homebrew-seekdb` formula with the private Thrift compatibility shim](https://github.com/oceanbase/homebrew-seekdb/blob/014e93121b08216f8eb5d0fbc1cef83f4b1367ea/Formula/seekdb.rb)
