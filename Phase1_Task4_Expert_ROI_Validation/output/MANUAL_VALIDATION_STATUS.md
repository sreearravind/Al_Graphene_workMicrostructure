# Task 4 — expert ROI preflight review

**Status: MANUAL ROI OVERLAP REVIEW REQUIRED.**

Original human ROI ZIP archives were found. Their source files are unchanged. The script has deliberately withheld human-vs-automatic IoU/Dice scoring until the overlapping expert polygon selections are reviewed.

- S06 field 1: 24 actual ROI entries, 5 overlapping ROI pair(s), 3 substantive, 1228 overlap pixel(s).
  - ROI #1 versus #3: 649 pixels; 2.67% of smaller ROI.
  - ROI #1 versus #10: 31 pixels; 0.29% of smaller ROI.
  - ROI #2 versus #18: 1 pixels; 0.01% of smaller ROI.
  - ROI #2 versus #19: 88 pixels; 1.77% of smaller ROI.
  - ROI #17 versus #24: 459 pixels; 10.84% of smaller ROI.

Refer to the individual Sxx_Fy_manual_ROI_overlap_diagnostic.jpg and overlapping-pairs CSVs, then edit the ROI Manager entries in Fiji/ImageJ, verify boundaries and re-export the authentic human ROI ZIP. Do not automatically delete overlapping ROIs.
