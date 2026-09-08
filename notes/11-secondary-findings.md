# 次要发现工作线（差异化核心）

日期：2026-08-26

## 为什么做这块

评委明确说 secondary findings 不计自动分、但入质性评审；榜单已满分饱和，质性评审是 Track 1 唯一区分器。评审团含临床医生与患者代表，Innovation 奖标准写明 "patient-centered design"。**这个孩子在抗癌 = 在化疗**，药物基因组学结果对其肿瘤团队可能即时有用。这是既帮到孩子、又几乎无人做的空档。

## 已发现的关键事实：PGx 位点在 VCF 中全部缺失

直查关键化疗毒性位点（坐标经 Ensembl REST /variation 核验，GRCh38），**全部无记录**：

| 位点 | GRCh38 坐标 | 药物关联 | VCF 状态 |
|---|---|---|---|
| DPYD \*2A (rs3918290, c.1905+1G>A) | 1:97450058 C>T | 5-FU/卡培他滨致死性毒性 | 无记录 |
| DPYD c.2846A>T (rs67376798) | 1:97082391 T>A | 同上 | 无记录 |
| DPYD HapB3 (rs75017182) | 1:97579893 G>C | 同上 | 无记录 |
| DPYD Y186C (rs115232898) | 1:97699474 T>C | 同上（非洲裔） | 无记录 |
| TPMT \*3B (rs1800460) | 6:18138997 C>T | 巯嘌呤类骨髓抑制 | 无记录 |
| TPMT \*3C (rs1142345) | 6:18130687 T>C | 同上 | 无记录 |
| NUDT15 \*3 (rs116855232) | 13:48045719 C>T | 巯嘌呤类骨髓抑制（东亚高频） | 无记录 |

> 坐标勘误：首轮查询使用手写坐标，其中 5 个有误，已按 Ensembl 重查。**结论不变**（正确坐标下仍全部无记录）。详见 [12-kmer-method.md](12-kmer-method.md)。

**这不等于野生型。** 本 VCF 由 Sentieon GVCFtyper `--emit_conf 10` 产出，是 variant-only VCF——不含纯合参考位点记录。缺失有两种可能：(a) 真野生型；(b) 该位点覆盖不足/未 call。二者在 VCF 层面不可区分。

PharmCAT 官方文档明确："任何不在输入 VCF 中的位点视为 no-call"，并将 `--absent-to-ref` 标注为 **DANGEROUS**——因覆盖不足而缺失的位点会被静默变成假野生型，而对 DPYD/TPMT 这类"存在即需减量"的基因，假"正常代谢型"正是最危险的错误方向。

## 因此本工作线的正确做法（管线设计）

1. **必须回到 FASTQ 做覆盖度验证**。计划：k-mer 定点基因分型——从参考序列取 PGx 位点两侧 k-mer（ref 与 alt 双版本），单遍流式扫描 FASTQ 计数。相比全基因组比对（10 核约 12-30 小时 + 数十 GB BAM），单遍扫描更省磁盘且直接回答"此位点有无覆盖、是何等位基因"。副产品：同一遍扫描可为 BUB1B 两变异做 read 级验证。
   - 风险：假基因/旁系同源混淆（DPYD/TPMT/NUDT15 尚可；CYP2D6 绝不可，需 StellarPGx + BAM）
2. 交叉验证：对同一批位点跑 PharmCAT（先 `--absent-to-ref` 得基线，必读 `.missing_pgx_var.vcf` 审计文件），与 k-mer 结果比对，二者不一致处即报告要点。
3. **ACMG SF v3.3（84 基因）** 筛查：从 ClinGen CSV 取清单（NCBI 页面停留在 v3.2，勿用），与本地 ClinVar P/LP 交叉，套用 ClinGen 每基因可报告性规则（变异类型/合子性）。

## ACMG SF v3.3 筛查结果（已完成，2026-08-26）

清单来源：ClinGen ACMG SF 页面渲染后提取，**84 基因**（与 v3.3 官方计数一致；v3.2 的 81 基因 + 新增 ABCD1/CYP27A1/PLN）。
方法：Ensembl 批量取 84 基因坐标（±500bp）→ bcftools norm 拆多等位 → 与本地 ClinVar VCF 按 (pos,ref,alt) 精确匹配 → 排除 no_assertion 评审状态。

- 84 基因区域内患儿变异 **11,277** 个（含常见多态）
- **Pathogenic/Likely pathogenic 命中：0**
- 与 Conflicting 分类记录重合：12 个 → 逐一复核，全部不可报告：
  - 隐性病单杂合携带（ATP7B Wilson 病、CYP27A1 脑腱黄瘤病）→ 携带者状态，非可行动次要发现
  - TTN 3 个杂合错义（TTN 极高多态性基因，非截短变异不可报告——ClinGen 明确 TTN 仅报告截短变异）
  - PCSK9 2 个（含 1 个纯合）→ 该基因功能缺失变异降低胆固醇，方向为保护性
  - HNF1A 2 个、DSP/SDHD/TRDN 各 1 个 → 均为分类冲突的错义 VUS 级别

**结论：84 个 ACMG 可行动基因中无可报告的次要发现。**

局限（须写进报告）：(a) 本 VCF 为 SNV/indel，未覆盖 CNV/SV，而部分 ACMG SF 基因（如 PMS2、SDHx）的致病变异常为拷贝数改变；(b) variant-only VCF 无法确认各基因区域的覆盖完整性；(c) 仅采用 ClinVar 已知分类，未对新变异做完整 ACMG 从头判读。

## 报告呈现的纪律（临床评委在看）

- 严格区分"已证实野生型"（有覆盖证据）与"未检出"（无覆盖证据）——这是全篇最重要的措辞纪律
- 不把 VUS 说成可行动发现（滥报在临床评委面前是减分项，比不写更糟）
- 结论只写进提交报告，由组织方临床团队决定是否转达家庭（规则禁止直接联系）
- 措辞参照临床遗传学报告规范，附 CPIC 指南等级

## 相关：主候选 ClinVar 本地核验（顺带得到的重要发现）

- **c.2210T>G p.L737X**：ClinVar VCV 533901，**Pathogenic/Likely pathogenic**，疾病标注直指 `Mosaic_variegated_aneuploidy_syndrome_1`（OMIM:257300），多提交者无冲突。ACMG 证据很强。
- **c.3006T>G p.N1002K**：本变异本身 ClinVar 无记录（新变异）。但**同一位点的 c.3006T>A 编码完全相同的氨基酸改变 p.Asn1002Lys，ClinVar 收录为 Uncertain significance**（单提交者，"Inborn genetic diseases"）；c.3006T>C 为同义变异，Likely benign。
  - ACMG 含义：PS1（与已知致病变异同一氨基酸改变）**不可套用**，因对照变异是 VUS 而非 P/LP。必须如实写明。
  - 但这不削弱本例判断，反而是可论证点：**MVA1 的低功能等位基因单独杂合时本就不致病**（隐性病 + 需搭配无效等位基因），因此一个独立提交者在无第二打击背景下将 p.N1002K 判为 VUS 完全合理。致病性来自"与 L737X 反式组合"这一构型，而非该错义变异自身。这正是 MVA1 遗传架构的直接体现。
  - 位置佐证：N1002 位于激酶结构域内，距 Hanks 2004 家系 3 的 L1012P 仅 10 个残基。
