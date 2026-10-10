# Task 2: Screening of existing optical segmentation

**Status:** Automated metric QA and image montages completed. No expert tracing verification performed yet.

## Researcher-reported ImageJ calibration

100x optical calibration 0.473 um/pixel, reportedly obtained using an ImageJ ruler reference on the same microscope.
Existing minimum threshold 500 pixels corresponds to an ECD of 11.93 um.
The original ImageJ ruler/reference image and pixel-reference measurement have not yet been archived for independent reproduction.

## Field-level screening (original BMP condition labels)

| Working sample | Historical TIFF | Detected region counts (3 fields) | Count max/min | Field-mean ECD CV | Priority |
|---|---|---|---:|---:|---|
| S1 | S1 | 98;164;84 | 1.95 | 14.0% | HIGH |
| S2 | S2 | 10;26;107 | 10.70 | 45.3% | HIGH |
| S3 | S3 | 174;74;12 | 14.50 | 78.8% | HIGH |
| S4 | S4 | 133;78;81 | 1.71 | 14.0% | HIGH |
| S5 | S5 | 87;140;172 | 1.98 | 10.9% | HIGH |
| S6 | S6 | 329;23;344 | 14.96 | 85.0% | HIGH |
| S7 | S7 | 170;84;150 | 2.02 | 18.1% | HIGH |
| S8 | S8 | 91;49;261 | 5.33 | 30.3% | HIGH |
| S9 | S9 | 72;17;17 | 4.24 | 33.0% | HIGH |
| S10 | S11 | 71;127;139 | 1.96 | 13.6% | HIGH |
| S11 | S12 | 106;57;27 | 3.93 | 29.4% | HIGH |
| S12 | S10 | 60;202;347 | 5.78 | 45.0% | HIGH |

## Important scientific limitations

- Automated segmented objects are not necessarily crystallographic grains. Etching contrasts, scratches and clustering can form false or merged objects.
- The morphology flags and unusual count ratios are only quality-control prompts, not automatic data exclusion rules.
- The 500-pixel minimum excludes any segmented feature with ECD less than 11.93 um. This truncation may bias size distributions.
- Existing outputs are reassociated to the researcher-confirmed BMP condition labels for audit only: old TIFF S10 -> working S12; old TIFF S11 -> working S10; old TIFF S12 -> working S11.
- Image fields are nested measurements within a condition. Three images do not establish three independently fabricated specimen replicates.
- The original images and historical quantitative calculations remain untouched.

## QA outputs

- per_field_morphology_QA.csv (includes cross-label traceability and morphology flag metrics)
- sample_level_segmentation_QA.csv (condition-level screening)
- anomalous_100x_fields.jpg (source-image context)
- overlay_review_first_fields.jpg (source BMP vs existing first-field overlay)

**Next before publication:** Visual classification of actual grain boundaries and quantitative manual-vs-automatic agreement on selected source fields; assess segmentation thresholds and retain full audit trail.