# Phase 1 — Task 4: Three-field S06 manual ImageJ ROI pilot

**Evidence status:** researcher-submitted S06_F1.zip / S06_F2.zip / S06_F3.zip found in the audit branch. Their source images were previously verified pixel-equivalent to the historical TIFF files. **Do not substitute manually outlined selected patches for a full-field true grain-size distribution.**

## Provenance and accepted analysis scope

- Working processing condition **S06: 2 wt.% graphene, 600 °C**. Original 100× BMP files: `2-600 - Copy/100x1.bmp`, `100x2.bmp`, `100x3.bmp`.
- Researcher-calibrated 100× optical scale: **0.473 µm/pixel**, derived from an ImageJ ruler reference on the same microscope. Independent reference image is not archived.
- Manual ROI ZIP counts: **F1 9, F2 16, F3 15**. The original F1 ZIP was preserved as `S06_F1_backup.zip` and excluded from current scoring.
- Existing 500px GrainStat full-field object totals: **F1 329 objects / mean ECD 24.73 µm; F2 23 / 95.15 µm; F3 344 / 24.18 µm**.
- Human polygon-selected mean ECDs: **F1 38.73 µm; F2 42.98 µm; F3 43.12 µm** (these values are **not population grain-size estimates**; F2/F3 also include duplicate or overlapping selections).
- F1 human-to-automatic agreement from nine NONoverlapping selections: **median IoU 0.548, mean Dice 0.692**, spatially sampled in six of twelve image sectors. Expert identification of grain boundaries remains unsigned.

## Validation gate by field

| Field | Manual ROIs | Automatic retained regions | Human ROI substantive overlaps | Current decision |
|---|---:|---:|---:|---|
| S06–F1 | 9 | 329 | 0 | Computational comparison completed; **scientific grain signoff pending** |
| S06–F2 | 16 | 23 | **3** | **Hold manual–automatic IoU/Dice** |
| S06–F3 | 15 | 344 | **2** | **Hold manual–automatic IoU/Dice** |

### S06–F2 exact review pairs

| Human ROI Manager positions | ROI names | Shared pixels | % of smaller ROI area |
|---|---|---:|---:|
| #1 / #5 | `0519-0660` / `0523-0647` | 12,726 | **81.24%** |
| #2 / #6 | `0797-0946` / `0789-0900` | 3,430 | **58.01%** |
| #4 / #11 | `0680-0483` / `0687-0484` | 2,147 | **87.74%** |

Total distinct F2 pixels contained in more than one polygon: **18,303**. These large pairwise overlaps suggest near-duplicate or mutually non-independent tracings; whether an ROI represents a genuine distinct grain must be decided against the original BMP.

### S06–F3 exact review pairs

| Human ROI Manager positions | ROI names | Shared pixels | % of smaller ROI area |
|---|---|---:|---:|
| #1 / #10 | `0642-0422` / `0634-0412` | 5,798 | **100.00%** |
| #9 / #15 | `0693-0291` / `0697-0283` | 5,281 | **99.02%** |

Total distinct F3 pixels contained in more than one polygon: **11,079**. The almost entirely overlapping contours are consistent with duplicate selection of the same apparent optical feature; verify in ROI Manager before choosing which true drawing, if any, should be retained.

## Scientific reading of the images (preliminary, not asserted mechanism)

The first-round automatic algorithm's very large F2 average and small object count, contrasted with F1/F3, raises a **possible under-segmentation/merged-region** concern for F2. The high F1/F3 object counts raise the distinct question of whether the algorithm segments fine contrast patches rather than entire grains. Both hypotheses should be tested rather than accepted as conclusions. Selected manual ROI means appearing similar in F2 and F3 do NOT disprove spatial microstructural heterogeneity because they are selected, overlapping/nonrandom features and not the same sample as the full-field segmentation.

## Corrective protocol — preserve originals

1. Open source BMP `2-600 - Copy/100x2.bmp` and corresponding **F2** ZIP in ImageJ/Fiji ROI Manager; enable **Show All**; review the three listed ROI pairs visually against physically credible boundaries.
2. For **F3**, open `100x3.bmp` and the F3 ZIP; review the two nearly duplicate pairs. Do not blindly delete by number; a qualified reviewer decides whether the polygons represent the same grain, distinct grains incorrectly overlapping, or ambiguous etching structures.
3. Save corrected manual archives as `S06_F2.zip` and `S06_F3.zip`, retaining backups of the present versions under `_backup.zip` suffix. The audit workflow ignores backups and accepts active names case-insensitively.
4. Commit the two updated active ZIPs to the same audit branch. The workflow checks pixel identity, polygon overlaps, and then calculates **selected-ROI** IoU/Dice and matched ECD.
5. Once all three selected field ROI sets pass geometrical QA, review full-resolution original/automatic/manual contour overlays before making publication statements; document fields where actual grain boundaries remain unresolvable.

## JMEP evidence decision

**No-go yet** for revising quantitative physical grain-size distributions, Hall–Petch strengthening interpretations, grain/tribology correlations or dynamic recrystallization claims. Existing source-image identity, ImageJ scale provenance and computational reproducibility are documented. Manual ROI work adds essential independent observer evidence but does not yet validate physical grain identity across the 12 experimental conditions.

## Linked audit artifacts

- `output/roi_field_validation_gate.csv`: per-field explicit PASS-TO-SCORE/HOLD status.
- `output/S06_F2_overlap_pairs.csv`, `output/S06_F3_overlap_pairs.csv`: exact overlapping object pairs.
- `output/S06_F2_manual_ROI_overlap_diagnostic.jpg`, `output/S06_F3_manual_ROI_overlap_diagnostic.jpg`: original/outlined/overlap graphics.
- `output/S06_F2_roi_inventory.csv`, `output/S06_F3_roi_inventory.csv`: original manual object indices, areas and diameter.
- `output/manual_vs_auto_per_field.csv`: currently scored fields only; must not imply missing fields have passed.
- `output/MANUAL_VALIDATION_STATUS.md`: automatically generated field-level status.

**Original experimental micrographs, previously published calculations and manuscript were not overwritten during this review.**
