# 开放问题追踪

更新：2026-08-26

## 待官方澄清（Discussions 区已有人问、组织方未回复）

1. **LLM API 与受控数据的合规边界** — [讨论帖 #2](https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/discussions/2)
   - doyleywoods 问了四点：变异级数据发给第三方 LLM API 是否算 "granting data access"；是否取决于服务商数据政策（零留存）；"衍生数据" 删除义务的边界（基因排名/含变异的 prompt 算不算）；API 日志无法删除怎么办
   - 13 赞、多人跟问，**组织方尚未回复**（截至 08-26）
   - 我们的立场（在官方澄清前）：批量数据只本地处理；仅把"本来就要写进公开 CC-BY 提交物"的入围候选变异送入 Claude 上下文；在 methods 中如实记录此数据处理姿势
   - **每隔几天复查此帖**；官方口径出来后调整工作流并在报告中引用

2. **GitHub 仓库公开时机 / 内容范围 / 模型命名** — [讨论帖 #4](https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/discussions/4)
   - 榜首 ChaimaeEH 所问，未回复。暂按保守做法：仓库先私有开发，提交时转公开；内容含脚本+配置+报告；模型名可描述方法（榜上现有名字都在描述方法，如 bub1b-targeted-acmg）

3. **奖项是否分 track**（规则未明说；1st/2nd/3rd 疑似综合评定）→ 可在 Discussions 发帖问，或等别人问

## 数据未知项（拿到访问权后立即确认）

- [ ] 11 个文件清单：VCF 之外有什么（FASTQ？CRAM？HPO 表型文件格式？临床摘要？）
- [ ] 已知文件名：WGS_EX2312012_HGWCNDSX7.vcf.gz（命名含测序批次 HGWCNDSX7 = NovaSeq S4 flowcell）
- [ ] VCF 是 single-sample germline 还是含 somatic；是否含 SV/CNV calls；用什么 caller 产出
- [ ] proband_id 具体值（提交 CSV 必填字段，数据里给）
- [ ] 复合杂合两变异的基因组距离（决定能否 read-based phasing）

## 战术未决

- [ ] 磁盘预算分配：数据(≤85GB，可只取 VCF+表型) + VEP cache + Exomiser data + dbNSFP，207GB 内怎么排（等方法栈调研 agent 结论）
- [ ] Java 17+ 安装（Exomiser 依赖）
- [ ] pitch 视频制作方案（分镜/配音/工具），10 月初再定

## 官方回应（2026-08-26 更新）

**讨论帖 #2（LLM API 合规）已获 Sage Bionetworks 总裁 LucaFoschini 回复**：
- 确认问题成立，团队正在准备逐条澄清数据使用限制
- **明确的临时指引**："please use a conservative interpretation of each data use clause in making your choices, in order to err on the side of protection"，并承认这可能暂时严重限制参赛方法
- → 我们既定的保守姿势（批量数据仅本地处理、仅入围候选变异进上下文）**与官方指引一致**，已写入 report/track1_methods.md §6 并引用
- **待办**：持续关注该帖的逐条澄清，若口径放宽或收紧需相应调整并在报告中说明
