# Task 6 scientific decision — Al–GNP optical microstructure evidence for JMEP

## Verification status

Task 6 completed the **entire predefined 12 × 3 = 36 100× image matrix**. Each original BMP is decoded-RGB-identical to its relevant TIFF. The BMP folder name is the researcher-confirmed true specimen-processing label; historical TIFF S10/S11/S12 were cyclically associated with the wrong folder names. Researcher confirms ImageJ ruler-based 100× calibration 0.473 µm/pixel but independent ruler file remains unavailable.

All 36 archived 500-pixel GrainStat region counts and mean equivalent circular diameters were reproduced exactly (mean tolerance 1e-6 µm). Computational reproducibility is established; **physical grain-boundary validity is not established**.

## Converging quality and segmentation warnings

1. Six of twelve conditions have ≥4-fold counts among their three 100× optical fields, despite identical nominal specimen condition and optical magnification. S02, S03, S06, S08, S09 and S12 are flagged, *not excluded*. Seven conditions have ≥25% CV in the three field-mean equivalent diameters (the six above plus S11).
2. Changing minimum region area from 500 to 1,000 px alters the median field-mean ECD by a median absolute 3.0% (36 fields); changing it to 250 px causes a median relative shift −0.87%. Filter-size choice is not the primary observed source of sensitivity in these tests.
3. Disabling the CLAHE contrast step while retaining sigma=1 Gaussian, Otsu, morphology radius=2, 500px minimum and watershed produces **median absolute field mean ECD shift 83.0%** (max 803.7%) and median region-count shift **−72.3%**. Examples: S04-F1 automatic objects 133→2, mean equivalent diameter 38.84→351.01 µm; S12-F3 objects 347→4, equivalent diameter 24.66→164.19 µm. These are *algorithm diagnostics* only: the CLAHE-off measurements are NOT an alternative physical grain measurement or a reason to select the apparently more favourable parameter.
4. Image grayscale 4×4 tile-mean ranges varied between ~22.1 and ~48.1 levels (median ~35.5) across fields. These values may arise from illumination, topography, etching, microstructural spatial texture or multiple factors. Brightness statistics cannot causally disentangle them without controlled reference acquisition.
5. The descriptive field-level Spearman correlations of six image-quality proxies with object count and mean ECD were all weak (absolute ρ ≤ 0.207). Because 36 fields are nested in only twelve separately processed specimen conditions, absence of monotonic pooled correlation does **not** establish that illumination does not affect segmentation.
6. Some historical retained segmented regions occupy large portions of the entire image: S02-F1 up to 15.73%, S09-F2 13.97%, S03-F3 10.13%. These are flags for possible merged-structure segmentation, not automatic proof of defects or errors.
7. Human ImageJ pilot from Task 5 detected strong disagreement in S06-F2 (candidate selected manual IoU median ~0.097, none ≥0.50) despite an exact and reproducible GrainStat output. The pilot covered selected regions only and does not validate all fields, crystalline grain boundaries, or independently replicated specimens.

## Publication-oriented decision

**PASS — defensible now:** archival provenance, consistent acquisition-format image matrix, evidence of applied 100× ImageJ calibration method (calibration source image not independently archived), deterministic GrainStat object segmentation and explicit sensitivity/QA tables. Qualitative optical microstructure can be discussed carefully as morphology and etched features, while noting the ambiguity between true boundaries and image contrast networks.

**HOLD / NOT DEFENSIBLE as stated:** data-derived Figure 4 described as a rigorous physical grain-size distribution; strong grain-size-to-hardness/UTS/tribological mechanism attribution; confirmed dynamic recrystallisation, Hall–Petch strengthening, or quantitative porosity/phase identification from only these optical images. Do not silently replace original values with selected manual ROIs, suppress low-quality fields, or present the CLAHE-off alternative as ground truth.

**Practical editorial strategy:** Treat the automated equivalent-diameter values as provisional or supplementary *sizes of software-segmented optical features* with a precise definition and method. Do not simply rename these objects grains. Consider removing the quantitative grain-size and associated mechanistic correlations from the manuscript's central claims unless a metallurgist can independently substantiate continuous original-image boundaries across representative fields. This may mean a Reviewer 2 grain-distribution demand cannot be fully satisfied without additional microscopy, so acknowledge the limitation rather than overpromise.

**XRD limitation:** User confirms 12-condition XRD scans were never acquired and physical specimens are unavailable; optical image processing cannot supply the missing diffraction evidence. Address through a truthful scope/limitations discussion and journal/editor decision, not fabricated multiple-condition patterns.

## Supporting reproducible files

- Task6_AUDIT_REPORT: output/TASK6_AUDIT_REPORT.md (primary detailed audit)
- All 36 field metrics: output/all_36field_QA.csv
- All twelve material conditions: output/all_12condition_QA_summary.csv
- Four global QA heatmaps: output/heatmap_counts.png; output/heatmap_ECD.png; output/heatmap_tile_grayscale.png; output/heatmap_CLAHE_effect.png
- Twelve three-field BMP/segmentation contact sheets named output/Sxx_BMP_vs_computed.jpg
- Descriptive noninferential correlation diagnostics: output/quality_segmentation_descriptive_spearman.csv

## Proposed next step

Before text or figure edits, author an evidence-aligned decision matrix for each second-round reviewer request. For optical figures, retain high-resolution original BMPs and provide independently calibrated 100× scale bars when the exact pixel ratio is traceable; do not apply 100× calibration to 200×/400× panels. Choose an explicit manuscript path (qualitative microstructure with limitations, or independent physical boundary validation if possible) and explain unresolved evidentiary gaps candidly.

No original image, GrainStat historical output, mechanical/tribological measurements, user manual ROI archive or manuscript was altered by Task 6.
