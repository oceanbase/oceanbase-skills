---
name: testing-and-benchmark
description: Run OceanBase functional tests and performance benchmarks through obd test, including mysqltest, Sysbench, TPC-H, and TPC-C. Use for correctness testing, benchmark preparation, load execution, result analysis, or cleanup. Do not use for ordinary tenant or cluster lifecycle work.
compatibility: Requires the complete oceanbase-deploy bundle, a compatible OBD controller, a running supported OceanBase test deployment and tenant, and separately approved test-tool installation when needed.
metadata:
  author: oceanbase
  version: "3.0"
---

<!-- Compatibility anchors retained for published 2.x deep links. -->
<a id="oceanbase-testing-benchmark-obd-test"></a>
<a id="oceanbase-testing--benchmark-obd-test"></a>
<a id="when-to-use-this-skill"></a>
<a id="important-rules"></a>
<a id="test-commands"></a>
<a id="mysql-test-functional"></a>
<a id="sysbench-benchmark"></a>
<a id="tpc-h-benchmark"></a>
<a id="tpc-h-benchmark-1"></a>
<a id="tpc-c-benchmark"></a>
<a id="tpc-c-benchmark-1"></a>
<a id="usage-examples"></a>
<a id="sysbench-quick-test"></a>
<a id="skill-functional-test"></a>
<a id="related-skills"></a>

# OceanBase Testing and Benchmarking

Read [common-workflow.md](references/common-workflow.md) for every test. Then read exactly the selected tool reference:

| Test | Required reference |
|---|---|
| Sysbench | [sysbench.md](references/sysbench.md) |
| TPC-H | [tpch.md](references/tpch.md) |
| TPC-C | [tpcc.md](references/tpcc.md) |
| mysqltest | [mysqltest.md](references/mysqltest.md) |

## Shared Gates

- Before selecting syntax, plugins, or artifacts, read [product and capability resolution](../references/product-and-capability-resolution.md).
- Before any live controller/host/deployment query, SSH/SQL/API/network access, tool discovery that may install, data preparation, parameter change, external action, or load execution, read the [operation contract](../references/operation-contract.md).
- Before reporting a test successful, read the [completion criteria](../references/completion-criteria.md).
- After a failed, timed-out, interrupted, or mixed run, read [failure recovery and evidence](../references/failure-recovery-and-evidence.md) before retrying or cleaning.
- Before removing a dataset, database object, generated file, tool, cache, or result, read [cleanup and ownership boundaries](../references/cleanup-boundaries.md).

## Hard Boundaries

- Benchmark preparation and workload execution can create, update, or delete tenant data. Use an approved test tenant and dataset; do not infer permission to load a production tenant.
- For Sysbench, TPC-H, and TPC-C, pass the installed command's long optimization option explicitly. Use the no-OBD-optimization level for the default baseline; any parameter mutation or restart requires separate authorization. Do not add this benchmark-only option to mysqltest.
- For Sysbench, TPC-H, and TPC-C, keep the built-in cluster status check enabled unless the user explicitly accepts a reviewed equivalent check. MySQLtest has a different option set. Never reuse a short option from a deployment command in an `obd test` command.
- Tool availability, tool installation, test preparation, test execution, result collection, and cleanup are separate stages and permissions.
- Inventory every required test binary before invoking `obd test`; supported OBD builds can install missing tools, JRE, OBClient, links, or profile entries as part of the test path. Stop for separate installation authorization rather than using the test command as discovery.
- For mysqltest, keep the installed long option equivalent to `--disable-reboot` enabled unless the user separately authorizes the exact snapshot/redeploy behavior. In verified current plugins, an ordinary failed case can otherwise lead to a forced redeploy even without auto-retry.
- Do not put database passwords in reusable commands, output, or reports.

For tenant creation or backup, use [tenant-management](../tenant-management/SKILL.md). For deployment, component, or cluster lifecycle work, use [cluster-management](../cluster-management/SKILL.md).
