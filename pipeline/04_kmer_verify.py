#!/usr/bin/env python3
"""无比对 k-mer 定点验证：单遍流式扫描 FASTQ，同时完成
(a) BUB1B 两个候选变异的 read 级等位基因计数（ref/alt 支持数）
(b) PGx 关键位点（DPYD/TPMT/NUDT15）的覆盖度与等位基因验证

原理：对每个位点，从参考基因组取变异两侧各 K-1 bp，构造 ref 与 alt 两个
(2K-1) bp 探针的全部 K 长子串中「跨越变异位点」的 k-mer 集合（含反向互补）。
流式扫描 FASTQ 的每条 read，命中计数。k=31 时人类基因组内 k-mer 几乎唯一，
但仍对每个探针做基因组内唯一性预检（记录警告）。

输出：仅每位点的聚合计数（ref_kmer 命中读数、alt_kmer 命中读数）。
不输出任何 read 序列。

用法: python3 04_kmer_verify.py build   # 生成探针（需 refs/GRCh38.fa 已索引）
      python3 04_kmer_verify.py scan data/*.fastq.gz   # 扫描（可分文件多次跑，结果累加保存）
"""
import gzip
import json
import subprocess
import sys
from pathlib import Path

BASE = Path("/Users/leotang/test/mva-hackathon")
FA = BASE / "refs/GRCh38.fa"
K = 31
# 扫描优先使用经唯一性 QC 净化的探针集（05_probe_uniqueness_qc.py 产出）
_MASKED = BASE / "pipeline/kmer_probes_masked.json"
PROBES_JSON = BASE / "pipeline/kmer_probes.json"
SCAN_PROBES = _MASKED if _MASKED.exists() else PROBES_JSON
COUNTS_JSON = BASE / "pipeline/kmer_counts.json"

# (name, chrom, pos, ref, alt) — GRCh38，无 chr 前缀（与 VCF/FASTA 命名一致）
# 坐标与等位基因均取自 Ensembl REST /variation（2026-08-26 核验）。
# DPYD 与 TPMT 位于负链，故基因组等位基因与 cDNA 记法互补。
# build() 内置断言：参考碱基必须与 FASTA 一致，坐标错误会直接失败而非静默出错。
SITES = [
    ("BUB1B_L737X_c.2210T>G", "15", 40209701, "T", "G"),
    ("BUB1B_N1002K_c.3006T>G", "15", 40220612, "T", "G"),
    ("DPYD_star2A_rs3918290", "1", 97450058, "C", "T"),        # c.1905+1G>A
    ("DPYD_c2846_rs67376798", "1", 97082391, "T", "A"),        # c.2846A>T
    ("DPYD_HapB3_rs75017182", "1", 97579893, "G", "C"),        # c.1129-5923C>G
    ("DPYD_Y186C_rs115232898", "1", 97699474, "T", "C"),       # c.557A>G
    ("TPMT_star3C_rs1142345", "6", 18130687, "T", "C"),        # c.719A>G
    ("TPMT_star3B_rs1800460", "6", 18138997, "C", "T"),        # c.460G>A
    ("NUDT15_star3_rs116855232", "13", 48045719, "C", "T"),    # c.415C>T
]

RC = str.maketrans("ACGT", "TGCA")

def revcomp(s):
    return s.translate(RC)[::-1]

def spanning_kmers(seq, var_lo, var_hi):
    """seq 中所有覆盖 [var_lo, var_hi)（0-based）的 K 长子串，含反向互补。"""
    out = set()
    for i in range(len(seq) - K + 1):
        if i <= var_lo and i + K >= var_hi:
            km = seq[i:i + K]
            if "N" in km:
                continue
            out.add(km)
            out.add(revcomp(km))
    return out

def build():
    probes = {}
    for name, chrom, pos, ref, alt in SITES:
        lo = pos - (K - 1)
        hi = pos + len(ref) - 1 + (K - 1)
        r = subprocess.run(["samtools", "faidx", str(FA), f"{chrom}:{lo}-{hi}"],
                           capture_output=True, text=True, check=True)
        ctx = "".join(r.stdout.split("\n")[1:]).upper()
        var_lo = (K - 1)
        var_hi = var_lo + len(ref)
        assert ctx[var_lo:var_hi] == ref, f"{name}: 参考碱基不符 {ctx[var_lo:var_hi]}!={ref}"
        alt_ctx = ctx[:var_lo] + alt + ctx[var_hi:]
        probes[name] = {
            "ref_kmers": sorted(spanning_kmers(ctx, var_lo, var_hi)),
            "alt_kmers": sorted(spanning_kmers(alt_ctx, var_lo, var_lo + len(alt))),
        }
        print(f"{name}: ref_kmers={len(probes[name]['ref_kmers'])} alt_kmers={len(probes[name]['alt_kmers'])}")
    PROBES_JSON.write_text(json.dumps(probes))
    print(f"探针已写入 {PROBES_JSON}")

def scan(fastqs):
    probes = json.loads(SCAN_PROBES.read_text())
    print(f"使用探针集: {SCAN_PROBES.name}")
    # k-mer -> (site, which)；若同一 k-mer 属多个位点则丢弃（唯一性保护）
    lookup, dup = {}, set()
    for name, p in probes.items():
        for which in ("ref_kmers", "alt_kmers"):
            for km in p[which]:
                if km in lookup and lookup[km][0] != name:
                    dup.add(km)
                lookup[km] = (name, which)
    for km in dup:
        lookup.pop(km, None)

    counts = json.loads(COUNTS_JSON.read_text()) if COUNTS_JSON.exists() else {}
    done_files = set(counts.get("_files", []))
    for fq in fastqs:
        fq = str(fq)
        if fq in done_files:
            print(f"跳过已扫描: {fq}")
            continue
        n_reads = 0
        local = {}
        with gzip.open(fq, "rt") as fh:
            for i, line in enumerate(fh):
                if i % 4 != 1:
                    continue
                n_reads += 1
                seq = line.rstrip("\n")
                hit_sites = set()  # 每条 read 对每个 (site,which) 只计一次
                for j in range(len(seq) - K + 1):
                    km = seq[j:j + K]
                    tgt = lookup.get(km)
                    if tgt:
                        hit_sites.add(tgt)
                for tgt in hit_sites:
                    key = f"{tgt[0]}|{tgt[1]}"
                    local[key] = local.get(key, 0) + 1
        for k, v in local.items():
            counts[k] = counts.get(k, 0) + v
        done_files.add(fq)
        counts["_files"] = sorted(done_files)
        COUNTS_JSON.write_text(json.dumps(counts, indent=1))
        print(f"{fq}: reads={n_reads:,} 本文件命中={sum(local.values())}")

    print("\n=== 累计计数 ===")
    for name, _, _, _, _ in SITES:
        r = counts.get(f"{name}|ref_kmers", 0)
        a = counts.get(f"{name}|alt_kmers", 0)
        tot = r + a
        vaf = a / tot if tot else 0
        print(f"{name:>28}: ref={r:>4} alt={a:>4} 总覆盖={tot:>4} VAF={vaf:.2f}")

if __name__ == "__main__":
    if sys.argv[1] == "build":
        build()
    else:
        scan(sys.argv[2:] if sys.argv[1] == "scan" else sys.argv[1:])
