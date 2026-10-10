# Phase 1 / Task 2 — Interpretation of segmentation QA and manual validation protocol

**Status:** Existing segmented outputs screened and source/overlay contact sheets visually inspected. **Segmentation is not yet scientifically validated.** No quantitative data were overwritten.

## Calibration provenance
The researcher states that the optical 100× calibration **0.473 µm/pixel** was established using a known ruler reference, the **same microscope**, and **ImageJ**. Treat this as a researcher-confirmed laboratory calibration. A future supplementary package should ideally contain the reference image, ruler interval and ImageJ pixel distance for independent replication. No other magnification was assumed to share the 100× conversion.

## Exact label crosswalk (established in Task 1)

| Correct processing condition (BMP identifier) | Historical TIFF folder used in segmentation |
|---|---|
| S10 — 4 wt.% / 500 °C | S11 |
| S11 — 4 wt.% / 550 °C | S12 |
| S12 — 4 wt.% / 600 °C | S10 |

Other nine conditions match their TIFF and original BMP labels. This crosswalk comes from exact matching decoded-image pixel hashes, not visual similarity. **No mechanical-test specimen identifiers are relabeled.**

## Automated QA results and high-priority anomalies

Existing stored first-field overlays depict the grayscale source plus **red centre markers only**. The displayed overlays **do not draw grain boundary contours**, so they cannot establish whether dark etched features/particles were segmented into valid grain boundaries.

Specific irregularities (100×, all image fields 1600 × 1200 pixels):

| Correct working condition | Field | Existing detected regions | Mean segmented ECD (µm) | Important QA observation |
|---|---:|---:|---:|---|
| S2 / 0 wt.% / 550 °C | 1 | 10 | 102.5 | Largest detected region covers **15.73% of entire image**; 60% of retained regions have roundness less than 0.2 |
| S2 | 3 | 107 | 41.4 | Count 10.7× field 1 despite same acquisition magnification and image dimensions |
| S3 / 0 wt.% / 600 °C | 1 | 174 | 33.1 | Compare with field 3 |
| S3 | 3 | 12 | 133.1 | Largest region covers **10.13%** of image; **91.7%** of accepted regions have roundness less than 0.2 |
| S6 / 2 wt.% / 600 °C | 1 | 329 | 24.7 | Compare fields 2 and 3 |
| S6 | 2 | 23 | 95.2 | **78.3%** of accepted regions have roundness less than 0.2 |
| S6 | 3 | 344 | 24.2 | Strong contrast with field 2 |
| S8 / 3 wt.% / 550 °C | 1,2,3 | 91,49,261 | — | Count ratio 5.3 |
| S9 / 3 wt.% / 600 °C | 2 | 17 | 103.7 | Largest region covers **13.97%** of image |
| S12 / 4 wt.% / 600 °C | 1,2,3 | 60,202,347 | — | Count ratio 5.8; prior numerical outputs were labeled TIFF S10 |

These metrics are **heuristic warnings, not grounds for automatic exclusion**. Real heterogeneity and automated under-/over-segmentation are competing explanations. Only field-by-field expert assessment can determine which is applicable.

The 500-pixel minimum-area filter at 0.473 µm/pixel censors any detected equivalent-circle diameter below approximately **11.93 µm**. The old histograms and mean sizes therefore describe an area-filtered segmentation population, not necessarily every physical grain.

## Manual optical verification (pre-defined sampling to avoid cherry-picking)

1. Inspect an initial **19 selected 100× fields**, covering all twelve processing conditions and the strong anomalous pairs. The corresponding protocol CSV is stored alongside this note.
2. On every selected field, manually assess boundary visibility, whether dark lines are grain boundaries, and whether isolated dark inclusions, scratches or pores are being mistaken for grains.
3. Trace a subset of **unambiguously identifiable** grains in ImageJ (target 20–30 per field *when feasible*). Mark a field as **unresolvable** if true grain boundaries cannot be differentiated reliably; do not force a numeric result.
4. Export traced grain areas and ECD using the same 0.473 µm/pixel 100× calibration, along with the original image file identifier. Do not use red centroids as a boundary reference.
5. Compare manual and algorithmic regions on the **same fields**, document disagreement, inspect segmentation masks/contours, and assess whether the 500-pixel cutoff materially shifts results.
6. If reliable grain boundaries are not discernible in enough fields, report **optical morphological feature sizes** rather than claiming validated metallographic grain diameters. DRX-specific assertions remain unsupported without orientation-resolved measurements.
7. Rebuild condition-level grain summaries only from a defensible segmentation workflow, preserve the S10–S12 BMP/TIFF identity crosswalk, and regenerate structure–property correlations. Distinguish fields within a specimen from replicate specimens.

## Visual evidence

- [100× suspect-field montage](output/anomalous_100x_fields.jpg)
- [First-field source vs existing centroid overlays (S2/S3/S5/S6)](output/overlay_review_group_1.jpg)
- [First-field source vs existing centroid overlays (S9/S10/S11/S12)](output/overlay_review_group_2.jpg)

## Decision for manuscript

**Not yet appropriate:** represent the existing pooled ECD values as independently validated true grain-size distributions, state quantitative Hall–Petch strengthening from the weak exploratory correlations, or place micron scale bars on 200×/400× images using only the 100× calibration.

**Appropriate now:** state original source-image availability; documented ImageJ 100× scale-setting method; explicit segmentation and sampling limitations; and the discovered historical image-label provenance correction.

No source images, master mechanical/tribology data, or manuscript text have been changed. This is a reproducible evidence-screening and review-planning record.
