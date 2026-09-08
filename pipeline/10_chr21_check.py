#!/usr/bin/env python3
"""chr21 深度残差精查：区分整数量化伪影 / 真实低比例嵌合三体 / 局部重复。

前一轮用中位深度，分辨率受整数量化限制（44 vs 45 = 2.3% 阶跃）。
本轮改用均值并做 GC 配对比较，同时检查升高是否均匀分布于全染色体。
"""
import subprocess, statistics as st
from collections import defaultdict

BASE = "/Users/leotang/test/mva-hackathon"
VCF = f"{BASE}/data/WGS_EX2312012_HGWCNDSX7.vcf.gz"
W = 1_000_000
MAIN = [str(i) for i in range(1, 23)]

# 复用窗口 GC（重算，快）
FA = f"{BASE}/refs/GRCh38.fa"
gc = {}
cur, keep, pos, buf = None, False, 0, []
def flush(c, w, seq):
    s = "".join(seq); at = s.count("A")+s.count("T"); g = s.count("G")+s.count("C")
    if g+at > W*0.5: gc[(c,w)] = g/(g+at)
with open(FA) as fh:
    for line in fh:
        if line[0] == ">":
            if keep and buf: flush(cur, pos//W, buf)
            cur = line[1:].split()[0]; keep = cur in MAIN; pos, buf = 0, []
            continue
        if not keep: continue
        for ch in line.strip().upper():
            buf.append(ch); pos += 1
            if pos % W == 0: flush(cur, (pos-1)//W, buf); buf = []
    if keep and buf: flush(cur, pos//W, buf)

# 窗口内 het SNP 深度（保留全部值以算均值）
vals = defaultdict(list)
q = subprocess.Popen(["bcftools","query","-i",'FILTER="PASS" && GT="het" && TYPE="snp"',
                      "-f","%CHROM\t%POS\t[%DP]\n",VCF], stdout=subprocess.PIPE, text=True)
for line in q.stdout:
    c,p,d = line.rstrip("\n").split("\t")
    if c not in MAIN or d == ".": continue
    dp = int(d)
    if 5 <= dp <= 200: vals[(c,int(p)//W)].append(dp)
q.wait()

win = {k: (st.mean(v), len(v)) for k,v in vals.items() if len(v) >= 100 and k in gc}
gmean = st.mean([m for m,_ in win.values()])
print(f"全基因组窗口均值深度: {gmean:.3f}x   窗口数: {len(win)}\n")

# GC 配对：每条染色体 vs 全基因组同 GC 分箱
print(f"{'chr':>4} {'窗口':>5} {'均值深度':>9} {'GC中位':>7} {'GC配对期望':>11} {'比值':>7} {'推断嵌合比例':>12}")
res = []
for c in MAIN:
    ks = [k for k in win if k[0]==c]
    if len(ks) < 5: continue
    obs = st.mean([win[k][0] for k in ks])
    cgc = st.median([gc[k] for k in ks])
    exp_pool = [win[k][0] for k in win if k[0]!=c and abs(gc[k]-cgc) < 0.01]
    exp = st.mean(exp_pool) if len(exp_pool) >= 30 else gmean
    ratio = obs/exp
    f = (ratio-1)*2          # 三体嵌合比例 f: ratio = 1 + f/2
    res.append((c, ratio, f, len(ks)))
    print(f"{c:>4} {len(ks):>5} {obs:>9.3f} {cgc:>7.3f} {exp:>11.3f} {ratio:>7.4f} {f*100:>11.1f}%")

print()
worst = max(res, key=lambda r: abs(r[1]-1))
print(f"最大偏离: chr{worst[0]} 比值 {worst[1]:.4f} → 若为三体嵌合，比例约 {worst[2]*100:.1f}%")

# chr21 沿染色体分布：均匀升高 vs 局部
print(f"\nchr21 各窗口深度/期望（检查是否均匀）:")
c21 = sorted([k for k in win if k[0]=="21"], key=lambda k: k[1])
line = []
for k in c21:
    cgc = gc[k]
    pool = [win[j][0] for j in win if j[0]!="21" and abs(gc[j]-cgc) < 0.01]
    e = st.mean(pool) if len(pool) >= 30 else gmean
    line.append(f"{k[1]}Mb:{win[k][0]/e:.3f}")
print("  " + "  ".join(line))
ratios = []
for k in c21:
    cgc = gc[k]; pool = [win[j][0] for j in win if j[0]!="21" and abs(gc[j]-cgc)<0.01]
    e = st.mean(pool) if len(pool)>=30 else gmean
    ratios.append(win[k][0]/e)
print(f"\nchr21 窗口比值: 中位 {st.median(ratios):.4f}  均值 {st.mean(ratios):.4f}  标准差 {st.pstdev(ratios):.4f}  范围 {min(ratios):.3f}-{max(ratios):.3f}")
