# Phase 1 — Task 1: optical source-image validation

Generated: 2026-10-10T10:55:28.855937+00:00

## Inventory and RGB image-equivalence checks

- additional_BMP: **11**
- core_BMP: **108**
- mismatch: **27**
- pixel_identical: **81**
- source_BMP: **119**
- Unique RGB hashes: **119**
- Exact duplicate pixel-content groups: **0**
- Unmapped BMPs: **0**

## Per-condition image counts

| Sample | wt.% | Temp C | 100x BMP | 200x BMP | 400x BMP |
|---|---:|---:|---:|---:|---:|
| S1 | 0 | 500 | 3 | 3 | 3 |
| S2 | 0 | 550 | 3 | 3 | 3 |
| S3 | 0 | 600 | 3 | 3 | 3 |
| S4 | 2 | 500 | 3 | 3 | 3 |
| S5 | 2 | 550 | 3 | 3 | 3 |
| S6 | 2 | 600 | 3 | 3 | 3 |
| S7 | 3 | 500 | 6 | 5 | 4 |
| S8 | 3 | 550 | 3 | 3 | 3 |
| S9 | 3 | 600 | 3 | 3 | 3 |
| S10 | 4 | 500 | 3 | 3 | 3 |
| S11 | 4 | 550 | 3 | 3 | 3 |
| S12 | 4 | 600 | 5 | 4 | 5 |

## Cross-label TIFF-to-BMP identity findings

- TIFF folder **S10** matches BMP source folder **S12** at 9 exact decoded-pixel-identical field(s).
- TIFF folder **S11** matches BMP source folder **S10** at 9 exact decoded-pixel-identical field(s).
- TIFF folder **S12** matches BMP source folder **S11** at 9 exact decoded-pixel-identical field(s).
**Critical:** This is a sample-label provenance discrepancy, NOT evidence that either historical TIFF labels or recent BMP folder labels are correct. Confirm with acquisition notebooks / original specimen log before reassigning any numerical grain results.
The prior grain-analysis TIFF-derived results for any affected sample are NOT validated against newly supplied BMP specimen identifiers.

## Calibration and scientific interpretation

- Previous grain analysis HARD-CODES **0.473 µm/pixel** for 100x images. This is an unverified calibration assumption in the absence of microscope-stage/calibration records.
- BMP header DPI and TIFF image DPI are not microscopy length calibration. Never infer a valid physical µm/pixel scale solely from DPI.
- The existing BMP/TIFF identity result can verify that image conversion did not alter RGB pixels, but cannot validate microscope scale, visible grain boundaries, independent fields, or dynamic recrystallization.
- Confirm scale from acquisition software, certified microscope calibration, or a genuinely embedded scale bar with known provenance. Do not fabricate a scale bar.
- 200x/400x micron/pixel ratios must be independently checked before micrometre scale bars are added.
- Additional BMP fields from S7 and S12 must be reviewed for quality/independence before expanding prior grain measurements.

## Exceptions and cautions

- TIFF mismatch: Optical miscrostructure_Figures_BMP file/4-500 - Copy/100x1.bmp => RGB PIXEL DIFFERENT
- TIFF mismatch: Optical miscrostructure_Figures_BMP file/4-500 - Copy/100x2.bmp => RGB PIXEL DIFFERENT
- TIFF mismatch: Optical miscrostructure_Figures_BMP file/4-500 - Copy/100x3.bmp => RGB PIXEL DIFFERENT
- TIFF mismatch: Optical miscrostructure_Figures_BMP file/4-500 - Copy/200x1.bmp => RGB PIXEL DIFFERENT
- TIFF mismatch: Optical miscrostructure_Figures_BMP file/4-500 - Copy/200x2.bmp => RGB PIXEL DIFFERENT
- TIFF mismatch: Optical miscrostructure_Figures_BMP file/4-500 - Copy/200x3.bmp => RGB PIXEL DIFFERENT
- TIFF mismatch: Optical miscrostructure_Figures_BMP file/4-500 - Copy/400x1.bmp => RGB PIXEL DIFFERENT
- TIFF mismatch: Optical miscrostructure_Figures_BMP file/4-500 - Copy/400x2.bmp => RGB PIXEL DIFFERENT
- TIFF mismatch: Optical miscrostructure_Figures_BMP file/4-500 - Copy/400x3.bmp => RGB PIXEL DIFFERENT
- TIFF mismatch: Optical miscrostructure_Figures_BMP file/4-550 - Copy/100x1.bmp => RGB PIXEL DIFFERENT
- TIFF mismatch: Optical miscrostructure_Figures_BMP file/4-550 - Copy/100x2.bmp => RGB PIXEL DIFFERENT
- TIFF mismatch: Optical miscrostructure_Figures_BMP file/4-550 - Copy/100x3.bmp => RGB PIXEL DIFFERENT
- TIFF mismatch: Optical miscrostructure_Figures_BMP file/4-550 - Copy/200x1.bmp => RGB PIXEL DIFFERENT
- TIFF mismatch: Optical miscrostructure_Figures_BMP file/4-550 - Copy/200x2.bmp => RGB PIXEL DIFFERENT
- TIFF mismatch: Optical miscrostructure_Figures_BMP file/4-550 - Copy/200x3.bmp => RGB PIXEL DIFFERENT
- TIFF mismatch: Optical miscrostructure_Figures_BMP file/4-550 - Copy/400x1.bmp => RGB PIXEL DIFFERENT
- TIFF mismatch: Optical miscrostructure_Figures_BMP file/4-550 - Copy/400x2.bmp => RGB PIXEL DIFFERENT
- TIFF mismatch: Optical miscrostructure_Figures_BMP file/4-550 - Copy/400x3.bmp => RGB PIXEL DIFFERENT
- TIFF mismatch: Optical miscrostructure_Figures_BMP file/4.600 - Copy/100x1.bmp => RGB PIXEL DIFFERENT
- TIFF mismatch: Optical miscrostructure_Figures_BMP file/4.600 - Copy/100x2.bmp => RGB PIXEL DIFFERENT
- TIFF mismatch: Optical miscrostructure_Figures_BMP file/4.600 - Copy/100x3.bmp => RGB PIXEL DIFFERENT
- TIFF mismatch: Optical miscrostructure_Figures_BMP file/4.600 - Copy/200x1.bmp => RGB PIXEL DIFFERENT
- TIFF mismatch: Optical miscrostructure_Figures_BMP file/4.600 - Copy/200x2.bmp => RGB PIXEL DIFFERENT
- TIFF mismatch: Optical miscrostructure_Figures_BMP file/4.600 - Copy/200x3.bmp => RGB PIXEL DIFFERENT
- TIFF mismatch: Optical miscrostructure_Figures_BMP file/4.600 - Copy/400x1.bmp => RGB PIXEL DIFFERENT
- TIFF mismatch: Optical miscrostructure_Figures_BMP file/4.600 - Copy/400x2.bmp => RGB PIXEL DIFFERENT
- TIFF mismatch: Optical miscrostructure_Figures_BMP file/4.600 - Copy/400x3.bmp => RGB PIXEL DIFFERENT

## Next step
Inspect contact sheets and representative original frames; authenticate 100x calibration before any µm-based grain-size reanalysis. Then perform manually checked segmentation overlays on anomalous fields (S2, S3, S6, S9).
