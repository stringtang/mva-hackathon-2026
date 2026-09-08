# Track 2 — Drug Repurposing

## A mechanism-first proposal for *BUB1B*-associated Mosaic Variegated Aneuploidy

**Proband:** WGS_EX2312012 · **Genotype:** *BUB1B* c.2210T>G p.(Leu737Ter) / c.3006T>G p.(Asn1002Lys), compound heterozygous

**Code:** https://github.com/stringtang/mva-hackathon-2026 · **Pitch video:** https://youtu.be/1amvH7Bh1Ew

> These are hypotheses for follow-up, not evidence that any medicine works. Nothing here is clinical advice, and no proposal below should be acted on outside a properly governed research setting.

---

## 1. The direction error this field invites, and why it matters here

Almost the entire literature on "targeting aneuploidy" is **anticancer**: it seeks compounds that selectively kill aneuploid cells (Tang et al., *Cell* 2011; Zhou et al., *Open Biol* 2020; Cohen-Sharir et al., *Nature* 2021). That logic inverts in constitutional MVA. Here the aneuploid cells **are the patient's own tissue** — brain, marrow, gut. A compound that selectively kills aneuploid cells is, in this child, a compound that selectively kills him.

We state this first because it is the most likely way a reasonable reader goes wrong, and because it disqualifies the largest body of apparently relevant pharmacology.

The second attractor is senolytics, and it fails for a different reason. Section 3 gives the argument in full; the short version is that the senescence-clearance evidence in BubR1-insufficient mice is **genetic, not pharmacological**, and the one genetic experiment that extended lifespan also **significantly increased tumour burden** (Baker et al., *Nat Cell Biol* 2008) — in a child whose defining risk is rhabdomyosarcoma, Wilms tumour and leukaemia.

The direction that survives is the one with a positive control: **raising BubR1 abundance reduced aneuploidy, reduced cancer, and extended lifespan** (Baker et al., *Nat Cell Biol* 2013). The goal in this child is therefore to **increase residual BubR1 and relieve the downstream stress it fails to prevent**, not to remove the cells its deficiency produces.

---

## 2. What this proband's genotype implies — worked from the data, not from the literature

The therapeutic logic below depends on a specific claim: that this is a **protein-dosage disease**, and that essentially all of the child's functional BubR1 comes from one allele. We derive that here.

### 2.1 Allele 1, c.2210T>G p.(Leu737Ter): predicted null

Computed from the canonical transcript ENST00000287598 (1,050 aa; CDS 3,153 nt across 23 coding exons):

| | |
|---|---|
| PTC position | c.2210, exon **17 of 23** |
| Last exon–exon junction | c.2957 |
| PTC → last junction | **747 nt upstream** |
| 50–55 nt rule | exceeded ~14-fold → **NMD strongly predicted** |
| If NMD were escaped | 736 aa product, C-terminal **314 residues lost** |
| Kinase domain (≈766–1050 aa) | **entirely absent** from any escape product |

Either branch yields no functional protein: the transcript is degraded, or the product lacks the whole kinase domain. **Allele 1 contributes ≈ 0 to the functional BubR1 pool.**

*Caveat:* NMD is a prediction. Confirming it needs patient RNA, which this dataset does not include. We flag this as the single cheapest experiment that would firm up the model (§7).

### 2.2 Allele 2, c.3006T>G p.(Asn1002Lys): predicted hypomorph acting through destabilisation

Population and computational evidence: 1 allele in 1,112,006 gnomAD v4 exomes (~9×10⁻⁷); AlphaMissense **0.923**, MVP 0.852 (REVEL 0.472 dissents — see the Track 1 methods for why we weight AlphaMissense here).

Structural analysis computed locally on AlphaFold AF-O60566-F1 v6:

- Asn1002 sits at **pLDDT 91.1** in a well-ordered region (residues 992–1012 mean 91.4).
- Its Cβ has 12 contacts within 8 Å, the nearest being **Val998 (3.4 Å), Phe977 (4.6 Å), Trp978 (5.1 Å)**, plus Ile1000, Phe997, Trp973 — a buried aromatic/hydrophobic cluster. Asn→Lys introduces a charge into that core.
- **Internal control:** the missense residues shown experimentally to *destabilise* BUBR1 (R814, I909, L1012; Suijkerbuijk et al., *Cancer Res* 2010) all occupy well-ordered kinase-domain positions (pLDDT 88.5, 87.0, 95.3), while R550 — shown *not* to reduce protein level — lies in a disordered linker (pLDDT 35.3). The structural confidence landscape reproduces the published functional split, which is why we place Asn1002 in the destabilising class rather than asserting it.
- Asn1002 is **10 residues** from Leu1012, the Hanks family-3 hypomorph.

The mechanism matters more than the label. **BUBR1 is a pseudokinase** (Suijkerbuijk et al., *Dev Cell* 2012). Kinase-domain missense variants therefore cannot act by abolishing catalysis; Suijkerbuijk 2010 showed they act by **accelerating turnover**, reducing BUBR1 abundance 5–10 fold. The lesion is quantity, not activity.

### 2.3 The consequence that drives everything below

Allele 1 makes nothing. Allele 2 makes a protein that is degraded too fast. Therefore:

> **All of this child's functional BubR1 originates from a single allele whose product is being destroyed faster than normal.**

This is the pharmacological opening. An intervention that slows BubR1 degradation acts on **100%** of his functional protein pool, not on half of it. Conversely, an intervention aimed at restoring catalytic activity has no target, because catalysis was never the defect.

### 2.4 An honest tension in the dosage arithmetic

Taking the numbers at face value — one null allele, one allele producing protein at 1/5 to 1/10 of normal — gives a residual of roughly **5–10% of wild-type**. Sieben et al. (*J Clin Invest* 2020) place >90% reduction in the range of progeria or early postnatal lethality, and 40–90% reduction in the range of tumour predisposition with milder ageing phenotypes.

This proband is alive in childhood with cancer predisposition, i.e. clinically in the milder band. Three readings are possible, and we cannot currently distinguish them:

1. **N1002K is a weaker destabiliser** than the 5–10× variants characterised in 2010. Its position 10 residues from L1012 is suggestive but not quantitative.
2. **The mouse thresholds do not transfer** quantitatively to human.
3. **Some NMD escape occurs**, leaving a partial contribution from allele 1 that the model omits.

We raise this rather than smoothing it because it is directly actionable: measuring BubR1 protein level in patient fibroblasts would discriminate among all three, and would calibrate how much headroom any dosage-raising therapy actually has. It is the second cheap experiment we would propose (§7).

### 2.5 What we could and could not see in the genome

Bulk WGS at 44× showed **no clonal or mosaic aneuploidy** in blood: after GC correction and exclusion of pericentromeric artefact windows, all 22 autosomes fall within 0.9745–1.0069 of the ensemble, bounding any clonal fraction at roughly ≤6% (Track 1 methods §5). This is consistent with, not contradictory to, the diagnosis — "variegated" means different cells carry different aneuploidies, which cancel in a bulk pool. It does mean that **any trial endpoint based on aneuploidy in this child must be per-cell**, which shapes §6.

---

## 3. Why we do not lead with senolytics

This is the answer the field expects, and we think it is wrong here. Setting it aside explicitly is part of the argument.

**The BubR1 senescence evidence is genetic, not pharmacological.** Baker et al. (*Nature* 2011) cleared p16-expressing cells from BubR1^H/H mice using the INK-ATTAC transgene plus the dimerizer AP20187 — a research reagent with no clinical counterpart. Adipose loss, sarcopenia, cataract onset and exercise capacity improved; **cardiac arrhythmia, arterial stiffening and overall survival did not**. No senolytic *drug* — not dasatinib + quercetin, not navitoclax, not fisetin — has ever been tested in a BubR1-insufficient model.

**The p16 axis is a cancer trap in this background.** Baker et al. (*Nat Cell Biol* 2008): ablating *p16Ink4a* in BubR1^H/H mice extended lifespan 25% and delayed lordokyphosis threefold — and produced **significantly more tumours**, 8 of 9 being lung adenocarcinomas. Senescence in a BubR1-deficient background is doing real tumour-suppressive work. In a child with a rhabdomyosarcoma already resected, dismantling that barrier is close to disqualifying.

**Paediatric specifics compound the problem.** Quercetin suppresses both NHEJ and homologous recombination and **increased MLL rearrangement frequency in human HSPCs** (Biechonski et al., *Int J Cancer* 2017) — in a child with documented MDS/AML/ALL risk. Dasatinib's label carries growth retardation, delayed epiphyseal fusion and osteopenia — in a child with severe short stature and failure to thrive — plus pulmonary arterial hypertension. All 22 registered D+Q trials set a minimum age of 18; there is no paediatric senolytic experience of any kind.

**Navitoclax we exclude outright**, rather than ranking it low: never approved, on-target dose-limiting thrombocytopenia, in a syndrome with documented MDS with monosomy 7 and marrow failure.

---

## 4. Candidates, ranked

Each is assessed on mechanistic fit to §2.3, evidence strength, paediatric feasibility, and how it would be falsified.

### 4.1 First — NAD⁺ precursor (nicotinamide riboside)

**Mechanistic fit: highest, and specific to this genotype.** BubR1 is acetylated at two lysines with opposite consequences, both substrates of SIRT2: **K250** acetylation *protects* BubR1 from APC/C-mediated degradation in mitosis; **K668** acetylation *promotes* ubiquitin-mediated degradation in interphase (Bloom & North, *Cell Biosci* 2021). Since this child's entire functional pool is a rapidly-degraded protein (§2.3), the degradative arm is the mechanistically correct handle.

**Evidence — and its limits.** North et al. (*EMBO J* 2014) showed a SIRT2 transgene extended median lifespan of BubR1^H/H mice by **58%** overall and 123% in males (no effect in females). Two caveats we will not paper over: (i) the **NMN experiment in that paper was done in wild-type mice for 7 days**, reading out BubR1 protein in testes — NMN was never given to BubR1^H/H animals; (ii) the same SIRT2 transgenic line showed **no lifespan effect on a normal background** in an independent replication (Wu et al., *Aging Cell* 2023), which those authors reconcile as a BubR1-specific effect — a reading that favours this application but leaves the mechanism singly-sourced. Note also the bidirectionality: SIRT2 deacetylates both the protective and the degradative site, so "activate SIRT2" is not unambiguously BubR1-raising. This is a real weakness in the causal chain.

**Paediatric feasibility: the strongest of any candidate.** NAD⁺ precursors have been dosed in **ataxia-telangiectasia — another paediatric chromosome-instability, cancer-predisposition syndrome — from age ≥2, for two years, orally, well tolerated**, with NAD⁺ levels rising and stabilising (Presterud et al., *Mov Disord* 2024); PBMC transcriptomics from that cohort showed NAD⁺ augmentation **suppressed interferon-response genes**. A double-blind randomised crossover of NR in Werner syndrome met several secondary endpoints (Shoji et al., *Aging Cell* 2025; n=9 enrolled, 6 per-protocol). NR is supplement-grade; NMN became lawful in US supplements in September 2025.

**Falsification.** If BubR1 protein in patient fibroblasts does not rise on NR exposure in vitro, the hypothesis fails before any child is dosed. That assay is cheap and should gate everything downstream.

### 4.2 Second — rapamycin / mTOR inhibition

**Mechanistic fit: moderate, via two independent routes.** Sieben et al. (*J Clin Invest* 2020) found hyperactive mTORC1 in BubR1-mutant muscle associated with sarcopenia — relevant to this child's documented skeletal muscle atrophy and failure to thrive. Separately, González-Blanco et al. (*Nat Commun* 2026) showed that in a *Drosophila* MVA model (SAC depletion in neural stem cells) microcephaly arises through **proteostasis failure and mitochondrial dysfunction** downstream of complex aneuploidy.

**Why this is the most under-cited candidate:** in that 2026 paper, **rapamycin — the actual drug, not a genetic manipulation — rescued the brain phenotype**, with mitochondrial chaperones and ROS scavengers giving the fullest rescue. It is the only *pharmacological* rescue in an MVA-specific model in the literature, it is four months old, and it is direction-correct: it **rescues** aneuploid tissue rather than killing it. (We note an unresolved tension in that paper's figures between the autophagy/TOR grouping and the rapamycin result; the effect size should be read from the figures rather than quoted from us.)

**Paediatric feasibility: strong.** Everolimus is approved for TSC-associated SEGA from age 1 and for TSC seizures from age 2; sirolimus from age 13 systemically and age 6 topically. Immunosuppression is the principal concern, and MVA has documented infection deaths — which argues for the lowest effective exposure and for treating this as a later-line hypothesis than §4.1.

**Cautionary precedent we volunteer:** mTOR inhibitors had excellent mechanism and animal data in ADPKD and failed two simultaneous NEJM trials. Mechanism is not enough.

### 4.3 Third — metformin

**Mechanistic fit: indirect** (AMPK activation; converges with the one aneuploidy-chemoprevention result, where oral resveratrol or aspirin repressed tetraploid-cell accumulation via AMPK — Lissa et al., *PNAS* 2014).

**Why it earns a place: the paediatric safety data transfer directly.** In Fanconi anaemia — a paediatric chromosome-instability cancer-predisposition syndrome — metformin was given to 14 children (median age 9.4, range 6.0–26.5) for 6 months; **13/14 tolerated maximal age-based dosing with no grade ≥3 attributable events** (Pollard et al., *Blood Adv* 2022). In FA mice it delayed tumour onset; in Li-Fraumeni mice it improved cancer-free survival.

**The objection we pre-empt.** Lyu et al. (*Food Chem Toxicol* 2022) report that metformin induces micronuclei and **deregulates BUBR1 and MAD2 expression** — a paper any reviewer will find, in a proposal about BubR1. The concentrations were **1–16 mM versus therapeutic human plasma levels of ~10–40 µM**, two to three orders of magnitude apart. This is not evidence that clinical metformin is genotoxic. It does argue that any trial must carry a mandatory micronucleus safety readout — which, conveniently, is the same assay as the efficacy endpoint (§6).

### 4.4 Fourth — JAK inhibition (the most novel angle here)

**Mechanistic fit: moderate, and the connection appears not to have been made.** Chromosome missegregation produces micronuclei, whose rupture activates cGAS–STING and drives type I interferon and NF-κB signalling (Mackenzie et al., *Nature* 2017; Harding et al., *Nature* 2017; Bakhoum et al., *Nature* 2018). In the *MAD1L1* aneuploidy syndrome, single-cell RNA showed mitochondrial stress with systemic inflammation and enhanced interferon/NF-κB signalling **in both aneuploid and euploid cells**, implying a non-cell-autonomous response (Villarroya-Beltri et al., *Sci Adv* 2022). Malumbres & Villarroya-Beltri (*Nat Rev Genet* 2024) list chronic immune response as a core MVA axis.

Two of our candidates converge on this readout: NAD⁺ augmentation **suppressed interferon genes** in the A-T cohort (§4.1). That convergence is testable.

**Paediatric feasibility: real.** Baricitinib has published paediatric PK and dosing in CANDLE and SAVI interferonopathies, and JAK1/2 inhibitors have treated-versus-untreated comparisons in AGS.

**Tension we state plainly:** adding immunosuppression with a class malignancy warning to a cancer-predisposition syndrome is a genuine problem. We rank this fourth for that reason, and would propose it only if an interferon signature were first *demonstrated* in this child's cells.

### 4.5 Zero-risk comparator arm

Exercise and micronutrient sufficiency. Exercise has never been tested as an intervention in a BubR1 model — it appears in those papers as an *outcome measure* — but it prevented senescent-cell accumulation in adipose tissue in a diet-induced model (Schafer et al., *Diabetes* 2016). Folate/B12 sufficiency is linked to micronucleus frequency (Fenech, *Mutat Res* 2012), though largely through uracil misincorporation rather than checkpoint-dependent missegregation; claiming it corrects SAC-driven missegregation would overstate the mechanism. Costs nothing to include; should not be omitted from a comparator design.

### 4.6 Explicitly excluded

| | Reason |
|---|---|
| **Navitoclax** | Never approved; on-target thrombocytopenia in a syndrome with documented marrow failure |
| **Growth hormone** | Three independent MVA2 reports found it ineffective; generally contraindicated in cancer-predisposition syndromes |
| **SAC-weakening agents** (MPS1 inhibitors, reversine) | Direction-inverted: designed to weaken an already-insufficient checkpoint |
| **k-MT destabilisers** (the CIN-suppression strategy) | Also direction-inverted here. BubR1 recruits PP2A-B56 to counteract Aurora B and is *required to form stable* kinetochore–microtubule attachments (Suijkerbuijk et al., *Dev Cell* 2012), so BubR1-insufficient cells have attachments that are already under-stable — the opposite defect from CIN cancer cells, where the destabilise-k-MT strategy was developed |
| **Low-dose taxanes** | Directionally stabilises k-MTs, but never tested in a BubR1 background, and stabilising agents in a checkpoint-weak cell risk mitotic catastrophe. An in-vitro question at most; not a patient proposal |

---

## 5. Where this sits relative to work already underway

`"mosaic variegated aneuploidy" AND chemoprevention` returns **0 results** in PubMed; ClinicalTrials.gov returns **0 registered studies** for either "mosaic variegated aneuploidy" or *BUB1B*. This is a first-in-field proposal, not an extension of an existing literature — and it should be framed as such rather than implying precedent that does not exist.

The MVA Society is already funding four projects, of which **the first is drug repurposing** (a *C. elegans* MVA model screened against an FDA-approved compound library) and **the third is supplements and cell stability** — the latter at the laboratory of the author of the SIRT2–BubR1 mechanism. Our proposal is therefore positioned as **complementary, not duplicative**: we contribute a *case-specific mechanistic stratification* (which class of BubR1 lesion this child has, and therefore which therapeutic direction is even coherent) plus a reusable computational pipeline — not another phenotypic screen.

Two gaps in the only existing MVA guideline are worth naming. Nakano et al. (*Clin Cancer Res* 2024) recommend renal ultrasound every 3 months to age 7, avoidance of radiation, and HPV vaccination. But: (i) **no haematological surveillance is recommended** despite MDS/AML/ALL being listed among MVA1 cancers; (ii) surveillance **stops at age 7**, and rhabdomyosarcoma — this child's presenting malignancy — has no imaging protocol at all.

---

## 6. Proposed trial design — copied from paediatric chromosome-instability practice, not from geroscience

The template is **NCT03476330**: quercetin chemoprevention in Fanconi anaemia, Cincinnati Children's, phase 2, n=48, **age ≥2**, funded by the FDA Office of Orphan Products Development, with primary endpoint **"participants with ≥20% reduction of buccal micronuclei at 1 year."** Completed.

Why this template and not a geroscience one:

- **Micronuclei are the directly measurable phenotype of this disease.** MVA is chromosome missegregation; micronuclei are its cellular footprint. The endpoint measures the mechanism, not a surrogate borrowed from another field.
- **The assay is already validated in a paediatric CIN population**, from age 2, with regulatory and funding precedent.
- **It sidesteps an impossible endpoint.** With roughly 40 known patients worldwide, a cancer-incidence endpoint cannot be powered. This is the central design constraint of the disease and the reason a conventional efficacy trial is not on the table.
- Buccal sampling is non-invasive — material in a child under oncological care.

Inherited weaknesses we would carry and must state: single-arm, no control, surrogate endpoint, and in the source trial ~40% attrition with roughly half the analysable group meeting the endpoint and no comparator for spontaneous variation.

**Sequencing.** Given §2.4, we would not start with dosing. The order is: (1) patient-derived fibroblasts, measure baseline BubR1 protein and micronucleus frequency; (2) test whether NR raises BubR1 protein in those cells; (3) only if it does, proceed to an n-of-1 or small open-label design on the NCT03476330 template. Steps 1–2 also resolve the §2.4 ambiguity and cost little.

---

## 7. What we do not know, stated up front

1. **Senescence has never been demonstrated in human MVA or *BUB1B* patient cells.** The entire senolytic rationale — including our rejection of it — rests on mouse data. Proposing that measurement is a stronger opening than assuming it either way.
2. **NMD of allele 1 is predicted, not observed** (§2.1). Patient RNA would settle it.
3. **Residual BubR1 protein level in this child is unknown** (§2.4), and it determines how much headroom a dosage-raising therapy has.
4. **No verified age-at-cancer-onset distribution exists for MVA1.** Published cancer-risk figures span 21% to >85% and derive from cohorts with materially different genotype architectures; we decline to quote a single penetrance number.
5. **The SIRT2–BubR1 mechanism is singly-sourced** and has not been independently reproduced in a BubR1-insufficient background.
6. **There is essentially no literature on chronic drug exposure in a child with a chromosome-instability cancer-predisposition syndrome.** Existing guidance addresses radiation and treatment-related second cancers, not chronic non-cytotoxic agents. This is an open regulatory and ethical gap, not a solved problem.

---

## 8. Scalability

The pipeline behind this report generalises past this child:

**Unbiased phenotype-driven prioritisation → structural stratification of missense alleles into destabilising versus function-altering → therapeutic direction chosen by lesion class (raise abundance versus restore function) → secondary findings, including pharmacogenomics, as an immediate clinical by-product.**

The middle step is the transferable idea. "Which drug for which gene" does not generalise; "which *class* of lesion does this patient have, and therefore which therapeutic direction is even coherent" does. In this case it is what separates a defensible proposal from the field's default answer: because the lesion is destabilisation of a pseudokinase, slowing degradation is mechanistically coherent and restoring catalysis is not.

The alignment-free k-mer verification module (Track 1 methods §2D), including its two mandatory pre-flight checks — genome-wide probe uniqueness, and sample-aware probe construction — is reusable wherever read-level evidence is needed at specific loci without justifying a whole-genome realignment.

---

## 9. AI-assistance disclosure

**AI-assistance disclosure** (per the 28 Aug 2026 update to the submission instructions). Provider: **Anthropic**. Product: **Claude Code**, model **Claude Fable 5.1**. Plan: **Max subscription**. The model was used for analysis design, code authoring, literature synthesis and report drafting. Scope of proband data exposed to the model: the supplied phenotype description and HPO terms; aggregate statistics (filter-cascade counts, per-chromosome depth and BAF summaries, k-mer totals); and variant-level detail for the finalist set only — the two *BUB1B* alleles, the twelve ClinVar-conflicting variants reviewed in the ACMG SF screen, and the nine pharmacogenomic loci — all of which appear in this CC BY 4.0 submission. **Not exposed:** raw sequence reads, the bulk VCF, or any genome-wide variant listing; those were processed exclusively by local scripts whose outputs are the aggregates above. **Account data-handling setting:** during the analysis period (26 August – 8 September 2026) the submitting participant's Claude account had the consumer "Help improve Claude" preference **enabled**, under which conversation content may be used for model training. For that window this does **not** meet the organisers' no-training condition, and we record it as a governance deviation rather than omit it. The preference was **disabled on 8 September 2026**; all subsequent work runs under the no-training setting. The exposure was limited to the data scope stated above — raw reads and the bulk VCF were never in scope.

---

## 10. Acknowledgement

This work was made possible through the Hackathon, organized by Sage Bionetworks in partnership with the MVA Society, Hugging Face, and BEACON (The Benchmarking, Evaluation, and Assessment Consortium for Science), with prize sponsorship from AWS and Anthropic. We are deeply grateful to the child and their family who generously contributed their data and their story to advance research into this rare disease. We acknowledge their trust in making this Hackathon possible.
