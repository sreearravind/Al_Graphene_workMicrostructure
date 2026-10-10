#!/usr/bin/env python3
"""Task 2: non-destructive screening of existing optical segmentation output.

Automated metrics and contact sheets are QA aids, NOT validated grain boundaries.
S10-12 historical TIFF indices are remapped to original BMP processing folders.
"""
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw
import math
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
OUT=Path(__file__).resolve().parent/'output'
BMP=ROOT/'Optical miscrostructure_Figures_BMP file'
TIFF=ROOT/'Optical microstructure'
HIST=ROOT/'Caluculaions'/'100x_report'
MF=ROOT/'Revision_Comments_3_4_5'/'output'
OLD_TO_WORK={**{i:i for i in range(1,10)},10:12,11:10,12:11}
WORK_TO_OLD={v:k for k,v in OLD_TO_WORK.items()}
CONDS={1:(0,500,'0-500 - Copy'),2:(0,550,'0-550 - Copy'),
3:(0,600,'0-600 - Copy'),4:(2,500,'2-500 - Copy'),
5:(2,550,'2-550 - Copy'),6:(2,600,'2-600 - Copy'),
7:(3,500,'3.500 - Copy'),8:(3,550,'3-550 - Copy'),
9:(3,600,'3-600 - Copy'),10:(4,500,'4-500 - Copy'),
11:(4,550,'4-550 - Copy'),12:(4,600,'4.600 - Copy')}
SCALE=0.473;MIN_AREA=500;FRAME_AREA=1600*1200
MIN_ECD=SCALE*math.sqrt(4*MIN_AREA/math.pi)

def thumb(path,w,h):
    with Image.open(path) as im:
        return ImageOps.fit(im.convert('RGB'),(w,h),method=Image.Resampling.LANCZOS)

def source_sheet(fields):
    picks=[(2,1),(2,3),(3,1),(3,3),(6,1),(6,2),(6,3),
           (9,1),(9,2),(9,3),(10,1),(11,1),(12,1)]
    w,h,pad=435,313,33;cols=3
    sheet=Image.new('RGB',(w*cols,(h+pad)*math.ceil(len(picks)/cols)),'white')
    for k,(n,fi) in enumerate(picks):
        p=BMP/CONDS[n][2]/f'100x{fi}.bmp'
        x=k%cols*w;y=k//cols*(h+pad)
        sheet.paste(thumb(p,w,h),(x,y))
        record=fields[(fields.Working_Num==n)&(fields.Field==fi)].iloc[0]
        d=ImageDraw.Draw(sheet)
        d.text((x+5,y+h+8),f'S{n}, field {fi}: n={record.Grain_Count}, mean ECD={record.Mean_ECD_um:.1f} um',fill='black')
    sheet.save(OUT/'anomalous_100x_fields.jpg',quality=88,optimize=True)

def overlay_sheet():
    nums=[2,3,5,6,9,10,11,12];w,h,pad=520,390,37
    canvas=Image.new('RGB',(2*w,len(nums)*(h+pad)),'white')
    for i,n in enumerate(nums):
        old=WORK_TO_OLD[n]
        src=BMP/CONDS[n][2]/'100x1.bmp'
        overlay=HIST/f'Sample_{old}_overlay.png'
        yy=i*(h+pad)
        canvas.paste(thumb(src,w,h),(0,yy))
        canvas.paste(thumb(overlay,w,h),(w,yy))
        d=ImageDraw.Draw(canvas)
        d.text((8,yy+h+7),f'Working S{n} original BMP (100x, field 1)',fill='black')
        d.text((w+8,yy+h+7),f'Historical TIFF S{old} stored overlay',fill='black')
    canvas.save(OUT/'overlay_review_first_fields.jpg',quality=87,optimize=True)
    # Smaller 4-condition groups are accessible for visual review.
    for j in range(2):
        section=canvas.crop((0,j*4*(h+pad),2*w,(j+1)*4*(h+pad)))
        section.save(OUT/f'overlay_review_group_{j+1}.jpg',quality=72,optimize=True)

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    ff=pd.read_csv(MF/'field_level_summary_100x.csv')
    gg=pd.read_csv(MF/'grain_level_multifield_100x.csv',low_memory=False)
    print('Grain table:',len(gg),'rows. Columns:',list(gg.columns))
    expected={'Sample','Field','area_px','solidity','aspect_ratio',
              'roundness','equivalent_diameter_um'}
    if not expected.issubset(gg.columns):
        raise KeyError(f'Missing grain metadata: {expected-set(gg.columns)}')
    out=[]
    for _,f in ff.iterrows():
        old=int(f.Sample_Number);working=OLD_TO_WORK[old]
        g=gg[(gg.Sample==f'S{old}') & (gg.Field==int(f.Field))]
        if len(g)!=int(f.Grain_Count):
            raise ValueError(f'CSV field count differs for TIFF S{old} field {f.Field}')
        d=g.equivalent_diameter_um.astype(float)
        area=g.area_px.astype(float)
        sol=g.solidity.astype(float);roundness=g.roundness.astype(float)
        ar=g.aspect_ratio.astype(float)
        wt,temp,folder=CONDS[working]
        flags=[]
        if len(g)<30:flags.append('LOW_REGION_COUNT')
        if d.mean()>80:flags.append('VERY_LARGE_MEAN_ECD')
        if area.max()>0.1*FRAME_AREA:flags.append('LARGE_MERGED_REGION_CANDIDATE')
        if (sol<0.6).mean()>0.25:flags.append('MANY_IRREGULAR_REGIONS')
        if (roundness<0.2).mean()>0.25:flags.append('MANY_LOW_ROUNDNESS_REGIONS')
        if (ar>4).mean()>0.1:flags.append('MANY_ELONGATED_REGIONS')
        out.append({
         'Working_Sample':f'S{working}','Working_Num':working,
         'GNP_wt_pct':wt,'Temperature_C':temp,'Original_BMP_Folder':folder,
         'Historical_TIFF_Sample':f'S{old}','Field':int(f.Field),
         'BMP_Path':str((BMP/folder/f.Image_File.replace('.tiff','.bmp')).relative_to(ROOT)),
         'TIFF_Path':str((TIFF/'100 x'/str(old)/f.Image_File).relative_to(ROOT)),
         'Grain_Count':len(g),'Mean_ECD_um':d.mean(),'Median_ECD_um':d.median(),
         'Max_ECD_um':d.max(),'Sum_Region_Area_fraction':area.sum()/FRAME_AREA,
         'Largest_Region_Area_fraction':area.max()/FRAME_AREA,
         'Fraction_Solidity_lt_060':(sol<0.6).mean(),
         'Fraction_Roundness_lt_020':(roundness<0.2).mean(),
         'Fraction_Aspect_Ratio_gt_4':(ar>4).mean(),
         'Fraction_ECD_gt_100um':(d>100).mean(),
         'Heuristic_Flags':';'.join(flags)})
    fields=pd.DataFrame(out).sort_values(['Working_Num','Field'])
    fields.to_csv(OUT/'per_field_morphology_QA.csv',index=False)
    srows=[]
    for n,sub in fields.groupby('Working_Num'):
        counts=sub.Grain_Count;means=sub.Mean_ECD_um
        cv=100*means.std(ddof=1)/means.mean()
        ratio=counts.max()/counts.min()
        high=ratio>=4 or (counts.min()<30 and cv>25)
        srows.append({
          'Working_Sample':f'S{n}','Working_Num':n,
          'Historical_TIFF_Sample':sub.Historical_TIFF_Sample.iloc[0],
          'GNP_wt_pct':sub.GNP_wt_pct.iloc[0],
          'Temperature_C':sub.Temperature_C.iloc[0],
          'Field_Counts':';'.join(str(int(v)) for v in counts),
          'Max_to_Min_Count_Ratio':ratio,'Mean_Field_ECD_um':means.mean(),
          'Field_ECD_CV_pct':cv,
          'Flagged_Fields':int((sub.Heuristic_Flags.fillna('')!='').sum()),
          'Review_Priority':'HIGH' if high else 'STANDARD'})
    ss=pd.DataFrame(srows).sort_values('Working_Num')
    ss.to_csv(OUT/'sample_level_segmentation_QA.csv',index=False)
    source_sheet(fields);overlay_sheet()
    lines=['# Task 2: Screening of existing optical segmentation', '',
      '**Status:** Automated metric QA and image montages completed. No expert tracing verification performed yet.',
      '',
      '## Researcher-reported ImageJ calibration',
      '',
      '100x optical calibration 0.473 um/pixel, reportedly obtained using an ImageJ ruler reference on the same microscope.',
      f'Existing minimum threshold {MIN_AREA} pixels corresponds to an ECD of {MIN_ECD:.2f} um.',
      'The original ImageJ ruler/reference image and pixel-reference measurement have not yet been archived for independent reproduction.',
      '',
      '## Field-level screening (original BMP condition labels)',
      '',
      '| Working sample | Historical TIFF | Detected region counts (3 fields) | Count max/min | Field-mean ECD CV | Priority |',
      '|---|---|---|---:|---:|---|']
    for _,r in ss.iterrows():
        lines.append(f'| {r.Working_Sample} | {r.Historical_TIFF_Sample} | {r.Field_Counts} | {r.Max_to_Min_Count_Ratio:.2f} | {r.Field_ECD_CV_pct:.1f}% | {r.Review_Priority} |')
    lines+=['','## Important scientific limitations','',
      '- Automated segmented objects are not necessarily crystallographic grains. Etching contrasts, scratches and clustering can form false or merged objects.',
      '- The morphology flags and unusual count ratios are only quality-control prompts, not automatic data exclusion rules.',
      '- The 500-pixel minimum excludes any segmented feature with ECD less than 11.93 um. This truncation may bias size distributions.',
      '- Existing outputs are reassociated to the researcher-confirmed BMP condition labels for audit only: old TIFF S10 -> working S12; old TIFF S11 -> working S10; old TIFF S12 -> working S11.',
      '- Image fields are nested measurements within a condition. Three images do not establish three independently fabricated specimen replicates.',
      '- The original images and historical quantitative calculations remain untouched.',
      '',
      '## QA outputs','',
      '- per_field_morphology_QA.csv (includes cross-label traceability and morphology flag metrics)',
      '- sample_level_segmentation_QA.csv (condition-level screening)',
      '- anomalous_100x_fields.jpg (source-image context)',
      '- overlay_review_group_1.jpg / overlay_review_group_2.jpg (source BMP vs first-field saved overlay; accessible review groups)',
      '',
      '**Next before publication:** Visual classification of actual grain boundaries and quantitative manual-vs-automatic agreement on selected source fields; assess segmentation thresholds and retain full audit trail.']
    (OUT/'TASK2_QA_SCREENING.md').write_text('\n'.join(lines),encoding='utf-8')
    print('HIGH priority:',ss.loc[ss.Review_Priority=='HIGH','Working_Sample'].tolist())
if __name__=='__main__':main()
