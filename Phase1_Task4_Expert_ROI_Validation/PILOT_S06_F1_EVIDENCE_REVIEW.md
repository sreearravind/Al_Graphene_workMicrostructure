# Task 4 — S06_F1 revised ImageJ ROI pilot: measured agreement

**Status: file/overlap check PASSED; selected polygon agreement CALCULATED; actual metallurgical grain validity still PENDING.**

## Evidence source and timeline

- Working condition **S06 = 2 wt.% graphene, 600 °C**; original BMP: `Optical miscrostructure_Figures_BMP file/2-600 - Copy/100x1.bmp`.
- 100× ImageJ ruler-based calibration, as confirmed by researcher: **0.473 µm/pixel**.
- **Archived original** manual ROI ZIP `manual_rois/S06_F1_backup.zip` (4,604 bytes; first pilot: 24 polygon ROIs, five overlapping pairs totaling 1,228 unique overlapping pixels).
- **Revised active** `manual_rois/S06_F1.zip` (1,745 bytes; nine polygon ROIs, **zero** overlapping pairs). This active ZIP alone was used for new manual–automated comparisons.
- Workflow initially failed because the backup file was parsed as an active archive. The code now excludes `_backup.zip` case-insensitively and keeps backup provenance unchanged.
- Original BMP and historical TIFF S06/F1 decoded pixels match. GrainStat 500-pixel original segmented total: **329 regions**, mean ECD **24.73 µm** (full-field algorithm population).

## Actual verified computational comparisons: active revised ZIP

| Measure | Result |
|---|---:|
| Human-drawn nonoverlapping polygon ROIs | 9 |
| Image sectors represented (4 × 3) | 6 of 12 |
| Overlap pairs | **0** |
| Median polygon-vs-matched-region IoU | **0.548** |
| Mean Dice (nine matched comparisons) | **0.692** |
| IoU ≥ 0.50 | **6 of 9** (66.7%) |
| IoU ≥ 0.70 | **2 of 9** (22.2%) |
| Manual mean ECD of the nine selected polygons | **38.73 µm** |
| Mean ECD of the nine matched automatic objects | **39.61 µm** |

The selected manual mean and matched automatic mean differ by about **2.3%** relative to the manual mean. The relatively close mean values **do not establish boundary agreement**, which is only moderate/variable across the nine regions. Moreover, they MUST NOT be compared with the **24.73 µm** full-field automated mean as if they represent an identical sampling population. Expert ROIs are selected features; they do not exhaustively trace 329 algorithmic objects.

## All nine polygon comparisons

| Manual ROI | IoU | Dice | Manual ECD (µm) | Matched auto ECD (µm) |
|---:|---:|---:|---:|---:|
| 1 | 0.416 | 0.587 | 50.55 | 43.04 |
| 2 | 0.548 | 0.708 | 59.13 | 55.44 |
| 3 | 0.733 | 0.846 | 41.26 | 46.76 |
| 4 | 0.559 | 0.717 | 48.90 | 51.20 |
| 5 | 0.716 | 0.835 | 31.42 | 36.44 |
| 6 | 0.609 | 0.757 | 29.39 | 31.96 |
| 7 | 0.530 | 0.692 | 34.97 | 45.19 |
| 8 | 0.425 | 0.597 | 34.62 | 30.47 |
| 9 | 0.324 | 0.489 | 18.31 | 15.98 |

Every comparison uses the exact original BMP for visualization and its decoded-pixel-identical historical TIFF for the GrainStat mask, maintaining the same 0.473 µm/pixel scale and 500-pixel segmentation minimum.

## What passes and what remains blocked

**PASS:** real ROI archive ingestion; preserved original backup; zero manual polygon overlaps; exact BMP/TIFF identity; software verification; matching to automated regions; non-fabricated IoU and Dice diagnostic scores.

**PENDING:** qualified expert assessment that the nine polygon outlines represent genuine metallographic grain boundaries, not merely bright patches, etching contrast, microconstituents or reinforcement agglomeration. The revised sample covers only half of the 12 spatial sectors, and its nine selectively drawn regions are too limited to validate all 329 full-field automated objects, let alone twelve material conditions.

**NO-GO for publication-level grain validation:** do not yet amend the grain-size distributions, structure–property correlations, EBSD/DRX claims, or Figure 4 using these nine-region diagnostics. A stronger independently sampled manual ROI set and representative fields are needed. The earlier 24-polygon set failed overlap QA; it must not be combined silently with the revised nine.

## Audit artifacts

- [Current workflow status and score summary](output/MANUAL_VALIDATION_STATUS.md)
- [Per-ROI IoU and Dice](output/manual_vs_auto_per_roi.csv)
- [Per-field agreement and sample coverage](output/manual_vs_auto_per_field.csv)
- [Original BMP, automated segmentation and actual human contours](output/S06_F1_manual_vs_auto.jpg)
- [Nine human ROIs with areas and no-overlap flags](output/S06_F1_roi_inventory.csv)
- [Provenance and human-ROI preflight JSON](output/expert_roi_preflight.json)

Old `S06_F1_overlap_pairs.csv` originated from the first manual upload and is **not a valid current finding**. The revised workflow removes this obsolete derived file automatically when the corrected ROI archive has zero overlaps. The earlier backup ZIP remains preserved.

## Recommended next scientific step

Review the actual red/green outlines at native resolution, then extend the manual pilot to a field with drastically different automated counts, particularly **S06_F2** (23 automatically detected regions) and **S06_F3** (344 automatically detected regions). This comparison can help distinguish heterogeneous microstructure from segmentation failures. If physical grain boundaries are unresolvable at 100×, record that limitation and consider restricting the analysis to explicitly defined optically segmented features instead of verified grains.
