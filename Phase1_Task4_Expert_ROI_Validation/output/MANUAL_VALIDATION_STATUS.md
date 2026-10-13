# Phase 1 Task 4 — Independent manual versus automated optical segmentation

Active manual ROI archives submitted: **3**.
Preserved historical backup ROI archives ignored: **1**.
Total independently drawn ROI polygons: **9**.

These are agreement metrics for the explicitly traced objects only.
No assertion of representative metallographic grain-size distribution or mechanism is made until expert field selection and boundary identity are signed off.

The sources of human ROI data are the uploaded ROI ZIP archives, not programmatic simulations.
Human contours were compared to rerun historical GrainStat objects on matching TIFFs, with exact BMP pixel identities and the fixed S10–S12 label crosswalk.

Expert signoff remains pending. Numerical agreement alone does not determine physical grain identity.

See manual_vs_auto_per_roi.csv, manual_vs_auto_per_field.csv and generated three-panel images.

## Field-level provenance and scientific validation gates

| Submitted field | Human ROIs | Substantive overlapping pairs | Scientific scoring status |
|---|---:|---:|---|
| S06 F1 | 9 | 0 | PROVISIONAL SCORED — expert grain identity signoff pending |
| S06 F2 | 16 | 3 | HOLD — inspect and revise polygon overlap |
| S06 F3 | 15 | 2 | HOLD — inspect and revise polygon overlap |

**IMPORTANT:** The workflow can complete successfully while some uploaded fields remain scientifically BLOCKED. The agreement tables include only eligible fields; do not interpret all submitted human ROIs as scored.

### Conflicting manual polygons requiring original-image review
- **S06 F2:** 3 substantive intersection(s).
  - ROI #1 versus #5: 12726 overlapping native pixels; 81.24% of smaller traced region.
  - ROI #2 versus #6: 3430 overlapping native pixels; 58.01% of smaller traced region.
  - ROI #4 versus #11: 2147 overlapping native pixels; 87.74% of smaller traced region.
- **S06 F3:** 2 substantive intersection(s).
  - ROI #1 versus #10: 5798 overlapping native pixels; 100.00% of smaller traced region.
  - ROI #9 versus #15: 5281 overlapping native pixels; 99.02% of smaller traced region.

Inspect original ImageJ ROI Manager objects against physical etched boundaries. Do NOT automatically delete or merge polygons to improve an agreement statistic.

## Measured agreement on SELECTED expert polygon ROIs

| Field | ROI count | Sectors covered (of 12) | Median IoU | Mean Dice | IoU >= 0.5 | Manual mean ECD (um) | Matched automatic mean ECD (um) |
|---|---:|---:|---:|---:|---:|---:|---:|
| S06 F1 | 9 | 6 | 0.548 | 0.692 | 66.7% | 38.73 | 39.61 |

**Scope limitation:** Researchers drew only a selected number of shapes, not a randomly sampled, complete or certified set of metallurgical grain boundaries. Scores apply ONLY to the selected traced ROIs and do not validate the remaining automated segmented regions.

