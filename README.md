# MVA Hackathon 2026 — Submission

Entry for **Rare Disease, Real Kid: The MVA Hackathon 2026** (Sage Bionetworks · MVA Society · Hugging Face · BEACON).

**Proband:** WGS_EX2312012 · **Assembly:** GRCh38 · **Answer:** *BUB1B* compound heterozygote, MVA1 (OMIM 257300)

| | GRCh38 | HGVS (NM_001211.6) | Consequence |
|---|---|---|---|
| Allele 1 | chr15:40209701 T>G | c.2210T>G p.(Leu737Ter) | nonsense, exon 17/23 — NMD predicted |
| Allele 2 | chr15:40220612 T>G | c.3006T>G p.(Asn1002Lys) | missense, kinase domain — destabilising |

## Reports

- **[report/track1_methods.md](report/track1_methods.md)** — Track 1 methods: unbiased prioritisation, locus audit, structural interpretation, read-level verification, mosaicism assessment, secondary findings, governance, limitations.
- **[report/track2_report.md](report/track2_report.md)** — Track 2 drug repurposing: mechanism worked from this proband's data, ranked candidates, trial design, stated unknowns.
- **[report/track2_pitch_script.md](report/track2_pitch_script.md)** — 3-minute pitch script and shot list.

## Headline results

**Unbiased recovery.** Exomiser 15.1.0 (data 2512) given only the VCF and the eight supplied HPO terms ranked *BUB1B* **#1 genome-wide** from 4,933,759 input variants (combined score 0.5565; runner-up 0.219, whose contributing variants are ClinVar-benign indels). The compound-heterozygous pair it assembled is exactly the submitted answer — no *BUB1B* prior was used.

**Read-level confirmation, alignment-free.** All 8 FASTQ files scanned with variant-centred 31-mers, bypassing aligner and variant caller: L737X 16 ref / 16 alt (VAF 0.50), N1002K 11 / 13 (VAF 0.54).

**Two silent failure modes found and fixed** — the methodological contribution:
1. *Outward:* genome-wide probe-uniqueness scan (3.09 Gbp) flagged **TPMT\*3C** probes shared with the **TPMTP2 pseudogene** on chr3, inflating apparent coverage ~2×. Confounded k-mers masked.
2. *Inward:* **TPMT\*3B** returned zero coverage — not a sequencing gap but a **homozygous variant 14 bp away** breaking exact matching. Sample-aware probes restored it to 74× / 0 alt.

**Secondary findings.** ACMG SF v3.3 (84 genes, ClinGen source) × ClinVar across 11,277 variants: **no reportable pathogenic findings**. Seven chemotherapy-toxicity loci (*DPYD* ×4, *TPMT* ×2, *NUDT15*) verified at 38–85× as **confirmed reference** — not merely absent from a variant-only VCF, a distinction that matters for a child receiving chemotherapy.

**Mosaicism.** GC-corrected, artefact-filtered per-chromosome depth bounds any clonal aneuploid fraction at **≤6%** in blood. Consistent with variegated mosaicism averaging out in bulk.

## Pipeline

```
01_bub1b_region_scan.py        locus scan with exon/splice annotation
02_mosaic_aneuploidy_scan.py   first-pass BAF/depth per chromosome
03_acmg_sf_screen.py           ACMG SF v3.3 × ClinVar secondary findings
04_kmer_verify.py              alignment-free probe construction and scanning
05_probe_uniqueness_qc.py      genome-wide probe uniqueness (mandatory pre-flight)
06_locate_dup_kmers.py         locate non-unique probes (found TPMTP2)
07_scan_fastq.sh               parallel FASTQ scan
08_make_track1_submission.py   submission CSV
09_gc_depth_correction.py      GC–depth model and correction
10_chr21_check.py              chr21 residual: mosaic trisomy vs artefact
11_mosaic_final.py             robust final mosaicism bound
exomiser/                      analysis config, phenopacket, results
```

**Reproducing.** Requires access to the gated dataset. Install bcftools/samtools 1.24, Java 21, Exomiser 15.1.0 + data 2512, ClinVar GRCh38, GRCh38 primary assembly. Run `01`–`11` in order; `04 build` before `05`, then `07`.

## Data governance

No individual-level data is in this repository — `data/` and `refs/` are git-excluded. Analysis ran entirely locally; no raw sequence or variant-level data was sent to any third-party service, including hosted LLM APIs. This is stricter than the organisers' published guidance requires (FAQ: *Are third-party LLMs allowed with this Hackathon's dataset?*). No contact was attempted with the data subject, family, or MVA Society. All controlled data will be deleted within 30 days of Hackathon close with confirmation emailed to the organisers.

## Acknowledgement

This work was made possible through the Hackathon, organized by Sage Bionetworks in partnership with the MVA Society, Hugging Face, and BEACON (The Benchmarking, Evaluation, and Assessment Consortium for Science), with prize sponsorship from AWS and Anthropic. We are deeply grateful to the child and their family who generously contributed their data and their story to advance research into this rare disease. We acknowledge their trust in making this Hackathon possible.

Submissions released under CC BY 4.0.
