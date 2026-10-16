# Task 5: transparent human ROI duplicate policy sensitivity

**Exploratory computational QA; not proof of actual metallurgical grains.**

## Predefined rule independent of agreement

- Preserve and audit all submitted manual ROIs.
- A pair with 50% or more overlap of the smaller manual area is a possible duplicate tracing, independent of GrainStat output.
- For sensitivity, evaluate retaining the first-drawn or last-drawn polygon per connected duplicate group. Report BOTH alternatives without selecting a preferred option by IoU.
- All less overlapping human polygons remain included. Retain the all-ROI diagnostics to show the consequences of double-counting.
- Reassess the chosen subset manually against visible physical boundaries before any publication claim.

## Per-field results

| Field | Policy | Manual ROIs | Duplicate groups | Median IoU | Mean Dice | IoU >=0.50 | Selected mean manual ECD um | Matched auto ECD um | Repeated auto labels |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| F1 | all_ROIs_including_duplicates | 9 | 0 | 0.548 | 0.692 | 6/9 | 38.73 | 39.61 | 0 |
| F1 | first_traced_in_duplicate_group | 9 | 0 | 0.548 | 0.692 | 6/9 | 38.73 | 39.61 | 0 |
| F1 | last_traced_in_duplicate_group | 9 | 0 | 0.548 | 0.692 | 6/9 | 38.73 | 39.61 | 0 |
| F2 | all_ROIs_including_duplicates | 16 | 3 | 0.100 | 0.204 | 0/16 | 42.98 | 131.50 | 6 |
| F2 | first_traced_in_duplicate_group | 13 | 3 | 0.097 | 0.190 | 0/13 | 42.48 | 128.11 | 3 |
| F2 | last_traced_in_duplicate_group | 13 | 3 | 0.097 | 0.202 | 0/13 | 41.43 | 128.11 | 3 |
| F3 | all_ROIs_including_duplicates | 15 | 2 | 0.458 | 0.614 | 5/15 | 43.12 | 36.68 | 2 |
| F3 | first_traced_in_duplicate_group | 13 | 2 | 0.458 | 0.613 | 4/13 | 43.16 | 36.70 | 0 |
| F3 | last_traced_in_duplicate_group | 13 | 2 | 0.458 | 0.611 | 4/13 | 42.42 | 36.70 | 0 |

## Full-image algorithmic results remain unchanged

| Field | Retained automated objects | Full-field automated mean ECD um |
|---|---:|---:|
| F1 | 329 | 24.73 |
| F2 | 23 | 95.15 |
| F3 | 344 | 24.18 |

## Interpretation and scientific limitations

- The selected hand-drawn feature distributions are nonrandom and do NOT estimate the full field grain-size distribution.
- F2 undersegmentation (merged regions), F1/F3 segmentation of etching contrast, true heterogeneity, defects, and uneven light are possible explanations, not independently established facts.
- Matching IoU is diagnostic only, not an inclusion criterion. Even close agreement between two masks does not establish physical grain identity.
- No independent specimen replicates or EBSD support were added. Grain-size strengthening, DRX and quantitative grain/property mechanism claims remain unverified.
- Where optical boundaries are ambiguous, use the qualified label optically segmented microstructural feature size, not validated grain diameter.

## Data outputs
- all_selected_ROI_comparisons.csv: all original manual selections plus two duplicate-handling scenarios.
- S06_duplicate_policy_sensitivity.csv: each scenario for each 100x field.
- duplicate_candidate_pairs.csv: geometry-determined duplicate candidates.
- other_overlap_pairs.csv: all lesser overlaps.
- Original human ROIs, source BMP/TIFF and manuscript were not altered.
