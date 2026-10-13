# Phase 1 Task 3: controlled segmentation reproduction and threshold sensitivity

**STATUS: completed computational QA, NOT manual / expert grain boundary validation.**

## Input and provenance
- 19 pre-registered optical fields, exactly pixel matched to original BMP images before analysing historical TIFF files.
- Reproduces the original TIFF loading behavior of GrainStat (which differs from BMP loading).
- Historical TIFF mapping preserved explicitly: TIFF S10 -> BMP S12; TIFF S11 -> BMP S10; TIFF S12 -> BMP S11.
- Researcher-confirmed ImageJ reference-ruler calibration for 100x: 0.473 micrometres/pixel. Original reference image not archived.
- GrainStat defaults: Gaussian sigma 1, CLAHE enabled, Otsu, morphology radius 2, watershed enabled; minimum area varied as shown.

## Reproducibility of archived 500-pixel output
- Exactly matching retained-region counts: **19/19 fields**.
- Means matching archival mean ECD within 1e-6 micrometres: **19/19 fields**.

| Working condition | Field | Archived count | Rerun count | Count delta | ECD mean delta (um) |
|---|---:|---:|---:|---:|---:|
| S1 | 1 | 98 | 98 | +0 | +0.000 |
| S2 | 1 | 10 | 10 | +0 | +0.000 |
| S2 | 3 | 107 | 107 | +0 | +0.000 |
| S3 | 1 | 174 | 174 | +0 | +0.000 |
| S3 | 3 | 12 | 12 | +0 | +0.000 |
| S4 | 1 | 133 | 133 | +0 | +0.000 |
| S5 | 1 | 87 | 87 | +0 | +0.000 |
| S6 | 1 | 329 | 329 | +0 | +0.000 |
| S6 | 2 | 23 | 23 | +0 | +0.000 |
| S6 | 3 | 344 | 344 | +0 | +0.000 |
| S7 | 1 | 170 | 170 | +0 | +0.000 |
| S8 | 1 | 91 | 91 | +0 | +0.000 |
| S8 | 3 | 261 | 261 | +0 | -0.000 |
| S9 | 1 | 72 | 72 | +0 | +0.000 |
| S9 | 2 | 17 | 17 | +0 | -0.000 |
| S10 | 1 | 71 | 71 | +0 | +0.000 |
| S11 | 1 | 106 | 106 | +0 | -0.000 |
| S12 | 1 | 60 | 60 | +0 | +0.000 |
| S12 | 3 | 347 | 347 | +0 | +0.000 |

## True rerun threshold sensitivity
Minimum area is applied both within GrainStat binary morphology before watershed and as a final region-area filter. These are true reruns of segmentation, not post-filtering old CSV rows.

| Min area (px) | ECD cutoff (um) | Total retained regions | Median field mean ECD (um) |
|---:|---:|---:|---:|
| 250 | 8.44 | 2571 | 43.12 |
| 500 | 11.93 | 2512 | 43.80 |
| 1000 | 16.88 | 2252 | 44.61 |

| Alternative threshold | Median absolute mean-ECD shift from 500px | Max absolute shift |
|---:|---:|---:|
| 250 | 0.8% | 2.9% |
| 1000 | 3.9% | 9.6% |

## Interpretation and expert validation gate
- The red boundaries in the output review sheets are **actual computed object contours**, but not scientifically confirmed grain boundaries.
- A stable computed contour under multiple thresholds is not proof of grain identity.
- Manually trace suitable grain boundaries in ImageJ on the same selected fields or mark a field UNRESOLVABLE. Archive ROI and manually traced ECD results before claiming objective agreement.
- Large dark networks may be etchant structures or merged regions; do not claim DRX fraction, Hall-Petch mechanism, or full experimental grain distribution from automated optical features alone.
- The 500-pixel minimum excludes areas whose equivalent-circle diameter would be below 11.93 um.
- No experimental file, archived grain-size value, mechanical/tribological measurement or manuscript content has been modified.

## Files
- segmentation_sensitivity_19_fields.csv: all runs and sample-identity crosswalk
- archived_baseline_reproduction.csv: exact comparison to historical field results
- threshold_change_relative_to_500.csv: field-level changes
- contours_Sxx_Fy.jpg: expert review sheets for selected fields at 500 px
