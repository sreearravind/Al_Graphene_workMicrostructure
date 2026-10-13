#!/usr/bin/env python3
"""Phase 1 Task 3: archived GrainStat reproducibility and 250/500/1000px sensitivity.
All contour lines are ALGORITHM OUTPUT, not expert validated grain boundaries.
"""
from pathlib import Path
import math, hashlib
import numpy as np
import pandas as pd
from PIL import Image, ImageDraw, ImageOps
from skimage.segmentation import find_boundaries
from grainstat import GrainAnalyzer

ROOT=Path(__file__).resolve().parents[1]
OUT=Path(__file__).resolve().parent/'output'
OUT.mkdir(parents=True,exist_ok=True)
BMP=ROOT/'Optical miscrostructure_Figures_BMP file'
TIFF=ROOT/'Optical microstructure/100 x'
PICKS=ROOT/'Phase1_Task2_Segmentation_QA/MANUAL_VALIDATION_TEMPLATE.csv'
HIST=ROOT/'Revision_Comments_3_4_5/output/field_level_summary_100x.csv'
SCALE=0.473
THRESHOLDS=(250,500,1000)
OLD_TO_WORK={**{i:i for i in range(1,10)},10:12,11:10,12:11}
WORK_TO_OLD={v:k for k,v in OLD_TO_WORK.items()}
VIEW={(2,1),(2,3),(3,3),(6,1),(6,2),(6,3),(9,2),(10,1),(11,1),(12,1)}
def rgb_hash(p):
    with Image.open(p) as im:
        return hashlib.sha256(im.convert('RGB').tobytes()).hexdigest()
def analyse(p,min_area):
    ga=GrainAnalyzer()
    result=ga.analyze(str(p),scale=SCALE,min_area=min_area)
    gr=pd.DataFrame.from_dict(result['metrics'],orient='index')
    if len(gr):
        gr=gr[gr.area_px>=min_area].copy()
    return ga,gr
def save_review(src,labels,ids,headline,dst):
    lab=labels.astype(np.int32,copy=True)
    lab[~np.isin(lab,list(ids))]=0
    edges=find_boundaries(lab,mode='inner')
    with Image.open(src) as im:
        arr=np.asarray(im.convert('RGB')).copy()
    annotated=arr.copy()
    annotated[edges]=[255,20,25]
    size=(480,360)
    source=ImageOps.contain(Image.fromarray(arr),size)
    outlined=ImageOps.contain(Image.fromarray(annotated),size)
    image=Image.new('RGB',(960,400),'white')
    image.paste(source,(0,0));image.paste(outlined,(480,0))
    pen=ImageDraw.Draw(image)
    pen.text((8,365),headline,fill='black')
    pen.text((8,382),'LEFT: source BMP      RIGHT: computed GrainStat region boundaries (NOT verified grains)',fill='black')
    image.save(dst,quality=86,optimize=True)
def main():
    picks=pd.read_csv(PICKS)
    master=pd.read_csv(HIST)
    results=[]
    for _,pr in picks.iterrows():
        work=int(str(pr.Working_sample)[1:]);old=WORK_TO_OLD[work]
        field=int(pr.Field)
        src=ROOT/str(pr.BMP_path)
        tif=TIFF/str(old)/('100x'+str(field)+'.tiff')
        if rgb_hash(src)!=rgb_hash(tif):
            raise ValueError('Unmatched BMP / TIFF for S%d field %d'%(work,field))
        hm=master[(master.Sample_Number==old)&(master.Field==field)]
        if len(hm)!=1:raise ValueError('No historical field row')
        historic=hm.iloc[0]
        for minimum in THRESHOLDS:
            ga,gr=analyse(tif,minimum)
            ecd=gr.equivalent_diameter_um.to_numpy(float)
            mean=float(ecd.mean()) if ecd.size else np.nan
            result={
              'Working_Sample':'S'+str(work),'Field':field,
              'Original_BMP':str(pr.BMP_path),
              'Historical_TIFF_Sample':'S'+str(old),
              'GNP_wt_pct':int(pr.GNP_wt_pct),'Sintering_Temperature_C':int(pr.Sinter_C),
              'Scale_um_per_pixel':SCALE,
              'Minimum_Area_px':minimum,
              'Minimum_Equivalent_Diameter_um':SCALE*math.sqrt(4*minimum/math.pi),
              'Region_Count':len(gr),
              'Mean_Equivalent_Diameter_um':mean,
              'Median_Equivalent_Diameter_um':float(np.median(ecd)) if len(ecd) else np.nan,
              'Accepted_Region_Area_Fraction':float(gr.area_px.sum())/(1600*1200),
              'Archived_500px_Region_Count':int(historic.Grain_Count),
              'Archived_500px_Mean_ECD_um':float(historic.Mean_ECD_um),
              'RGB_identical':True,'Human_grain_boundary_validated':False}
            results.append(result)
            if minimum==500 and (work,field) in VIEW:
                save_review(src,ga.labeled_image,gr.index,
                   'Working S%d F%d / TIFF S%d: n=%d, mean ECD=%.1f um'%(work,field,old,len(gr),mean),
                   OUT/('contours_S%02d_F%d.jpg'%(work,field)))
        print('Completed working S%d F%d from TIFF S%d'%(work,field,old),flush=True)
    df=pd.DataFrame(results)
    df.to_csv(OUT/'segmentation_sensitivity_19_fields.csv',index=False)
    baseline=df[df.Minimum_Area_px==500].copy()
    baseline['Region_Count_Delta']=baseline.Region_Count-baseline.Archived_500px_Region_Count
    baseline['ECD_Mean_Delta_um']=baseline.Mean_Equivalent_Diameter_um-baseline.Archived_500px_Mean_ECD_um
    baseline.to_csv(OUT/'archived_baseline_reproduction.csv',index=False)
    piv=df.pivot(index=['Working_Sample','Field'],columns='Minimum_Area_px',
                 values=['Region_Count','Mean_Equivalent_Diameter_um'])
    records=[]
    for (sample,field),block in df.groupby(['Working_Sample','Field'],sort=False):
        ref=block.loc[block.Minimum_Area_px==500].iloc[0]
        for _,v in block.iterrows():
            if v.Minimum_Area_px==500:continue
            records.append({'Working_Sample':sample,'Field':int(field),
             'Area_Threshold_px':int(v.Minimum_Area_px),
             'Regions_500px':int(ref.Region_Count),'Regions_Alternate':int(v.Region_Count),
             'Region_Count_Change_pct':100*(v.Region_Count-ref.Region_Count)/max(ref.Region_Count,1),
             'Mean_ECD_500px_um':ref.Mean_Equivalent_Diameter_um,
             'Mean_ECD_Alternate_um':v.Mean_Equivalent_Diameter_um,
             'Mean_ECD_Change_pct':100*(v.Mean_Equivalent_Diameter_um-ref.Mean_Equivalent_Diameter_um)/ref.Mean_Equivalent_Diameter_um})
    change=pd.DataFrame(records)
    change.to_csv(OUT/'threshold_change_relative_to_500.csv',index=False)
    exactly=(baseline.Region_Count_Delta==0).sum()
    means=(baseline.ECD_Mean_Delta_um.abs()<=1e-6).sum()
    lines=['# Phase 1 Task 3: controlled segmentation reproduction and threshold sensitivity',
      '', '**STATUS: completed computational QA, NOT manual / expert grain boundary validation.**',
      '', '## Input and provenance',
      '- 19 pre-registered optical fields, exactly pixel matched to original BMP images before analysing historical TIFF files.',
      '- Reproduces the original TIFF loading behavior of GrainStat (which differs from BMP loading).',
      '- Historical TIFF mapping preserved explicitly: TIFF S10 -> BMP S12; TIFF S11 -> BMP S10; TIFF S12 -> BMP S11.',
      '- Researcher-confirmed ImageJ reference-ruler calibration for 100x: 0.473 micrometres/pixel. Original reference image not archived.',
      '- GrainStat defaults: Gaussian sigma 1, CLAHE enabled, Otsu, morphology radius 2, watershed enabled; minimum area varied as shown.',
      '', '## Reproducibility of archived 500-pixel output',
      '- Exactly matching retained-region counts: **%d/19 fields**.'%exactly,
      '- Means matching archival mean ECD within 1e-6 micrometres: **%d/19 fields**.'%means,
      '', '| Working condition | Field | Archived count | Rerun count | Count delta | ECD mean delta (um) |',
      '|---|---:|---:|---:|---:|---:|']
    for _,v in baseline.iterrows():
        lines.append('| %s | %d | %d | %d | %+d | %+.3f |'%(
         v.Working_Sample,v.Field,v.Archived_500px_Region_Count,
         v.Region_Count,v.Region_Count_Delta,v.ECD_Mean_Delta_um))
    lines+=['','## True rerun threshold sensitivity',
     'Minimum area is applied both within GrainStat binary morphology before watershed and as a final region-area filter. These are true reruns of segmentation, not post-filtering old CSV rows.',
     '', '| Min area (px) | ECD cutoff (um) | Total retained regions | Median field mean ECD (um) |',
     '|---:|---:|---:|---:|']
    for minimum in THRESHOLDS:
        sub=df[df.Minimum_Area_px==minimum]
        lines.append('| %d | %.2f | %d | %.2f |'%(
          minimum,SCALE*math.sqrt(4*minimum/math.pi),int(sub.Region_Count.sum()),
          sub.Mean_Equivalent_Diameter_um.median()))
    lines+=['','| Alternative threshold | Median absolute mean-ECD shift from 500px | Max absolute shift |',
      '|---:|---:|---:|']
    for minimum in [250,1000]:
        sub=change[change.Area_Threshold_px==minimum]
        lines.append('| %d | %.1f%% | %.1f%% |'%(
          minimum,sub.Mean_ECD_Change_pct.abs().median(),sub.Mean_ECD_Change_pct.abs().max()))
    lines+=['','## Interpretation and expert validation gate',
      '- The red boundaries in the output review sheets are **actual computed object contours**, but not scientifically confirmed grain boundaries.',
      '- A stable computed contour under multiple thresholds is not proof of grain identity.',
      '- Manually trace suitable grain boundaries in ImageJ on the same selected fields or mark a field UNRESOLVABLE. Archive ROI and manually traced ECD results before claiming objective agreement.',
      '- Large dark networks may be etchant structures or merged regions; do not claim DRX fraction, Hall-Petch mechanism, or full experimental grain distribution from automated optical features alone.',
      '- The 500-pixel minimum excludes areas whose equivalent-circle diameter would be below 11.93 um.',
      '- No experimental file, archived grain-size value, mechanical/tribological measurement or manuscript content has been modified.',
      '', '## Files',
      '- segmentation_sensitivity_19_fields.csv: all runs and sample-identity crosswalk',
      '- archived_baseline_reproduction.csv: exact comparison to historical field results',
      '- threshold_change_relative_to_500.csv: field-level changes',
      '- contours_Sxx_Fy.jpg: expert review sheets for selected fields at 500 px',
      '']
    (OUT/'TASK3_QA_REPORT.md').write_text('\n'.join(lines),encoding='utf-8')
    print('DONE: %d/19 baseline counts exact, %d/19 baseline ECD means exact.'%(exactly,means),flush=True)
if __name__=='__main__':main()
