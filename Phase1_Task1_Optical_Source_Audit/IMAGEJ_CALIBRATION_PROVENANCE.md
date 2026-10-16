# ImageJ calibration provenance — researcher statement

**Recorded:** 2026-10-10.

Researcher confirms that the prior **0.473 µm/pixel** conversion used for the **100× optical micrographs** was established in **ImageJ**, using a known ruler/scale reference imaged on the **same optical microscope**.

## Audit treatment
- Calibration is **researcher-confirmed from an instrument-specific ruler reference**, rather than an arbitrary software default.
- This statement supports continued review of the 100× segmentation at the reported scale.
- The original ruler/reference image, known physical interval, ImageJ pixel length, and any acquisition setting details are **not yet archived with the repository**. An independent reviewer cannot reproduce the calibration from the statement alone.
- The microscope's camera sampling/zoom/cropping and objective must match the condition used for the ruler reference to reuse the same µm/pixel.
- **Do not extrapolate 0.473 µm/pixel from 100× to 200× or 400×**, and do not infer physical magnification from TIFF 300 DPI.
- The previous 500-pixel area cutoff translates to a minimum equivalent circular diameter of **11.93 µm**, calculated as `0.473 * sqrt(4*500/pi)`. This can censor small detected regions and requires sensitivity analysis.
- These are analytical provenance and method concerns, **not an accusation that the original ImageJ measurement was incorrect**.

## Next action
Task 2 evaluates source BMP images and existing segmentation outputs, checks automated segmentation plausibility and morphology flags, and preserves the historical measurements unchanged. Please archive the original ImageJ reference if available for final journal supplement.
