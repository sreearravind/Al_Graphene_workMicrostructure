# Phase 2 — Task 4: measured-property figure integration into manuscript v8.2

**Status: Word v8.2 working file delivered separately in the ChatGPT conversation.** This GitHub folder is an **audit log**, not a claim that the binary Word file was committed. Main branch, original microscopy, manually traced ROI ZIP files and experimental measurements remain unchanged.

## Source provenance and corrections

- Source data: `Revision_Comment10/comment10_factor_comparison_data.csv` and `Revision_Comment7/hardness_data.csv` on the repository. The local Task 3 snapshots were used for regenerated charts.
- 12 measured condition-level records and nine archived spatial hardness values per condition.
- S12 coefficient of friction: the archived factor table gives **0.125**; manuscript v8.1 had both **0.124** and **0.125**. The v8.2 Abstract, Results, Conclusions, Figure 9 and the *present-study Table 2 cell* consistently use **0.125 (archived table)**. **Native tribometer data remains unverified**.
- Pearson extruded-density vs mass-loss coefficient recomputed from the source 12 rows: **r = −0.230504570668585 → −0.231**, replacing **−0.247**. This is an arithmetic correction, not new data.
- Pearson COF vs mass loss: **r = −0.221617512865771 → −0.222**.
- Existing bulk-density/mass-loss **−0.343** was not reasserted because the available source CSV does not include an independently verified bulk-density series.

## Figure revisions in Word v8.2

| Figure | Revised figure | Data and qualification |
|---|---|---|
| Figure 6 | Rockwell hardness mean ± 1 SD (n = 9 spatial indentations), extruded density | Original hardness readings are sorted; raw instrument exports, load and dwell pending |
| Figure 9 | COF and gravimetric mass loss, separate axes/panels | 12 archived condition values; test log confirmation pending |
| Figure 10 | COF vs mass loss | Descriptive Pearson r −0.222, n = 12 |
| Figure 11 | Seven-variable measured-property correlation matrix | No software-segmented grain diameter, no unverified bulk density |
| Figure 12 | Measured response correlation comparison | Co-measured hardness/COF not independent causal predictors |
| Figure 13 | Five-panel GNP × temperature condition plots | Extruded density, HRB, UTS, COF, loss; obsolete grain panel removed |

The source Python figures and a complete Word-document v8.2 were delivered as downloadable artifacts in the ChatGPT task session, not uploaded as executable repository outputs.

## Scientific and editorial safeguards

1. **Figure 4 remains an explicitly labelled v7 working placeholder** with invalid grain-size interpretation; this figure must be removed or replaced before journal submission, not treated as validated data.
2. Figure 3 requires authentic **400×** scale reference; the original verified **100×** scale cannot simply be transferred to it.
3. Figure 5 represents one unverified-native-source XRD scan, not multi-condition phase evolution (no twelve XRD scans were performed; original physical samples unavailable).
4. Original Rockwell conditions, tensile machine settings, and native tribometer records remain unverified; no experimental settings are guessed.
5. Historical TIFF S10–S12 optical specimen mismatch cannot alter mechanical/tribological specimen IDs; avoid physical grain-size correlations.
6. Full-factor categorical interaction model for twelve non-replicated cells has **zero residual error degrees of freedom**. Figures use descriptive trajectories only.
7. Primary literature source verification and repeated bibliography entries are pending.

**Next:** Phase 2 Task 5 image/record integrity check: figure 3 optical scale and source panels, figure 4 removal/supplement decision, XRD original scan/provenance, machine settings and final bibliography review.