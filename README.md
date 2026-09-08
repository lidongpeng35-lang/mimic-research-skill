# MIMIC Research Skill

[![CI](https://github.com/lidongpeng35-lang/mimic-research-skill/actions/workflows/ci.yml/badge.svg)](https://github.com/lidongpeng35-lang/mimic-research-skill/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Agent Plugins 1.0.0](https://img.shields.io/badge/Agent%20Plugins-1.0.0-informational.svg)](plugin.json)
[![MIMIC-IV](https://img.shields.io/badge/Data-MIMIC--IV-informational.svg)](https://mimic.mit.edu/docs/IV/)

面向 MIMIC-IV 回顾性临床研究的数据提取 Skill / Agent Plugin / Codex Plugin / Claude Code Plugin。

它保留轻量 MIMIC Skill 常见的 `SKILL.md + references/` 使用体验，同时增加：可执行语义注册表、版本化研究 Contract、SQL compiler、受控 Preview、质量检查、provenance、revision-aware approval，以及显式确认后的 CSV/XLSX 导出。

> 核心目标不是“让模型凭记忆写一段能跑的 SQL”，而是把研究问题转换为可审计、可复现、可修订、可用于论文 Methods/Supplement 的数据提取规格。

## 为什么做这个项目

MIMIC 研究最常见的高风险错误通常不是 SQL 语法错误，而是研究语义错误：错误的 `itemid`/ICD、MIMIC-III 与 IV 混用、错误时间窗、错误分析单位、无意的 join 扩增、未经说明的 first/max/mean、单位混合、或把“代码能运行”误当成“临床定义已验证”。

本项目把这些选择显式化并进入版本化 Contract，再由注册定义和 compiler 生成 SQL。患者数据执行与最终导出分别经过 Preview/QC 和授权门控。

## 当前能力快照

| 能力 | 状态 |
|---|---|
| 生命体征、实验室、诊断/合并症 | ✅ |
| 药物、ICU infusion、输入/输出、尿量 | ✅ |
| 手术/操作/治疗 | ✅ |
| SOFA、SAPS II、OASIS、LODS、Charlson 等派生概念 | ✅，仅限已登记定义 |
| ICU/住院死亡及时间化结局 | ✅ |
| raw event 与显式 first/min/max/mean/median 聚合 | ✅ |
| 自然语言 → 研究 Contract → SQL | ✅ |
| SQL + read-only Python wrapper | ✅ |
| 语义检索/定义注册表 | ✅ |
| 版本化 Contract + SQL hash | ✅ |
| 15-tool MCP runtime | ✅ |
| Preview gate + QC | ✅ |
| revision 后旧 approval 失效 | ✅ |
| CSV/XLSX export gate | ✅，当前 revision Preview 后且精确确认 |
| eICU | ❌，不在本仓库范围 |
| 下游统计建模/因果推断 | ❌，属于提取后的分析阶段 |

当前 runtime index 包含 **359 个可检索的指标/队列过滤条目**（303 indicators + 56 cohort filters），并附带 **20 个 acceptance cases**。研究定义资源中当前有 **263 个 measurement definitions**；其中 262 个标记为 `candidate`、1 个为 `quarantined`。这意味着“已登记/可执行”不等于“已经对所有论文场景完成独立临床验证”。定义成熟度见 [`docs/DEFINITION_LIFECYCLE.md`](docs/DEFINITION_LIFECYCLE.md)。

## 工作流

```text
研究问题
  ↓
概念检索 + provenance / candidate resolution
  ↓
完整、版本化 Contract
  ↓
compiler → SQL + hash
  ↓
研究者确认当前 revision
  ↓
受控 Preview
  ↓
QC / revision loop
  ↓
精确收到“确认导出”
  ↓
CSV/XLSX + export receipt
```

任何条件修改都会产生新的 revision，并使旧 Preview/approval 失效。

## 安装

### 1. OpenClaw：Skill 模式

Git 安装要求仓库根目录存在 `SKILL.md`，本仓库保留了该入口：

```bash
openclaw skills install git:lidongpeng35-lang/mimic-research-skill@main
```

OpenClaw Skill 模式优先用于研究规格、references、概念检索和 SQL 设计。若宿主没有加载本仓库 MCP server，不得把静态结果声称为已执行患者数据查询。

### 2. Claude Code

```bash
git clone https://github.com/lidongpeng35-lang/mimic-research-skill.git
cd mimic-research-skill
python3 scripts/bootstrap_catalog.py
python3 scripts/launch_mcp.py --doctor
claude --plugin-dir .
```

Claude Code 使用 `.claude-plugin/plugin.json`，Skill 位于 `skills/mimic-research/SKILL.md`，MCP launcher 使用 `${CLAUDE_PLUGIN_ROOT}`。持久状态优先写入宿主提供的 `CLAUDE_PLUGIN_DATA`。

### 3. Codex / Agent Plugins 客户端

仓库同时提供：

- `plugin.json` + `mcp.json`：Agent Plugins 1.0.0 portable package；
- `.codex-plugin/plugin.json`：Codex native/legacy compatibility surface，内联 MCP launcher 与环境变量透传；
- `skills/mimic-research/SKILL.md`：portable Agent Skill。

本地开发先运行：

```bash
git clone https://github.com/lidongpeng35-lang/mimic-research-skill.git
cd mimic-research-skill
python3 scripts/bootstrap_catalog.py
python3 scripts/launch_mcp.py --doctor
```

随后通过客户端的 Plugins/本地插件入口加载整个仓库目录，而不是仅复制 `SKILL.md`。

### 4. 仅做静态研究设计 / SQL

无患者数据库时仍可使用：`SKILL.md`、`references/`、`resources/`、compiler 和离线 MCP smoke。此模式可以做 concept resolution、Contract、SQL 生成和 validation plan，但必须标记为 **not executed**；不得模拟患者行、样本量、患病率、missingness 或 export receipt。

## 数据库环境

运行患者 Preview/Export 时使用环境变量，不要把密码写入仓库：

```bash
export PGHOST=localhost
export PGPORT=5432
export PGDATABASE=mimiciv
export PGUSER=readonly_user
export PGPASSWORD='...'
```

推荐使用独立的 PostgreSQL read-only role。示例见 [`config/example.env`](config/example.env)。

运行环境检查：

```bash
python3 scripts/launch_mcp.py --doctor
```

没有数据库、派生表或依赖时，runtime 应 fail closed，而不是伪造 Preview 或自动降级成不受控患者查询。

## 使用示例

```text
请在 MIMIC-IV 中构建 ICU 脓毒症队列：年龄 ≥65 岁，排除 RRT；
以 ICU 入科为 time zero，提取 0–24 h lactate 首次值、SOFA 最大值、
去甲肾上腺素暴露和 28 天死亡，并先给我 Contract 与 Preview。
```

Skill 应先解析并核验 sepsis、RRT、lactate、SOFA、norepinephrine、mortality 等概念，而不是直接凭记忆拼 `itemid`/ICD。若某个定义存在实质歧义，保持 `unresolved` 并让研究者选择。

## 关键研究原则

1. **不凭记忆发明定义。** `itemid`、ICD、表、单位、公式和派生评分必须来自注册表、字典或可追溯来源。
2. **先定义研究语义，再写 SQL。** cohort、analysis unit、index time、window、variable role、aggregation、missingness、output grain 必须进入 Contract。
3. **未指定 aggregation 时默认 raw event。** 不自动把“24 h 内 lactate”解释成 first/max/mean。
4. **字典命中不等于临床等价。** label/code 存在只证明映射候选存在，不证明适合当前研究定义。
5. **Preview 与 Export 分离。** Preview 验证 row grain、window、unit、missingness 和 join multiplicity；导出另需当前 revision 的显式授权。
6. **导出短语是精确门控。** 只有当前 revision 完成 Preview 后，精确收到 `确认导出` 才允许最终导出。
7. **失败分类明确。** “0 rows”“unresolved definition”“source missing”“DB unavailable”“SQL failed”不能合并成同一种失败。

## 仓库结构

```text
mimic-research-skill/
├── README.md / README_EN.md
├── SKILL.md                         # OpenClaw / root skill entry
├── plugin.json                      # Agent Plugins 1.0.0 manifest
├── mcp.json                         # portable MCP configuration
├── .claude-plugin/plugin.json       # Claude Code manifest + MCP launcher
├── .codex-plugin/plugin.json        # Codex manifest + native/legacy MCP overlay
├── skills/
│   └── mimic-research/SKILL.md      # portable packaged skill
├── references/                      # human-readable research references
├── resources/                       # registry/index/acceptance/catalog assets
├── runtime/
│   ├── src/                         # TypeScript source snapshot
│   ├── dist/                        # bundled precompiled runtime
│   └── corpus/                      # provenance/source SQL corpus
├── scripts/
│   ├── bootstrap_catalog.py
│   ├── search_catalog.py
│   ├── launch_mcp.py
│   ├── validate_repo.py
│   └── build_release.py
├── examples/
├── docs/
└── .github/                         # CI, release, issue/PR templates
```

## References 覆盖范围

与轻量 `mimic-skill` 相同的入口全部保留：

- `references/schema.md`
- `references/vital_signs.md`
- `references/labs.md`
- `references/diagnoses.md`
- `references/common_queries.md`

另外增加：medications、procedures、scores、outcomes、cohort design、quality control、provenance、Python wrapper、runtime、security 和 reference audit。

## 大字典与 GitHub 文件限制

完整 SQLite catalog 解压后超过 GitHub 单文件限制，因此仓库跟踪 `resources/catalog.sqlite.gz`。本地执行：

```bash
python3 scripts/bootstrap_catalog.py
python3 scripts/search_catalog.py "D-dimer" --limit 5
```

bootstrap 会校验 archive SHA-256 后再解压到本地缓存；未压缩数据库不会提交进 Git。

## 自检与 CI

```bash
python3 scripts/validate_repo.py
node runtime/dist/mcp-smoke.js
python3 scripts/launch_mcp.py --doctor
```

`validate_repo.py` 检查 portable/Codex/Claude manifests、Skill 同步、注册表规模、acceptance cases、catalog checksum、GitHub 文件大小和常见 secret 泄漏模式。离线 MCP smoke 验证 15-tool schema 和 workflow gating。

发布时：

```bash
python3 scripts/build_release.py
```

GitHub tag `vX.Y.Z` 会触发 release workflow，重复 validation/smoke，构建 deterministic ZIP 和 `SHA256SUMS` 并发布 GitHub Release。

## 论文复现建议

论文 Methods/Supplement 不应只写“data were extracted from MIMIC-IV”。建议冻结并保存：cohort rule、analysis unit、time zero、window boundary、变量 source/code/itemid/unit、aggregation、missingness、Contract revision/hash、SQL hash、repo commit/version、definition provenance 与 QC summary。详见 [`docs/MANUSCRIPT_REPORTING.md`](docs/MANUSCRIPT_REPORTING.md)。

## MIMIC 边界

- MIMIC-IV core 与 MIMIC-IV-ED、Note、CXR、ECG 是不同数据产品，不假设全部 schema 已安装。
- MIMIC timestamps 经过患者级去标识化偏移，不解释为患者真实日历时间或真实时区。
- MIMIC-IV 与 MIMIC-III 的表和键不同，例如 ICU stay 使用 `stay_id`。
- 本仓库不包含患者数据、PhysioNet 凭据或数据库密码。
- 本仓库 MIT License 不改变 PhysioNet/MIMIC 数据使用协议。

## 参考与致谢

主要来源包括：

- MIMIC-IV documentation: https://mimic.mit.edu/docs/IV/
- PhysioNet MIMIC-IV: https://physionet.org/content/mimiciv/
- MIT-LCP MIMIC Code: https://github.com/MIT-LCP/mimic-code
- 轻量展示结构参考: https://github.com/yongfanbeta/mimic-skill

本项目不会把轻量参考仓库的示例 SQL当作执行依据；可执行定义应回到本仓库 registry/compiler/corpus 和目标数据库验证。详见 [`ACKNOWLEDGEMENTS.md`](ACKNOWLEDGEMENTS.md)。

## 贡献、引用与安全

- 贡献规范：[`CONTRIBUTING.md`](CONTRIBUTING.md)
- 定义成熟度：[`docs/DEFINITION_LIFECYCLE.md`](docs/DEFINITION_LIFECYCLE.md)
- 验证策略：[`docs/VALIDATION.md`](docs/VALIDATION.md)
- Security：[`SECURITY.md`](SECURITY.md)
- 软件引用：[`CITATION.cff`](CITATION.cff)
- Changelog：[`CHANGELOG.md`](CHANGELOG.md)

MIT License。
