# 方法栈选型（已定稿，2026-08-26）

来源：方法栈调研 agent 报告（全部版本/大小/许可证经官方源验证）。本文是操作层提炼。

## 核心架构决策

**Exomiser 一个数据包解决主线**：2512 数据包自带 gnomAD 频率 + REVEL/MVP/AlphaMissense/SpliceAI/ClinVar + 自动 ACMG 判读（15.x 新功能）。无需单独下 VEP cache/dbNSFP/gnomAD VCF（gnomAD v4 全量 817GiB，笔记本不可行）。

**LLM 的角色定位（报告核心论点，有文献背书）**：EJHG 2026 基准（5,213 病例）显示最佳 LLM 直接排序仅 23.6% top-1 vs Exomiser 35.5%。因此我们的 agentic 设计是 **Claude 编排已验证工具 + 证据合成 + 报告生成**，不是让 LLM 排变异。这个"知道 LLM 边界"的定位本身就是方法学卖点。

## 选定组件与版本（全部钉死）

| 组件 | 版本 | 用途 | 许可 |
|---|---|---|---|
| Exomiser CLI | **15.1.0** + data **2512**（hg38+phenotype） | 主排序 + 自动 ACMG | AGPL-3.0 |
| LIRICAL | 2.4.1 | 独立似然比交叉验证 | JAX 非商用（hackathon OK，README 注明） |
| PharmCAT | 3.4.0（docker, 原生 arm64） | PGx（21 基因含 DPYD/TPMT/NUDT15） | MPL-2.0 |
| bcftools/samtools | 1.24 | VCF 处理 | MIT |
| WhatsHap | 2.8（conda osx-arm64） | 相位尝试（预期失败，如实报告） | MIT |
| igv-reports | 1.16.3 | read 级证据 HTML | MIT |
| ACMG SF | **v3.3（84 基因）** | 次要发现清单，**从 ClinGen CSV 取**（NCBI 页面还停在 v3.2，勿用） | — |
| Java | openjdk 21（brew openjdk@21，默认 brew openjdk=26 不兼容声明） | Exomiser/LIRICAL/PharmCAT 共用 | — |

## Exomiser 调参（Genome Medicine 2025 优化论文，386 UDN 病例验证）

优化后 top-10 检出 49.7%→85.5%（GS）。直接采用：

- pathogenicity sources：**REVEL, MVP, ALPHA_MISSENSE, SPLICE_AI**（明确不用 CADD 归一分与 PolyPhen/SIFT/MutationTaster 老三样——量表不兼容）
- **hiPhive 限 human-only** + omimPrioritiser
- 质量门：GQ≥20，杂合 VAF 15-85%，去 `*` 等位
- HPO 术语宜多不宜少（队列中位数 20 个；容忍不精确）
- 人工复核 top 30
- 基准模式**不开** ClinVar whitelist（避免循环论证；临床模式才开）

## 版本陷阱（已验证）

- 文档写 2602/15.1.1，但数据服务器 2602 返回 404——**用 2512 并在 application.properties 显式钉死**
- 15.0.0 起 combined score 模型变更（融入 ACMG），与 14.x 基准不可比；CLI 改为 `analyse` 子命令；JSON 输出改 **PARQUET**
- Genomiser（GENOME preset，非编码变异）需另下 ReMM 14.87GiB——本例两变异均编码区，exome preset 足够；非编码覆盖作为管线通用性论述 + 磁盘允许时补跑

## PGx 三大坑（secondary findings 质量的关键）

1. **缺失位点 ≠ 野生型**：变异-only VCF 会让 PharmCAT 把 1,226 个 PGx 位点几乎全判 no-call。正解：FASTQ 比对后对 pharmcat_positions.vcf 出 gVCF 定点重call。过渡方案 `--absent-to-ref`（官方标注 DANGEROUS）仅作首轮参考且必须写明。必读 `.missing_pgx_var.vcf` 审计文件。
2. **TPMT 相位陷阱**：\*3A = 两位点顺式；双杂合无相位时 \*1/\*3A vs \*3B/\*3C 无法区分（表型不同）——PharmCAT 会如实报歧义，我们照实呈现。**DPYD 设计上不依赖相位**（CPIC 取两条等位最低活性分之和）。
3. **CYP2D6 必须 BAM 级**（SV/杂交等位）：用 StellarPGx（MIT，活跃，PharmCAT 官方推荐）而非 Cyrius（2021 年停更，PolyForm 限制性许可）。

## 相位诚实条款

WhatsHap 官方 FAQ：短读长无法桥接大多数复合杂合对。我们的两变异相距 10.9kb >> 片段长度 → **本质不可相位**（无亲本、无长读长）。报告写"unphased, trans 构型由群体遗传学+文献架构推断"，不假装解决。

## 评分复现

PhEval（Apache-2.0，Monarch 官方）+ Stenton 2024 rank-points 阶梯（top5=100/6-10=50/11-20=25/21-50=10/51-100=5）与 F-max（EPCR 阈值扫描取最大 F1）。用于本地自测提交文件。

## 磁盘预算（207GB 可用）

Exomiser 下载 36GiB→解包 ~55-65GiB（解包后删 zip）+ ClinVar 0.2 + FASTA 3.1 + GFF3 0.1 ≈ 60GiB。FASTQ 85GB 视比对方案再定（可能只取 2 lanes 或流式处理）。ReMM 15GiB 备选。
