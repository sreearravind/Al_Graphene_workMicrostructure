# Phase 2 — Task 6: New 400× calibration and original experimental evidence closure

**Status: researcher-scale reference measured, conditional-scale Figure 3 generated, other instrument evidence pending. This is NOT journal-final.**

## Source of new 400× scale

- User uploaded original `Scale_reference_400x1.jpg`, native **1600 × 1200** pixels (same dimensions as original 400× source BMPs).
- The visibly labelled **50 µm** horizontal white bar extends from x=1204 to 1351 inclusive, over y=1056–1063; 148 contiguous pixels at RGB thresholds 200, 225 and 245.
- Thus **50 µm / 148px = 0.33783784 µm/pixel**. A nominal **100 µm** scale bar should have a native-image span of **296px**, or **166px** after the uniform 1600→900px display panel reduction.
- SHA-256 of the unchanged uploaded JPEG: `b16409f2d06ea63469060850dcc5939b6c5bd5f74cd205508e1832b6e34ad3ec`.
- **The actual original reference JPEG is a user-uploaded conversation attachment, not yet committed to this branch.** To independently rerun the ruler digitization, add that original JPEG unchanged to this folder; the JSON captures its hash and geometry.
- The 400× source audit independently confirms **36/36 decoded-RGB-identical BMP/TIFF pairs**, including the S10→historical TIFF S11, S11→historical TIFF S12 and S12→historical TIFF S10 label crosswalk.

### Calibration transfer condition

A bar in one photograph cannot automatically calibrate all archived images solely because they have matching 1600×1200 pixel dimensions and a 400× label. The author should confirm unchanged **microscope objective, camera and adaptor, field of view, digital zoom, image cropping, and software export/resizing** across the scale reference and all source 400× BMP files.

The previous researcher-reported 100× scale **0.473 µm/pixel** divided by this 400× estimate **0.337838 µm/pixel** gives 1.40×, not the nominal objective/total-magnification 4× ratio. Different camera acquisition or cropping could explain this, but we must resolve it rather than silently assuming either value is true for a different condition.

### New working Figure 3

The [calibration workflow](../../.github/workflows/phase2_task6_provisional_400x_calibration.yml) renders all twelve processing conditions at nominal 400×, using the first original archived field F1 at every condition (no subjective field selection) and a **provisional 100 µm** bar derived from the submitted 50 µm reference.

- [Full-resolution conditional-calibration 12-panel figure](output/FIGURE3_400x_12conditions_100um_PROVISIONAL.png) — **do not submit until acquisition settings confirmed**.
- [Compact author-review preview](output/FIGURE3_400x_PROVISIONAL_REVIEW_PREVIEW.jpg).
- [Original 36 source-image paths and SHA hashes](output/figure3_400x_source_and_calibration_manifest.csv).
- [Figure calibration transfer/readiness record](output/figure3_calibration_transfer_readiness.json).
- [Author approval conditions](output/FIGURE3_AUTHOR_APPROVAL_GATE.md).
- [Measured source-image calibration evidence](400x_reference_calibration_audit.json).

No global image enhancement, physical grain segmentation or microscope-image modification is used in the figure reconstruction, beyond uniform publication-panel resizing and scale/label annotations.

## Scientific interpretation of optical morphology

The microscope shows etched contrast networks, locally brighter matrix regions and darker features, but **a contrast region need not be an individual crystallographic grain**. Phase 1's image audit confirmed numerical repeatability of the archived GrainStat processing but documented strong CLAHE dependence and S06 mismatch with independently traced selected image features.

The author should avoid turning this new pixel scale into grain-size distributions or reintroducing claims of confirmed Hall–Petch strengthening, dynamic recrystallisation, spatial GNP dispersion, interfacial carbide chemistry or quantified porosity. The removed original Figure 4 stays removed from manuscript v8.3.

## XRD and physical testing — honest closure status

- **XRD:** user has requested the **native measured scan** from the collaborator. Status: **REQUESTED / NOT RECEIVED**. If recovered, verify the authentic 2θ–intensity file, source sample ID, sintering temperature and acquisition method before replotting the single measured pattern. Multi-condition XRD cannot be invented because it was never performed and there are no original specimens.
- **Hardness:** nine archived within-condition values per processing level were arithmetically reconciled, but the Rockwell scale configuration, indenter/loads, dwell time and native source file remain unconfirmed.
- **Tensile:** native UTM trace, specimen gauge and strain rate/crosshead speed remain unconfirmed.
- **Tribology:** native COF-vs-time and mass-loss records pending; archived S12 COF 0.125 is a source table value, not a new instrument validation.
- **DOE:** retrospective 4×3 factorial matrix verified; not a genuine original Minitab run-order screenshot; the unreplicated full interaction model has no residual degrees of freedom.

## Reviewer response strategy

- **R2 comment 5:** Once optical acquisition consistency is established, replace manuscript Figure 3 with the source-verified, conditional-calibrated 400× montage and include a precise calibration procedure. Do not claim it is independently calibrated before that check.
- **R2 comments 6–7:** Quantitative crystallographic grain boundaries are not independently validated. Retain the removal of original Figure 4; discuss visible optical morphology carefully. This does not completely satisfy Reviewer 2's grain-distribution request.
- **R2 comment 8:** XRD primary-source file requested; no phase-evolution comparison across the twelve conditions is experimentally available.
- **R2 comment 4:** supply machine parameters only if the actual lab logs are recovered; no guessed ASTM standard settings.

## Next action

**Author confirms:** “Was `Scale_reference_400x1.jpg` captured through the same microscope objective, camera/adapter and digital zoom/export settings as the archived 400× BMP images, without cropping/resizing?” Then the figure can be promoted from **PROVISIONAL** to **RESEARCHER-CONFIRMED CALIBRATED** (still not crystallographic grain verification) and inserted into a separate manuscript v8.4 working copy.

Keep the draft PR unmerged. Preserve the native JPEG, specimen source images, manual ROI ZIPs and previous manuscript versions.
