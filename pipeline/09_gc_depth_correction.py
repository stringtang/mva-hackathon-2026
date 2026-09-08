#!/usr/bin/env python3
"""GC 偏倚校正：验证染色体级深度升高是否由 GC 含量驱动。

方法：
1. 从参考基因组按 1Mb 窗口计算 GC 含量
2. 从 VCF 的 PASS 杂合 SNP 计算同窗口的中位深度
3. 拟合 depth ~ GC 关系（按 GC 分箱取中位数）
4. 用该关系校正各染色体深度，看异常是否消失

若校正后染色体深度趋于一致 → 支持 GC 偏倚解释；
若某染色体仍显著偏离 → 提示真实拷贝数改变。
"""
import subprocess, statistics as st
from collections import defaultdict

BASE = "/Users/leotang/test/mva-hackathon"
FA = f"{BASE}/refs/GRCh38.fa"
VCF = f"{BASE}/data/WGS_EX2312012_HGWCNDSX7.vcf.gz"
W = 1_000_000
MAIN = [str(i) for i in range(1, 23)]

# --- 1. 窗口 GC ---
print("计算窗口 GC 含量...", flush=True)
gc = {}   # (chrom, widx) -> gc_frac
cur, keep, pos, buf = None, False, 0, []
def flush(chrom, widx, seq):
    s = "".join(seq)
    at = s.count("A") + s.count("T")
    g = s.count("G") + s.count("C")
    if g + at > W * 0.5:            # 跳过高 N 窗口
        gc[(chrom, widx)] = g / (g + at)

with open(FA) as fh:
    for line in fh:
        if line[0] == ">":
            if keep and buf:
                flush(cur, pos // W, buf)
            cur = line[1:].split()[0]
            keep = cur in MAIN
            pos, buf = 0, []
            continue
        if not keep:
            continue
        s = line.strip().upper()
        for ch in s:
            buf.append(ch)
            pos += 1
            if pos % W == 0:
                flush(cur, (pos - 1) // W, buf)
                buf = []
    if keep and buf:
        flush(cur, pos // W, buf)
print(f"  窗口数: {len(gc)}")

# --- 2. 窗口深度 ---
print("统计窗口深度（PASS 杂合 SNP）...", flush=True)
depths = defaultdict(list)
q = subprocess.Popen(["bcftools", "query", "-i",
                      'FILTER="PASS" && GT="het" && TYPE="snp"',
                      "-f", "%CHROM\t%POS\t[%DP]\n", VCF],
                     stdout=subprocess.PIPE, text=True)
for line in q.stdout:
    c, p, d = line.rstrip("\n").split("\t")
    if c not in MAIN or d == ".":
        continue
    dp = int(d)
    if 5 <= dp <= 200:
        depths[(c, int(p) // W)].append(dp)
q.wait()

win = {k: st.median(v) for k, v in depths.items() if len(v) >= 50 and k in gc}
print(f"  可用窗口: {len(win)}")

# --- 3. GC-深度曲线 ---
bins = defaultdict(list)
for k, d in win.items():
    bins[round(gc[k], 2)].append(d)
curve = {g: st.median(v) for g, v in bins.items() if len(v) >= 30}
gmed = st.median(list(win.values()))
print(f"\n全基因组窗口中位深度: {gmed:.1f}x")
print(f"{'GC':>6} {'窗口数':>7} {'中位深度':>9} {'相对':>7}")
for g in sorted(curve):
    print(f"{g:>6.2f} {len(bins[g]):>7} {curve[g]:>9.1f} {curve[g]/gmed:>7.3f}")

# --- 4. 校正 ---
print(f"\n{'chr':>4} {'GC':>6} {'原始':>7} {'原始/全基因组':>13} {'GC校正后':>10} {'残差':>8}")
rows = []
for c in MAIN:
    ks = [k for k in win if k[0] == c]
    if not ks:
        continue
    raw = st.median([win[k] for k in ks])
    cg = st.median([gc[k] for k in ks])
    exp = [curve.get(round(gc[k], 2)) for k in ks]
    exp = [e for e in exp if e]
    expected = st.median(exp) if exp else gmed
    corrected = raw / expected
    rows.append((c, cg, raw, raw / gmed, corrected))
    print(f"{c:>4} {cg:>6.3f} {raw:>7.1f} {raw/gmed:>13.3f} {corrected:>10.3f} {abs(corrected-1)*100:>7.1f}%")

print("\n判读：GC 校正后比值应接近 1.0。偏离 >5% 且非 GC 可解释者提示真实拷贝数改变。")
worst = max(rows, key=lambda r: abs(r[4] - 1))
print(f"最大残差染色体: chr{worst[0]} = {worst[4]:.3f} ({abs(worst[4]-1)*100:.1f}%)")
