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

## Measured agreement on SELECTED expert polygon ROIs

| Field | ROI count | Sectors covered (of 12) | Median IoU | Mean Dice | IoU >= 0.5 | Manual mean ECD (um) | Matched automatic mean ECD (um) |
|---|---:|---:|---:|---:|---:|---:|---:|
| S06 F1 | 9 | 6 | 0.548 | 0.692 | 66.7% | 38.73 | 39.61 |

**Scope limitation:** Researchers drew only a selected number of shapes, not a randomly sampled, complete or certified set of metallurgical grain boundaries. Scores apply ONLY to the selected traced ROIs and do not validate the remaining automated segmented regions.

