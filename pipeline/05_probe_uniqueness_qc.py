#!/usr/bin/env python3
"""探针唯一性 QC：单遍扫描 GRCh38 参考基因组，统计每个探针 k-mer 的出现次数。

k-mer 定点分型方法的效力前提是：探针 k-mer 在基因组中唯一。若某 ref k-mer
在参考中出现 >1 次（假基因、片段重复、低复杂度区），来自旁系同源位点的 reads
会被误计，导致等位基因比例失真。本脚本为该前提提供直接证据。

只扫描 primary assembly 的主染色体（1-22,X,Y,MT），跳过 scaffold。
输出：每位点的 ref/alt k-mer 集合中「基因组内出现次数 >1」的比例与最大计数。
"""
import json
from pathlib import Path

BASE = Path("/Users/leotang/test/mva-hackathon")
FA = BASE / "refs/GRCh38.fa"
K = 31
probes = json.loads((BASE / "pipeline/kmer_probes.json").read_text())

# 建反查表：kmer -> [(site, which), ...]
lookup = {}
for name, p in probes.items():
    for which in ("ref_kmers", "alt_kmers"):
        for km in p[which]:
            lookup.setdefault(km, []).append((name, which))
print(f"待查 k-mer 总数（含反向互补）: {len(lookup)}")

MAIN = {str(i) for i in range(1, 23)} | {"X", "Y", "MT"}
counts = {km: 0 for km in lookup}

cur_chrom, keep, buf = None, False, ""
n_bases = 0
with open(FA) as fh:
    for line in fh:
        if line.startswith(">"):
            cur_chrom = line[1:].split()[0]
            keep = cur_chrom in MAIN
            buf = ""
            if keep:
                print(f"  扫描 chr{cur_chrom} ...", flush=True)
            continue
        if not keep:
            continue
        buf += line.strip().upper()
        n_bases += len(line.strip())
        # 保留末尾 K-1 以跨行匹配
        if len(buf) >= 1_000_000:
            for i in range(len(buf) - K + 1):
                km = buf[i:i + K]
                if km in counts:
                    counts[km] += 1
            buf = buf[-(K - 1):]
    if keep and buf:
        for i in range(len(buf) - K + 1):
            km = buf[i:i + K]
            if km in counts:
                counts[km] += 1

print(f"\n扫描碱基数: {n_bases:,}")
print(f"\n{'位点':>28} {'集合':>10} {'kmer数':>7} {'命中0次':>8} {'命中1次':>8} {'>1次':>6} {'最大':>5}")
ok = True
for name, p in probes.items():
    for which in ("ref_kmers", "alt_kmers"):
        c = [counts[km] for km in p[which]]
        # 每个 k-mer 及其反向互补都在集合中，参考基因组单链扫描 → 正确 ref kmer 期望命中 1 次
        z, one, multi = sum(1 for x in c if x == 0), sum(1 for x in c if x == 1), sum(1 for x in c if x > 1)
        flag = "" if multi == 0 else "  ⚠ 非唯一"
        if multi:
            ok = False
        print(f"{name:>28} {which:>10} {len(c):>7} {z:>8} {one:>8} {multi:>6} {max(c):>5}{flag}")
print("\n结论:", "全部探针 k-mer 在 GRCh38 内唯一，方法前提成立" if ok
      else "存在非唯一 k-mer，相关位点结果须谨慎解读")
json.dump({k: counts[k] for k in counts}, open(BASE / "pipeline/probe_genome_counts.json", "w"))
