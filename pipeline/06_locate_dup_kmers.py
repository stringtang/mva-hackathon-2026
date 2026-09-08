import json
from pathlib import Path
BASE = Path("/Users/leotang/test/mva-hackathon")
K = 31
probes = json.loads((BASE/"pipeline/kmer_probes.json").read_text())
gc = json.loads((BASE/"pipeline/probe_genome_counts.json").read_text())
dup = {km for km in probes["TPMT_star3C_rs1142345"]["ref_kmers"] if gc.get(km,0) > 1}
print(f"待定位的非唯一 k-mer 数: {len(dup)}")
MAIN = {str(i) for i in range(1,23)} | {"X","Y","MT"}
hits = []
cur, keep, buf, offset = None, False, "", 0
with open(BASE/"refs/GRCh38.fa") as fh:
    for line in fh:
        if line.startswith(">"):
            cur = line[1:].split()[0]; keep = cur in MAIN; buf=""; offset=0
            continue
        if not keep: continue
        buf += line.strip().upper()
        if len(buf) >= 1_000_000:
            for i in range(len(buf)-K+1):
                if buf[i:i+K] in dup:
                    hits.append((cur, offset+i+1))
            offset += len(buf)-(K-1); buf = buf[-(K-1):]
    if keep and buf:
        for i in range(len(buf)-K+1):
            if buf[i:i+K] in dup:
                hits.append((cur, offset+i+1))
from collections import Counter
loci = Counter()
for c,p in hits:
    loci[(c, p//100000*100000)] += 1
print("命中位置聚类（染色体, 100kb 窗口起点）: 计数")
for (c,w),n in sorted(loci.items(), key=lambda x:-x[1]):
    print(f"  chr{c}:{w:,}-{w+100000:,}  {n}")
