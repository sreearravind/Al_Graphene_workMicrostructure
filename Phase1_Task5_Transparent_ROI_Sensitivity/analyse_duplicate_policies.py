#!/usr/bin/env python3
"""Task 5, non-cherry-picked sensitivity of three researcher ROI archives.

Exploratory, not crystallographic grain verification. Original ZIPs unmodified.
A duplicate-candidate rule based ONLY on human-human polygon overlap is fixed
before consulting segmentation agreement scores.
"""
from collections import defaultdict
from hashlib import sha256
from pathlib import Path
import math,sys
import numpy as np
import pandas as pd
from PIL import Image
from grainstat import GrainAnalyzer
from roifile import roiread

ROOT=Path(__file__).resolve().parents[1]
HERE=Path(__file__).resolve().parent
OUT=HERE/"output"
ROIS=ROOT/"Phase1_Task4_Expert_ROI_Validation/manual_rois"
SOURCE=ROOT/"Optical miscrostructure_Figures_BMP file/2-600 - Copy"
TIFF=ROOT/"Optical microstructure/100 x/6"
SCALE=0.473
MINIMUM_AREA=500
FIELDS=[1,2,3]
NEAR_DUPLICATE_OVERLAP_FRACTION=0.5
sys.path.insert(0,str(ROOT/"Phase1_Task4_Expert_ROI_Validation"))
from compare_manual_rois import mask_from_points,match_one,ALLOWED_ROIS

def image_hash(path):
    with Image.open(path) as im:
        if im.size!=(1600,1200):raise ValueError("Image geometry changed")
        return sha256(im.convert("RGB").tobytes()).hexdigest()

def get_human_rois(path):
    rr=roiread(path)
    if not isinstance(rr,list):rr=[rr]
    if not rr:raise ValueError("No human drawn ROI polygons")
    arr=[]
    for i,roi in enumerate(rr,1):
        if roi.roitype not in ALLOWED_ROIS:
            raise ValueError("Unsupported ROI type for manual grain polygon")
        arr.append((i,roi.name or "ROI_"+str(i),mask_from_points(roi.coordinates())))
    return arr

def overlapping_components(traces):
    n=len(traces)
    parent=list(range(n))
    def find(x):
        while parent[x]!=x:
            parent[x]=parent[parent[x]]
            x=parent[x]
        return x
    def union(a,b):
        aa,bb=find(a),find(b)
        if aa!=bb:parent[bb]=aa
    pairs=[]
    incidental=[]
    for i in range(n):
        mi=traces[i][2]; ai=int(mi.sum())
        for j in range(i+1,n):
            mj=traces[j][2]
            intersection=int(np.count_nonzero(mi & mj))
            if not intersection:continue
            proportion=intersection/min(ai,int(mj.sum()))
            item={"ROI_A":traces[i][0],"ROI_B":traces[j][0],
                  "Intersect_px":intersection,
                  "Intersect_fraction_smaller":proportion}
            if proportion>=NEAR_DUPLICATE_OVERLAP_FRACTION:
                union(i,j)
                pairs.append(item)
            else:incidental.append(item)
    groups=defaultdict(list)
    for i in range(n):groups[find(i)].append(i)
    return list(groups.values()),pairs,incidental

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    roi_records=[]
    field_records=[]
    duplicate_pairs=[]
    other_pairs=[]
    for field in FIELDS:
        archive=ROIS/("S06_F"+str(field)+".zip")
        bmp=SOURCE/("100x"+str(field)+".bmp")
        tif=TIFF/("100x"+str(field)+".tiff")
        if not archive.exists():raise FileNotFoundError(archive)
        if image_hash(bmp)!=image_hash(tif):
            raise ValueError("BMP/TIFF RGB mismatch F"+str(field))
        traced=get_human_rois(archive)
        components,pairs,minor=overlapping_components(traced)
        duplicate_pairs += [{"Field":field,**p} for p in pairs]
        other_pairs += [{"Field":field,**p} for p in minor]
        scenarios={
          "all_ROIs_including_duplicates":list(range(len(traced))),
          "first_traced_in_duplicate_group":sorted(min(c) for c in components),
          "last_traced_in_duplicate_group":sorted(max(c) for c in components)
        }
        ga=GrainAnalyzer()
        result=ga.analyze(str(tif),scale=SCALE,min_area=MINIMUM_AREA)
        automatic={int(key):int(value["area_px"])
             for key,value in result["metrics"].items()
             if int(value["area_px"])>=MINIMUM_AREA}
        auto_ecd=[SCALE*math.sqrt(4*area/math.pi) for area in automatic.values()]
        for policy,selected in scenarios.items():
            run=[]
            for idx in selected:
                ordinal,name,mask=traced[idx]
                match=match_one(mask,ga.labeled_image,automatic)
                rec={
                   "Specimen":"S06","Field":field,"Policy":policy,
                   "Source_BMP":str(bmp.relative_to(ROOT)),
                   "Source_ROI_ZIP":str(archive.relative_to(ROOT)),
                   "ROI_Ordinal":ordinal,"ROI_Name":name,
                   "Manual_ECD_um":SCALE*math.sqrt(4*int(mask.sum())/math.pi),
                   "Automatic_Label":match["Matched_Auto_Label"],
                   "Matched_Auto_ECD_um":match["Auto_ECD_um"],
                   "IoU":match["IoU"],"Dice":match["Dice"],
                   "Physical_Grain_Identity_Validated":False
                }
                run.append(rec)
                roi_records.append(rec)
            d=pd.DataFrame(run)
            found=d.Automatic_Label.replace("",np.nan).dropna().astype(int)
            field_records.append({
                "Specimen":"S06","Field":field,"Policy":policy,
                "All_Manual_ROIs":len(traced),
                "Manual_ROIs_Included":len(d),
                "Candidate_Duplicate_Groups":sum(len(c)>1 for c in components),
                "Auto_FullField_Retained_Objects":len(automatic),
                "Auto_FullField_Mean_ECD_um":float(np.mean(auto_ecd)),
                "Manual_Selected_Mean_ECD_um":float(d.Manual_ECD_um.mean()),
                "Matched_Auto_Mean_ECD_um":float(d.Matched_Auto_ECD_um.mean()),
                "Median_IoU":float(d.IoU.median()),
                "Mean_Dice":float(d.Dice.mean()),
                "ROI_IoU_ge_0p50":int(d.IoU.ge(.5).sum()),
                "ROI_IoU_ge_0p70":int(d.IoU.ge(.7).sum()),
                "Repeated_Matched_Auto_Labels":int(found.duplicated().sum()),
                "Unmatched_Manual_ROIs":int(d.Automatic_Label.eq("").sum()),
                "Human_Physical_Grain_Boundaries_Proven":False,
            })
        print("S06 F%d: %d manual; %d candidate duplicate pairs; independent-of-IoU subset %d"%(
            field,len(traced),len(pairs),len(scenarios["first_traced_in_duplicate_group"])),
            flush=True)
    allroi=pd.DataFrame(roi_records)
    summary=pd.DataFrame(field_records)
    allroi.to_csv(OUT/"all_selected_ROI_comparisons.csv",index=False)
    summary.to_csv(OUT/"S06_duplicate_policy_sensitivity.csv",index=False)
    cols=["Field","ROI_A","ROI_B","Intersect_px","Intersect_fraction_smaller"]
    pd.DataFrame(duplicate_pairs,columns=cols).to_csv(OUT/"duplicate_candidate_pairs.csv",index=False)
    pd.DataFrame(other_pairs,columns=cols).to_csv(OUT/"other_overlap_pairs.csv",index=False)
    report=["# Task 5: transparent human ROI duplicate policy sensitivity",
            "",
            "**Exploratory computational QA; not proof of actual metallurgical grains.**",
            "",
            "## Predefined rule independent of agreement",
            "",
            "- Preserve and audit all submitted manual ROIs.",
            "- A pair with 50% or more overlap of the smaller manual area is a possible duplicate tracing, independent of GrainStat output.",
            "- For sensitivity, evaluate retaining the first-drawn or last-drawn polygon per connected duplicate group. Report BOTH alternatives without selecting a preferred option by IoU.",
            "- All less overlapping human polygons remain included. Retain the all-ROI diagnostics to show the consequences of double-counting.",
            "- Reassess the chosen subset manually against visible physical boundaries before any publication claim.",
            "",
            "## Per-field results",
            "",
            "| Field | Policy | Manual ROIs | Duplicate groups | Median IoU | Mean Dice | IoU >=0.50 | Selected mean manual ECD um | Matched auto ECD um | Repeated auto labels |",
            "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for _,r in summary.iterrows():
        report.append("| F%d | %s | %d | %d | %.3f | %.3f | %d/%d | %.2f | %.2f | %d |"%(
          int(r.Field),r.Policy,int(r.Manual_ROIs_Included),int(r.Candidate_Duplicate_Groups),
          r.Median_IoU,r.Mean_Dice,int(r.ROI_IoU_ge_0p50),int(r.Manual_ROIs_Included),
          r.Manual_Selected_Mean_ECD_um,r.Matched_Auto_Mean_ECD_um,
          int(r.Repeated_Matched_Auto_Labels)))
    report+=["","## Full-image algorithmic results remain unchanged",
             "",
             "| Field | Retained automated objects | Full-field automated mean ECD um |",
             "|---|---:|---:|"]
    for field in FIELDS:
        r=summary[(summary.Field==field)&(summary.Policy=="first_traced_in_duplicate_group")].iloc[0]
        report.append("| F%d | %d | %.2f |"%(field,
                      int(r.Auto_FullField_Retained_Objects),r.Auto_FullField_Mean_ECD_um))
    report+=["","## Interpretation and scientific limitations",
             "",
             "- The selected hand-drawn feature distributions are nonrandom and do NOT estimate the full field grain-size distribution.",
             "- F2 undersegmentation (merged regions), F1/F3 segmentation of etching contrast, true heterogeneity, defects, and uneven light are possible explanations, not independently established facts.",
             "- Matching IoU is diagnostic only, not an inclusion criterion. Even close agreement between two masks does not establish physical grain identity.",
             "- No independent specimen replicates or EBSD support were added. Grain-size strengthening, DRX and quantitative grain/property mechanism claims remain unverified.",
             "- Where optical boundaries are ambiguous, use the qualified label optically segmented microstructural feature size, not validated grain diameter.",
             "",
             "## Data outputs",
             "- all_selected_ROI_comparisons.csv: all original manual selections plus two duplicate-handling scenarios.",
             "- S06_duplicate_policy_sensitivity.csv: each scenario for each 100x field.",
             "- duplicate_candidate_pairs.csv: geometry-determined duplicate candidates.",
             "- other_overlap_pairs.csv: all lesser overlaps.",
             "- Original human ROIs, source BMP/TIFF and manuscript were not altered.",
             ""]
    (OUT/"TASK5_REPORT.md").write_text("\n".join(report),encoding="utf-8")
    print("Task 5 complete; comparison diagnostics and candid limitations saved.")
if __name__=="__main__":
    main()
