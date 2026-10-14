# Phase 2 — Task 3: electronic experimental response and DOE verification

**Status:** completed electronic source-table audit and processing-property figure rebuilding. **Not** full laboratory instrument certification or Minitab historical-run proof. Source manuscript v8.1 and master measurement files are unchanged.

## Data and provenance
Sources are the repository's original [12-condition factor response CSV](../Revision_Comment10/comment10_factor_comparison_data.csv) and [nine-indentation hardness CSV](../Revision_Comment7/hardness_data.csv). The analyst also produced a seven-sheet formula-driven Excel workbook, a four-page Word verification report, five single-property figures and a combined figure, and downloadable CSV/script bundles in the ChatGPT working session.

The original response table includes a historical optical grain-size column, but this figure task **excludes** it because Phase 1 did not independently validate actual crystallographic grain boundaries and found cyclic historical TIFF labels for optical S10–S12.

## Verified directly from electronic table
- Complete GNP × sintering matrix: 4 fractions (0,2,3,4 wt.%) × 3 temperatures (500,550,600 °C), twelve cells with no missing or duplicated pair.
- Categorical factorial degrees of freedom: GNP 3, sintering 2, interaction 6, total centred 11, **residual 0** with one independently measured value per condition. No inferential fully interacted ANOVA significance established.
- Reported nine-point hardness means, sample SD and SE are numerically reproducible from the CSV for all 12 samples; all nine readings are arranged in nondecreasing order. Indentation measurement order and original instrument printouts remain unverified.
- Maximum UTS S11 = 129 MPa (4 wt.% / 550 °C); highest reported hardness S12 = 24.5 HRB; lowest mass loss S5 = 0.0024 g; minimum archived COF S12 = 0.125.
- Temperature-matched Al comparison: S11 UTS is +69.74% versus S2 (129 vs 76 MPa); S5 mass loss −20.0% versus S2 (0.0024 vs 0.0030 g); S12 COF −79.54% versus S3 (0.125 vs 0.611). These are descriptive, not confidence-bounded effects.

## Two manuscript corrections / record checks
1. **S12 COF precision:** v8.1 Abstract, friction discussion and Conclusions use **0.124**, another factor-response paragraph uses **0.125**, while archived response CSV is **0.125**. Resolve from actual tribometer log before choosing authoritative precision or rounding.
2. **Pearson r(extruded density, mass loss):** archived twelve-value columns compute **−0.23050457 (≈ −0.231)**, whereas v8.1 claims **−0.247**. Do not silently change or substitute the separate manuscript's *bulk density* variable, which is absent from this CSV.

Other descriptive correlations reproduced (approx.): COF–mass loss −0.222, GNP–mass loss +0.400, temperature–mass loss −0.299, GNP–hardness +0.846, GNP–COF −0.603. All are twelve-condition associations, not causal findings.

## Retrospective DOE documentation
A CSV containing the twelve processing cells in manuscript order can be imported into Minitab. Its order is reconstructed from sample IDs and **is not a chronologically documented, randomized or historically Minitab-generated run sequence**. A reviewer-required original Minitab design screenshot/project cannot be claimed unless it actually existed or is clearly labelled retrospective.

## Additional laboratory archive gates
- Original Rockwell indenter, major/minor load and dwell (and confirmation of test scale), native instrument export.
- Tensile gauge configuration, strain rate or actual crosshead speed and original test record.
- S12 COF raw trace, balance and sliding test records, raw density/Archimedes sheets.
- Original Minitab project / run log and independent sample fabrication replicates, if any.
- XRD measured for one representative condition only; there is no experimental XRD comparison across twelve conditions, and no physical specimens remain.

## Figure decisions
Retain density, hardness, UTS, COF and mass-loss interactions as descriptive condition-level trajectories, with no grain-size panel and no inferential significance symbols. A mean ± SD HRB plot may use the archived n=9 spatial-indentation statistics, **clearly noting machine-provenance pending**, and may not be described as n=9 independently fabricated specimens.

## Next recommended work
**Phase 2 Task 4:** reconcile v8.1 numerical text and existing mechanical/tribology graphic labels to authoritative values; replace the obsolete grain panel in the interaction figure; maintain a separate v8.2 manuscript file. Keep Minitab screenshot, machine tests and XRD claims explicitly bounded by source evidence.

Source calculation/package produced in Task 3 is available as separate user-linked XLSX/DOCX/CSV-and-code/PNG-SVG artifacts, not automatically committed as manuscript text to this repository.
