# build-seekdb

Build SeekDB binaries and/or installation packages for one or more target platforms.

## Usage

```
/build-seekdb [platform] [action] [options]
```

**platform** (default: auto-detect current OS):
- `mac`     — macOS arm64/x86_64
- `linux`   — Linux x86_64
- `android` — Android arm64-v8a (cross-compile on macOS/Linux host)
- `windows` — Windows x86_64 (native PowerShell environment only)

**action** — what to do (default: `compile release`):

| Platform | Compile actions | Package actions |
|----------|----------------|-----------------|
| `mac`    | `release` `debug` `perf` | `tgz` |
| `linux`  | `release` `debug` `perf` | `rpm` `deb` |
| `android`| `release` `debug` | `apk` |
| `windows`| `release` `debug` | `installer` |

- Compile actions build the seekdb binary + libseekdb_embed_c.
- Package actions build an installable artifact (implies a release compile first if needed).
- Multiple actions can be requested in one invocation, e.g. `release tgz` or `debug rpm`.

**options**:
- `--init`        — Force re-initialize dependencies before building
- `--jobs N`      — Parallel jobs (default: all CPU cores)
- `--version V`   — Version string for package naming (e.g. `4.3.5`, default: `beta`)
- `--release R`   — Release/date string for package naming (e.g. `20260407`, default: today's date)
- `--with-jni`    — (Android only) Also build libseekdb_embed.so JNI library
- `--install`     — (Android only) adb install the APK after building

---

## Instructions

When the user runs `/build-seekdb`, follow these steps.

### Step 1 — Parse arguments

- Extract platform, action(s), and options from `$ARGUMENTS`.
- If no platform given, detect via `uname -s`: Darwin → mac, Linux → linux.
- If no action given, default to `release` (compile only).
- Default version: `beta`. Default release: today's date as `YYYYMMDD`.
- Default jobs: detect with `sysctl -n hw.ncpu` (mac/android) or `nproc` (linux).
- Reject invalid combinations (e.g. `deb` on mac, `tgz` on linux, `perf` on android/windows)
  and tell the user which package/compile types are supported for their platform.

---

### Step 2 — Determine repo root

```bash
REPO_ROOT=$(pwd)
```
Use `$REPO_ROOT` for all subsequent commands. Do NOT hardcode any absolute path.

**Key rule — package actions vs compile-only actions:**

- **Package actions** (`apk`, `rpm`, `deb`, `tgz`, `installer`): call the dedicated packaging
  script directly. These scripts already handle clean + init + make internally.
  **Do NOT run a separate init step before them.**

- **Compile-only actions** (`release`, `debug`, `perf`): no packaging script is involved.
  Run the dep check below first, then call `build.sh --make`.

#### Dependency check (compile-only actions only)

`dep_create.sh` writes two marker files on successful init:
- `deps/3rd/DONE` — generic completion flag
- `deps/3rd/<MD5>` — MD5 of the platform-specific `.deps` file

**Checking only `DONE` is insufficient.** The MD5 marker must match the *current* `.deps`
file for the *target* platform. A missing MD5 marker means:
- the `.deps` file was updated (new or changed packages), OR
- the last init was for a different platform (e.g. macOS deps present, but Android marker absent).

```bash
# 1. Determine the .deps file for the target platform
#    Android:          $REPO_ROOT/deps/init/oceanbase.android.arm64.deps
#    macOS arm64 ≥15:  $REPO_ROOT/deps/init/oceanbase.macos15.arm64.deps
#    macOS arm64 13-14:$REPO_ROOT/deps/init/oceanbase.macos13.arm64.deps
#    Linux el8 x86_64: $REPO_ROOT/deps/init/oceanbase.el8.x86_64.deps
#    Linux el9 x86_64: $REPO_ROOT/deps/init/oceanbase.el9.x86_64.deps
#
# 2. Compute its MD5
#    macOS: MD5=$(md5 -r <DEPS_FILE> | cut -d' ' -f1)
#    Linux: MD5=$(md5sum <DEPS_FILE>  | cut -d' ' -f1)
#
# 3. Check the marker
DEPS_MARKER="$REPO_ROOT/deps/3rd/$MD5"
```

**OS_TAG reference table:**

| Target | OS_TAG |
|--------|--------|
| Android cross-compile | `android.arm64` |
| macOS arm64, macOS ≥ 15 | `macos15.arm64` |
| macOS arm64, macOS 13–14 | `macos13.arm64` |
| macOS x86_64, macOS ≥ 15 | `macos15.x86_64` |
| Linux x86_64, RHEL/CentOS 8 | `el8.x86_64` |
| Linux x86_64, RHEL/CentOS 9 | `el9.x86_64` |

On macOS: detect version with `sw_vers -productVersion`; detect arch with
`sysctl -n hw.optional.arm64` (returns `1` for arm64, correct even under Rosetta).

**Decision logic (compile-only):**

| Condition | Action |
|-----------|--------|
| `--init` explicitly passed | Always run init: `./build.sh release [--android] --init` |
| `$DEPS_MARKER` missing | Auto-run init, print `[build-seekdb] deps marker not found — running --init for <PLATFORM> ...` |
| `$DEPS_MARKER` exists | Skip init, print `[build-seekdb] deps OK — skipping init.` |

> `dep_create.sh` is idempotent — if the MD5 marker already matches it exits immediately.

---

### Step 3 — Execute builds

#### macOS

**Compile modes:**

| Action | build.sh command | Build dir | Key flags |
|--------|-----------------|-----------|-----------|
| `release` | `./build.sh release --make -j<N>` | `build_release/` | RelWithDebInfo |
| `debug`   | `./build.sh debug --make -j<N>`   | `build_debug/`   | Debug |
| `perf`    | `./build.sh mac_perf --make -j<N>`| `build_mac_perf/`| RelWithDebInfo + ThinLTO (no FDO/BOLT — macOS limitation) |

Artifact (inside the build dir):
- `src/observer/seekdb`

Verify: `./build_release/src/observer/seekdb --version`

**Package: `tgz`**

macOS does **not** support Thin LTO in the package build configuration (`build.sh tgz`
enables it by default). Call `build.sh` directly from `$REPO_ROOT` with
`-DENABLE_THIN_LTO=OFF` — no need to `cd` into any subdirectory:

```bash
./build.sh tgz \
    -DOB_RELEASEID=<RELEASE> \
    -DBUILD_NUMBER=<RELEASE> \
    -DUSE_LTO_CACHE=ON       \
    -DENABLE_THIN_LTO=OFF    \
    --init --make tgz
# Artifact: build_tgz/seekdb-<VERSION>-<RELEASE>-macos26-arm64.tar.gz
```

---

#### Linux

**Compile modes:**

| Action | build.sh command | Build dir | Key flags |
|--------|-----------------|-----------|-----------|
| `release` | `./build.sh release --make -j<N>` | `build_release/` | RelWithDebInfo |
| `debug`   | `./build.sh debug --make -j<N>`   | `build_debug/`   | Debug |
| `perf`    | `./build.sh perf --make -j<N>`    | `build_perf/`    | RelWithDebInfo + ThinLTO + AutoFDO + BOLT |

Artifact (inside the build dir):
- `src/observer/seekdb`

**Package: `rpm`**

Call `rpm/seekdb-build.sh` directly — it handles clean + init + make internally:
```bash
cd $REPO_ROOT/rpm && bash seekdb-build.sh . seekdb <VERSION> <RELEASE>
# Artifact: $REPO_ROOT/rpm/seekdb-<VERSION>-<RELEASE>.rpm
```

**Package: `deb`** (Debian/Ubuntu hosts only)

Call `package/deb/seekdb-build.sh` directly — it handles clean + init + make internally:
```bash
cd $REPO_ROOT/package/deb && bash seekdb-build.sh . seekdb <VERSION> <RELEASE>
# Artifact: $REPO_ROOT/package/deb/seekdb-<VERSION>-<RELEASE>.deb + .ddeb
```

---

#### Android (cross-compile from macOS or Linux host)

**Environment prerequisites:**
```bash
export PATH="${ANDROID_HOME:-$HOME/Library/Android/sdk}/platform-tools:$PATH"
export ANDROID_NDK_HOME="${ANDROID_NDK_HOME:-${ANDROID_HOME:-$HOME/Library/Android/sdk}/ndk/27.3.13750724}"
```

**Compile modes:**

| Action | build.sh command | Build dir |
|--------|-----------------|-----------|
| `release` | `./build.sh release --android --make -j<N>` | `build_android_release/` |
| `debug`   | `./build.sh debug --android --make -j<N>`   | `build_android_debug/`   |

Artifacts (inside the build dir):
- `src/observer/seekdb`
- `src/observer/embed/libseekdb_embed_c.so`
- `src/observer/embed/embedded_client`

**Incremental make** (fastest for day-to-day iteration; skip dep check — deps already resolved):
```bash
cd $REPO_ROOT/build_android_release && make -j<N>
```

**Package: `apk`**

`seekdb-apk-build.sh --build` runs `build.sh clean + release --android --init + make`
internally — skip Step 2 init check when using `--build`:
```bash
cd $REPO_ROOT
./package/apk/seekdb-apk-build.sh --build --apk [--with-jni] [--install] \
    seekdb <VERSION> <RELEASE>
# Artifact: package/apk/seekdb-<VERSION>-<RELEASE>.apk
#
# --build    : clean + android init + make
# --apk      : gradlew assembleDebug, rename and move APK
# --with-jni : also build/sync libseekdb_embed.so
# --install  : adb install -r onto connected device/emulator
```

Script requirements:
- `ANDROID_NDK_HOME` set (default: `$HOME/Library/Android/sdk/ndk/27.3.13750724`)
- JDK 17+ for Gradle (auto-detected from Android Studio JBR if not set)
- `curl` or `wget` (downloads `gradle-wrapper.jar` on first run)

Manual APK steps (alternative to seekdb-apk-build.sh):
```bash
# Step A: binary already built by compile step above

# Step B: strip + copy into jniLibs
_prebuilt=$(ls $ANDROID_NDK_HOME/toolchains/llvm/prebuilt/ | head -1)
NDK_STRIP="$ANDROID_NDK_HOME/toolchains/llvm/prebuilt/$_prebuilt/bin/llvm-strip"
$NDK_STRIP -o $REPO_ROOT/build_android_app/app/src/main/jniLibs/arm64-v8a/libseekdb_embed_c.so \
              $REPO_ROOT/build_android_release/src/observer/embed/libseekdb_embed_c.so
$NDK_STRIP -o $REPO_ROOT/build_android_app/app/src/main/jniLibs/arm64-v8a/libembedded_client.so \
              $REPO_ROOT/build_android_release/src/observer/embed/embedded_client

# Step C: build APK
echo "sdk.dir=${ANDROID_HOME:-$HOME/Library/Android/sdk}" > $REPO_ROOT/build_android_app/local.properties
cd $REPO_ROOT/build_android_app && ./gradlew assembleDebug
# Artifact: build_android_app/app/build/outputs/apk/debug/app-debug.apk
```

---

#### Windows (native PowerShell only — cannot cross-compile)

If the user requests `windows` from a macOS/Linux host, print:
> Windows builds cannot be cross-compiled. Run the following natively on Windows:

```powershell
# Prerequisites (one-time)
winget install -e --id Microsoft.DotNet.SDK.8
# restart PowerShell, then:
dotnet tool install --global wix

# Init
.\build.ps1 init

# Compile
.\build.ps1 release --ninja -j 16   # or: debug
```

**Package: `installer`** (WiX, after compile):
```powershell
cd build_release
cmake --build . --target package
```

Verify:
```bash
mysql -h 127.0.0.1 -uroot -P2881 -Dtest -A
```

---

#### Python Wheel (Linux only, inside manylinux container)

```bash
# Must run inside quay.io/pypa/manylinux_2_28
PACKAGE_VERSION=0.0.1
for python_home in /opt/python/cp3*/; do
    PACKAGE_VERSION=$PACKAGE_VERSION PYTHON_HOME=$python_home bash package/wheel/build_python.sh
done
# Artifacts: build_python/wheelhouse/seekdb-*.whl  seekdb_lib-*.whl
```

---

### Step 4 — Report results

After each action:
- Print success or failure (exit code).
- Print artifact path(s) and file sizes (`ls -lh`).
- If init failed → abort, report error, do not proceed to make.
- If make failed after successful init → suggest re-running with `--init` (marker may be stale).
- If Android NDK missing → remind user to set `ANDROID_NDK_HOME`.
- If `windows` requested on non-Windows → show PowerShell instructions, do not attempt build.

