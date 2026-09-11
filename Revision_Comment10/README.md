# Reviewer Comment 10 – comparative factor-response plots

This folder contains the data table and plotting script prepared to address Reviewer Comment 10:

> Provide comparative plots showing graphene-content and sintering-temperature effects on density, grain size, hardness, strength, and wear behaviour.

## Figure structure

The script generates one six-panel interaction figure using GNP content (0, 2, 3, and 4 wt.%) on the x-axis and separate lines for 500, 550, and 600 °C:

- (a) extruded density
- (b) mean equivalent grain diameter
- (c) Rockwell hardness
- (d) ultimate tensile strength
- (e) coefficient of friction
- (f) mass loss

The resulting non-parallel and crossover trends provide a direct visual representation of composition–temperature coupling across the 4 × 3 experimental matrix.

## Files

- `comment10_factor_comparison_data.csv` – current condition-level values used in the revised manuscript.
- `figure_comment10_comparative.py` – reproducible plotting script.

Running the script creates:

- `Fig_12_Comparative_Factor_Response.png` (600 dpi)
- `Fig_12_Comparative_Factor_Response.tiff` (600 dpi, LZW-compressed)
- `Fig_12_Comparative_Factor_Response.svg` (vector)

## Important revision note

The grain-size values currently reproduce the condition-average values obtained from the existing 100× single-field analysis used in the manuscript. The repository contains three 100× optical micrographs for each condition; if the planned multi-field grain-size reanalysis is adopted for the grain-analysis reviewer comments, update the grain-size column in the CSV and rerun this script before final submission.

The hardness values are the current condition means. Reviewer Comment 7 separately requests mean ± standard deviation from nine spatially separated hardness measurements. Once those replicate values are recovered, the hardness panel can be updated with error bars without changing the overall Comment 10 figure structure.
