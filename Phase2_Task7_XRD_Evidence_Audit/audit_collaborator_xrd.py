#!/usr/bin/env python3
"""Task 7: preliminary audit of collaborator XRD matrix, NOT raw-scan authentication.

Only source CSV from pinned main branch is analysed. This does NOT certify
the existence of original instrument scans or origin of tested material.
No unmeasured phase assignments, crystallite sizes, or refinement statistics.
"""
import csv, math, json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

ROOT=Path(__file__).resolve().parents[1]
IN=ROOT/"_xrd_main_source/XRD_analysis"
OUT=ROOT/"Phase2_Task7_XRD_Evidence_Audit/output"
EXPECTED=[
"Al-600","Al-550","Al-500",
"A4-600","A4-550","A4-500",
"A3-600","A3-550","A3-500",
"A2-600","A2-550","A2-500"]
LABELS={
"Al-500":("S01",0,500),"Al-550":("S02",0,550),"Al-600":("S03",0,600),
"A2-500":("S04",2,500),"A2-550":("S05",2,550),"A2-600":("S06",2,600),
"A3-500":("S07",3,500),"A3-550":("S08",3,550),"A3-600":("S09",3,600),
"A4-500":("S10",4,500),"A4-550":("S11",4,550),"A4-600":("S12",4,600)}
REF_PEAKS=[
("C002",26.54,(26.20,26.90)),
("Al111",38.47,(38.10,38.90)),
("Al200",44.73,(44.30,45.10)),
("Al220",65.10,(64.50,65.60)),
("Al311",78.22,(77.50,78.80)),
]
def mean_section(x,y,lo,hi):
    xx=(x>=lo-1e-8)&(x<=hi+1e-8)
    return float(np.mean(y[xx]))
def best_apex(x,y,range_):
    l,r=range_
    ix=np.where((x>=l)&(x<=r))[0]
    idx=ix[np.argmax(y[ix])]
    return float(x[idx]),float(y[idx])
def savecsv(path,rows):
    with path.open("w",newline="",encoding="utf-8") as f:
        wr=csv.DictWriter(f,fieldnames=list(rows[0]))
        wr.writeheader();wr.writerows(rows)
def main():
    OUT.mkdir(parents=True,exist_ok=True)
    path=IN/"Combined_Matrix_Data_revised.csv"
    with path.open(newline="",encoding="utf-8-sig") as f:
        lines=list(csv.reader(f))
    if lines[0] != ["2-theta"]+EXPECTED:
        raise ValueError("Unexpected 12 scan headers; do not silently remap")
    matrix=np.asarray([[float(z) for z in row] for row in lines[1:]],dtype=float)
    if matrix.shape!=(6001,13) or not np.isfinite(matrix).all():
        raise ValueError("Unexpected numeric scan matrix shape or missing values")
    x=matrix[:,0]; y=matrix[:,1:]
    if not np.allclose(x,np.linspace(20,80,6001),rtol=0,atol=1e-8):
        raise ValueError("Angular grid differs from expected 20-80 at 0.01 degrees")
    if np.any(y<0) or np.any(np.abs(y-np.rint(y))>1e-8):
        raise ValueError("Unexpected negative or noninteger intensities")
    info=(IN/"Info.txt").read_text(encoding="utf-8")
    summary=[];apices=[]; derived={}
    for j,name in enumerate(EXPECTED):
        counts=y[:,j]
        sid,wt,temp=LABELS[name]
        peaks={}
        for label,target,rng in REF_PEAKS:
            pos,amp=best_apex(x,counts,rng)
            peaks[label]=(pos,amp)
            apices.append({
                "Column":name,"Condition":sid,"GNP_wt_pct":wt,
                "Sintering_C":temp,"Window":label,
                "Reference_2theta_deg":target,"Recorded_peak_maximum_deg":pos,
                "Recorded_peak_maximum_counts":amp,
                "Is_verified_crystallographic_phase_assignment":False})
        bgc=0.5*(mean_section(x,counts,25.0,25.5)+mean_section(x,counts,27.5,28.0))
        bga=0.5*(mean_section(x,counts,37.1,37.4)+mean_section(x,counts,39.5,39.8))
        corrected_c=max(0,peaks["C002"][1]-bgc)
        corrected_al=peaks["Al111"][1]-bga
        summ={
            "Source_Column":name,"Working_Condition":sid,"GNP_wt_pct":wt,
            "Sinter_C":temp,"2theta_first":float(x[0]),
            "2theta_last":float(x[-1]),"Points":len(x),
            "Intensity_Mean":round(float(counts.mean()),5),
            "Intensity_Min":int(np.min(counts)),
            "Intensity_Max":int(np.max(counts)),
            "Overall_Maximum_2theta":float(x[np.argmax(counts)]),
            "C002_window_peak_2theta":peaks["C002"][0],
            "C002_window_apex_counts":peaks["C002"][1],
            "C002_flanking_baseline_counts":round(bgc,3),
            "C002_apex_minus_baseline_counts":round(corrected_c,3),
            "Al111_window_peak_2theta":peaks["Al111"][0],
            "Al111_window_apex_counts":peaks["Al111"][1],
            "Al111_flanking_baseline_counts":round(bga,3),
            "C002_to_Al111_APEX_RATIO_NOT_PHASE_FRACTION":
               round(corrected_c/corrected_al,6),
            "Authentic_Native_Instrument_Scan_Verified":False,
            "Measured_PreOrPostExtrusion_Verified":False
        }
        summary.append(summ)
        derived[name]=summ
    savecsv(OUT/"12condition_preliminary_peak_windows.csv",summary)
    savecsv(OUT/"12condition_all_peak_windows.csv",apices)
    # Actual supplied intensity profiles shown UNMODIFIED, only vertical
    # offset for legibility. No baseline subtraction or synthetic spectrum.
    for zoom,lim,file in [
        ("full",(20,80),"PRELIMINARY_12_XRD_patterns.png"),
        ("graphite window",(24.5,29.0),"PRELIMINARY_graphite_002_region.png")]:
        fig,axs=plt.subplots(3,1,figsize=(11,9),sharex=True)
        for row,temp in enumerate([500,550,600]):
            ax=axs[row]
            for j,wt in enumerate([0,2,3,4]):
                name=f"Al-{temp}" if wt==0 else f"A{wt}-{temp}"
                c=y[:,EXPECTED.index(name)]
                ax.plot(x,c,linewidth=0.95,label=f"{wt} wt.% GNP")
            ax.set_xlim(*lim)
            ax.set_ylabel("Recorded intensity")
            ax.set_title(f"Sintering {temp} °C — source records, not instrument-certified")
            ax.legend(loc="upper right",fontsize=8,ncol=4)
        axs[-1].set_xlabel("2θ (degrees)")
        fig.suptitle("Collaborator-supplied XRD matrix | preliminary source verification required",fontsize=12)
        fig.tight_layout(rect=(0,0,1,.96))
        fig.savefig(OUT/file,dpi=175,bbox_inches="tight")
        plt.close(fig)
    # No inferential comparison: one profile per putative condition.
    fig,ax=plt.subplots(figsize=(8,4.8))
    for temp in [500,550,600]:
        subset=sorted((r for r in summary if r["Sinter_C"]==temp),key=lambda r:r["GNP_wt_pct"])
        ax.plot([r["GNP_wt_pct"] for r in subset],
                [r["C002_to_Al111_APEX_RATIO_NOT_PHASE_FRACTION"] for r in subset],
                marker="o",label=f"{temp} °C")
    ax.set_xlabel("Nominal GNP loading (wt.%)")
    ax.set_ylabel("C(002)-window / Al(111)-window baseline-adjusted peak-height ratio")
    ax.set_xticks([0,2,3,4])
    ax.legend()
    ax.set_title("Exploratory peak-height comparison (NOT phase fraction)")
    fig.tight_layout()
    fig.savefig(OUT/"PRELIMINARY_002_to_Al111_peak_ratio.png",dpi=180)
    plt.close(fig)
    status={
      "pinned_main_source_sha":"1e03a978fbdaf6eecd8517707a86020291678af1",
      "matrix_source_git_blob_sha":"bbea94803dee30d3af4c0b20c504d73c37a06ae2",
      "info_source_git_blob_sha":"b600a82196210fd5a6999b518f717b793a4b2d80",
      "source_matrix":"XRD_analysis/Combined_Matrix_Data_revised.csv",
      "points_per_pattern":6001,"patterns":12,"grid_start":20,
      "grid_end":80,"angular_step":0.01,
      "no_missing_numbers":True,
      "source_integer_counts":True,
      "source_attribution":"User says received from collaborator; ORIGINAL NATIVE INSTRUMENT FILES NOT YET PROVIDED",
      "metadata_inconsistencies":[
        "Info.txt reports 40mA while v8.4 reports 20mA",
        "Info.txt says flat pressed powder while manuscript discusses hot-extruded samples",
        "Info.txt says Ar or vacuum to be supplied",
        "Info.txt phase databases listed as alternatives",
        "Info.txt refinement R-factors blank/ellipsis",
        "Info.txt 0.01deg step x 1s implies 0.6deg/min, while 1.0deg/min declared",
        "Earlier experiment record reported one 4wt% XRD scan vs supplied 12-condition matrix"
      ],
      "final_phase_identification_proven":False,
      "no_fabrication_claim_or_forgery_inference_from_mismatch":True,
      "no_quantitative_al4c3_detection_limit_estimated":True}
    (OUT/"source_authentication_and_scan_QA.json").write_text(
        json.dumps(status,indent=2,ensure_ascii=False),encoding="utf-8")
    lines=[
       "# Task 7 — New 12-column XRD matrix: preliminary numeric audit",
       "",
       "**HOLD for manuscript insertion until ORIGINAL INSTRUMENT SOURCE and SPECIMEN PROVENANCE are authenticated.**",
       "",
       "## What was actually checked",
       "",
       "- Pin user-supplied main-branch repository commit and keep native combined CSV unmodified.",
       "- CSV has 12 labelled intensity series × 6001 rows, 2θ 20.00°–80.00° at 0.01° intervals; all intensity values finite, nonnegative integers.",
       "- One labelled pattern per combination of GNP 0/2/3/4wt% and sinter 500/550/600°C; archived S01–S12 mapping is listed in table below.",
       "- Prominent peaks at 38.47–38.48°, 44.71–44.73°, 65.08–65.10°, 78.22–78.24° are consistent with expected fcc Al reflection windows. These are **tentative position comparisons, not certified phase identification**.",
       "- A feature near 26.5° grows with nominal GNP loading in the supplied matrix. The ratio is a baseline-adjusted **peak-height proxy**, not a graphite fraction, phase content, or demonstration of reinforcement survival.",
       "- No independent instrumental resolution standard, replicate scans, peak-profile deconvolution, Rietveld output, 2θ calibration standard or Al4C3 detection-limit analysis is available.",
       "",
       "| Source label | Working ID | GNP wt.% | Sinter °C | Al(111) apex ° | C(002)-window apex ° | Window peak-height ratio¹ |",
       "|---|---|---:|---:|---:|---:|---:|"]
    for r in sorted(summary,key=lambda z:(z["GNP_wt_pct"],z["Sinter_C"])):
        lines.append(
         f'| {r["Source_Column"]} | {r["Working_Condition"]} | {r["GNP_wt_pct"]} | {r["Sinter_C"]} | '
         f'{r["Al111_window_peak_2theta"]:.2f} | {r["C002_window_peak_2theta"]:.2f} | '
         f'{r["C002_to_Al111_APEX_RATIO_NOT_PHASE_FRACTION"]:.3f} |')
    lines+=["",
       "¹ C(002) window 26.20–26.90° apex after averaging local flanks 25.0–25.5° and 27.5–28.0°, divided by similarly background-adjusted Al(111) apex. **Exploratory descriptive metric only.**",
       "",
       "## Inconsistencies and authentication gates",
       "",
       "| Question | New Info.txt | Existing manuscript v8.4 | Required clarification |",
       "|---|---|---|---|",
       "| Scan count | 12 sample IDs | One representative 4wt% scan; remaining scans described as not acquired | Original date-stamped native Bruker files or signed acquisition history for all twelve |",
       "| Current | 40 mA | 20 mA | Bruker instrument metadata / original run method |",
       "| Sample stage | Flat pressed powder | Sintered and subsequently hot-extruded specimen study | Were scans on precursor pressed powder, sintered preforms, or final extrudates? Which stage for each? |",
       "| Sintering atmosphere | 'Ar or vacuum (to be supplied)' | Actual processing route must be described accurately | Collaborator confirms actual atmosphere and source sample batch |",
       "| Speed and step | 0.01° /1s, plus '1.0°/min' | 0.01° /1s | Different continuous-vs-step interpretation or corrected acquisition method |",
       "| Refinement | Rwp, Rp and χ² unspecified | None demonstrated | Supply raw GSAS-II project and refinement outputs if claimed |",
       "",
       "The 'Info.txt' includes candidate phase databases (ICDD/COD/ICSD) and prefilled lattice/crystallite/microstrain values, but lacks actual fitted residuals and phase-identification outputs. **Those listed values are not demonstrated as measured results.**",
       "",
       "## Recommended collaborator return package",
       "",
       "- One original instrument acquisition file per sample, e.g. Bruker .brml/.raw/.uxd (or signed documented alternate instrument export), unmodified and linked to the label.",
       "- Original experiment acquisition dates, Bruker D8 method screenshot/export, scan current and scan time, sample holder/reference calibration.",
       "- Specimen history map showing whether each was taken from sintered green preform, pressed powder or final hot-extruded material; source batch/sample IDs.",
       "- Confirm whether the 'Combined_Matrix_Data_revised.csv' represents original detector counts, corrected/rebinned intensities, background-subtracted data, simulated/predicted intensities or another reconstructed dataset.",
       "- If they claim refined phases, original GSAS-II project, reference patterns, fitted residual and numeric Rwp/Rp/χ².",
       "",
       "## Journal decision",
       "",
       "**If all twelve profiles are verifiably measured from the relevant specimens**, the availability materially changes the prior XRD limitation and supports a properly qualified composition–temperature comparison. If they are illustrative, simulated, derived from fewer real scans, or measured from a different process stage, they must not be submitted as the twelve measured final-composite XRD patterns.",
       "",
       "The current revision v8.4 is **not changed** by this audit. The existing single-scan limitations should be revised only after specimen and acquisition authenticity have been established.",
       "",
       "## Diagnostic outputs",
       "",
       "- 12condition_preliminary_peak_windows.csv",
       "- 12condition_all_peak_windows.csv",
       "- PRELIMINARY_12_XRD_patterns.png",
       "- PRELIMINARY_graphite_002_region.png",
       "- PRELIMINARY_002_to_Al111_peak_ratio.png",
       "- source_authentication_and_scan_QA.json",
       ""]
    (OUT/"TASK7_XRD_PRELIMINARY_AUDIT.md").write_text(
        "\n".join(lines),encoding="utf-8")
    print("PASS: collaborator matrix numerical check; HOLD: original instrument scan authenticity unresolved.")
if __name__=="__main__":main()
