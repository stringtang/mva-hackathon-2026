# Track 1 — Variant Prediction: Methods

**Proband:** WGS_EX2312012 · **Assembly:** GRCh38 · **Submission:** `stringtang_bub1b-compound-het-unbiased.csv`

---

## 1. Summary of the prediction

A **compound heterozygous pair in *BUB1B*** (15q15.1), consistent with **Mosaic Variegated Aneuploidy syndrome 1** (MVA1; OMIM 257300; autosomal recessive):

| | Allele 1 | Allele 2 |
|---|---|---|
| GRCh38 | chr15:40209701 T>G | chr15:40220612 T>G |
| HGVS (NM_001211.6 / ENST00000287598.11) | c.2210T>G p.(Leu737Ter) | c.3006T>G p.(Asn1002Lys) |
| Location | exon 17/23 | exon 23/23, kinase domain |
| Consequence | nonsense (predicted NMD) | missense |
| gnomAD v4 | AC 111 / 1,111,986 exomes NFE (~1e-4) | AC 1 / 1,112,006 exomes (~9e-7) |
| ClinVar | **VCV000533901 Pathogenic/Likely pathogenic for MVA1**, multiple submitters, no conflicts | not present |
| In silico | n/a (LoF) | AlphaMissense **0.923**, MVP 0.852, REVEL 0.472 |

This matches the canonical MVA1 genotype architecture: **one null allele plus one hypomorphic allele**. Hanks et al. (2004, *Nat Genet* 36:1159) reported that every family carried one missense and one truncating/absent-transcript mutation, and explicitly found *no* cases with biallelic missense or biallelic truncating mutations.

---

## 2. Pipeline

All analysis ran **locally**; no individual-level genomic data left the machine (see §6).

```
proband VCF (Sentieon Haplotyper/GVCFtyper, GATK VariantFiltration; 5,012,204 records)
   │
   ├─(A) Unbiased phenotype-driven prioritisation ── Exomiser 15.1.0 / data 2512
   │        hiPhive (human-only) + OMIM prioritiser
   │        pathogenicity: REVEL, MVP, AlphaMissense, SpliceAI
   │        inputs: VCF + the 8 supplied HPO terms only
   │
   ├─(B) Locus completeness audit ── BUB1B ±5 kb, upstream 50 kb regulatory window
   │
   ├─(C) Structural interpretation ── AlphaFold AF-O60566-F1 v6 local geometry
   │
   ├─(D) Read-level verification ── alignment-free k-mer genotyping from raw FASTQ
   │        with genome-wide probe-uniqueness QC
   │
   └─(E) Secondary findings ── ACMG SF v3.3 (84 genes) × ClinVar; pharmacogenomics
```

### (A) Unbiased prioritisation — the central methodological claim

The submitted answer was **not** obtained by looking up the known MVA gene. It was recovered by a phenotype-driven run that received only the VCF and the supplied HPO terms.

Filter cascade (Exomiser log):

| Stage | Variants remaining |
|---|---|
| Input | 4,933,759 |
| Failed-variant filter | 4,701,716 |
| Allele-balance filter | 4,497,268 |
| Variant-effect filter | 23,930 |
| Frequency filter (<2%) | 1,010 |
| Inheritance-mode filter | **588** (363 genes) |

**Result: *BUB1B* ranks #1 genome-wide**, combined score **0.5565**, under the autosomal-recessive compound-heterozygous model. The runner-up (*FANCD2*, 0.219) is contributed by two indels already classified Benign/Likely benign in ClinVar — i.e. the noise floor sits 2.5× below the signal. The two variants Exomiser selected as the contributing compound-het pair are exactly the two reported above.

Parameters follow the published Exomiser optimisation study (*Genome Medicine* 2025), which raised top-10 recall from 49.7% to 85.5% on 386 UDN probands: human-only hiPhive, the REVEL/MVP/AlphaMissense/SpliceAI score set, and explicit avoidance of normalised CADD and the legacy SIFT/PolyPhen/MutationTaster trio. The ClinVar whitelist was left at its preset default; note that allele 1 is whitelisted, so the ranking is reported alongside the independent lines of evidence in §3 rather than resting on ClinVar alone.

### (B) Locus completeness

MVA1's second allele is frequently **non-coding** — documented forms include deep-intronic splice variants, an intronic *Alu* insertion (Kato 2017), and an intergenic SNV 44 kb upstream of the TSS (Ochiai 2014, *PNAS*). A coding-only search can therefore miss it. We audited:

- ***BUB1B* ± 5 kb:** 17 variants (16 PASS). Only 2 fall within exons ± 12 bp — the two reported.
- **Upstream 50 kb (chr15:40,110,984–40,160,984):** 74 variants (71 PASS, 45 heterozygous). The published Japanese founder hypomorph **rs576524605 (chr15:40117088 G>A) is absent** in this proband — a clean negative control consistent with the second allele here being coding.

### (C) Structural interpretation of p.Asn1002Lys

From AlphaFold AF-O60566-F1 (v6), computed locally:

- Asn1002 sits at **pLDDT 91.1**, inside a well-ordered region (mean pLDDT 91.4 across residues 992–1012; kinase domain 766–1050 mean 81.9 vs 63.6 full-length).
- Its Cβ has **12 contacts within 8 Å**, the nearest being **Val998 (3.4 Å), Phe977 (4.6 Å), Trp978 (5.1 Å), Ile1000, Phe997, Trp973** — a buried aromatic/hydrophobic cluster. Introducing a charged lysine is a classic destabilising substitution.
- **Internal consistency check:** the missense residues shown experimentally to *destabilise* BUBR1 (R814, I909, L1012 — Suijkerbuijk 2010, *Cancer Res* 70:4891) all sit in well-ordered kinase-domain positions (pLDDT 88.5, 87.0, 95.3), whereas R550 — shown *not* to reduce protein level — falls in a disordered linker (pLDDT 35.3). The structural confidence landscape reproduces the published functional stratification, which supports placing Asn1002 in the destabilising class.
- Asn1002 lies **10 residues** from Leu1012, the Hanks family-3 hypomorph.

This matters mechanistically: BUBR1 is a **pseudokinase**, so kinase-domain missense variants act through reduced protein abundance (5–10× faster turnover), not loss of catalysis. The disease mechanism is **dosage insufficiency**.

### (D) Read-level verification — alignment-free k-mer genotyping

**Results.** All 8 supplied FASTQ files were scanned (~80 GB; the nominal 44× depth):

| Locus | ref | alt | depth | VAF | Call |
|---|---|---|---|---|---|
| *BUB1B* c.2210T>G p.(Leu737Ter) | 16 | 16 | 32 | 0.50 | heterozygous |
| *BUB1B* c.3006T>G p.(Asn1002Lys) | 11 | 13 | 24 | 0.54 | heterozygous |
| *DPYD* \*2A (rs3918290) | 38 | 0 | 38 | 0 | reference homozygote |
| *DPYD* c.2846A>T (rs67376798) | 40 | 0 | 40 | 0 | reference homozygote |
| *DPYD* HapB3 (rs75017182) | 49 | 0 | 49 | 0 | reference homozygote |
| *DPYD* Y186C (rs115232898) | 41 | 0 | 41 | 0 | reference homozygote |
| *TPMT* \*3C (rs1142345) | 85 | 0 | 85 | 0 | reference homozygote † |
| *TPMT* \*3B (rs1800460) | 74 | 0 | 74 | 0 | reference homozygote ‡ |
| *NUDT15* \*3 (rs116855232) | 50 | 0 | 50 | 0 | reference homozygote |

Both *BUB1B* variants are confirmed heterozygous by a route that bypasses the aligner and variant caller entirely, independently reproducing the VCF's allelic depths (Sentieon AD 21,25 and 15,13). The k-mer depths are lower because only reads with ≥15 bp flanking the variant are counted — a criterion applied identically to reference and alternate alleles, so it introduces no allelic bias.

† The QC prediction was borne out quantitatively: *TPMT*\*3C depth (85) is ≈2× the comparable loci (38–50), matching the expected contribution of *TPMTP2*-derived reads. The alternate probe is genome-unique, so the negative call stands; the depth figure at this locus should not be read as true coverage.

‡ **A second failure mode, caught and fixed.** The first pass returned ref = 0 *and* alt = 0 at *TPMT*\*3B — superficially "no coverage." Interrogating the surrounding window instead of accepting that result revealed the cause: this proband carries a **homozygous variant 14 bp upstream (chr6:18138983 G>A, GT 1/1)**, inside the 31-mer window. Every genuine read therefore carries A at that position while the reference-derived probe carries G, so the reference *and* alternate probes both failed to match, manufacturing a false coverage gap.

The fix is to make probes **sample-aware**: patch homozygous variants from the proband's own VCF into the window before deriving the reference and alternate k-mers (`TGATGGCAACTAATGCTCCTCTATCCCAAAT` → `TAATGGCAACTAATGCTCCTCTATCCCAAAT`). Re-scanning returned **ref = 74, alt = 0**, confirming the diagnosis.

This failure mode deserves emphasis because it is **silent**: exact k-mer matching is brittle to nearby variants, and the failure presents as absent coverage, which is easily misread as a sequencing gap. Without this check we would have reported *TPMT*\*3B as uncallable — conservative in direction but factually wrong. Together with the uniqueness scan, this defines two mandatory pre-flight checks for any reference-derived probe genotyping: **outward**, is the probe unique in the genome (guarding against pseudogene and repeat cross-talk); **inward**, does the probe match the sample's actual haplotype (guarding against nearby-variant false negatives). Heterozygous neighbours would require both haplotype versions of the probe; none occurred within the windows examined here.

**Clinical reading.** At every locus verified, the proband carries no known loss-of-function allele of *DPYD*, *TPMT*, or *NUDT15*, each supported by 38–85× measured coverage — that is, **confirmed reference, not merely absent from the VCF**. The distinction matters for a child receiving chemotherapy: a variant-only VCF cannot separate "wild-type" from "not sequenced," and PharmCAT's own documentation flags its `--absent-to-ref` option as DANGEROUS precisely because a poorly covered position silently becomes a false normal-metaboliser call. **CYP2D6 was not assessed** — its structural variants, copy-number changes and *CYP2D7* hybrid alleles put it beyond both this method and VCF-based calling, and it requires an alignment-based caller such as StellarPGx.

Full WGS realignment (12–30 h, tens of GB of BAM) is unnecessary to interrogate 9 specific loci. For each locus we take the reference 31-mer **centred on the variant** plus its alternate-allele counterpart, and both reverse complements, then stream every FASTQ once, counting exact matches on sequence lines only. Each spanning read with ≥15 bp flanking contributes exactly one count, so ref/alt counts are read counts and the criterion is identical for both alleles.

**Probe-uniqueness QC (essential, and where this method earns its keep).** k-mer genotyping is only valid if probes are genomically unique. Rather than assume this, we scanned the whole GRCh38 primary assembly (3,088,286,401 bp) and counted every probe k-mer:

- **All 9 alternate-allele k-mer sets occur 0 times in the reference** — a positive control confirming alt signal cannot arise from the reference sequence itself.
- 8 of 9 reference probes are unique.
- **TPMT\*3C (rs1142345) is not unique:** 7 of its reference k-mers occur twice. Locating the duplicates placed them at **chr3:42,145,646–42,146,371 = *TPMTP2*, a processed TPMT pseudogene.**

Consequence and handling: pseudogene-derived reads inflate the *reference* count at this locus, overstating apparent coverage; they cannot create false alternate calls, since the alt k-mer is absent genome-wide. A negative call at TPMT\*3C therefore remains safe, while any coverage claim there is caveated. The 7 confounded k-mers are excluded from the masked probe set used for scanning. TPMT pseudogene interference is a known clinical-genetics pitfall; this pipeline detects and quantifies it rather than silently inheriting it.

---

## 3. Evidence summary for the compound-heterozygous call

**Allele 1 — c.2210T>G p.(Leu737Ter)**
Nonsense in exon 17 of 23; the premature stop lies >50 nt upstream of the final exon-exon junction, predicting nonsense-mediated decay. ClinVar Pathogenic/Likely pathogenic **specifically for MVA1**. Falls in the same segment as the 731X/753X truncating alleles of published patient cell lines.

**Allele 2 — c.3006T>G p.(Asn1002Lys)**
Kinase-domain missense; 1 allele in 1.1 M gnomAD exomes; AlphaMissense 0.923; structurally destabilising (§C).

*Discordant predictors, reported transparently:* REVEL (0.472) disagrees with AlphaMissense (0.923) and MVP (0.852). We weight AlphaMissense more heavily here because the pathogenic mechanism is protein destabilisation within a folded domain — the regime AlphaMissense's structural training targets — whereas REVEL's conservation-weighted ensemble is less sensitive to stability effects in a pseudokinase whose catalytic residues are not under classical functional constraint.

*A ClinVar nuance that must not be over-read:* the same amino-acid change p.Asn1002Lys arising from **c.3006T>A** is in ClinVar as **Uncertain significance** (single submitter, "Inborn genetic diseases"). **PS1 is therefore not applicable.** This does not weaken the present call: in a recessive disease a hypomorphic allele carried heterozygously without a second hit is not expected to be pathogenic on its own, so a VUS classification in that context is appropriate. Pathogenicity here derives from the *trans* configuration with a null allele — which is precisely the MVA1 architecture.

**Phase — stated honestly.** The two variants are **10,911 bp apart**, far beyond Illumina fragment length, and no parental samples are available. Read-backed phasing is impossible in principle here (WhatsHap's own documentation notes most heterozygous pairs are not bridged by short-read pairs). *Trans* configuration is **inferred**, not demonstrated, from: (i) recessive disease requiring biallelic hits; (ii) two independently ultra-rare variants in the single gene whose phenotype matches; (iii) the published architecture in which the two alleles are inherited from different parents. We report this as an inference and do not claim resolution.

---

## 4. Phenotype input

The eight supplied HPO terms were used verbatim, with no additions:

HP:0002859 Rhabdomyosarcoma · HP:0000121 Nephrocalcinosis · HP:0004322 Short stature · HP:0001508 Failure to thrive · HP:0003202 Skeletal muscle atrophy · HP:0001622 Premature birth · HP:0001518 Small for gestational age · HP:0200067 Recurrent spontaneous abortion

Sex was set to **male**, derived from the data rather than assumed: chrX homozygous:heterozygous call ratio 108,682:8,375 (~13:1) plus 13,840 chrY records.

The parental miscarriage history is phenotypically informative rather than background: in chromosomal-instability disorders, reproductive loss is a recognised correlate.

---

## 5. Mosaicism assessment from bulk WGS — a quantified negative result

MVA is defined cytogenetically by mosaic aneuploidy across multiple chromosomes. We asked whether bulk blood WGS shows it.

**First pass — and why it was not sufficient.** Per-chromosome B-allele frequency and normalised depth over all PASS heterozygous SNPs (DP ≥ 15) gave a genome-wide autosomal median of **44×** and median |BAF − 0.5| ≈ 0.056 for most chromosomes, but chr16/17/19/20/21/22 showed 4.5–9% depth elevation. These are largely GC-rich chromosomes, so coverage bias was the obvious hypothesis — but a hypothesis is not a result, so we tested it.

**GC correction.** The genome was binned into 1 Mb windows; GC content was computed per window from the reference, and mean depth per window from heterozygous SNPs (≥100 SNPs/window; 2,707 usable windows). The dataset shows a clear monotonic GC–depth relationship (median depth 43× at GC 0.34, 44× at GC 0.38–0.42, 45× at GC 0.43–0.50). Correcting each chromosome against GC-matched windows collapsed **21 of 22 autosomes to a ratio of exactly 1.000**. The chr16/17/19/20/22 elevation is fully explained by GC content. **chr21 was the exception**: average GC (0.400) but elevated depth.

**Resolving chr21.** Because MVA is by definition a mosaic-aneuploidy disorder and trisomy 21 is among the reported events, this residual was pursued rather than dismissed. Window-level inspection showed the elevation is **not uniform**: it is confined to 5–13 Mb (window ratios up to 2.64), with every window from 14 Mb onward at ~1.00. That interval is the acrocentric short arm and pericentromeric satellite region, which attracts mismapped reads. The same pattern appears on the other acrocentrics and at known heterochromatic blocks — flagging windows with ratio > 1.15 independently recovered the centromere map (chr9 39–42 and 61–67 Mb spanning the 9q12 block, chr21 5–13 Mb, chr22 11–16 Mb, chr14/15 16–22 Mb, chr16 32–36 Mb, chr20 25–31 Mb; 71 windows total).

**Final estimate.** Using the median of GC-matched window ratios (robust to those outlier windows) and excluding flagged artefact windows:

| | Result |
|---|---|
| Range across all 22 autosomes | 0.9745 (chr11) – 1.0069 (chr22) |
| chr21 after correction | **1.0008** |
| Typical within-chromosome MAD | 0.0147 |

No chromosome departs from the ensemble by more than ~3%, which for a mosaic trisomy (depth ratio = 1 + f/2) bounds any clonal fraction at roughly **6% or below**. **There is no evidence of clonal or mosaic aneuploidy in this blood sample.** Note that absolute ratios carry a systematic offset of ~1.5% (the GC-matched reference pool itself contains artefact windows), so the informative quantity is that no chromosome stands apart from the others, not the absolute value.

**Interpretation.** This negative is expected, not contradictory. "Variegated" aneuploidy means *different cells carry different aneuploidies*; in a bulk pool these cancel, and no single chromosome reaches a detectable clonal fraction. Bulk short-read WGS at 44× cannot resolve variegated mosaicism below a few percent per chromosome — quantifying it requires per-cell data (karyotype, single-cell sequencing), which is where the clinical diagnosis came from. We report the bound rather than presenting the null as evidence of absence.

## 6. Data governance

- Raw sequence reads and the bulk VCF were processed **locally by scripts only** and were not transmitted to any third-party service. Aggregate statistics and finalist-candidate variant detail — content that appears in this CC BY 4.0 submission — were exposed to an AI assistant as disclosed below.
- Public resources queried by coordinate/identifier only (Ensembl REST, AlphaFold); annotation databases (ClinVar, Exomiser 2512, GRCh38) were downloaded and run locally.
- No attempt was made to contact the data subject, family, or MVA Society, per the Hackathon Rules.
- All data will be deleted within 30 days of Hackathon close, with confirmation emailed to the organisers.

The organisers have since issued formal guidance on this point (FAQ: "Are third-party LLMs allowed with this Hackathon's dataset?", with the detailed answer in the Community discussion). Sage Bionetworks' Chief Privacy Officer draws the distinction between a **processor** — "a service that processes data solely to return a result to you, takes no rights in it, and cannot use it for its own purposes" — and a **recipient**, which "gains the right to use, retain, or learn from the data". Use of an LLM API is permitted where (i) there is no training on inputs or outputs and the provider takes no rights in either, and (ii) retention is limited in time and purpose; zero retention is not required, and short-lived logs for abuse monitoring or debugging are acceptable. Participants must record the provider, plan or tier, and the relevant setting. The deletion obligation extends to systems under participant control, not to a provider's short-lived logs.

**AI-assistance disclosure** (per the 28 Aug 2026 update to the submission instructions). Provider: **Anthropic**. Product: **Claude Code**, model **Claude Fable 5.1**. Plan: **Max subscription**. The model was used for analysis design, code authoring, literature synthesis and report drafting. Scope of proband data exposed to the model: the supplied phenotype description and HPO terms; aggregate statistics (filter-cascade counts, per-chromosome depth and BAF summaries, k-mer totals); and variant-level detail for the finalist set only — the two *BUB1B* alleles, the twelve ClinVar-conflicting variants reviewed in the ACMG SF screen, and the nine pharmacogenomic loci — all of which appear in this CC BY 4.0 submission. **Not exposed:** raw sequence reads, the bulk VCF, or any genome-wide variant listing; those were processed exclusively by local scripts whose outputs are the aggregates above.

We note the organisers' caution that credit or grant programmes may attach terms overriding an account's defaults — relevant here because Anthropic sponsors the prize credits — and that disabling training is not always complete.

## 7. Reproducibility

Code: see the accompanying GitHub repository. Pinned versions: Exomiser **15.1.0** / data **2512**; ClinVar GRCh38 **2026-08-22**; Ensembl REST **r116**; AlphaFold **AF-O60566-F1 v6**; bcftools/samtools **1.24**; ACMG SF **v3.3** (84 genes, obtained from ClinGen — the NCBI ClinVar ACMG page still documents v3.2 and should not be used as the source).

Note on Exomiser versioning: release 15.0.0 changed the combined-score model to incorporate automated ACMG assignment, so scores are **not comparable** with 14.x results. The data bundle is pinned explicitly because the documentation references a version (2602) that returns HTTP 404 on the data server; 2512 is the newest available.

## 8. Known limitations

1. Phase is inferred, not demonstrated (§3).
2. The supplied VCF contains SNVs/indels only — **no CNV/SV calling**. Given that an intronic *Alu* insertion has caused MVA1 (Kato 2017), a structural-variant search of the raw reads would be a genuine completeness gain and is not covered here.
3. Read-level verification interrogates **nine pre-specified loci**, not the genome. It confirms and refutes specific hypotheses; it does not discover new variants. *CYP2D6* is explicitly out of scope (see §2D).
4. The nine loci were checked for *homozygous* neighbouring variants within each probe window. A *heterozygous* neighbour would require haplotype-resolved probes; none was present here, but a general implementation must handle that case.
5. Mosaic aneuploidy quantification is under-powered in bulk WGS (§5).
6. Secondary-findings screening used ClinVar classifications rather than de novo ACMG curation of novel variants, and inherits the same no-CNV limitation.
