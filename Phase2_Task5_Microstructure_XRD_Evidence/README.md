# Phase 2 Task 5 — source-calibrated figure and instrument evidence gate

**Status:** Completed archival image provenance review and working-text Figure 4 removal. **Not submission-ready**, because original 400× physical calibration, native XRD, and machine records remain unavailable.

## Verified by source audit
- Automated [GitHub Action](https://github.com/sreearravind/Al_Graphene_workMicrostructure/actions/runs/38548227786) successfully decoded and verified **all 36 original 400× microscope BMP/TIFF pairs**, using the S10→TIFF S11, S11→TIFF S12 and S12→TIFF S10 corrected crosswalk. Pixel SHA checks and all source folder paths are archived.
- A [twelve-panel Figure 3 draft](output/FIG3_400x_12condition_PROVISIONAL_NO_SCALE.jpg) is built using **F1** from each composition/temperature condition, predeclared regardless of visual appearance, with consistent original source-image treatment. It intentionally contains **no micrometre scale bars** and is stamped **NOT FOR SUBMISSION**.
- [All 36 original 400× image paths and pixel digests](output/figure3_400x_36field_source_manifest.csv) are preserved as an auditable image-level manifest.
- The file `microstructure_scale.tif` (2235 × 1668 px) was inventoried. Its [archived preview](output/microstructure_scale_provenance_preview.jpg) visibly contains a **100 µm scale marker** and a “Grain boundary” arrow on a grayscale image; no evidence currently links that image to the same magnification/illumination-camera settings as the twelve original colour 400× micrographs. The [TIFF metadata](output/scale_candidate_metadata.json) is **not** physical optical calibration.
- The available 100× ImageJ ruler-derived 0.473 µm/px must **not** be transferred unverified to 400×.

## Controlled manuscript revision v8.3 — prepared as a separate Word attachment
- Starting from the **v8.2 working DOCX**, delete only the former **Figure 4** image and caption: unvalidated grain-size distributions and correlations.
- Replace the associated legacy paragraph with a transparent limitation explanation; no reported tensile, tribological or hardness experimental values altered.
- Renumber all other figure captions and body references: old XRD Figure 5 → new **Figure 4**; former Figures 6–13 → **Figures 5–12**.
- Result: **12 figure captions, 16 embedded images, two original tables**; 33-page rendered working document. Figure 3 remains visibly labelled *working placeholder* pending authentic 400× scale reference; the new Figure 4 remains one-source XRD placeholder.
- The Word binary and standalone author evidence report are user-downloadable in the conversation but not uploaded to the repository, to avoid modifying source paper assets or misrepresenting binary commits.

## Evidence-to-claim readiness
| Workstream | What can be claimed | Must remain provisional / requested evidence |
|---|---|---|
| Optical Figure 3 | 36/36 image provenance, 12 processing-condition panel identity, nominal 400× | Actual 400× µm per pixel and valid calibrated bar; ImageJ ruler picture plus objective-camera metadata |
| Grain-size Figure | No independently validated physical grain-size distribution. Remove old Fig. 4 | No claims of confirmed DRX, Hall–Petch or grain-size/hardness/tribology mechanism |
| Representative XRD (new Fig. 4) | One illustrated 4 wt.% XRD pattern with reported Cu Kα, 40 kV, 20 mA, 20–80° range, 0.01° step, 1 s step | Native 2θ-intensity data and original specimen sintering-temperature ID absent from inspected sources; never assert 12-condition XRD |
| Hardness | Arithmetic means/SD of nine sorted within-condition readings reproduce | Rockwell indenter, major/minor load, dwell and original instrument printout |
| Tensile | Reported stress–strain plots and UTS values | Original strain rate/crosshead speed, gauge length and raw UTM export |
| Tribology | Archived S12 COF **0.125**, S5 lowest mass loss **0.0024 g** | Native COF logs, testing repeat structure and balance provenance |
| DOE | All 12 4×3 factorial cells documented, no residual df for fully interacted unreplicated model | Minitab historical project/run order unavailable; if recreated label as retrospective |

## Suggested next task
Source-record closure and **reviewer-response strategy**: (a) attempt retrieval of microscope 400× ruler; (b) recover native XRD and mechanical/tribological machine logs; (c) verify bibliography and external quantitative studies; (d) decide whether JMEP resubmission is scientifically feasible given the nonrecoverable multi-condition phase evidence. Do not present archived software segmentation as validated grain-size results.

**Scope guard:** This task did not create XRD peaks, new hardness/tensile instrument settings, physical grain diameters, missing independent experiments or fictitious microscopy calibration. All original source images and user-authored ImageJ ROIs remain unchanged.
