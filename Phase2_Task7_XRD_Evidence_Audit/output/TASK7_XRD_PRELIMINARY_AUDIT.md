# Task 7 — New 12-column XRD matrix: preliminary numeric audit

**HOLD for manuscript insertion until ORIGINAL INSTRUMENT SOURCE and SPECIMEN PROVENANCE are authenticated.**

## What was actually checked

- Pin user-supplied main-branch repository commit and keep native combined CSV unmodified.
- CSV has 12 labelled intensity series × 6001 rows, 2θ 20.00°–80.00° at 0.01° intervals; all intensity values finite, nonnegative integers.
- One labelled pattern per combination of GNP 0/2/3/4wt% and sinter 500/550/600°C; archived S01–S12 mapping is listed in table below.
- Prominent peaks at 38.47–38.48°, 44.71–44.73°, 65.08–65.10°, 78.22–78.24° are consistent with expected fcc Al reflection windows. These are **tentative position comparisons, not certified phase identification**.
- A feature near 26.5° grows with nominal GNP loading in the supplied matrix. The ratio is a baseline-adjusted **peak-height proxy**, not a graphite fraction, phase content, or demonstration of reinforcement survival.
- No independent instrumental resolution standard, replicate scans, peak-profile deconvolution, Rietveld output, 2θ calibration standard or Al4C3 detection-limit analysis is available.

| Source label | Working ID | GNP wt.% | Sinter °C | Al(111) apex ° | C(002)-window apex ° | Window peak-height ratio¹ |
|---|---|---:|---:|---:|---:|---:|
| Al-500 | S01 | 0 | 500 | 38.48 | 26.86 | 0.026 |
| Al-550 | S02 | 0 | 550 | 38.48 | 26.46 | 0.037 |
| Al-600 | S03 | 0 | 600 | 38.47 | 26.31 | 0.025 |
| A2-500 | S04 | 2 | 500 | 38.48 | 26.55 | 0.096 |
| A2-550 | S05 | 2 | 550 | 38.47 | 26.55 | 0.088 |
| A2-600 | S06 | 2 | 600 | 38.47 | 26.60 | 0.119 |
| A3-500 | S07 | 3 | 500 | 38.47 | 26.49 | 0.129 |
| A3-550 | S08 | 3 | 550 | 38.48 | 26.59 | 0.157 |
| A3-600 | S09 | 3 | 600 | 38.47 | 26.44 | 0.148 |
| A4-500 | S10 | 4 | 500 | 38.48 | 26.55 | 0.179 |
| A4-550 | S11 | 4 | 550 | 38.48 | 26.63 | 0.185 |
| A4-600 | S12 | 4 | 600 | 38.47 | 26.54 | 0.175 |

¹ C(002) window 26.20–26.90° apex after averaging local flanks 25.0–25.5° and 27.5–28.0°, divided by similarly background-adjusted Al(111) apex. **Exploratory descriptive metric only.**

## Inconsistencies and authentication gates

| Question | New Info.txt | Existing manuscript v8.4 | Required clarification |
|---|---|---|---|
| Scan count | 12 sample IDs | One representative 4wt% scan; remaining scans described as not acquired | Original date-stamped native Bruker files or signed acquisition history for all twelve |
| Current | 40 mA | 20 mA | Bruker instrument metadata / original run method |
| Sample stage | Flat pressed powder | Sintered and subsequently hot-extruded specimen study | Were scans on precursor pressed powder, sintered preforms, or final extrudates? Which stage for each? |
| Sintering atmosphere | 'Ar or vacuum (to be supplied)' | Actual processing route must be described accurately | Collaborator confirms actual atmosphere and source sample batch |
| Speed and step | 0.01° /1s, plus '1.0°/min' | 0.01° /1s | Different continuous-vs-step interpretation or corrected acquisition method |
| Refinement | Rwp, Rp and χ² unspecified | None demonstrated | Supply raw GSAS-II project and refinement outputs if claimed |

The 'Info.txt' includes candidate phase databases (ICDD/COD/ICSD) and prefilled lattice/crystallite/microstrain values, but lacks actual fitted residuals and phase-identification outputs. **Those listed values are not demonstrated as measured results.**

## Recommended collaborator return package

- One original instrument acquisition file per sample, e.g. Bruker .brml/.raw/.uxd (or signed documented alternate instrument export), unmodified and linked to the label.
- Original experiment acquisition dates, Bruker D8 method screenshot/export, scan current and scan time, sample holder/reference calibration.
- Specimen history map showing whether each was taken from sintered green preform, pressed powder or final hot-extruded material; source batch/sample IDs.
- Confirm whether the 'Combined_Matrix_Data_revised.csv' represents original detector counts, corrected/rebinned intensities, background-subtracted data, simulated/predicted intensities or another reconstructed dataset.
- If they claim refined phases, original GSAS-II project, reference patterns, fitted residual and numeric Rwp/Rp/χ².

## Journal decision

**If all twelve profiles are verifiably measured from the relevant specimens**, the availability materially changes the prior XRD limitation and supports a properly qualified composition–temperature comparison. If they are illustrative, simulated, derived from fewer real scans, or measured from a different process stage, they must not be submitted as the twelve measured final-composite XRD patterns.

The current revision v8.4 is **not changed** by this audit. The existing single-scan limitations should be revised only after specimen and acquisition authenticity have been established.

## Diagnostic outputs

- 12condition_preliminary_peak_windows.csv
- 12condition_all_peak_windows.csv
- PRELIMINARY_12_XRD_patterns.png
- PRELIMINARY_graphite_002_region.png
- PRELIMINARY_002_to_Al111_peak_ratio.png
- source_authentication_and_scan_QA.json
