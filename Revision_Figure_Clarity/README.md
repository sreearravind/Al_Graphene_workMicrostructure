# Revision Figure Clarity

This folder contains the manuscript-revision plotting script for Figures 5, 6, 8, 9, 10 and 11.

## Scope of the revision

The script changes **presentation only**: larger axis labels, larger tick labels, clearer legends, larger numerical annotations, improved spacing, and 600-dpi publication outputs. It reads the same master CSV used by the original plotting scripts, so the numerical values and statistical calculations are not altered.

Outputs are generated as PNG (600 dpi), TIFF (600 dpi, LZW compressed) and SVG.

## Script

`publication_figures_5_6_8_9_10_11.py`

Default input file:

`C:\Users\HP\OneDrive\2026\Al Graphene\Supplementary_Grain_Size_hardness_tensile_desnity.csv`

The path can be overridden from the command line:

```bash
python publication_figures_5_6_8_9_10_11.py --csv "path\to\master.csv" --out "path\to\output"
```

## Important manuscript notes

- Figure 5 is only a **clarity upgrade** at this stage. Hardness error bars required by Reviewer Comment 7 should be added once the nine replicate indentation values per condition are recovered.
- Figure 6 remains the condition-level YS/UTS/elongation summary. Reviewer Comments 1 and 8 still require the full engineering stress-strain curves.
- Figures 8 and 9 retain the same COF and mass-loss data and linear trend calculation.
- Figures 10 and 11 recompute the Pearson coefficients from the same master CSV rather than entering correlation values manually.
- No experimental values are changed by this plotting revision.
