---
name: ob-deploy
description: Manage OceanBase clusters using obd. Supports deploying (including interactive mode), starting, stopping, destroying, redeploying, upgrading, and testing clusters; SeekDB (obd seekdb) install/takeover, primary-standby switchover/failover/decouple. OCP defaults to ocp-ce; ocp-express only when explicitly requested. Also covers OCP takeover and monitoring.
---

# OceanBase Deployer (obd)

## Overview
This skill allows you to manage OceanBase clusters using the `obd` command-line tool. You can deploy, start, stop, destroy, and redeploy clusters.

For a quick start guide on deploying OceanBase Community Edition, refer to the official documentation:
[https://www.oceanbase.com/docs/common-obd-cn-1000000005246289](https://www.oceanbase.com/docs/common-obd-cn-1000000005246289)

## Installation
If `obd` is not installed, you can download the RPM package from the OceanBase mirror repository:
[https://mirrors.oceanbase.com/community/stable/el/](https://mirrors.oceanbase.com/community/stable/el/)

## OCP 术语约定（必读）
- 用户说 **「部署 OCP」「OCP」「上 OCP」** 等且**未**单独说明时，一律指 **OCP 社区版（OCP CE）**，在 OBD 配置里使用组件 **`ocp-ce`**（按官方 OCP CE 部署文档与示例 YAML 编写依赖与 `global` 参数）。
- **`ocp-express`** 是**轻量 Web 控制台**，与 OCP CE 不同。**仅当用户明确要求**「OCP Express」「ocp-express」「轻量 OCP / express」等时，才部署或推荐 `ocp-express`。
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
  - Use `-c` to specify components (e.g., `oceanbase-ce`, `obproxy-ce`, `obagent`). For **OCP** use **`ocp-ce`** unless the user explicitly asked for **`ocp-express`**.
  - Example: `obd demo -c oceanbase-ce,obproxy-ce`

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

- **`obd seekdb install`**：交互式安装单机 SeekDB。
- **`obd seekdb install --primary`**：以主机群模式安装，开启 RPC，供备机同步日志。
- **`obd seekdb install --standby`**：以备机群模式安装，从已部署且状态为 **RUNNING** 的 SeekDB 主库列表中选择主库；备机侧用于 redo 的磁盘可用空间需 **不小于主库配置的 `log_disk_size`**。**`--standby` 与 `--primary` 不可同时使用。**
- **`obd seekdb list`**：只列出包含 seekdb 组件的部署。
- **`obd seekdb deploy` / `start` / `stop` / `restart` / `display` / `destroy`**：生命周期与普通 OBD 部署相同，但**仅适用于包含 seekdb 的部署**。
- **`obd seekdb takeover`**：接管**并非由 OBD 部署**的已有 SeekDB 实例。通过配置、命令行参数或交互补齐主机、`mysql_port`、`root` 密码、SSH 及实例目录等信息后，由 OBD 生成配置并纳入管理；不同 OBD 构建对必填项的暴露方式可能不同。

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
| `obd seekdb takeover <name>` | 接管未由 OBD 部署的已有 SeekDB 实例（通过命令行参数、配置或交互补齐 host/port/password/实例目录等连接信息） |
| `obd seekdb switchover <name>` | 主备互换：指定备集群提升为主，原主降为备（主须在线） |
| `obd seekdb failover <name>` | 故障切换：主不可用时将指定备集群提升为主；**主未 stop 时执行会报错，不允许 failover** |
| `obd seekdb decouple <name>` | 解耦：将指定备集群从主备关系中脱离，该备变为主（独立运行） |

### SeekDB 安全与约束

- **destroy**：销毁带备集群的主时，必须显式加 `--ignore-standby`，否则报错并提示风险。
- **failover**：仅当主集群已 stop 或不可达时允许执行；主仍存活时应使用 **switchover**。
- `--standby` 与 `--primary` 不可同时指定。备机模式会校验主库 `enable_rpc_service`，未开启时需先重启主或稍后处理。

### SeekDB 提测验收要点（内联摘要，无外链）

以下内容来自 OBD SeekDB 相关提测说明的归纳，便于验收与写自动化用例；**不包含任何语雀或其它文档 URL**。

**A. 部署与安装类**

- 能力范围：`obd seekdb` 子命令仅作用于**含 seekdb 组件**的部署；`obd seekdb list` 只列出这类部署。
- **install**：支持单机（Standalone）、主机群（`--primary`）、备机群（`--standby`）；`--standby` 与 `--primary` 不可同时指定。
- **备机 install**：从已部署且 **RUNNING** 的 SeekDB 主库列表选主库，拉取 IP、`mysql_port`、`root_password`，校验主库 `enable_rpc_service`；未开启时可选：立即重启主、稍后处理、还原改动。
- **采集与校验**：安装 IP、OS 用户、密码、`home_path`、`data_dir`、`redo_dir`、`mysql_port`（默认 2881）、`rpc_port`（主/备默认 2882）、是否开机自启；端口占用、目录与空间等需校验。redo 目录可用空间须 **≥2GB 或 ≥ 主库 `log_disk_size`**；本机可用内存 **≥1GB**；SSH 可达。
- **运行模式**：总内存 <5GB 仅可选 Dev；Prod 下内存策略含平衡（Soft 50% / Hard 90%）与性能（Soft 90% / Hard 90%）；Base 内存可手输或默认（总内存×90%），**Hard 由 Base×90% 推算，不再单独输入**。
- **集群名**：流程中录入的名称须唯一；已存在且非 DESTROYED 不可复用，DESTROYED 可复用。
- **takeover**：`obd seekdb takeover <name>` 用于接管已有实例；实例目录、host、`mysql_port`、`root` 密码、SSH 等信息可通过命令行参数、配置或交互提供。OBD 会据此发现版本、`data_dir`、`redo_dir`、`memory_limit`、`log_disk_size`、`enable_rpc_service`、`rpc_port` 等并生成 OBD 配置。

**B. 主备与高可用类（命令面）**

- 涉及命令：`switchover`、`failover`、`decouple`、`display -g`、`destroy`（含带备销毁约束）。
- **拓扑**：`obd seekdb display <name> -g` 应能展示一主多备、级联等；需在**级联与一主多备**场景下覆盖。
- **switchover**：计划内切换；原主变备、原备变主；多备时原主下的备挂到新主下，原备下的备挂到新备下。
- **decouple**：指定备脱离主备关系后变为**独立主**继续运行；一主一备、级联、一主多备场景均需覆盖。
- **failover**：主**未** stop 且仍可达时执行 failover **应拒绝**，并提示使用 switchover；主 stop 或不可达后 failover 可成功。
- **destroy**：正常销毁应清理主备关系相关元数据；文档还提到清理 **`/tmp/.seekdb_ca/<集群名>`** 下 CA 目录等侧效应（以实际 OBD 版本行为为准）。带备集群的 **主** 执行 destroy 须 **`--ignore-standby`**，否则报错。

**C. 自动化脚本**

- 仓库内 `run-seekdb-tice-tests.sh`：对可非交互验证的项做巡检；交互式 install、多机主备等需目标环境已部署后通过环境变量指定集群名并（可选）打开变更类开关再跑。

## Advanced Scenarios

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

### Mirror & Repository Management
Manage local and remote package repositories.

-   **List Mirrors**: `obd mirror list [repo_name]`
-   **Update Mirrors**: `obd mirror update`
-   **Clone RPM**: `obd mirror clone <path_to_rpm> [-f]`
-   **Create Mirror**: `obd mirror create -n <name> -p <path> -V <version>`
-   **Enable/Disable**: `obd mirror enable <repo_name>` / `obd mirror disable <repo_name>`
-   **Clean Mirrors**: `obd mirror clean`

### Testing
**Skill 功能测试**：测试本 SKILL 所描述的全部 OBD 能力（集群管理、租户、备份、与 OCP CE 对接、镜像、obproxy/obagent/Grafana 等），而不仅是 `obd test` 压测。仓库内 `ob-16g-full-11.124.9.67.yaml` 含 **`ocp-express`**（仅用于覆盖轻量控制台场景）；若用户要测 **OCP CE**，应使用含 **`ocp-ce`** 的配置。可使用 `run-skill-features-test-11.124.9.67.sh` 与上述 YAML 在目标机上跑一遍并生成报告。

**SeekDB 提测巡检**：`run-seekdb-tice-tests.sh` — 对齐上文「SeekDB 提测验收要点」中的可自动化项；多机 switchover/failover/decouple 等需设置 `SEEKDB_MASTER` / `SEEKDB_STANDBY`（及可选 `SEEKDB_ALLOW_MUTATE=1`）在已部署 SeekDB 主备的环境上执行。

**obd test 压测**：Run built-in tests on the cluster. **Do not install ob-sysbench, obtpch, or obtpcc via yum**: when the machine is online, OBD will automatically pull and install these dependencies when you run the corresponding `obd test` command. For non-interactive execution (e.g. in scripts or CI), set auto-confirm before running tests: `obd env set IO_DEFAULT_CONFIRM 1`. When running a full test suite, **do not abort on first failure**: run all test cases to completion, then produce a single test report summarizing pass/fail/skip and brief notes for each item.

-   **MySQL Test**: Run mysqltest cases.
    ```bash
    obd test mysqltest <deploy_name> --test-set <test_set>
    ```
-   **Sysbench**: Run Sysbench performance tests (OBD auto-installs ob-sysbench when online).
    ```bash
    obd test sysbench <deploy_name> --tenant=<tenant> --script-name=<script>
    ```
-   **TPC-H**: Run TPC-H benchmark (OBD auto-installs obtpch when online).
    ```bash
    obd test tpch <deploy_name> --tenant=<tenant>
    ```
-   **TPC-C**: Run TPC-C benchmark (OBD auto-installs obtpcc when online; Java may still need to be installed separately if missing).
    ```bash
    obd test tpcc <deploy_name> --tenant=<tenant>
    ```

## Usage Examples

### Example 1: Quickly deploy a local demo cluster
User: "帮我快速起一个本机 OceanBase 演示环境。"
Agent:
```bash
obd demo
```

### Example 2: Deploy with interactive prompts
User: "我想交互式部署一个集群，名字叫 my-cluster。"
Agent:
```bash
obd cluster deploy my-cluster -i
```

### Example 3: Deploy from a config file
User: "用 config.yaml 部署 my-cluster。"
Agent:
```bash
obd cluster deploy my-cluster -c config.yaml
```

### Example 4: Check cluster status before further actions
User: "看看 my-cluster 现在是不是正常运行。"
Agent:
```bash
obd cluster display my-cluster
```

### Example 5: OCP defaults to OCP CE
User: "帮我部署 OCP。"
Agent: "未特别说明时，`OCP` 默认按 `OCP CE` 处理，也就是配置组件 `ocp-ce`，不会默认使用 `ocp-express`。如果你确认要部署轻量版控制台，我再改成 `ocp-express`。"

### Example 6: Explicitly requested OCP Express
User: "我要装 OCP Express，不是 OCP CE。"
Agent: "已按 `ocp-express` 处理；这是轻量控制台，不等同于完整 OCP。后续配置和组件选择都会使用 `ocp-express`。"

### Example 7: Destructive destroy requires confirmation
User: "把 my-cluster 删掉。"
Agent: "这会执行 `obd cluster destroy my-cluster`，会销毁集群并删除数据。请确认是否继续。"
User: "确认。"
Agent:
```bash
obd cluster destroy my-cluster
```

### Example 8: Redeploy requires confirmation
User: "重建 my-cluster。"
Agent: "这通常对应 `obd cluster redeploy my-cluster`，会先销毁再重新部署，数据会丢失。请确认是否继续。"
User: "继续。"
Agent:
```bash
obd cluster redeploy my-cluster
```

### Example 9: SeekDB switchover vs failover
User: "把 seekdb-standby 切成主。"
Agent: "如果当前主库仍在线，应执行计划内切换 `switchover`；只有主库不可达或已停机时，才应执行 `failover`。我会先确认当前主库状态，再选择正确命令。"

### Example 10: Run benchmark tests without manual yum install
User: "对 test-cluster 的 mysql 租户跑个 sysbench。"
Agent: "我会直接使用 `obd test sysbench`。在线环境下不需要先手动 `yum install ob-sysbench`，OBD 会自动拉取所需依赖。"
Agent:
```bash
obd test sysbench test-cluster --tenant=mysql --script-name=oltp_read_write.lua
```
