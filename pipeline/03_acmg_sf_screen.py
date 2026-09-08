#!/usr/bin/env python3
"""ACMG SF v3.3（84 基因）次要发现筛查。

流程：Ensembl 批量取基因坐标（公开元数据）→ 患儿 VCF 区域提取（本地）
→ 本地 ClinVar VCF 精确 (pos,ref,alt) 匹配 → 输出 P/LP 命中。

输出策略：聚合计数 + 命中行（命中行是拟报告的候选，允许进上下文）。
CLNSIG 规则：顶层以 Pathogenic / Likely_pathogenic / Pathogenic/Likely_pathogenic
开头者入选；Conflicting 单独计数不入选。评审状态排除 no_assertion*。
"""
import json
import subprocess
import urllib.request

BASE = "/Users/leotang/test/mva-hackathon"
VCF = f"{BASE}/data/WGS_EX2312012_HGWCNDSX7.vcf.gz"
CLINVAR = f"{BASE}/refs/clinvar.vcf.gz"
GENES = [l.strip() for l in open(f"{BASE}/refs/acmg_sf_v33_genes.txt") if l.strip()]

# 1. 基因坐标（Ensembl 批量 POST，公开元数据）
req = urllib.request.Request(
    "https://rest.ensembl.org/lookup/symbol/homo_sapiens",
    data=json.dumps({"symbols": GENES}).encode(),
    headers={"Content-Type": "application/json", "Accept": "application/json"})
info = json.load(urllib.request.urlopen(req))
regions = {}
for g in GENES:
    d = info.get(g)
    if not d:
        print(f"WARN: {g} 无坐标")
        continue
    regions[g] = (d["seq_region_name"], d["start"] - 500, d["end"] + 500)
print(f"取得坐标: {len(regions)}/{len(GENES)} 基因")

def norm_records(vcf, chrom, start, end):
    """返回 {(pos,ref,alt): info} — 多等位拆分。"""
    out = {}
    p = subprocess.run(
        ["bcftools", "norm", "-m", "-any", "-r", f"{chrom}:{start}-{end}", vcf],
        capture_output=True, text=True)
    for line in p.stdout.splitlines():
        if line.startswith("#"):
            continue
        f = line.split("\t")
        out[(int(f[1]), f[3], f[4])] = f
    return out

def clnsig_ok(sig):
    top = sig.split("|")[0]
    return top.startswith(("Pathogenic", "Likely_pathogenic")) and \
        not top.startswith("Pathogenic_")  # 排除 low_penetrance 等修饰主类的形态由人工复核

hits, n_child_vars, n_conflict_match = [], 0, 0
for g, (chrom, start, end) in sorted(regions.items()):
    child = norm_records(VCF, chrom, start, end)
    n_child_vars += len(child)
    if not child:
        continue
    cv = subprocess.run(["tabix", CLINVAR, f"{chrom}:{start}-{end}"],
                        capture_output=True, text=True)
    for line in cv.stdout.splitlines():
        f = line.split("\t")
        key = (int(f[1]), f[3], f[4])
        if key not in child:
            continue
        inf = dict(kv.split("=", 1) for kv in f[7].split(";") if "=" in kv)
        sig = inf.get("CLNSIG", "")
        rev = inf.get("CLNREVSTAT", "")
        if "no_assertion" in rev:
            continue
        if sig.split("|")[0].startswith("Conflicting"):
            n_conflict_match += 1
            continue
        if not clnsig_ok(sig):
            continue
        cf = child[key]
        fmt = dict(zip(cf[8].split(":"), cf[9].split(":")))
        hits.append({
            "gene": g, "chrom": chrom, "pos": key[0], "ref": key[1], "alt": key[2],
            "GT": fmt.get("GT"), "AD": fmt.get("AD"), "FILTER": cf[6],
            "CLNSIG": sig, "REVSTAT": rev,
            "HGVS": inf.get("CLNHGVS", ""), "DISEASE": inf.get("CLNDN", "")[:80],
        })

print(f"\n84 基因区域内患儿变异总数（含常见多态）: {n_child_vars}")
print(f"与 ClinVar Conflicting 记录重合（人工复核池）: {n_conflict_match}")
print(f"P/LP 命中: {len(hits)}\n")
for h in hits:
    print(f"  {h['gene']} {h['chrom']}:{h['pos']} {h['ref']}>{h['alt']} GT={h['GT']} AD={h['AD']} FILTER={h['FILTER']}")
    print(f"    {h['CLNSIG']} [{h['REVSTAT']}]")
    print(f"    {h['HGVS']} | {h['DISEASE']}")

with open(f"{BASE}/pipeline/acmg_sf_hits.json", "w") as fh:
    json.dump(hits, fh, indent=1)
print("\n已写入 pipeline/acmg_sf_hits.json")
