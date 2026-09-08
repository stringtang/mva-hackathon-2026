#!/usr/bin/env python3
"""生成 Track 1 提交 CSV（官方模板字段）。

字段（官方 Submit-Track1 页规定）：
proband_id, chrom_1, pos_1, ref_1, alt_1, chrom_2, pos_2, ref_2, alt_2,
epcr, finding_type, notes

规则：
- 复合杂合对占「一行」，两个变异分别填 _1 / _2 列
- 坐标 GRCh38，chrom 用 chr 前缀（官方示例 chr15；VCF 内部无前缀，此处转换）
- epcr = 自评致病概率 (0,1]，仅相对排序有意义
- 最多 10 行
"""
import csv
from pathlib import Path

BASE = Path("/Users/leotang/test/mva-hackathon")
OUT = BASE / "submissions"
OUT.mkdir(exist_ok=True)
PROBAND = "PROBAND01"  # 评分器要求的挑战内标识（VCF 样本名为 WGS_EX2312012）

FIELDS = ["proband_id", "chrom_1", "pos_1", "ref_1", "alt_1",
          "chrom_2", "pos_2", "ref_2", "alt_2",
          "epcr", "finding_type", "notes"]

rows = [
    {
        "proband_id": PROBAND,
        # 主候选：BUB1B 复合杂合对（MVA1, OMIM:257300, 常染色体隐性）
        "chrom_1": "chr15", "pos_1": 40209701, "ref_1": "T", "alt_1": "G",
        "chrom_2": "chr15", "pos_2": 40220612, "ref_2": "T", "alt_2": "G",
        "epcr": 0.98,
        "finding_type": "primary",
        "notes": (
            "BUB1B compound heterozygote, MVA1 (OMIM:257300, AR). "
            "Allele 1 NM_001211.6:c.2210T>G p.(Leu737Ter) - nonsense in exon 17/23, "
            "ClinVar VCV000533901 Pathogenic/Likely pathogenic for MVA1 "
            "(multiple submitters, no conflicts), gnomAD v4 AF~1e-4. "
            "Allele 2 c.3006T>G p.(Asn1002Lys) - missense in kinase domain exon 23/23, "
            "gnomAD v4 exomes 1 allele (~9e-7), AlphaMissense 0.923, MVP 0.852 "
            "(REVEL 0.472, discordant - see report). "
            "Matches the canonical MVA1 architecture of one null plus one hypomorphic "
            "allele (Hanks 2004; Suijkerbuijk 2010, where kinase-domain missense act via "
            "protein destabilisation, BUBR1 being a pseudokinase). "
            "AlphaFold AF-O60566 places Asn1002 at pLDDT 91.1 buried in an aromatic/"
            "hydrophobic cluster (V998 3.4A, F977, W978); Asn->Lys is a destabilising "
            "substitution. Recovered rank 1 genome-wide by an unbiased Exomiser 15.1.0 "
            "run (data 2512) from 4.93M variants using only the supplied HPO terms. "
            "Phase not directly demonstrable: the two variants are 10.9 kb apart, "
            "beyond Illumina fragment length, and no parental samples are available; "
            "trans configuration is inferred from recessive disease architecture."
        ),
    },
]

path = OUT / "stringtang_bub1b-compound-het-unbiased.csv"
with path.open("w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=FIELDS)
    w.writeheader()
    for r in rows:
        w.writerow(r)
print(f"已写入 {path}  ({len(rows)} 行)")
print(path.read_text())
