# Phase 2 Task 7 — Original XRD measurement authentication checklist

**Purpose:** The user's collaborator supplied twelve XRD-like intensity profiles in `main/XRD_analysis/Combined_Matrix_Data_revised.csv` on 2026-10-15, alongside a partly specified `Info.txt`. This is important new documentary evidence but does **not by itself establish** that twelve independent instrument scans were acquired from the twelve final hot-extruded specimens.

## Source package — pinned and unchanged

- GitHub source commit: `1e03a978fbdaf6eecd8517707a86020291678af1`.
- CSV Git blob: `bbea94803dee30d3af4c0b20c504d73c37a06ae2`.
- Instrument info Git blob: `b600a82196210fd5a6999b518f717b793a4b2d80`.
- Twelve 2θ profiles, 6001 measurements each, 20.00–80.00° at 0.01°.
- The parent v8.4 manuscript was based on one representative 4 wt.% pattern (unknown sintering condition), with acquisition written as 40 kV, **20 mA** and no documented further scans; it must not be overwritten before origin is authenticated.

## Sample mapping from CSV (provisional until laboratory registry confirmation)

| Column | Working ID | GNP wt.% | Prior sintering, °C |
|---|---|---:|---:|
| Al-500 | S01 | 0 | 500 |
| Al-550 | S02 | 0 | 550 |
| Al-600 | S03 | 0 | 600 |
| A2-500 | S04 | 2 | 500 |
| A2-550 | S05 | 2 | 550 |
| A2-600 | S06 | 2 | 600 |
| A3-500 | S07 | 3 | 500 |
| A3-550 | S08 | 3 | 550 |
| A3-600 | S09 | 3 | 600 |
| A4-500 | S10 | 4 | 500 |
| A4-550 | S11 | 4 | 550 |
| A4-600 | S12 | 4 | 600 |

This XRD source naming is distinct from the **historical optical TIFF S10/S11/S12 label permutation**. Do not import that optical image crosswalk into source XRD, tensile, tribological or hardness specimen identifiers.

## Mandatory collaborator verification questions

1. Were there **twelve separate measured XRD acquisitions**? Are the twelve CSV intensity columns original instrument readings, corrected/rebinned scans, derived reconstructions, reference-model calculations, or simulated curves? If some are calculated, label them accurately and never call them experimentally measured XRD.
2. Supply each **original instrument file** (e.g., Bruker .brml, .raw or .uxd), its timestamp and unmodified method header. Preserve original files rather than regenerating them to match the CSV.
3. Provide acquisition-log mapping from the instrument sample name to **GNP fraction, 500/550/600°C prior sintering temperature, specimen batch and XRD acquisition date**.
4. Were the specimens **flat-pressed powder** as in `Info.txt`, sintered precursors, or **final hot-extruded composite** as implied by the mechanical-study manuscript? XRD results from a different processing stage cannot be described as phase characterization of final extruded samples without qualification.
5. Confirm original Bruker tube current (**20 mA in manuscript, 40 mA in Info.txt**), angle/time/speed recording convention (0.01° and 1s mathematically ~0.6°/min, distinct from 1°/min), sample rotation and ambient conditions.
6. Resolve `Info.txt` placeholders `Ar or vacuum (to be supplied)`, alternative phase databases, and blank `Rwp/Rp/χ²`. Do not present listed crystallite sizes/microstrain as fitted values without actual profiles/refinement.
7. Supply the native GSAS-II project `.gpx`, instrument broadening reference/standard, phase list and Rwp/Rp/χ² **only if** refinement was actually performed.
8. Identify which, if any, of the new scans corresponds to the one pattern previously used in manuscript Figure 4 and explain why the earlier manuscript stated the other eleven scans were unavailable.

## Evidence status and manuscript action

**HOLD** current v8.4 XRD methods, Figure 4, and phase discussion unchanged until the above primary-source provenance is established. The existing statement about single-scan coverage may need correction if twelve genuine historical scans are demonstrated; keep track of the revision transparently rather than silently replacing the experimental history.

A clear 26.5° feature in GNP samples is only **consistent with** graphite/graphene stacking. It does not prove GNP exfoliation, distribution or unchanged interface chemistry; absence of an easily resolved Al4C3 peak does not establish chemical nonreaction. There is no evidence here to support a new mechanistic phase-strengthening claim.

The workflow `.github/workflows/phase2_task7_xrd_preliminary_audit.yml` prepares **source-pinned, preliminary figures and per-spectrum tables**; these are *not manuscript-ready* until the collaborator confirms the source and specimen history.
