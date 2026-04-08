# oceanbase-deploy

OceanBase OBD 部署与运维 Skill，供任意 AI Agent 加载使用。加载 `SKILL.md` 之后，直接按下面的提示词提问即可。

源码位置：[`oceanbase/oceanbase-skills`](https://github.com/oceanbase/oceanbase-skills) 的 `skills/oceanbase-deploy/` 目录。

## 快速用法

把 `SKILL.md` 加到 Agent 的规则、系统提示词或项目说明里后，直接描述你的目标。最有效的提问方式是：

- 说清楚你要操作的对象：集群名、租户名、配置文件名、目标版本。
- 说清楚你要做的动作：部署、启动、停止、扩容、备份、压测、接管。
- 如果是高风险操作，明确是否允许销毁数据。

例如，不要只说：

```text
帮我处理一下 OceanBase
```

更推荐这样说：

```text
用 obd 部署一个名为 test-cluster 的 OceanBase 社区版集群，配置文件是 config.yaml
```

## 13 个最常用提示词

下面这些提示词可以直接复制给 Agent。

1. 部署 OceanBase 开源版本

```text
部署一个本机 OceanBase 开源版本，能快速跑起来就行
```

2. 用 `obd demo` 快速起演示环境

```text
用 obd demo 快速部署一个本机演示环境
```

3. 用配置文件部署集群

```text
用 config.yaml 部署一个名为 test-cluster 的 OceanBase 社区版集群
```

4. 交互式部署

```text
交互式部署一个 OceanBase 集群，名字叫 demo-cluster
```

5. 安装 / 部署 OCP

```text
帮我部署 OCP
```

说明：默认会按 `OCP CE` 处理，不会默认切到 `ocp-express`。

6. 启动并检查状态

```text
帮我直接启动 test-cluster，并检查启动后状态
```

7. 停止集群

```text
停止 test-cluster 集群
```

8. 创建租户

```text
在 test-cluster 上创建一个名为 mysql 的租户
```

9. 配置并执行备份

```text
给 test-cluster 上的 mysql 租户配置备份路径并执行一次备份
```

10. 部署并启动 SeekDB

```text
部署并启动一个 SeekDB 实例
```

11. 创建 SeekDB 主备集群

```text
创建一个 SeekDB 主备集群，并告诉我主库和备库分别怎么部署
```

12. 查看 SeekDB 主备切换建议

```text
查看 seekdb-test 的拓扑，如果主库挂了该用 switchover 还是 failover
```

13. 运行压测

```text
对 test-cluster 的 mysql 租户跑一个 sysbench 测试
```

## 其他常见提示词

```text
查看 test-cluster 当前状态，并告诉我有没有异常
```

```text
查看 test-cluster 上有哪些租户
```

```text
对 test-cluster 执行 mysqltest，测试集是 basic
```

```text
跑一遍这个 Skill 涵盖的 OBD 功能测试，并输出测试报告
```

```text
帮我部署 OCP 社区版
```



## 提问建议

- 想让 Agent 直接执行时，明确说“帮我执行”。
- 想先看方案时，明确说“先不要执行，只给我命令和步骤”。
- 涉及销毁、重建、故障切换时，明确说“我确认允许高风险操作”或“先不要执行破坏性命令”。

## 三种推荐问法

### 1. 先要方案，不立即执行

```text
我要部署一个三节点 OceanBase 社区版集群，先不要执行，只给我 obd 配置建议和命令
```

### 2. 允许 Agent 直接操作

```text
帮我直接启动 test-cluster，并检查启动后状态
```

### 3. 高风险操作前要求确认

```text
我要重建 test-cluster，但在你执行 destroy 或 redeploy 前必须先征求我确认
```

## 文件说明

| 文件 | 说明 |
|------|------|
| `SKILL.md` | 供 Agent 实际加载的主说明文件 |
| `README.md` | 面向用户的使用说明与提示词示例 |

## License

MIT
