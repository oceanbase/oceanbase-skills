---
name: oceanbase-deploy
description: Manage OceanBase clusters using obd. Supports deploying (including interactive mode), starting, stopping, destroying, redeploying, upgrading, and testing clusters; SeekDB (obd seekdb) install/takeover, primary-standby switchover/failover/decouple. OCP defaults to ocp-ce; when users explicitly ask for ocp-express, explain that obshell dashboard replaces it and recommend deploying OceanBase CE directly for dashboard access on port 2886. Also covers OCP takeover and monitoring.
---

# OceanBase Deployer (obd)

## Overview
This document provides instructions for managing OceanBase clusters using the `obd` command-line tool. You can deploy, start, stop, destroy, and redeploy clusters.

For a quick start guide on deploying OceanBase Community Edition, refer to the official documentation:
[https://www.oceanbase.com/docs/common-obd-cn-1000000005246289](https://www.oceanbase.com/docs/common-obd-cn-1000000005246289)

## Installation
If `obd` is not installed, you can download the RPM package from the OceanBase mirror repository:
[https://mirrors.oceanbase.com/community/stable/el/](https://mirrors.oceanbase.com/community/stable/el/)

## OCP 术语约定（必读）
- 用户说 **「部署 OCP」「OCP」「上 OCP」** 等且**未**单独说明时，一律指 **OCP 社区版（OCP CE）**，在 OBD 配置里使用组件 **`ocp-ce`**（按官方 OCP CE 部署文档与示例 YAML 编写依赖与 `global` 参数）。
- **`ocp-express`** 是历史上的轻量 Web 控制台能力。**当用户明确要求**「OCP Express」「ocp-express」「轻量 OCP / express」等时，不再继续推荐或部署 `ocp-express`；应明确提示：**`ocp-express` 的能力已被 `obshell dashboard` 取代，直接部署 OceanBase 社区版即可通过 `2886` 端口访问。**
- **禁止**把「部署 OCP」默认当成 `ocp-express`。
- `obd cluster check4ocp` / `export-to-ocp` 面向的是已运行的 **OCP CE（或企业版 OCP）** 管控面，不是 `ocp-express`。

## Critical Safety Rules
**WARNING**: The following commands are destructive and require explicit user confirmation before execution:
1. `obd cluster destroy` - Destroys a cluster and deletes data.
2. `obd cluster redeploy` - Destroys and redeploys a cluster, deleting data.
3. `obd cluster prune-config` - Deletes configuration files of destroyed/configured clusters.

**Always ask the user for confirmation before running these commands.**

## Common Commands

### Quick Start (Demo)
- **Demo Deployment**: Quickly deploy a local demo cluster without a configuration file.
  ```bash
  obd demo
  ```
  - Use `-c` to specify components (e.g., `oceanbase-ce`, `obproxy-ce`, `obagent`). For **OCP** use **`ocp-ce`** by default. If the user explicitly asks for **`ocp-express`**, do not switch components automatically; instead explain that `ocp-express` has been replaced by `obshell dashboard`, and that deploying `oceanbase-ce` directly provides access on port `2886`.
  - Example: `obd demo -c oceanbase-ce,obproxy-ce`
  - **Note**: `obd demo` uses default ports 2881 (MySQL), 2882 (RPC), and 2886 (obshell). If those ports are in use by another OB instance on the same machine, the demo will fail with a port-conflict error. Use a config file with alternate ports in that case.

### Cluster Management

- **Deploy**: Register a configuration and deploy a cluster.
  ```bash
  obd cluster deploy <deploy_name> -c <config_file>
  ```

- **Interactive Deploy**: Interactively configure and deploy a cluster.
  ```bash
  obd cluster deploy <deploy_name> -i
  ```
  *Use this when the user wants to be guided through the configuration process.*

- **Start**: Start a deployed cluster.
  ```bash
  obd cluster start <deploy_name>
  ```

- **Stop**: Stop a running cluster.
  ```bash
  obd cluster stop <deploy_name>
  ```

- **Restart**: Restart a running cluster.
  ```bash
  obd cluster restart <deploy_name>
  ```

- **List**: List all registered clusters.
  ```bash
  obd cluster list
  ```

- **Display**: Show the status of a specific cluster.
  ```bash
  obd cluster display <deploy_name>
  ```

- **Edit Config**: Edit the configuration of a cluster.
  ```bash
  obd cluster edit-config <deploy_name>
  ```

- **Reload**: Reload a running cluster to apply configuration changes.
  ```bash
  obd cluster reload <deploy_name>
  ```

- **Upgrade**: Upgrade a component in a running cluster.
  ```bash
  obd cluster upgrade <deploy_name> -c <component_name> -V <version>
  ```

- **Scale Out**: Scale out a component in a running cluster.
  ```bash
  obd cluster scale_out <deploy_name> -c <config_file>
  ```

- **Add Component**: Add a new component to a running cluster.
  ```bash
  obd cluster component add <deploy_name> -c <config_file>
  ```

- **Delete Component**: Delete a component from a running cluster.
  ```bash
  obd cluster component del <deploy_name> <component_name>
  ```

### Tenant Management

- **Create Tenant**: Create a new tenant.
  ```bash
  obd cluster tenant create <deploy_name> -n <tenant_name> [options]
  ```

- **Drop Tenant**: Drop an existing tenant.
  ```bash
  obd cluster tenant drop <deploy_name> -n <tenant_name>
  ```

- **Show Tenants**: View tenants in the cluster.
  ```bash
  obd cluster tenant show <deploy_name>
  ```

- **Optimize Tenant**: Optimize a tenant for a specific workload (e.g., `express_oltp`, `olap`).
  ```bash
  obd cluster tenant optimize <deploy_name> <tenant_name> -o <workload>
  ```

### Backup & Restore

- **Set Backup Config**: Configure backup paths.
  ```bash
  obd cluster tenant set-backup-config <deploy_name> <tenant_name> -d <data_uri> -a <log_uri>
  ```

- **Backup Tenant**: Start a tenant backup.
  ```bash
  obd cluster tenant backup <deploy_name> <tenant_name>
  ```

- **Restore Tenant**: Restore a tenant from backup.
  ```bash
  obd cluster tenant restore <deploy_name> <tenant_name> <data_uri> <log_uri>
  ```

## SeekDB (obd seekdb)

SeekDB 是 OBD 管理的轻量数据库组件。以下命令**仅对包含 seekdb 组件的部署**生效；对不包含 seekdb 的集群执行会报错。

### SeekDB 安装与接管（行为说明）

- **`obd seekdb install`**：交互式安装单机 SeekDB。**需要真实 TTY 终端**，无法通过管道传入输入自动化；如需脚本化部署，改用 `obd seekdb deploy <name> -c <config>`。
- **`obd seekdb install --primary`**：以主机群模式安装，开启 RPC，供备机同步日志。**同样需要 TTY**。
- **`obd seekdb install --standby`**：以备机群模式安装，从已部署且状态为 **RUNNING** 的 SeekDB 主库列表中选择主库；备机侧用于 redo 的磁盘可用空间需 **不小于主库配置的 `log_disk_size`**。**`--standby` 与 `--primary` 不可同时使用。同样需要 TTY。⚠️ 备库必须部署在与主库不同的 IP 上**；若主备 IP 相同，OBD 会抑制 `--role=STANDBY` 启动参数（同机防冲突逻辑），导致备库以主库模式启动，日志无法同步。
- **⚠️ 非交互式部署无法建立真实主备同步**：`obd seekdb deploy -c config.yaml` 方式即使在 YAML 中设置了 `log_restore_source`，OBD 也不会向 seekdb 进程传入 `--role=STANDBY` 启动参数，备库进程会以主库模式启动，日志无法从主库同步。建立真实主备同步**必须**通过 `obd seekdb install --standby`（需要 TTY）且主备**位于不同 IP**。
- **`obd seekdb list`**：只列出包含 seekdb 组件的部署。
- **`obd seekdb deploy` / `start` / `stop` / `restart` / `display` / `destroy`**：生命周期与普通 OBD 部署相同，但**仅适用于包含 seekdb 的部署**。
- **`obd seekdb takeover`**：接管**并非由 OBD 部署**的已有 SeekDB 实例。必填 **`--home-path`**；还需通过配置或交互提供主机、`mysql_port`、`root` 密码及 SSH 等信息，由 OBD 生成配置并纳入管理。

### SeekDB 主备与高可用（行为说明）

- **`obd seekdb display <name> -g`**：展示集群拓扑（一主多备、级联等）。
- **`obd seekdb switchover <name>`**：**计划内**主备互换：将指定备集群提升为主，原主降为备；要求主集群**仍在线**。
- **`obd seekdb failover <name>`**：**故障**切换：主不可用时将指定备集群提升为主；若主仍处于运行（未 stop），执行会报错，应改用 **switchover**。
- **`obd seekdb decouple <name>`**：将指定备集群从主备关系中解耦，该备变为**独立主**继续运行。
- **`obd seekdb destroy`**：若销毁的是**仍挂有备集群的主**，必须加 **`--ignore-standby`** 才会允许销毁，否则报错并提示风险。

### SeekDB 命令总览

| 命令 | 说明 |
| --- | --- |
| `obd seekdb install` | 交互式安装 SeekDB（单机） |
| `obd seekdb install --standby` | 以备机群模式安装，从已部署且 RUNNING 的 SeekDB 主库列表中选择主库 |
| `obd seekdb install --primary` | 以主机群模式安装（开启 RPC 供备机同步） |
| `obd seekdb list` | 仅列出包含 seekdb 组件的部署 |
| `obd seekdb deploy <name> -c <config>` | 使用配置文件部署指定名称的 SeekDB 集群 |
| `obd seekdb start <name>` | 启动指定 SeekDB 集群 |
| `obd seekdb stop <name>` | 停止指定 SeekDB 集群 |
| `obd seekdb restart <name>` | 重启指定 SeekDB 集群 |
| `obd seekdb display <name>` | 展示指定 SeekDB 集群信息 |
| `obd seekdb display <name> -g` | 展示集群拓扑图（一主多备/级联） |
| `obd seekdb destroy <name>` | 销毁指定 SeekDB 集群；若为主且存在备集群，需加 `--ignore-standby` 才允许销毁 |
| `obd seekdb takeover <name> --home-path <path>` | 接管未由 OBD 部署的已有 SeekDB 实例（必填 `--home-path`，另需 host/port/password 等连接信息） |
| `obd seekdb switchover <name>` | 主备互换：指定备集群提升为主，原主降为备（主须在线） |
| `obd seekdb failover <name>` | 故障切换：主不可用时将指定备集群提升为主；**主未 stop 时执行会报错，不允许 failover** |
| `obd seekdb decouple <name>` | 解耦：将指定备集群从主备关系中脱离，该备变为主（独立运行） |

### SeekDB 安全与约束

- **destroy**：销毁带备集群的主时，必须显式加 `--ignore-standby`，否则报错并提示风险。
- **failover**：仅当主集群已 stop 或不可达时允许执行；主仍存活时应使用 **switchover**。
- `--standby` 与 `--primary` 不可同时指定。备机模式会校验主库 `enable_rpc_service`，未开启时需先重启主或稍后处理。
- **同机部署限制**：主备必须部署在不同 IP 的机器上。若主备 IP 相同，OBD 的同机防冲突逻辑会将 `mock_primary_rpc_info` 置为 None，导致备库进程不传 `--role=STANDBY`，备库以主库模式启动（`ACCESS_MODE=APPEND`），日志无法同步。

## Advanced Scenarios

### OS & Environment Requirements
- **GLIBC**: OceanBase CE 4.3+ el8 packages require GLIBC 2.27+ (RHEL/CentOS 8+ or compatible). AliOS 7 / CentOS 7 ship GLIBC 2.17 — use the **el7 package of OceanBase CE ≤4.3.x** (e.g. `4.3.5.5`) for those OS versions. OBD only needs to run on the control machine; it SSHes to remote nodes to deploy, so remote nodes do not need OBD installed.
- **OCP CE packages**: `ocp-ce` is **not** in the public community mirror by default. It requires an internal or separately provided mirror. Use `obd mirror list` to verify package availability before planning an OCP CE deployment.
- **Port isolation on the same host**: When co-deploying multiple OB stacks on one machine, ensure each uses distinct ports for MySQL (2881), RPC (2882), and obshell (2886). Pass `obshell_port` in the config to override the default 2886.

### OCP Takeover Preparation
Prepare an OBD-deployed cluster to be managed by a **full OCP** instance (**OCP CE** `ocp-ce` or enterprise OCP), not OCP Express.

1.  **Check Conditions**:
    ```bash
    obd cluster check4ocp <deploy_name> -V <ocp_version>
    ```
2.  **Export to OCP**:
    ```bash
    obd cluster export-to-ocp <deploy_name> -a <ocp_address> -u <user> -p <password>
    ```

### Monitoring (Prometheus & Grafana)
You can add GUI-based monitoring to a cluster.
-   **Scenario 1**: If OBAgent is NOT deployed, add `obagent`, `prometheus`, and `grafana` to the config and redeploy/start.
-   **Scenario 2**: If OBAgent IS deployed, add `prometheus` and `grafana` to the config, manually configure Prometheus to scrape OBAgent, and redeploy.
-   **Note**: When OBD deploys Prometheus it enables HTTP basic auth. The generated credentials (admin + random password) are shown in `obd cluster display <name>`. Use those credentials when accessing the Prometheus web UI or API (e.g., `curl -u admin:<password> http://<host>:9090/-/ready`).
-   **Component deletion order**: Components with dependants must be deleted after their dependants. For example, delete `grafana` and `prometheus` before deleting `obagent`; otherwise OBD returns a "still depends" error. Use `obd cluster component del <name> grafana prometheus` together, then `obd cluster component del <name> obagent`.

### Mirror & Repository Management
Manage local and remote package repositories.

-   **List Mirrors**: `obd mirror list [repo_name]`
-   **Update Mirrors**: `obd mirror update`
-   **Clone RPM**: `obd mirror clone <path_to_rpm> [-f]`
-   **Create Mirror**: `obd mirror create -n <name> -p <path> -V <version>`
-   **Enable/Disable**: `obd mirror enable <repo_name>` / `obd mirror disable <repo_name>`
-   **Clean Mirrors**: `obd mirror clean`

### Testing
**Skill 功能测试**：覆盖集群/租户/备份、与 **OCP CE** 对接、镜像与各组件时，按上文 **OCP 术语约定**：默认测 **`ocp-ce`**；若测试需求提到 **`ocp-express`**，应先提示其能力已被 **`obshell dashboard`** 取代，优先改为验证直接部署 OceanBase 社区版后的 `2886` 端口访问能力。

**obd test 压测**：Run built-in tests on the cluster. **Do not install ob-sysbench, obtpch, or obtpcc via yum**: when the machine is online, OBD will automatically pull and install these dependencies when you run the corresponding `obd test` command. For non-interactive execution (e.g. in scripts or CI), set auto-confirm before running tests: `obd env set IO_DEFAULT_CONFIRM 1`. When running a full test suite, **do not abort on first failure**: run all test cases to completion, then produce a single test report summarizing pass/fail/skip and brief notes for each item.

-   **MySQL Test**: Run mysqltest cases.
  ```bash
  obd test mysqltest <deploy_name> --test-set <test_set>
  ```
-   **Sysbench**: Run Sysbench performance tests (OBD auto-installs ob-sysbench when online).
  ```bash
  obd test sysbench <deploy_name> --tenant=<tenant> --script-name=<script>
  ```
-   **TPC-H**: Run TPC-H benchmark (OBD auto-installs obtpch when online). `--remote-tbl-dir` is **required** to specify a directory for TPC-H table files on the server.
  ```bash
  obd test tpch <deploy_name> --tenant=<tenant> --remote-tbl-dir=<server_dir>
  ```
-   **TPC-C**: Run TPC-C benchmark (OBD auto-installs obtpcc when online; Java may still need to be installed separately if missing). Use `--run-mins` (not `--running-minutes`) to cap the run duration.
  ```bash
  obd test tpcc <deploy_name> --tenant=<tenant> --warehouses=<n> --run-mins=<minutes>
  ```

## Usage Examples

### Quick Demo
To quickly start a local demo cluster:
```bash
obd demo
```

### Interactive Deployment
To deploy a cluster named "my-cluster" by answering interactive prompts:
```bash
obd cluster deploy my-cluster -i
```

### Deploying with Config File
To deploy a cluster named "my-cluster" using "config.yaml":
```bash
obd cluster deploy my-cluster -c config.yaml
```

### Explicitly Requesting OCP Express
User: "帮我部署 ocp-express。"
Agent: "`ocp-express` 是轻量版 OCP，但它的能力已经被 `obshell dashboard` 取代。直接部署 OceanBase 社区版后，就可以通过 `2886` 端口访问 dashboard；因此这里不再继续推荐部署 `ocp-express`。"

### Destroying a Cluster (Requires Confirmation)
User: "Destroy the my-cluster cluster."
Agent: "This will destroy the cluster 'my-cluster' and all its data. Are you sure you want to proceed?"
User: "Yes."
Agent:
```bash
obd cluster destroy my-cluster
```

### Redeploying a Cluster (Requires Confirmation)
User: "Redeploy my-cluster."
Agent: "This will destroy and redeploy 'my-cluster', causing data loss. Are you sure?"
User: "Yes."
Agent:
```bash
obd cluster redeploy my-cluster
```
