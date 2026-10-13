#!/usr/bin/env python3
"""Phase 1 Task 6: 36-field optical image quality and segmentation reliability.
Researcher-confirmed 100x ImageJ scale 0.473 um/pixel; source-image labels
as original BMP folders. No field is excluded, no original is modified.
"""
from pathlib import Path
from hashlib import sha256
import math
import numpy as np
import pandas as pd
from PIL import Image,ImageOps,ImageDraw
from scipy import ndimage
from skimage.measure import shannon_entropy
from skimage.segmentation import find_boundaries
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from grainstat import GrainAnalyzer

ROOT=Path(__file__).resolve().parents[1]
OUT=Path(__file__).resolve().parent/"output"
BMP=ROOT/"Optical miscrostructure_Figures_BMP file"
TIFF=ROOT/"Optical microstructure/100 x"
HISTORY=ROOT/"Revision_Comments_3_4_5/output/field_level_summary_100x.csv"
CAL=0.473
W,H=1600,1200
CONDS={
1:(0,500,"0-500 - Copy"),2:(0,550,"0-550 - Copy"),3:(0,600,"0-600 - Copy"),
4:(2,500,"2-500 - Copy"),5:(2,550,"2-550 - Copy"),6:(2,600,"2-600 - Copy"),
7:(3,500,"3.500 - Copy"),8:(3,550,"3-550 - Copy"),9:(3,600,"3-600 - Copy"),
10:(4,500,"4-500 - Copy"),11:(4,550,"4-550 - Copy"),12:(4,600,"4.600 - Copy")}
OLD_TO_WORK={**{i:i for i in range(1,10)},10:12,11:10,12:11}
WORK_TO_OLD={v:k for k,v in OLD_TO_WORK.items()}
def digest(path):
    with Image.open(path) as im:
        if im.size!=(W,H):raise ValueError("Frame geometry mismatch: "+str(path))
        return sha256(im.convert("RGB").tobytes()).hexdigest()
def quality(path):
    with Image.open(path) as im:l=np.asarray(im.convert("L"),np.uint8)
    f=l.astype(np.float32)/255
    tile=np.asarray([float(f[y:y+300,x:x+400].mean()) for y in range(0,H,300) for x in range(0,W,400)])
    smoothed=ndimage.gaussian_filter(f,1)
    p5,p95=np.percentile(l,[5,95])
    return {
      "MeanGray":float(l.mean()),
      "StdGray":float(l.std()),
      "SpreadP95P05":float(p95-p5),
      "RMSContrast":float(f.std()/max(f.mean(),1e-6)),
      "EntropyBits":float(shannon_entropy(l,base=2)),
      "BlackFraction":float((l<=5).mean()),
      "WhiteFraction":float((l>=250).mean()),
      "TileMeanRangeGray":float((tile.max()-tile.min())*255),
      "TileMeanCV":float(tile.std()/max(tile.mean(),1e-6)),
      "TileMeanMinGray":float(tile.min()*255),
      "TileMeanMaxGray":float(tile.max()*255),
      "LaplacianVarianceSigma1":float(ndimage.laplace(smoothed).var())
    }
def segment(path,area=500,clahe=True):
    ga=GrainAnalyzer()
    if not clahe:
        ga.preprocessor.apply_filters=(
          lambda image,sigma=1.0:
          ga.preprocessor.gaussian_smooth(image,sigma) if sigma>0 else image.copy())
    result=ga.analyze(str(path),scale=CAL,min_area=area)
    acc={int(k):v for k,v in result["metrics"].items() if float(v["area_px"])>=area}
    ecd=np.asarray([float(v["equivalent_diameter_um"]) for v in acc.values()])
    area_values=np.asarray([float(v["area_px"]) for v in acc.values()])
    solid=np.asarray([float(v["solidity"]) for v in acc.values()])
    return ga,acc,{
     "count":len(ecd),
     "mean":float(ecd.mean()) if len(ecd) else np.nan,
     "median":float(np.median(ecd)) if len(ecd) else np.nan,
     "area_frac":float(area_values.sum()/(W*H)),
     "max_area_frac":float(area_values.max()/(W*H)) if len(area_values) else 0.0,
     "low_solidity":float((solid<0.6).mean()) if len(solid) else np.nan
    }
def sheet(cond,fields):
    wt,temp,_=CONDS[cond];w,h=480,360
    canvas=Image.new("RGB",(w*2,3*(h+53)),"white")
    d=ImageDraw.Draw(canvas)
    for idx,(source,labels,accepted,rec) in enumerate(fields):
        with Image.open(source) as im:orig=np.asarray(im.convert("RGB"))
        lab=labels.astype(np.int32).copy()
        lab[~np.isin(lab,np.asarray(list(accepted),dtype=np.int32))]=0
        edges=find_boundaries(lab,mode="inner")
        over=orig.copy();over[edges]=[255,0,0]
        for col,arr in enumerate((orig,over)):
            im=ImageOps.contain(Image.fromarray(arr),(w,h),Image.Resampling.LANCZOS)
            canvas.paste(im,(col*w+(w-im.width)//2,idx*(h+53)))
        y=idx*(h+53)+h+7
        d.text((7,y),f"S{cond:02d} ({wt}wt%, {temp}C) F{idx+1}: auto n={int(rec['Count500'])}, ECD={rec['MeanECD500']:.1f} um",fill="black")
        d.text((7,y+20),"Left: original BMP  Right: computed red boundaries (NOT verified grains)",fill="black")
    canvas.save(OUT/f"S{cond:02d}_BMP_vs_computed.jpg",quality=78,optimize=True)
def heat(df,metric,file,title):
    pivot=df.pivot(index="WorkingSample",columns="Field",values=metric)
    pivot=pivot.reindex([f"S{i:02d}" for i in range(1,13)])
    arr=pivot.to_numpy(float)
    fig,ax=plt.subplots(figsize=(7,6.3))
    im=ax.imshow(arr,aspect="auto",cmap="cividis")
    ax.set_xticks([0,1,2],["Field 1","Field 2","Field 3"])
    ax.set_yticks(list(range(12)),pivot.index)
    ax.set_title(title)
    for (j,i),v in np.ndenumerate(arr):
        ax.text(i,j,f"{v:.2f}" if abs(v)<10 else f"{v:.0f}",ha="center",va="center",fontsize=8,
                color="white" if v<np.nanpercentile(arr,20) else "black")
    fig.colorbar(im,ax=ax)
    fig.tight_layout();fig.savefig(OUT/file,dpi=140);plt.close(fig)
def main():
    OUT.mkdir(parents=True,exist_ok=True)
    h=pd.read_csv(HISTORY)
    rows=[]
    for n in range(1,13):
        wt,temp,folder=CONDS[n];old=WORK_TO_OLD[n];sheetdata=[]
        for field in [1,2,3]:
            b=BMP/folder/f"100x{field}.bmp"
            t=TIFF/str(old)/f"100x{field}.tiff"
            if digest(b)!=digest(t):raise ValueError(f"BMP/TIFF pixel mapping S{n} F{field}")
            historic=h[(h.Sample_Number==old)&(h.Field==field)]
            if len(historic)!=1:raise ValueError("Missing historical row")
            hist=historic.iloc[0]
            r={"WorkingSample":f"S{n:02d}","GNPwtPct":wt,
               "SinterC":temp,"Field":field,"BMP":str(b.relative_to(ROOT)),
               "HistoricalTIFF":str(t.relative_to(ROOT)),
               "RGBPixelMatch":True,"Calibration100x_um_per_px":CAL,
               **quality(b)}
            for area in [250,500,1000]:
                ga,objects,stats=segment(t,area,True)
                r[f"Count{area}"]=stats["count"]
                r[f"MeanECD{area}"]=stats["mean"]
                if area==500:
                    r["MaskCoverage500"]=stats["area_frac"]
                    r["MaxObjectFrac500"]=stats["max_area_frac"]
                    r["LowSolidityFrac500"]=stats["low_solidity"]
                    r["ArchivedCount"]=int(hist.Grain_Count)
                    r["ArchivedMeanECD"]=float(hist.Mean_ECD_um)
                    r["ReproducedCount"]=stats["count"]==int(hist.Grain_Count)
                    r["ReproducedECD"]=abs(stats["mean"]-float(hist.Mean_ECD_um))<=1e-6
                    main_ga=ga;main_objects=objects
            _,_,alt=segment(t,500,False)
            r["CountNoCLAHE"]=alt["count"];r["MeanECDNoCLAHE"]=alt["mean"]
            for area in [250,1000]:
                r[f"MeanECDchange_{area}_pct"]=100*(r[f"MeanECD{area}"]/r["MeanECD500"]-1)
                r[f"CountChange_{area}_pct"]=100*(r[f"Count{area}"]-r["Count500"])/max(r["Count500"],1)
            r["MeanECDchange_NoCLAHE_pct"]=100*(r["MeanECDNoCLAHE"]/r["MeanECD500"]-1)
            r["CountChange_NoCLAHE_pct"]=100*(r["CountNoCLAHE"]-r["Count500"])/max(r["Count500"],1)
            r["ActualMetallurgicalGrainBoundariesValidated"]=False
            rows.append(r)
            sheetdata.append((b,main_ga.labeled_image,main_objects,r))
            print(f"S{n:02d} F{field}: objects 500px={r['Count500']}, no CLAHE={r['CountNoCLAHE']}",flush=True)
        sheet(n,sheetdata)
    df=pd.DataFrame(rows).sort_values(["GNPwtPct","SinterC","Field"])
    df.to_csv(OUT/"all_36field_QA.csv",index=False)
    if not bool(df.ReproducedCount.all() and df.ReproducedECD.all()):
        raise AssertionError("Archived 500px baseline not reproduced for all 36 image fields")
    sums=[]
    for n in range(1,13):
        part=df[df.WorkingSample==f"S{n:02d}"]
        c=part.Count500.to_numpy(float);e=part.MeanECD500.to_numpy(float)
        ratio=float(c.max()/max(1,c.min()))
        cv=float(100*e.std(ddof=1)/e.mean())
        wt,temp,_=CONDS[n]
        sums.append({"WorkingSample":f"S{n:02d}","GNPwtPct":wt,
         "SinterC":temp,"FieldCount":3,
         "AutoObjectsTotal":int(c.sum()),
         "CountMin":int(c.min()),"CountMax":int(c.max()),
         "CountMaxMinRatio":ratio,
         "ECDmin_um":float(e.min()),"ECDmax_um":float(e.max()),"ECDFieldCVpct":cv,
         "MaxLargestObjectFrac":float(part.MaxObjectFrac500.max()),
         "MaxTileMeanRangeGray":float(part.TileMeanRangeGray.max()),
         "MaxAbsECDNoCLAHEchange":float(part.MeanECDchange_NoCLAHE_pct.abs().max()),
         "LargeFieldCountRatio_GE4":ratio>=4,
         "LargeFieldMeanECD_CV_GE25":cv>=25})
    sums=pd.DataFrame(sums)
    sums.to_csv(OUT/"all_12condition_QA_summary.csv",index=False)
    for metric,file,title in [
      ("Count500","heatmap_counts.png","Algorithm objects per optical field (not verified grains)"),
      ("MeanECD500","heatmap_ECD.png","Automated optical equivalent-diameter proxy (um)"),
      ("TileMeanRangeGray","heatmap_tile_grayscale.png","4x4 tile mean grayscale range (contrast/illumination proxy)"),
      ("MeanECDchange_NoCLAHE_pct","heatmap_CLAHE_effect.png","Change in automated mean ECD without CLAHE (%)")
    ]:heat(df,metric,file,title)
    corr=[]
    for x in ["RMSContrast","SpreadP95P05","TileMeanRangeGray","EntropyBits",
              "LaplacianVarianceSigma1","BlackFraction"]:
        for y in ["Count500","MeanECD500"]:
            corr.append({"QualityProxy":x,"SegmentMetric":y,
                "SpearmanRho":float(df[x].corr(df[y],method="spearman")),
                "Note":"Descriptive only; 36 nested fields, no independent specimen replication"})
    pd.DataFrame(corr).to_csv(OUT/"quality_segmentation_descriptive_spearman.csv",index=False)
    report=["# Task 6: optical image quality and segmentation reliability across all 12 conditions",
      "","**36 source BMP fields; no excluded or selected image fields. Computed boundary outlines are not physically verified crystallographic grains.**",
      "",
      "## Provenance and repeatability",
      "- All 36 original 100x BMPs matched the archived TIFFs exactly by decoded RGB pixels.",
      "- Original condition BMP labels used, with historical TIFF S10-S12 cyclic sample-folder discrepancy explicitly tracked.",
      "- Researcher-reported ImageJ ruler calibration for 100x: 0.473 um/pixel. Original ruler image is not available in the archive.",
      f"- Archived 500px segmentation counts independently reproduced in {int(df.ReproducedCount.sum())}/36 fields.",
      f"- Archived mean ECD independently reproduced within 1e-6 um in {int(df.ReproducedECD.sum())}/36 fields.",
      "- Each field rerun with GrainStat area thresholds 250, 500, 1000 pixels (Gaussian sigma=1, CLAHE on, Otsu, morphology radius=2, watershed).",
      "- Each field additionally rerun with CLAHE OFF at 500px, retaining all other GrainStat settings.",
      "",
      "## Variability of original 500px segmented-object measurements",
      "| Condition | GNP wt.% | Temp C | Automated object-count range | Count max/min | Field mean ECD range um | Field ECD CV % | Count ratio >=4 |",
      "|---|---:|---:|---|---:|---|---:|---|"]
    for _,v in sums.iterrows():
        report.append(f"| {v.WorkingSample} | {int(v.GNPwtPct)} | {int(v.SinterC)} | "+
        f"{int(v.CountMin)}-{int(v.CountMax)} | {v.CountMaxMinRatio:.2f} | "+
        f"{v.ECDmin_um:.1f}-{v.ECDmax_um:.1f} | {v.ECDFieldCVpct:.1f} | "+
        ("yes" if v.LargeFieldCountRatio_GE4 else "no")+" |")
    report+=["","## Image quality descriptors and preprocessing sensitivity",
      "Grayscale range, 4x4 tile-mean range, contrast, entropy and Laplacian variance are image descriptors; their variation may arise from actual microstructural texture, illumination, or both. No objective focus calibration image is available and no proxy alone establishes the cause.",
      "",
      "| Quantity across 36 fields | Median | Minimum | Maximum |",
      "|---|---:|---:|---:|"]
    for key,label in [
      ("TileMeanRangeGray","Tile mean grayscale range (0-255)"),
      ("SpreadP95P05","P95-P05 grayscale spread"),
      ("RMSContrast","Relative RMS contrast"),
      ("LaplacianVarianceSigma1","Laplacian variance sigma=1"),
      ("MeanECDchange_250_pct","ECD shift 250px vs 500px (%)"),
      ("MeanECDchange_1000_pct","ECD shift 1000px vs 500px (%)"),
      ("MeanECDchange_NoCLAHE_pct","ECD shift no CLAHE (%)"),
      ("CountChange_NoCLAHE_pct","Count shift no CLAHE (%)")]:
        values=df[key]
        report.append(f"| {label} | {values.median():.3f} | {values.min():.3f} | {values.max():.3f} |")
    report+=["",
      f"- {int(sums.LargeFieldCountRatio_GE4.sum())}/12 conditions exhibit more than fourfold automated object-count variation across three 100x fields. This is a REVIEW FLAG, not a basis to remove images.",
      f"- Median absolute mean-ECD change without CLAHE: {df.MeanECDchange_NoCLAHE_pct.abs().median():.1f}%; maximum: {df.MeanECDchange_NoCLAHE_pct.abs().max():.1f}%.",
      f"- Median absolute mean-ECD change at 1000px versus 500px: {df.MeanECDchange_1000_pct.abs().median():.1f}%.",
      "",
      "## Evidence deliverables",
      "- all_36field_QA.csv: every original field, pixel provenance, image-quality proxies and segmentation sensitivities.",
      "- all_12condition_QA_summary.csv: every condition, nested-field count/ECD variability.",
      "- Sxx_BMP_vs_computed.jpg: 12 three-field source-versus-contour contact sheets.",
      "- heatmap_counts.png, heatmap_ECD.png, heatmap_tile_grayscale.png, heatmap_CLAHE_effect.png.",
      "- quality_segmentation_descriptive_spearman.csv: descriptive correlations only (no statistical p-values or causal inference).",
      "",
      "## Scientific publication guardrails",
      "- No original source files, manual ROI ZIPs, previously reported numeric dataset or manuscript changed; original user field choices are retained.",
      "- High within-condition field variation is compatible with true spatial heterogeneity OR inconsistent automated segmentation, illumination, etching and focus effects. The source alone does not establish a unique cause.",
      "- A repeatable algorithm can segment pores, etching networks and contrast patches rather than actual metallurgical grain boundaries.",
      "- Unless genuine grain boundaries are independently interpretable, report explicitly defined optically segmented feature sizes instead of crystallographically verified grain diameters. Do not claim EBSD, quantitative DRX, Hall-Petch strengthening or independently replicated materials responses.",
      "- User has confirmed that 12-condition XRD was never performed and no physical samples remain; optical processing cannot create those measurements.",
      "- Reviewer demand for validated physical grain-size distributions may remain unmet despite exhaustive optical QA.",
      ""]
    (OUT/"TASK6_AUDIT_REPORT.md").write_text("\n".join(report),encoding="utf-8")
    print("TASK6 COMPLETED: 36/36 source pairs, all standard 500px baselines, 4 methods per field",flush=True)
if __name__=="__main__":main()
