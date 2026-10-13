# Phase 2 · Task 1 — Reviewer Evidence-to-Claim Reconciliation

**Manuscript:** JMEP-26-06-50175 | **Baseline:** `Manuscript_Al-GNP_Tribo_v7.docx` (34 pp.) | **Second round:** 1 Reviewer 1 item, 10 Reviewer 2 items, Associate Editor recommendation.

**Decision:** **Start v8.1 evidence-bounded text revision immediately**; keep native XRD, machine test parameters, Minitab/run proof, and 400× scale calibration as narrowly targeted *parallel archive-search gates*. This audit does not establish that all JMEP reviewer requests can be fulfilled. Source v7 and original experimental files are unchanged.

## Reviewer reconciliation matrix

| Point | Status | Manuscript area | Required action |
|---|---|---|---|
| AE | HIGH_RISK | Whole manuscript | Complete evidence-aligned restructuring with measured multiresponse focus |
| R1 | PARTIAL | Intro/Design pp2-9 | Specify deliberately high-loading screening; tradeoffs and limits; no unrecorded trials |
| R2-1 | EDIT_RESEARCH | Intro pp1-4; Table2 pp27-28 | Rebuild critical numeric evidence table; de-duplicate sources; narrow research gap |
| R2-2 | PARTIAL | Design pp5-8; Table1; Fig13 | Create retrospective Minitab matrix and honest provenance statement; descriptive trends only |
| R2-3 | PARTIAL | Design/Fabrication pp5-9 | State actual basis without post-hoc claimed trials; high content experimental screen |
| R2-4 | CRITICAL_RECORD | Methods pp9-10 | Retain etchant; insert only confirmed actual load indenter dwell tensile extension or strain rate |
| R2-5 | PARTIAL | Figure3 pp11-12 | Rebuild 12 original-BMP panels by true processing folder; add only independently supported 400x bars |
| R2-6 | NOT_VALIDATED | Methods pp9-10; Fig4; Results pp12-16,23-26 | Withdraw physically validated grain ECD and causal correlations; maybe qualify software-defined optical feature diagnostics |
| R2-7 | REMOVE_OR_QUALIFY | Figure4 p13; Abstract/Conclusion | Remove grain-size figure from central evidence; preserve audit-only exploratory feature results with correct traceability if used |
| R2-8 | BLOCKER | Figure5 p14; limitations p29 | Narrow XRD to representative screen; replot ONLY authentic native 2theta-intensity if recovered |
| R2-9 | PARTIAL | Mechanics pp14-20; tribology pp20-22 | Calculate same-temp % deltas and multiobjective comparisons; cautious mechanisms only |
| R2-10 | HIGH_RISK | Entire manuscript; conclusions pp29-30 | Reframe as screening-level coupled processing-property study; remove overclaimed grain/interfacial mechanisms |

Full per-comment rationale, source evidence, and missing-record instructions are in [the machine-readable CSV](reviewer_claim_matrix.csv).

## Decisive manuscript-wide corrections

1. **Optical S10–S12 label provenance.** Original BMP folder processing identities are researcher-defined: working S10 4%/500°C corresponds to TIFF folder S11 (historical ECD 40.02µm); working S11 4%/550°C corresponds to TIFF S12 (historical ECD 52.27µm); working S12 4%/600°C corresponds to TIFF S10 (historical ECD 29.93µm). These are **provisional algorithmic feature metrics**, not physically validated grain diameters. Mechanical test identifiers must not be relabeled from optical evidence.

2. **Grain size and mechanisms.** Task 6 reproduced all 36 500px GrainStat counts and means, but 6/12 conditions have ≥4× object-count variation across three imaged fields; median absolute mean-ECD change without CLAHE is ~83%; S06-F2 user-traced pilot median IoU is ~0.097. Neither numerical repeatability nor threshold sensitivity establishes physical grain boundaries. Remove/qualify grain ECD from abstract, body and conclusion; remove grain-based correlations and Hall–Petch/Zener/DRX attributions from central claims. If feature-size plots are retained, supply traceable source mapping and label explicitly as **optically segmented features**.

3. **XRD scope.** Only one reported 4wt% pattern, unknown prior sintering condition; no 12-condition XRD was performed, and no physical specimens remain. A reconstructed processing-factor comparison is impossible. Replot one authentic scan only if original 2θ-intensity is recovered. Do not claim absence of interfacial Al4C3 across all samples.

4. **Machine parameters.** Page 9 already provides SiC grinding, 0.05µm alumina and Poulton HNO3:HCl:HF:H2O 6:12:1:1 / ~10sec. Rockwell indenter/load/dwell and tensile rate remain absent. The H1–H9 hardness CSV is sorted in nondecreasing order for every condition; source-sheet provenance is not established. Retrieve instrument records, do not infer standard values.

5. **Factorial statistical boundaries.** Four GNP and three temperature levels exhaust twelve cells. A full interacted categorical two-factor model has zero residual degrees of freedom if each cell has one independently measured condition value. Minitab may establish a **retrospective matrix reconstruction** but cannot serve as historical randomized-run proof.

6. **Reference list QA.** Investigate repeated items 5/36, 15/22, 18/35 and verify all quantitative cited claims and journal/year metadata.

7. **Claim architecture.** Retain actually measured divergent condition optima: S11 UTS 129MPa, S5 minimum mass loss 0.0024g, S12 COF ~0.125, while unreinforced S3 UTS 128MPa. Discuss these as screening observations, not statistically proven global optimisation or an established interface mechanism.

## v8 section-by-section edit sequence

- **Begin now**: Introduction and quantitative literature logic; research gap; 4×3 design; real-range selection rationale; measured density/hardness/tensile/COF/mass-loss condition comparisons.
- **Begin now but qualify**: Optical Methods/Results and study limitations; no validated physical grains, DRX fraction or interfacial chemistry.
- **Pending records**: Actual Rockwell load/dwell/indenter; tensile strain rate/crosshead method; 400× microscope scale reference; authentic native XRD trace and specimen ID; historic run-order proof.
- **After record gate**: High-res Figure 3 rebuild; decide removal or supplementary status for old Figure 4; single-pattern XRD Figure 5 replot only from source; remove grain inputs from correlation/interaction figures and recompute if retained.
- **Finalize last**: Title, abstract, conclusions, point-by-point rebuttal, editorial suitability decision.

## Suggested revised contribution framing

*A full 4 × 3 factorial screening of GNP fraction and pre-extrusion sintering temperature under a common hot extrusion route, demonstrating different processing conditions for ultimate tensile strength, dry-sliding friction and mass-loss performance.*

This is a **screening-level processing–property** statement; it is not a claim of independently demonstrated grain-refinement, dispersion, phase-evolution or interfacial-bonding mechanisms.

## Follow-on execution

**Phase 2 Task 2**: Draft Introduction + experimental design + evidence-cautious microstructural methodology in a **separate v8.1 Word copy** while the targeted historical record retrieval continues. Preserve archived v7, all original microscopy files and manually drawn ROI ZIPs unchanged.

Source anchors: v7 pp. 5–6 (DOE); p. 9–10 (methods); pp. 11–14 (Figures 3–5); pp. 14–22 (mechanical/tribology); pp. 23–26 (correlations); pp. 29–30 (limitations/conclusion). Optical audit: [Task 6 decision](../Phase1_Task6_Image_Quality_36Fields/TASK6_JMEP_EVIDENCE_DECISION.md), [specimen-ID provenance](../Phase1_Task1_Optical_Source_Audit/SPECIMEN_LABEL_PROVENANCE.md).

**No original experimental measurement has been changed by this Task 1.**
