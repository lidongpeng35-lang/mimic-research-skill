# MIMIC Research Skill

一个专注于 **MIMIC-IV 数据提取 SQL 生成** 的科研 Skill。

它只做一件事：

> **自然语言研究需求 → 明确研究语义 → MIMIC-IV 表/字段/定义映射 → 可审阅、可复现的 PostgreSQL SQL**

本项目不连接数据库、不执行患者级查询、不导出数据，也不提供 MCP server。它的核心价值是减少 MIMIC 研究中常见的语义错误：表/字段选错、MIMIC-III/IV 混用、时间窗不清、分析单位错误、聚合方式隐含、单位混合、join 扩增，以及凭记忆编造 itemid/ICD/评分定义。

## 能做什么

给出类似需求：

> 在 MIMIC-IV 中构建首次 ICU 入住的脓毒症患者队列，提取 ICU 入科后 0–24 h 首次乳酸、最大 SOFA、机械通气暴露、去甲肾上腺素暴露和 28 天死亡。

Skill 应按以下顺序工作：

1. 识别 cohort、analysis unit、index time、变量、时间窗、aggregation 和输出粒度；
2. 查询本仓库 registry / references 中已有定义；
3. 对存在实质歧义的定义先提出最少必要澄清，不擅自猜测；
4. 生成完整 PostgreSQL SQL；
5. 同时给出关键定义、来源、假设和需要人工核验的部分。

## 当前 v0.2 资源

- `resources/core-registry.json`：首批高频 MIMIC-IV 队列、生命体征、实验室、评分、治疗和结局概念；
- `resources/acceptance-cases.json`：20 个自然语言到 SQL 行为验收案例；
- `references/`：MIMIC-IV schema、生命体征、实验室、诊断、药物、操作、评分、结局、队列设计、QC、provenance 等说明；
- `SKILL.md`：宿主 Agent 的核心工作规范。

之前整理的更大变量/定义资源正在迁移到纯 Skill 结构中；在它们正式进入仓库并通过 CI 前，本 README 不把它们算作线上能力。

## 核心原则

1. **只做 MIMIC-IV。** 不把 MIMIC-III、eICU 或其他数据库逻辑混入默认输出。
2. **先定义语义，再写 SQL。** cohort、analysis unit、index time、window、aggregation、missingness、output grain 必须明确。
3. **不凭记忆发明定义。** itemid、ICD、表、字段、单位、评分公式必须来自仓库资源或明确可追溯来源。
4. **未指定 aggregation 时，不擅自选择 first/max/mean。** 必要时询问；若输出 raw events，则明确说明。
5. **字典命中不等于临床等价。** 同名变量可能来自不同 specimen、表或单位。
6. **优先使用 MIMIC-IV 官方 schema 与 MIT-LCP mimic-code 逻辑。** 使用 `mimiciv_derived` 时应明确其依赖和时间语义。
7. **SQL 必须可审阅。** 使用清晰 CTE、显式 join keys、显式半开时间窗 `[start, end)`、明确去重/排序规则。
8. **不执行数据库。** 本仓库输出 SQL 和定义说明；数据库运行、权限和结果验证由使用者环境负责。

## 推荐输出格式

一个完整研究请求应输出四部分：

1. **研究规格 / Extraction specification** — population、analysis unit、index time、stay selection、变量、时间窗、aggregation、output grain。
2. **需要确认的歧义 / Blocking ambiguities** — 只列真正会改变 SQL 结果的问题。
3. **正式 SQL** — 完整 PostgreSQL SQL，而不是伪代码或 `SELECT *` 骨架。
4. **定义与来源 / Definition notes** — 关键表、字段、derived concept、假设和 candidate 警告。

## 仓库结构

```text
mimic-research-skill/
├── README.md
├── README_EN.md
├── SKILL.md
├── resources/
│   ├── core-registry.json
│   └── acceptance-cases.json
├── references/
├── examples/
├── docs/
├── scripts/validate_repo.py
├── .claude-plugin/
├── .codex-plugin/
└── .github/workflows/ci.yml
```

## 验证

```bash
python3 scripts/validate_repo.py
```

CI 验证 Skill 结构、manifest、核心 registry、20 个 acceptance cases、MCP 残留检查以及关键规则。它**不声称任何 SQL 已在患者数据库上执行成功**。

## 参考来源

- MIMIC-IV documentation: https://mimic.mit.edu/docs/IV/
- PhysioNet MIMIC-IV: https://physionet.org/content/mimiciv/
- MIT-LCP MIMIC Code: https://github.com/MIT-LCP/mimic-code
- 轻量结构参考: https://github.com/yongfanbeta/mimic-skill

MIT License 仅适用于本仓库软件与文档，不改变 MIMIC/PhysioNet 数据使用协议。
