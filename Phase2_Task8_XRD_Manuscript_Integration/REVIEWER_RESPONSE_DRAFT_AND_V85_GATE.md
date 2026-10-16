# Phase 2 Task 8 — XRD manuscript changes and reviewer response (DRAFT)

**JMEP Reviewer 2, XRD comment — evidence-based proposed response (not yet sent):**

> We thank the reviewer for highlighting the need for composition- and temperature-dependent diffraction evidence. Following a search of our historical electronic research archive and consultation with the former XRD collaborator, we retrieved the surviving numerical intensity-export matrix for twelve individually tested specimens, corresponding to GNP contents of 0, 2, 3 and 4 wt.% and pre-extrusion sintering temperatures of 500, 550 and 600 °C. The corresponding sections were taken from the final hot-extruded sample lengths and submitted independently for XRD testing, as confirmed by the author who delivered the specimens. We have prepared comparative diffraction figures using all twelve complete exported profiles (20–80° in 2θ, 0.01° intervals). We have also revised the XRD Methods and Discussion to limit phase interpretation to the accessible information. Because the original instrument-native files and detailed acquisition headers were not retained under the laboratory's historical data-retention practice for pre-2022 records, we have disclosed the source and limitation of the recovered exports rather than claiming complete instrument-level provenance. The prominent Al-associated diffraction maxima and the ~26.5° carbon-associated feature are now described as tentative peak-position assignments; we do not infer quantitative GNP phase fractions, absence of trace Al4C3, or nanoscale interfacial chemistry from these patterns alone.

**Important:** This response accurately reflects the user's firsthand recollection of testing and the numerical dataset but cannot independently reconstruct missing run-method records. If the journal explicitly requires original instrument-native files or independently verified refinement, state their unavailability without evasion.

## Source profile figure strategy

- Publication-intended Figure 4 from original **6001 × 12** source array (unmodified raw-exported numerical values): [12 profiles, 3 sintering temperature panels](output/FIGURE4_TWELVE_XRD_EXPORTS.png).
- Dedicated supporting Fig. S1 carbon ~26.5° region: [full-resolution window](output/FIGURE4_CARBON_002_INSET.png).
- Peak position table: [all 12 processing conditions, candidate reflections](output/phase_window_indices_all_conditions.csv).
- Processing methodology, caption and limits: [author evidence notes](output/TASK8_XRD_FIGURE_CAPTION_AND_LIMITS.md).
- Working manuscript v8.5 DOCX was created separately in the conversation, preserving source v8.4. The embedded Figure 4 is a real **12-condition ~26.5°/Al111 peak-height diagnostic**, not the full traces; replace that diagnostic with the new full-resolution 12-profile Figure 4 for submission layout.

## Evidence hierarchy

1. **Author eyewitness:** personally handed twelve sections cut from final extruded material to the analyst, independently for XRD testing.
2. **Surviving measured-export record:** complete `XRD_analysis/Combined_Matrix_Data_revised.csv`, pinned Git blob `bbea94803dee30d3af4c0b20c504d73c37a06ae2`.
3. **Supplied laboratory note:** `Info.txt`, partly inconsistent with original manuscript (20 vs 40 mA, "flat pressed powder" vs author's post-extrusion specimens), and includes placeholder parameters. Do not silently adopt unsupported method details.
4. **Instrument-native files:** irrecoverable prior to 2022 due lab's retention policy, per the author's report. Do not state native trace-level independently certified results.

## Manuscript v8.5 edits
- Introduction/fabrication evidence paragraph, abstract, XRD Methods and Results, peak interpretation, limitation and conclusion updated for twelve individually tested post-extrusion profiles.
- Full matrix now enables quantitative **descriptive** reflection positions and relative ~26.5° feature contrast. It does **not** enable independent replicate uncertainty estimates or interface-mechanism identification.
- Optical grain-size exclusion, author-confirmed Figure 3 400× scale, mechanical/tribology results and unreplicated DOE limitations left untouched.
- **No simulated/refined spectra, phase fraction estimates, Rietveld coefficients or Al4C3 absence claims inserted.**

## Remaining pre-submission actions
- Replace v8.5's embedded peak-ratio diagnostic with full-source Figure 4 from this audit output.
- Archive the exported CSV and provenance note alongside the manuscript/supplementary data; clarify original acquisition-current mismatch if any older written instrument note is available.
- Verify bibliography and recover original hardness/tensile machine settings as far as possible.
- Obtain coauthor/supervisor acknowledgment of XRD provenance statement and manuscript-vs-Info.txt method conflict.
