#!/usr/bin/env python3
"""从单样本 WGS VCF 检测血源 DNA 的嵌合非整倍体信号。

原理：
- 二倍体染色体上，杂合位点 B 等位基因频率 (BAF = AD_alt/(AD_ref+AD_alt)) 期望 0.5。
- 嵌合三体（比例 f）使杂合 BAF 分裂为 (1+f)/(2+f) 与 1/(2+f) 两峰；
  嵌合单体使其分裂为 1/(2-f) 与 (1-f)/(2-f)。均表现为 |BAF-0.5| 系统性偏移。
- 同时染色体级测序深度相对全基因组中位数上/下浮 f/2。
输出：每条染色体的杂合位点数、中位深度（对全基因组归一）、BAF 中位偏移、
BAF 分布的偏移分位数 —— 仅聚合统计，不输出任何位点级数据。
"""
import subprocess
import statistics as st

VCF = "/Users/leotang/test/mva-hackathon/data/WGS_EX2312012_HGWCNDSX7.vcf.gz"
CHROMS = [str(i) for i in range(1, 23)] + ["X"]

q = subprocess.Popen(
    ["bcftools", "query", "-i", 'FILTER="PASS" && GT="het" && TYPE="snp"',
     "-f", "%CHROM\t[%AD]\n", VCF],
    stdout=subprocess.PIPE, text=True)

baf = {c: [] for c in CHROMS}
dp = {c: [] for c in CHROMS}
for line in q.stdout:
    chrom, ad = line.rstrip("\n").split("\t")
    if chrom not in baf:
        continue
    parts = ad.split(",")
    if len(parts) != 2:
        continue
    try:
        r, a = int(parts[0]), int(parts[1])
    except ValueError:
        continue
    tot = r + a
    if tot < 15:  # 深度过滤，降低噪声
        continue
    baf[chrom].append(a / tot)
    dp[chrom].append(tot)
q.wait()

all_dp_medians = {c: st.median(dp[c]) for c in CHROMS if dp[c]}
autosomal_dp = st.median([all_dp_medians[c] for c in CHROMS[:22]])

print(f"全基因组常染色体中位深度: {autosomal_dp:.0f}x")
print(f"{'chr':>4} {'n_het':>8} {'depth':>6} {'norm':>6} {'medBAF':>7} {'|BAF-.5|med':>11}  flag")
for c in CHROMS:
    if not baf[c]:
        continue
    m_dp = all_dp_medians[c]
    norm = m_dp / autosomal_dp
    m_baf = st.median(baf[c])
    dev = st.median([abs(b - 0.5) for b in baf[c]])
    flag = ""
    if c != "X":
        if abs(norm - 1) > 0.03:
            flag += " DEPTH_SHIFT"
        if dev > 0.09:  # 二倍体典型值 ~0.05-0.07（取决于深度）
            flag += " BAF_SHIFT"
    print(f"{c:>4} {len(baf[c]):>8} {m_dp:>6.0f} {norm:>6.3f} {m_baf:>7.3f} {dev:>11.3f} {flag}")
