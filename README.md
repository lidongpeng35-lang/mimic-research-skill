# MIMIC Research Skill

[![CI](https://github.com/lidongpeng35-lang/mimic-research-skill/actions/workflows/ci.yml/badge.svg)](https://github.com/lidongpeng35-lang/mimic-research-skill/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![MIMIC-IV](https://img.shields.io/badge/Data-MIMIC--IV-informational.svg)](https://mimic.mit.edu/docs/IV/)

面向 MIMIC-IV 回顾性临床研究的数据提取 Skill / Agent Plugin / Codex Plugin / Claude Code Plugin。

它保留轻量 MIMIC Skill 常见的 `SKILL.md + references/` 体验，但把重点从“让模型直接写一段 SQL”提升到：**概念解析 → 版本化研究 Contract → SQL/provenance → 确认 → Preview/QC → 受控导出**。

> 目标不是让 SQL 看起来能跑，而是让 cohort、变量定义、时间窗、聚合、单位、缺失处理和输出粒度都可审计、可复现、可写进论文 Methods/Supplement。

## 为什么做这个项目

MIMIC 研究中高风险错误往往不是 SQL 语法，而是研究语义：错误 `itemid`/ICD、MIMIC-III/IV 混用、错误 analysis unit/time zero、隐式 first/max/mean、单位混合、错误 specimen、或 one-to-many join 改变 cohort。

因此本项目坚持：

- 不凭模型记忆发明 itemid / ICD / table / unit / score formula；
- 先定义研究语义，再生成 SQL；
- 未指定 aggregation 时优先保留 raw event；
- “字典命中”不等于“临床定义已验证”；
- Preview 与 Export 分离；
- revision 后旧 Preview/approval 失效；
- 无数据库时 fail closed，不伪造患者行、样本量、missingness 或 export receipt。

## 当前公开版能力

| 能力 | 状态 |
|---|---|
| MIMIC-IV schema / vital / lab / diagnosis references | ✅ |
| medications / procedures / scores / outcomes references | ✅ |
| cohort design / QC / provenance / security guidance | ✅ |
| starter semantic registry | ✅，当前为可审计 starter definitions |
| 自然语言研究请求 → Contract 结构 | ✅ |
| Contract / SQL SHA-256 | ✅ |
| 15-tool stdio MCP | ✅ |
| confirmation / revision state machine | ✅ |
| Preview / Export fail-closed gate | ✅ |
| 精确 `确认导出` 授权规则 | ✅ |
| unrestricted patient SQL execution | ❌，明确禁止 |
| publication-grade definition certification | ❌，需逐研究验证 |
| eICU | ❌，不在本仓库范围 |

当前 `resources/registry.json` 是公开 starter registry。定义默认标记为 `candidate`；**registered/executable 不等于 publication-validated**。后续扩展应通过 provenance + regression/acceptance review，而不是直接增加“看起来像”的代码或 itemid。

## 工作流

```text
研究问题
  ↓
概念检索 / provenance resolution
  ↓
完整 versioned Contract
  ↓
SQL scaffold + Contract hash + SQL hash
  ↓
研究者确认当前 revision
  ↓
受控 Preview（仅在 reviewed read-only executor 可用时）
  ↓
QC / revision loop
  ↓
精确收到“确认导出”
  ↓
CSV + receipt
```

## 安装

### OpenClaw / Skill 模式

```bash
openclaw skills install git:lidongpeng35-lang/mimic-research-skill@main
```

### Claude Code

```bash
git clone https://github.com/lidongpeng35-lang/mimic-research-skill.git
cd mimic-research-skill
python3 scripts/launch_mcp.py --doctor
claude --plugin-dir .
```

### Codex / Agent Plugins

仓库同时提供：

- `plugin.json`：portable plugin manifest
- `mcp.json`：portable MCP config
- `.codex-plugin/plugin.json`：Codex compatibility surface
- `.claude-plugin/plugin.json`：Claude Code manifest
- `skills/mimic-research/SKILL.md`：packaged Agent Skill

## 数据库安全

真实患者 Preview 必须使用授权的 MIMIC 安装和独立 read-only PostgreSQL role。连接信息只通过环境变量或安全 secret manager 提供：

```bash
export PGHOST=localhost
export PGPORT=5432
export PGDATABASE=mimiciv
export PGUSER=readonly_user
export PGPASSWORD='...'
```

运行：

```bash
python3 scripts/launch_mcp.py --doctor
```

当前公开 scaffold 故意不启用 unrestricted patient executor；当没有经过审核的只读执行器时，`mimic_run_preview` 会 fail closed。这比悄悄执行未经验证的 SQL 更适合科研工作流。

## MCP tools

公开 runtime 暴露 15 个工具：

`mimic_system_status`, `mimic_v2_search`, `mimic_v2_compile`, `mimic_start_resolution`, `mimic_continue_resolution`, `mimic_run_preview`, `mimic_export`, `mimic_status`, `mimic_inspect`, `mimic_retry`, `mimic_cancel`, `mimic_list_requests`, `mimic_validate_contract`, `mimic_get_provenance`, `mimic_get_flowchart`。

所有工具 schema 对未声明字段 fail closed。

## References

与 `yongfanbeta/mimic-skill` 相同的核心入口全部保留：

- `references/schema.md`
- `references/vital_signs.md`
- `references/labs.md`
- `references/diagnoses.md`
- `references/common_queries.md`

我们另外增加：

- `references/medications.md`
- `references/procedures.md`
- `references/scores.md`
- `references/outcomes.md`
- `references/cohort_design.md`
- `references/quality_control.md`
- `references/provenance.md`
- `references/python_usage.md`
- `references/runtime.md`
- `references/security.md`

## 使用示例

```text
请在 MIMIC-IV 中构建 ICU 脓毒症队列：年龄 ≥65 岁，排除 RRT；
以 ICU 入科为 time zero，提取 0–24 h lactate 首次值、SOFA 最大值、
去甲肾上腺素暴露和 28 天死亡。先给我完整 Contract，不要直接执行患者数据。
```

正确行为是先解析 sepsis、RRT、lactate、SOFA、norepinephrine、mortality 的定义和时序语义。如果某个概念未在 registry 中得到唯一、可信映射，就保持 unresolved，而不是凭记忆补一个 itemid/ICD。

## 论文复现建议

论文/Supplement 建议冻结：

- cohort rule 与每一步纳排数量；
- analysis unit / ICU-selection rule；
- index time / time-window boundary；
- source table/view / code / itemid / unit / specimen；
- aggregation / tie-breaking / missingness；
- Contract revision + SHA-256；
- SQL SHA-256；
- repo release/commit；
- definition provenance 与 QC summary。

## 自检

```bash
python3 scripts/validate_repo.py
python3 scripts/launch_mcp.py --doctor
```

GitHub Actions 会在 push / pull request 时自动检查 repository structure、JSON manifests、registry size、MCP initialize、15-tool discovery 和 schema fail-closed 规则。

## 边界

- MIMIC-IV core 与 MIMIC-IV-ED / Note / CXR / ECG 是不同数据产品，不假设全部已安装。
- MIMIC timestamps 经过去标识化偏移，不解释为真实患者日历时间/时区。
- MIMIC-IV ICU key 是 `stay_id`，不要混用 MIMIC-III 的 `icustay_id`。
- 本仓库不包含患者数据、PhysioNet 凭据或数据库密码。
- MIT License 仅适用于本软件，不改变 PhysioNet/MIMIC 数据使用协议。

## 来源与致谢

主要技术来源应追溯到：MIMIC-IV 官方文档、PhysioNet MIMIC-IV 数据说明、MIT-LCP MIMIC Code，以及仓库内记录的 provenance。

仓库的轻量展示结构参考了 `yongfanbeta/mimic-skill`；其示例 SQL **不作为本项目临床定义或执行权威**。详见 `ACKNOWLEDGEMENTS.md`。

## Contributing / Citation / Security

- `CONTRIBUTING.md`
- `SECURITY.md`
- `CITATION.cff`
- `CHANGELOG.md`

MIT License.
