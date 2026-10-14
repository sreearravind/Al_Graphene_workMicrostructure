# Phase 2 Task 6 — 400× scale transfer: author-confirmed

**Author confirmation received 14 October 2026.** The researcher confirms that the 50 µm reference photograph was acquired without resizing or cropping and explicitly authorizes transfer of its 400× calibration to the archived 400× micrographs. We treat this as author confirmation of common 400× acquisition/export conditions, not independently archived camera metadata.

## Calibration

- Reference: user-uploaded `Scale_reference_400x1.jpg`, 1600 × 1200 pixels, SHA-256 `b16409f2d06ea63469060850dcc5939b6c5bd5f74cd205508e1832b6e34ad3ec`.
- Physical reference label: 50 µm.
- White bar measured: 148 original image pixels (x=1204–1351), stable across pixel-intensity thresholds.
- **Scale: 50/148 = 0.337837838 µm/pixel (approximately 0.338 µm/pixel).**
- **Standardized 100 µm bar at native 1600×1200 image size: 296 pixels**, and approximately 166 pixels when the image is uniformly reduced to 900×675 panel size.
- Archived input: 36/36 400× original BMP and correctly crosswalked TIFF pairs matched by decoded RGB pixels.
- Figure panels: first archived 400× field of each of twelve original processing folders; no grain segmentation or favourable-field selection.
- **Author-confirmed new Figure 3:** [full-resolution 12-panel image](output/FIGURE3_400x_12conditions_100um_AUTHOR_CONFIRMED.png); [compact review copy](output/FIGURE3_400x_AUTHOR_CONFIRMED_PREVIEW.jpg).
- Prior 100× calibration (`0.473 µm/pixel`) remains a *separate calibration*; the 1.4× ratio to 400× does not match nominal 4× and cannot prove an error without common-camera optics/field-of-view documentation. No 100× values are used in the 400× figures.

## Publication limits

This settles the **author-side 400× scale-bar transfer** for Figure 3. Original instrument camera logs or independent calibration certification remain unavailable and should not be claimed. Physical grain boundary identity is **NOT** established from software segmentation or a labelled optical micrograph.

The previous grain-size-based Figure 4 remains withdrawn in v8.3. Newly scaled Figure 3 is now a candidate to replace its old source-placeholder image in a next Word edit, with a caption describing unenhanced original 400× optical morphology. No XRD raw data have yet arrived; collaborator has been asked.

## Suggested evidence-aligned manuscript language

**Methods:** "Optical micrographs obtained at nominal 400× were calibrated using an unmodified microscope reference image containing a 50 µm marker spanning 148 pixels. The corresponding calibration (0.338 µm pixel⁻¹) was applied consistently to original 1600 × 1200-pixel images acquired under the same settings, as confirmed by the researcher. Image contrast was used for qualitative morphological comparison, not to identify crystallographic boundaries quantitatively."

**Figure 3 caption:** "Optical micrographs of hot-extruded aluminium–graphene nanoplatelet specimens across GNP fractions of 0, 2, 3 and 4 wt.% and sintering temperatures of 500, 550 and 600 °C. Each panel shows the first archived nominal 400× optical field of its processing condition. Scale bars: 100 µm, derived from an unmodified 50 µm / 148-pixel reference acquired under the same imaging conditions. Etched contrast features are not independently verified grain boundaries."

**Unchanged external evidence blockers:** Only one representative 4 wt.% XRD pattern was reported; the collaborator has been asked for the original native scan. No 12-condition XRD experiment was performed and no physical specimens remain. Rockwell load/dwell, tensile rate/gauge and original tribometer traces remain external record checks.

**Figure endorsement is limited to the 400× optical scale and source-image identity.** No grain-size histogram, DRX, carbide/phase identification or strengthening mechanism is newly established.
