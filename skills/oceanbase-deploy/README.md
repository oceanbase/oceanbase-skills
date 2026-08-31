# oceanbase-deploy

OceanBase Community Edition 的 OBD 部署与运维 Skill 集合。此分支只保留已经完成正式测试的工作流，并以当前安装的 OBD、插件、仓库和制品能力为准。

源码位置：[`oceanbase/oceanbase-skills`](https://github.com/oceanbase/oceanbase-skills) 的 `skills/oceanbase-deploy/` 目录。

## Skill 列表

| Skill | 功能 |
|---|---|
| [`oceanbase-deploy`](./) | 总入口：识别目标、能力和执行模式，并路由到具体 skill |
| [`cluster-management`](./cluster-management/) | 社区版集群部署、多节点最大化资源规格、配置、生命周期、升级、组件、Config Server、监控和网络接入 |
| [`obd-administration`](./obd-administration/) | 已测试的 OBD 安装升级/回滚、镜像仓库、动态工具、Trace 证据和运行状态 |
| [`tenant-management`](./tenant-management/) | 租户创建、删除、优化、备份恢复和物理主备 |
| [`testing-and-benchmark`](./testing-and-benchmark/) | Sysbench、TPC-H、TPC-C 和 mysqltest |
| [`obdiag-diagnostics`](./obdiag-diagnostics/) | 按实际安装能力使用 obdiag 做采集、分析、巡检和根因定位 |

当前版本已删除的工作流统一标记为“当前 Skill 版本不支持”；这只描述本 Skill 的覆盖范围，不代表 OBD 产品本身不具备相应能力。完整清单见 [`current-version-unsupported.md`](./references/current-version-unsupported.md)。

> 更多 skill 持续开发中，计划覆盖：内核调优、SQL 诊断、数据迁移等。

---

## 安装方式

### skills.sh 一键安装（推荐）

```bash
npx skills add oceanbase/oceanbase-skills --skill oceanbase-deploy
```

`npx skills add` 会自动识别 Claude Code、Cursor、Windsurf 等支持的 Agent，并安装完整的 `oceanbase-deploy` bundle。

### 手动安装（克隆后复制）

克隆仓库后复制完整目录，以便固定和校验所用 Skill 版本。不要只复制根 `SKILL.md`，它需要子 Skill 和 `references/`。

```bash
git clone https://github.com/oceanbase/oceanbase-skills.git
cd oceanbase-skills
mkdir -p .claude/skills
cp -R skills/oceanbase-deploy .claude/skills/
```

Cursor 和 Windsurf 可分别使用 `.cursor/skills/`、`.windsurf/skills/`。克隆方式可固定并校验所用 skill 版本。

### 在 GitHub 上浏览 skill

在仓库中检查完整 bundle 及其目录结构：

```text
https://github.com/oceanbase/oceanbase-skills/tree/master/skills/oceanbase-deploy
```

---

## Agent 集成

### Claude Code

使用上方 [skills.sh 一键安装](#skillssh-一键安装推荐)，或把完整的 `skills/oceanbase-deploy/` 目录复制到 `.claude/skills/oceanbase-deploy/`。

### Cursor

```bash
npx skills add oceanbase/oceanbase-skills --skill oceanbase-deploy
```

也可克隆后把完整目录复制到 `.cursor/skills/`。

### Windsurf

使用支持完整 Skill 目录的安装方式，把 bundle 放入 `.windsurf/skills/`；不要仅粘贴根文件。

### 其他 Agent

仅当集成方式能保留并解析完整的 `oceanbase-deploy/` 目录树时使用本 bundle。只接受单个规则文件的平台无法安全加载这个路由式 Skill。

---

## 常用提示词

先说明希望 Agent 做到哪一步：

- “只解释”“只审查配置”“只给方案”：保持只读，不部署、不安装工具。
- “诊断”：先采集最小必要证据；安装诊断工具或执行高开销采集需要单独确认。
- “执行”：在变更前展示目标、影响、风险和验收方法；破坏性操作需针对具体对象明确授权。

### 集群管理

```text
在三台机器上部署社区版三节点集群；未指定规格时使用最大化资源配置。
```

```text
将现有社区版集群按当前 OBD 证明的路径执行滚动升级。
```

```text
为已有集群补充 Prometheus 和 Grafana，先检查拓扑、端口和变更影响。
```

### 租户管理

```text
在 test-cluster 创建生产租户，先给出资源、白名单和验收计划。
```

```text
对 mysql 租户运行 Sysbench；不要自动修改租户参数，先做前置检查。
```

```text
用 obdiag 诊断最近一次启动失败；如果工具缺失，按已测试的控制机下载与动态工具安装流程处理。
```

### 压测

```text
对 test-cluster 的 mysql 租户跑一个 sysbench 测试
```

```text
给我跑 TPC-H 的完整命令和参数
```

---

## 提问建议

- 想让 Agent 直接执行 → 说 **“帮我执行”**。
- 想先看方案 → 说 **“先不要执行，只给我命令和步骤”**。
- 涉及销毁、重建、故障切换等高影响操作时，先让 Agent 展示具体对象、当前状态、准确动作、影响和恢复边界，再只确认这一项已展示的操作；提前或笼统授权无效。

## 兼容性原则

- 不把源码中存在的能力当成当前已安装版本必然可用的能力。
- 不凭空补写组件名、配置字段或版本范围；优先读取本机帮助、插件元数据和仓库元数据。
- 命令成功不等于任务完成；还需验证拓扑、服务、控制面和数据面结果。

## License

[Apache License 2.0](./LICENSE)
