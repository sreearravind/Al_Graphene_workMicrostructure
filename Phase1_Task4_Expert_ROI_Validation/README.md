# Phase 1 — Task 4: independent expert tracing and quantitative validation

## Scientific status

The 19-field original-image GrainStat analysis is **computationally reproducible**. The TIFF S10/S11/S12 pixel-label permutation has been documented. The 100x scale of **0.473 µm/pixel** was obtained by the researcher in ImageJ using a ruler reference from the same microscope, but the original ruler image has not yet been archived.

**No manually traced ROI archive existed when Task 4 was created.** Therefore, no manual-to-automatic IoU/Dice value has yet been measured. Do not interpret the software-only checks as validation of true metallurgical grain boundaries.

## First priority: eight-field pilot

To minimize unnecessary manual work, start with these fixed fields:

| Priority | Working field | Why it matters |
|---|---|---|
| 1 | S02_F1 | Only 10 objects at previous 500px setting; possible large merged regions |
| 2 | S03_F3 | Only 12 objects and very high mean ECD |
| 3 | S06_F1 | High-count reference (329 previously detected) |
| 4 | S06_F2 | Only 23 objects; strong within-condition disagreement |
| 5 | S09_F2 | Only 17 objects; possible merged regions |
| 6 | S10_F1 | Check 4 wt.% / 500 °C against original BMP label, not historic TIFF S10 |
| 7 | S11_F1 | Check 4 wt.% / 550 °C against original BMP label |
| 8 | S12_F1 | Check 4 wt.% / 600 °C against original BMP label |

If boundary identity is not defensible in these fields, stop and document UNRESOLVABLE before spending time on the remaining 11 of the pre-registered 19 fields. Do not manually select only easy fields while silently omitting difficult ones.

## Human ROI procedure in Fiji / ImageJ

1. Open the ORIGINAL BMP (not a recompressed screenshot) under the original BMP archive. The macro checks the specimen/field code against the folder and image filename.
2. Open the macro ImageJ_Expert_Trace_100x.ijm via Plugins > Macros > Run. Select the source BMP; enter its working sample code, e.g. S02_F1.
3. Confirm 100x imaging and the 0.473 µm/pixel scale with the originally measured ruler/reference settings. The script enters this calibration, but cannot independently verify microscope acquisition settings.
4. Divide the image conceptually into **4 columns by 3 rows**, each 400 x 400 pixels. Try to trace two fully distinguishable grains from each of the twelve sectors using polygon/freehand ROI (nominal target 24 grains), avoiding selective sampling of only easy regions. Do not force 24 if boundaries are not identifiable. Note sectors that contain no distinguishable grains.
5. Draw CLOSED contours around only unambiguous physical grain interiors; press T to add each polygon to ROI Manager. **Do not** trace clusters, scratches, porosity, stains or uncertain etching patterns as confirmed grains.
6. If no reliable boundary contours can be distinguished, mark the field UNRESOLVABLE in the human review register. Do not manufacture ROIs, and do not treat the absence of manual data as evidence of automatic accuracy.
7. At completion, the macro exports S02_F1.zip (actual ImageJ ROI objects) plus S02_F1_manual_measurements.csv. These outputs are human-derived. Keep any calibration reference image and handwritten/typed review notes.
8. Upload only the genuine ROI ZIPs to the manual_rois subfolder of the audit branch. Do not upload software-generated toy/sample contours or change the original image.
9. Run the workflow Phase 1 Task 4 Human ROI Comparison. If no ROI ZIPs are present, it will report PENDING, not fictional numerical validation.

## Algorithmic comparison

The program compare_manual_rois.py:
- Checks that each ROI ZIP belongs to the pre-selected 19-field manifest.
- Verifies exact decoded RGB identity between the original BMP and historical TIFF used for GrainStat, accounting for the historical S10/S11/S12 permutation.
- Runs the **archived 500px** GrainStat method on the matched historical TIFF.
- Reads actual human polygon/freehand/trace ROIs in original **pixel (x,y) coordinates**, and rejects unsupported ROI types, overlapping human ROIs, invalid coordinates, or files with ambiguous names.
- Computes per-object expert-vs-best-matching-automatic **intersection-over-union (IoU)** and **Dice**, manual equivalent diameter, matched algorithmic equivalent diameter, and image-sector coverage.
- Produces three-panel original BMP / algorithmic red contour / human GREEN contour sheets **only when actual human ROI ZIP files are present**.
- Reports metrics at ROI and image-field level with a forced EXPLICIT EXPERT_SIGNOFF_PENDING status. Numerical agreement does not itself prove physically meaningful grains or authorize a manuscript edit.

Per-field expectations of 20-30 traced ROIs and representation across 4x3 image sectors are methodological goals, **not a reason to invent grains**. There is no claim of an ASTM acceptance threshold in this comparison. Decisions must be documented with evidence.

## Files

- ImageJ_Expert_Trace_100x.ijm — ImageJ macro to collect real polygon/freehand ROIs; checks BMP filename and folder condition ID.
- manual_rois — folder for manually captured human ROI ZIPs; empty until researcher completes tracing.
- compare_manual_rois.py — reproducible comparison with GrainStat mask.
- output/MANUAL_VALIDATION_STATUS.md — PENDING until real data exist.
- output/manual_vs_auto_per_roi.csv — generated **only** after expert ROIs are submitted.
- output/manual_vs_auto_per_field.csv — generated **only** after expert ROIs are submitted.
- output/Sxx_Fy_manual_vs_auto.jpg — generated **only** after expert ROIs are submitted.
- ../Phase1_Task2_Segmentation_QA/MANUAL_VALIDATION_TEMPLATE.csv — original fixed 19-field review register.

## Publication gate

JMEP reviewer request concerns defensible actual microstructure; reproducibility and IoU on interpreted optical features are not equivalent to EBSD crystallographic identification. If enough 100x fields have physically ambiguous grain boundaries, report optical segmented feature morphology under the stated preprocessing method, retract stronger claims of confirmed physical grain size / dynamic recrystallization, or plan new characterization on future specimens. No matter how high the IoU, one dataset with one specimen per condition cannot establish independently fabricated replicates.
