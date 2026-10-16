# Sample-label provenance clarification — Phase 1 / Task 1

## Researcher clarification

On 10 October 2026, the researcher clarified: **"The folder name given on the basis of weight percentage of graphene and sintering temperature."**

This clarification identifies the *meaning* of the original BMP folder labels. For further audit work, use these BMP labels as the **working condition identifiers**, subject to cross-checking available laboratory/acquisition records if any exist. This is a researcher statement, not independent instrument metadata.

## Confirmed decoded-pixel match mapping

The initial non-destructive audit compared the decoded RGB contents of each source BMP and the corresponding TIFF image, irrespective of TIFF compression. For all three magnifications and three standard fields per condition, the exact matching BMP/TIFF pairs for the 4 wt.% GNP conditions are:

| Working sample ID | GNP wt.% | Sinter temperature (°C) | Correct original BMP folder | Exact matching TIFF folder | Image pairs |
|---|---:|---:|---|---|---:|
| S10 | 4 | 500 | `4-500 - Copy` | `Optical microstructure/{magnification} x/11` (TIFF S11) | 9 |
| S11 | 4 | 550 | `4-550 - Copy` | `Optical microstructure/{magnification} x/12` (TIFF S12) | 9 |
| S12 | 4 | 600 | `4.600 - Copy` | `Optical microstructure/{magnification} x/10` (TIFF S10) | 9 |

For each magnification **{magnification} = 100, 200, or 400**, with fields 1–3.

All other 81 standard BMP/TIFF pairs match under their current condition labels.

**Important:** Treat the older numerical grain-size outputs for TIFF-labeled S10–S12 as **provisionally misassigned** relative to the newly confirmed BMP folder naming convention. Do not overwrite or silently relabel the historical results: retain both identities in any corrected dataset as e.g. `Working_Condition`, `Original_BMP_Folder`, `Historical_TIFF_Folder`, and `Analysis_Field`.

## Implications for published interpretation

- The reported historical ECD measurements, if segmentation/calibration prove valid, would map as follows:
  - TIFF-labeled **S11** ECD 40.024 µm -> working **S10** (4 wt.% / 500 °C).
  - TIFF-labeled **S12** ECD 52.274 µm -> working **S11** (4 wt.% / 550 °C).
  - TIFF-labeled **S10** ECD 29.930 µm -> working **S12** (4 wt.% / 600 °C).
- **These three numbers are provisional audit-only references, not corrected final grain-size results.**
- Historical grain-size correlations, interaction plots and grain-related discussion must be recomputed from a validated, traceable dataset after reviewing calibration and segmentation.
- Tensile/hardness/tribological measurements cannot be relabeled on the basis of optical-file comparisons alone. They need their own specimen provenance.

## Remaining scientific gates

1. Verify the actual physical calibration (previous 100× scale 0.473 µm/pixel is hard-coded).
2. Inspect and validate grain/etching-feature segmentation in representative images, especially anomalous fields for S2, S3, S6, S9 and mapped S10–S12.
3. Confirm extra S7/S12 fields are independent and representative; do not include additional fields without documenting selection.
4. Recalculate condition-level grain-size distributions, uncertainty and grain–property correlations with explicit old/new image traceability.
5. Update manuscript figures and claims **only after** checks 1–4.

**No experimental images or numerical measurements were changed when this note was created.**
