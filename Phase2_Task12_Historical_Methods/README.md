# Phase 2 Task 12 — Thesis-based test-method recovery and clean manuscript v8.9

**User source:** `Mtech_main_Thesis_May2018_no title.pdf`, 2018, chiefly project-report printed pp. 38–42, with reinforced hardness details pp. 47–48, tensile results pp. 51–52 and tribological measurements p. 55.

**Local outputs (delivered as conversation DOCX attachments; no binary manuscript committed to repo):**
- `Manuscript_Al-GNP_Tribo_v8_9_Historical_Methods_Clean.docx` — separate, rendered **32-page** scientific manuscript using the v8.8 document as baseline.
- `Al_GNP_Phase2_Task12_MTech_Experimental_Method_Extract_and_Verification.docx` — detailed two-page primary-source method extraction and discrepancy assessment.

## Original thesis technical record

| Test | Source-derived details | Not actually specified |
|---|---|---|
| Rockwell hardness | ASTM E18; HRB; nine indents at different positions per sample in §4.2.1; historical Table 4.2 identifies **sintered reinforced specimens S4–S12** | Indenter specification, major/minor force and dwell, actual acquired instrument printouts; thesis does not list unreinforced S1–S3 HRB |
| Tensile | Twelve **extruded** specimens, ASTM standards (exact ASTM designation not given), yield strength, UTS and elongation; machined dog-bone photographs | Gauge length, actual speed/strain rate, crosshead/UTM model, original force-extension files |
| Dry pin-on-disc | Nominal load **20 N**, disc **300 rpm**, duration **25 min**, twelve conditions; wear loss with four-decimal Shimadzu balance | Counterface specs, track radius, measured sliding distance, instrument calibration; **normal load contradiction below** |
| XRD | Thesis §3.9 gives Cu Kα **40 kV/20 mA for a 4wt% GNP specimen** | XRD instrument make/model in thesis, full numerical parameters for twelve conditions; collaborator note separately attributes Bruker D8 Advance and includes a conflicting 40mA |

## Priority scientific inconsistencies

1. **Sintered-versus-extruded hardness stage:** original M.Tech report describes HRB on sintered samples, not assured post-extrusion hardness. v8.9 Methods/Results/Figure 5 explicitly distinguish reported sintered-state hardness from extruded density and tensile performance. Any correlation across different processing stages must remain descriptive.
2. **Wear-test applied load:** Methods printed p42 says **20 N**, results p55 says **20 kN**, but examples frictional-force/COF in table p55 produce ~**2 N**: S1 1.180878661/0.590628~1.999N, S5 0.757804878/0.378871~2.000N and S12 0.249986169/0.124834~2.003N. The cause is not demonstrated. v8.9 reports *nominal 20 N* source protocol with a concise study limitation. Author must verify original force unit or calibration, **do not silently convert to 2 N**.
3. **XRD current:** original thesis documents 20mA for a described 4wt% scan; later incomplete Info.txt suggests 40mA. The clean v8.9 manuscript gives Bruker D8 Advance/Cu Kα per newer note and the surviving numerical 20–80° grid, **does not claim either current** for twelve measurements.
4. **Tensile ASTM designation and Rockwell loading parameters:** absent from the original thesis; no standard values were invented.

## Word editing QA

- 46 text passages were rewritten to replace editorial note/author-facing process language with technical methods, figure captions and concise formal scientific limitations.
- **26 original media parts preserved bit-for-bit** and **two original tables** preserved.
- Verified no remaining statements about synthetic or generated diffraction profiles, no note about conflicting 20/40mA source metadata in paper, and no deferred response-letter/task language.
- Preserved original bibliography numbering and citations for later author Mendeley update.
- Rendered in LibreOffice to **32 pages** and visually reviewed pages and all figure/table layouts.
- Baseline v8.8 and historical original files unchanged.

**Status: clean journal-formatted v8.9 working manuscript, but not yet defensible as fully submission-ready until reported wear normal-load discrepancy and sintered/extruded hardness provenance are resolved.**