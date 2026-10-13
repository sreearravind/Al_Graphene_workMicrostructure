# Task 4 — S06_F1 user-submitted ImageJ ROI pilot

**Status: geometry QA completed; manual–automatic scientific agreement on hold.**

## Provenance and quantitative facts

- User-uploaded source: `manual_rois/S06_F1.zip`, preserved unchanged.
- The ImageJ ROI ZIP was successfully parsed as **24 closed polygon ROIs** using the original 1600 × 1200-pixel source image. All 12 review sectors (4 columns × 3 rows) contain ROI centroids.
- Researcher-confirmed ImageJ scale for 100× images: **0.473 µm per pixel**.
- Across the 24 selected manually drawn polygons, mean equivalent circular diameter **50.30 µm**, range **30.47–90.44 µm**. These are selected *polygon feature* measurements, not yet representative or verified grain-size statistics.
- The historic automated GrainStat result on the full image contains 329 objects, mean ECD 24.73 µm. **Do not compare these two means as independent measurements of the same population**; the ImageJ ROIs are a selected subset.
- Pixel-coordinate rasterization identified 5 pairs of overlapping manual polygons, total **1,228 unique overlapping pixels**. No expert polygons were deleted or altered.

## ROI pairs requiring ImageJ boundary inspection

| ROI positions | ImageJ saved ROI names | Shared pixels | Fraction of smaller ROI |
|---|---|---:|---:|
| 1 and 3 | `0740-0417` / `0769-0587` | 649 | 2.67% |
| 1 and 10 | `0740-0417` / `0678-0237` | 31 | 0.29% |
| 2 and 18 | `0785-1060` / `0875-1207` | 1 | 0.01% |
| 2 and 19 | `0785-1060` / `0748-1210` | 88 | 1.77% |
| 17 and 24 | `0877-1367` / `0834-1433` | 459 | 10.84% |

Substantial overlaps (#1/#3, #2/#19, and #17/#24) deserve particular attention. One-pixel contact and small contour intersections can arise through pixel rasterization, but must still be recorded; their practical interpretation requires expert judgement.

## How to review without damaging the evidence

1. Open the ORIGINAL BMP file in `Optical miscrostructure_Figures_BMP file/2-600 - Copy/100x1.bmp` in Fiji/ImageJ.
2. In `Analyze > Tools > ROI Manager`, open the existing `S06_F1.zip`, then enable **Show All**. The ROI Manager entries should correspond to the saved names in the table.
3. For each pair, inspect whether the two polygons really represent distinct physically distinguishable grains. Correct the original polygon contours manually where defensible; mark an uncertain boundary **UNRESOLVABLE** rather than inventing one.
4. Save a corrected `S06_F1.zip` in a **new local folder** while retaining a backup of the original ZIP. Then update the audit-branch `manual_rois/S06_F1.zip` with the verified file. Do not use automated post-processing to force contours apart.
5. Rerun `Phase 1 Task 4 Human ROI Boundary Comparison`. The workflow will re-evaluate ROI geometry and only report actual overlap-aware manual-versus-GrainStat IoU/Dice if the accepted manual ROI set has passed QA.

## Source audit outputs

- `output/S06_F1_manual_ROI_overlap_diagnostic.jpg`: original BMP (left), drawn polygons and overlap pixels (right).
- `output/S06_F1_roi_inventory.csv`: per-polygon area, ECD, and image coordinates.
- `output/S06_F1_overlap_pairs.csv`: reproducible overlap intersections and percentage of smaller ROI.
- `output/expert_roi_preflight.json`: complete machine-readable preflight.
- `output/MANUAL_VALIDATION_STATUS.md`: intentionally **REVIEW REQUIRED** (not an invented agreement score).

## Manuscript implication

Task 4 has progressed from no expert contours to a real 24-polygon ImageJ pilot and a traceable QA report. However, the outlines have not been approved as true grain boundaries, and the 24-object selected mean must not replace the previous 329-object automated result. Figure 4 and grain–property correlations are still on hold pending verified expert ROI boundaries.
