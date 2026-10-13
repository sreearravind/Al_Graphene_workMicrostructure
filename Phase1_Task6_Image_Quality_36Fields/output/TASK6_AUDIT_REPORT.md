# Task 6: optical image quality and segmentation reliability across all 12 conditions

**36 source BMP fields; no excluded or selected image fields. Computed boundary outlines are not physically verified crystallographic grains.**

## Provenance and repeatability
- All 36 original 100x BMPs matched the archived TIFFs exactly by decoded RGB pixels.
- Original condition BMP labels used, with historical TIFF S10-S12 cyclic sample-folder discrepancy explicitly tracked.
- Researcher-reported ImageJ ruler calibration for 100x: 0.473 um/pixel. Original ruler image is not available in the archive.
- Archived 500px segmentation counts independently reproduced in 36/36 fields.
- Archived mean ECD independently reproduced within 1e-6 um in 36/36 fields.
- Each field rerun with GrainStat area thresholds 250, 500, 1000 pixels (Gaussian sigma=1, CLAHE on, Otsu, morphology radius=2, watershed).
- Each field additionally rerun with CLAHE OFF at 500px, retaining all other GrainStat settings.

## Variability of original 500px segmented-object measurements
| Condition | GNP wt.% | Temp C | Automated object-count range | Count max/min | Field mean ECD range um | Field ECD CV % | Count ratio >=4 |
|---|---:|---:|---|---:|---|---:|---|
| S01 | 0 | 500 | 84-164 | 1.95 | 36.3-48.1 | 14.0 | no |
| S02 | 0 | 550 | 10-107 | 10.70 | 41.4-102.5 | 45.3 | yes |
| S03 | 0 | 600 | 12-174 | 14.50 | 33.1-133.1 | 78.8 | yes |
| S04 | 2 | 500 | 78-133 | 1.71 | 38.8-50.1 | 14.0 | no |
| S05 | 2 | 550 | 87-172 | 1.98 | 35.0-42.5 | 10.9 | no |
| S06 | 2 | 600 | 23-344 | 14.96 | 24.2-95.2 | 85.0 | yes |
| S07 | 3 | 500 | 84-170 | 2.02 | 35.6-48.4 | 18.1 | no |
| S08 | 3 | 550 | 49-261 | 5.33 | 28.0-52.8 | 30.3 | yes |
| S09 | 3 | 600 | 17-72 | 4.24 | 51.5-103.7 | 33.0 | yes |
| S10 | 4 | 500 | 71-139 | 1.96 | 37.0-47.6 | 13.6 | no |
| S11 | 4 | 550 | 27-106 | 3.93 | 44.6-78.3 | 29.4 | no |
| S12 | 4 | 600 | 60-347 | 5.78 | 24.7-56.5 | 45.0 | yes |

## Image quality descriptors and preprocessing sensitivity
Grayscale range, 4x4 tile-mean range, contrast, entropy and Laplacian variance are image descriptors; their variation may arise from actual microstructural texture, illumination, or both. No objective focus calibration image is available and no proxy alone establishes the cause.

| Quantity across 36 fields | Median | Minimum | Maximum |
|---|---:|---:|---:|
| Tile mean grayscale range (0-255) | 35.545 | 22.052 | 48.123 |
| P95-P05 grayscale spread | 127.000 | 113.000 | 157.000 |
| Relative RMS contrast | 0.276 | 0.232 | 0.369 |
| Laplacian variance sigma=1 | 0.001 | 0.000 | 0.001 |
| ECD shift 250px vs 500px (%) | -0.869 | -2.878 | 0.048 |
| ECD shift 1000px vs 500px (%) | 3.045 | 0.000 | 9.631 |
| ECD shift no CLAHE (%) | 82.983 | -13.361 | 803.677 |
| Count shift no CLAHE (%) | -72.334 | -98.847 | 15.333 |

- 6/12 conditions exhibit more than fourfold automated object-count variation across three 100x fields. This is a REVIEW FLAG, not a basis to remove images.
- Median absolute mean-ECD change without CLAHE: 83.0%; maximum: 803.7%.
- Median absolute mean-ECD change at 1000px versus 500px: 3.0%.

## Evidence deliverables
- all_36field_QA.csv: every original field, pixel provenance, image-quality proxies and segmentation sensitivities.
- all_12condition_QA_summary.csv: every condition, nested-field count/ECD variability.
- Sxx_BMP_vs_computed.jpg: 12 three-field source-versus-contour contact sheets.
- heatmap_counts.png, heatmap_ECD.png, heatmap_tile_grayscale.png, heatmap_CLAHE_effect.png.
- quality_segmentation_descriptive_spearman.csv: descriptive correlations only (no statistical p-values or causal inference).

## Scientific publication guardrails
- No original source files, manual ROI ZIPs, previously reported numeric dataset or manuscript changed; original user field choices are retained.
- High within-condition field variation is compatible with true spatial heterogeneity OR inconsistent automated segmentation, illumination, etching and focus effects. The source alone does not establish a unique cause.
- A repeatable algorithm can segment pores, etching networks and contrast patches rather than actual metallurgical grain boundaries.
- Unless genuine grain boundaries are independently interpretable, report explicitly defined optically segmented feature sizes instead of crystallographically verified grain diameters. Do not claim EBSD, quantitative DRX, Hall-Petch strengthening or independently replicated materials responses.
- User has confirmed that 12-condition XRD was never performed and no physical samples remain; optical processing cannot create those measurements.
- Reviewer demand for validated physical grain-size distributions may remain unmet despite exhaustive optical QA.
