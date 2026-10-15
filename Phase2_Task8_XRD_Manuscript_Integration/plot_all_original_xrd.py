#!/usr/bin/env python3
"""Task 8: original twelve post-extrusion XRD exports, author attested.

Plots ORIGINAL 6001-point profiles as supplied, no peak synthesis,
baseline subtraction, smoothing, background manipulation or claimed
refinement. Historic native instrument files no longer retained.
"""
from pathlib import Path
import csv, json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/"_xrd_main_source/XRD_analysis/Combined_Matrix_Data_revised.csv"
OUT=Path(__file__).resolve().parent/"output"
LABEL=["Al-600","Al-550","Al-500","A4-600","A4-550","A4-500","A3-600","A3-550","A3-500","A2-600","A2-550","A2-500"]
def save_csv(path, rows):
    with path.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]))
        w.writeheader();w.writerows(rows)
def main():
    OUT.mkdir(exist_ok=True,parents=True)
    with SRC.open(encoding="utf-8-sig",newline="") as f:
        reader=csv.reader(f);head=next(reader)
        a=np.asarray([[float(z) for z in row] for row in reader])
    if head != ["2-theta"]+LABEL or a.shape!=(6001,13):
        raise ValueError("Unexpected source XRD matrix")
    x=a[:,0]
    if not np.allclose(x,np.linspace(20,80,6001),atol=1e-8):
        raise ValueError("Changed 2theta grid")
    if not np.isfinite(a).all():raise ValueError("Missing or non-finite measurements")
    mapdata={nm:a[:,i+1] for i,nm in enumerate(LABEL)}
    colors={0:"#29456c",2:"#db7a35",3:"#388d74",4:"#b84b65"}
    fig,axes=plt.subplots(3,1,figsize=(11.8,8.6),sharex=True,sharey=True)
    for row,temp in enumerate((500,550,600)):
        ax=axes[row]
        for wt in (0,2,3,4):
            nm=(f"Al-{temp}" if wt==0 else f"A{wt}-{temp}")
            ax.plot(x,mapdata[nm],label=f"{wt} wt.%",color=colors[wt],lw=.69,alpha=.9)
        ax.set_ylabel("Recorded intensity")
        ax.set_title(f"Prior sintering temperature: {temp} °C",loc="left")
        ax.grid(alpha=.13)
        ax.legend(ncol=4,fontsize=8,loc="upper right",frameon=False)
        for pos in (38.47,44.73,65.1,78.22):
            ax.axvline(pos,color="#7b7b7b",linestyle=":",linewidth=.45,alpha=.47)
    axes[-1].set_xlabel(r"Diffraction angle, 2θ (°)")
    axes[-1].set_xlim(20,80)
    fig.suptitle("12 individually tested post-extrusion specimens | historical XRD intensity exports",
                 fontsize=12)
    fig.tight_layout(rect=(0,0,1,.965))
    fig.savefig(OUT/"FIGURE4_TWELVE_XRD_EXPORTS.png",dpi=300,bbox_inches="tight")
    fig.savefig(OUT/"FIGURE4_TWELVE_XRD_EXPORTS.svg",bbox_inches="tight")
    plt.close(fig)
    fig,axes=plt.subplots(3,1,figsize=(10,7.4),sharex=True)
    for row,temp in enumerate((500,550,600)):
        ax=axes[row]
        for wt in (0,2,3,4):
            nm=f"Al-{temp}" if wt==0 else f"A{wt}-{temp}"
            ax.plot(x,mapdata[nm],color=colors[wt],lw=.7,label=f"{wt} wt.%")
        ax.set_xlim(24.6,28.8);ax.set_ylabel("Recorded intensity")
        ax.set_title(f"{temp} °C",loc="left")
        ax.legend(ncol=4,loc="upper right",fontsize=8,frameon=False)
    axes[-1].set_xlabel(r"Diffraction angle, 2θ (°)")
    fig.suptitle("Carbon-associated ~26.5° reflection window: measured-export comparison",fontsize=12)
    fig.tight_layout(rect=(0,0,1,.96))
    fig.savefig(OUT/"FIGURE4_CARBON_002_INSET.png",dpi=300,bbox_inches="tight")
    fig.savefig(OUT/"FIGURE4_CARBON_002_INSET.svg",bbox_inches="tight")
    plt.close(fig)
    # Window apex data: descriptive, not true phase quantification.
    windows={
     "Carbon_002_candidate":(26.2,26.9),
     "Al_111":(38.1,38.9),"Al_200":(44.3,45.1),
     "Al_220":(64.5,65.6),"Al_311":(77.5,78.8)}
    rows=[]
    for w in (0,2,3,4):
      for temp in (500,550,600):
        nm=f"Al-{temp}" if w==0 else f"A{w}-{temp}"
        y=mapdata[nm]
        sid=(temp-500)//50 + (1 if w==0 else ({2:4,3:7,4:10}[w]))
        rec={"XRD_original_export_col":nm,"Condition":f"S{sid:02d}",
            "GNP_wt_pct":w,"Prior_Sintering_C":temp,
            "Author_Test_Stage":"post-hot-extrusion",
            "Native_Instrument_File":"not retained before 2022"}
        for label,(lo,hi) in windows.items():
            sel=np.where((x>=lo)&(x<=hi))[0]
            p=sel[np.argmax(y[sel])]
            rec[f"{label}_apex_2theta"]=float(x[p])
            rec[f"{label}_apex_intensity"]=float(y[p])
        rows.append(rec)
    save_csv(OUT/"phase_window_indices_all_conditions.csv",rows)
    caption=(
"# Figure 4: twelve-condition historical experimental XRD export\n\n"
"**Researcher eyewitness provenance:** Twelve physically distinct samples were sectioned from final hot-extruded Al–GNP lengths and individually submitted for XRD. The surviving numerical matrix contains 6001 recorded intensity entries over 20°–80° in 2θ for each processing condition. The original native Bruker acquisition files were discarded under the laboratory's pre-2022 retention policy.\n\n"
"**Figure 4 caption (proposed):** 'Diffraction-intensity profiles from individually tested hot-extruded Al–GNP specimens with 0, 2, 3 and 4 wt.% GNP sintered at (a) 500 °C, (b) 550 °C and (c) 600 °C before extrusion. The curves reproduce the historical numerical intensity exports without background correction or smoothing. The main maxima are consistent with fcc Al reflections, and the higher intensity feature near 26.5° in reinforced conditions is compatible with carbon (002) stacking. Peak intensity is not used to calculate phase fractions. Original native instrument files are no longer retained.'\n\n"
"**What is NOT claimed:** No quantitative GNP phase fraction, graphene exfoliation, grain size, interface strengthening, Rietveld refinement, measured Al4C3 detection limit, or verified absence of interfacial reaction.\n\n"
"**Method metadata conflict:** prior manuscript stated tube current 20 mA, new collaborator's partly templated Info.txt 40 mA. Original instrument header is unavailable. Do not fill this gap with an assumed value. The old analyst file's 'flat pressed powder' note conflicts with author eyewitness samples from final extruded lengths. Clearly prioritize author-confirmed specimen provenance and disclose that original test notebook/method printout was not recovered.\n\n"
"**Publication limit:** author attestation supplies specimen history; full native-acquisition traceability remains limited by historical record retention. Treat exported intensity columns as the archived experimental dataset and provide the unchanged CSV in research data availability.\n")
    (OUT/"TASK8_XRD_FIGURE_CAPTION_AND_LIMITS.md").write_text(caption,encoding="utf-8")
    print("PASS: Full source 6001 × 12 intensity profiles plotted without modifying counts.")
if __name__=="__main__":
    main()
