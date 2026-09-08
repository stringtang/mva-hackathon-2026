#!/usr/bin/env python3
"""BUB1B 区域初筛：提取基因区域变异，标注外显子/剪接窗口位置与基因型。

输出策略（合规约定）：仅打印外显子±12bp 窗口内的变异行（候选材料）
以及区域级聚合计数；内含子深处的常见变异只计数不打印。
"""
import json
import subprocess
import sys

VCF = "/Users/leotang/test/mva-hackathon/data/WGS_EX2312012_HGWCNDSX7.vcf.gz"
GENE_JSON = "/Users/leotang/test/mva-hackathon/pipeline/bub1b_ensembl.json"
SPLICE_PAD = 12  # 外显子边界外延，覆盖经典剪接位点 ±1-2 及近端剪接区

d = json.load(open(GENE_JSON))
gene_start, gene_end = d["start"], d["end"]
canon = [t for t in d["Transcript"] if t.get("is_canonical")][0]
exons = sorted([(e["start"], e["end"]) for e in canon["Exon"]])
# 正链基因：外显子按基因组坐标排序即转录顺序
region = f"15:{gene_start - 5000}-{gene_end + 5000}"

q = subprocess.run(
    ["bcftools", "query", "-r", region,
     "-f", "%POS\t%REF\t%ALT\t%FILTER\t[%GT]\t[%AD]\t[%DP]\n", VCF],
    capture_output=True, text=True, check=True)

rows = [line.split("\t") for line in q.stdout.strip().split("\n") if line]

def locate(pos, ref):
    span_end = pos + max(len(ref) - 1, 0)
    for i, (s, e) in enumerate(exons, 1):
        if pos <= e + SPLICE_PAD and span_end >= s - SPLICE_PAD:
            inside = pos >= s and span_end <= e
            return i, "exon" if inside else "splice_window"
    return None, "intron/flank"

n_total = n_pass = n_exonic = 0
print(f"BUB1B region {region} | canonical {canon['id']} exons={len(exons)}")
print(f"{'POS':>10} {'REF':>12} {'ALT':>12} {'FILTER':>8} {'GT':>5} {'AD':>9} {'DP':>4}  location")
for pos_s, ref, alt, filt, gt, ad, dp in rows:
    pos = int(pos_s)
    n_total += 1
    if filt in ("PASS", "."):
        n_pass += 1
    exon_i, loc = locate(pos, ref)
    if loc != "intron/flank":
        n_exonic += 1
        ref_p = ref if len(ref) <= 12 else ref[:9] + f"+{len(ref)-9}"
        alt_p = alt if len(alt) <= 12 else alt[:9] + f"+{len(alt)-9}"
        print(f"{pos:>10} {ref_p:>12} {alt_p:>12} {filt:>8} {gt:>5} {ad:>9} {dp:>4}  exon{exon_i} ({loc})")

print(f"\n聚合：区域内变异 {n_total}（PASS/无标记 {n_pass}），外显子±{SPLICE_PAD}bp 内 {n_exonic}")
