#!/usr/bin/env python3
"""Non-destructive Phase 1 Task 1 audit: BMP/TIFF identity and scale provenance.

Reports source counts, maps samples, compares decoded RGB pixels, records metadata,
flags duplicates and extra frames. Does not authenticate a micron-per-pixel scale
or validate any grain segmentation.
"""
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw
from collections import defaultdict, Counter
import csv, hashlib, json, re
from datetime import datetime, timezone

ROOT=Path(__file__).resolve().parents[1]
OUT=Path(__file__).resolve().parent/'output'
SRC=ROOT/'Optical miscrostructure_Figures_BMP file'
TIFF=ROOT/'Optical microstructure'
C=[
 (1,0,500,'0-500 - Copy'),(2,0,550,'0-550 - Copy'),
 (3,0,600,'0-600 - Copy'),(4,2,500,'2-500 - Copy'),
 (5,2,550,'2-550 - Copy'),(6,2,600,'2-600 - Copy'),
 (7,3,500,'3.500 - Copy'),(8,3,550,'3-550 - Copy'),
 (9,3,600,'3-600 - Copy'),(10,4,500,'4-500 - Copy'),
 (11,4,550,'4-550 - Copy'),(12,4,600,'4.600 - Copy')]
MAG=(100,200,400)
FILE_RE=re.compile(r'^(100|200|400)x(\d+)\.bmp$',re.I)

def inspect(p):
    with Image.open(p) as im:
        dims=im.size;mode=im.mode
        inf={str(k):str(v)[:120] for k,v in im.info.items()}
        if hasattr(im,'tag_v2'):
            for tag,name in [(270,'ImageDescription'),(282,'XResolution'),
                             (283,'YResolution'),(296,'ResolutionUnit'),
                             (305,'Software'),(306,'DateTime')]:
                v=im.tag_v2.get(tag)
                if v is not None:inf[name]=str(v)[:180]
        pixelhash=hashlib.sha256(im.convert('RGB').tobytes()).hexdigest()
    return dims,mode,inf,pixelhash

def make_sheet(mag):
    w,h=300,225
    sheet=Image.new('RGB',(w*4,(h+28)*3),'white')
    d=ImageDraw.Draw(sheet)
    for idx,(num,gnp,temp,folder) in enumerate(C):
        p=SRC/folder/f'{mag}x1.bmp'
        x=(idx%4)*w;y=(idx//4)*(h+28)
        if p.exists():
            with Image.open(p) as im:
                sheet.paste(ImageOps.fit(im.convert('RGB'),(w,h)),(x,y))
        d.text((x+5,y+h+5),f'S{num} | {gnp} wt% | {temp} C | {mag}x',fill='black')
    sheet.save(OUT/f'contact_sheet_{mag}x.jpg',quality=83,optimize=True)

def run():
    OUT.mkdir(parents=True,exist_ok=True)
    rows=[];hashes=defaultdict(list);counts=Counter();seen=set();group=defaultdict(Counter)
    for num,gnp,temp,folder in C:
        for mag in MAG:
            ps=sorted((SRC/folder).glob(f'{mag}x*.bmp'))
            group[num][mag]=len(ps);counts['source_BMP']+=len(ps)
            for p in ps:
                seen.add(p.resolve())
                m=FILE_RE.fullmatch(p.name)
                field=int(m.group(2)) if m else -1
                core=1<=field<=3
                dims,mode,meta,h=inspect(p)
                hashes[h].append(str(p.relative_to(ROOT)))
                q=TIFF/f'{mag} x'/str(num)/f'{mag}x{field}.tiff'
                status='extra source field; not in prior 3-field analysis'
                tdims=''; tmeta={};th=''
                if core:
                    counts['core_BMP']+=1
                    if not q.exists():status='MISSING TIFF';counts['missing_TIFF']+=1
                    else:
                        dd,mm,tmeta,th=inspect(q);tdims=str(dd)
                        if dims!=dd:status='DIMENSION MISMATCH';counts['mismatch']+=1
                        elif h==th:status='RGB PIXEL IDENTICAL';counts['pixel_identical']+=1
                        else:status='RGB PIXEL DIFFERENT';counts['mismatch']+=1
                else: counts['additional_BMP']+=1
                if dims!=(1600,1200):counts['unexpected_size']+=1
                rows.append({'Sample':f'S{num}','GNP_wt_pct':gnp,'Temperature_C':temp,
                    'Source_folder':folder,'Magnification':mag,'Field':field,
                    'Classification':'core' if core else 'additional',
                    'BMP':str(p.relative_to(ROOT)),'BMP_dimensions':str(dims),'BMP_mode':mode,
                    'BMP_metadata':json.dumps(meta),'BMP_RGB_SHA256':h,
                    'TIFF':str(q.relative_to(ROOT)) if core else '',
                    'TIFF_dimensions':tdims,'TIFF_metadata':json.dumps(tmeta),
                    'TIFF_RGB_SHA256':th,'Status':status})
    # Cross-label matching: detect when a TIFF is precisely an ORIGINAL BMP
    # belonging to a different specimen directory, rather than changed pixels.
    bmp_by_hash={x['BMP_RGB_SHA256']:x for x in rows}
    cross_matches=[]
    for row in rows:
        if row['Classification']!='core' or row['Status']!='RGB PIXEL DIFFERENT':
            continue
        match=bmp_by_hash.get(row['TIFF_RGB_SHA256'])
        if match is not None:
            cross_matches.append({
              'TIFF_assigned_sample':row['Sample'],
              'TIFF_path':row['TIFF'],
              'Original_BMP_label':match['Sample'],
              'Original_BMP_path':match['BMP'],
              'Magnification':row['Magnification'],
              'Field':row['Field'],
              'Pixel_sha256':row['TIFF_RGB_SHA256']})
    if cross_matches:
        with (OUT/'cross_label_matches.csv').open('w',newline='',encoding='utf-8') as f:
            w=csv.DictWriter(f,fieldnames=list(cross_matches[0].keys()))
            w.writeheader();w.writerows(cross_matches)
    unmapped=[str(p.relative_to(ROOT)) for p in SRC.rglob('*.bmp') if p.resolve() not in seen]
    dup=[v for v in hashes.values() if len(v)>1]
    for mag in (100,400):make_sheet(mag)
    with (OUT/'manifest.csv').open('w',newline='',encoding='utf-8') as f:
        wr=csv.DictWriter(f,fieldnames=list(rows[0].keys()));wr.writeheader();wr.writerows(rows)
    report=['# Phase 1 — Task 1: optical source-image validation',
      '',f'Generated: {datetime.now(timezone.utc).isoformat()}',
      '', '## Inventory and RGB image-equivalence checks','']
    report += [f'- {k}: **{v}**' for k,v in sorted(counts.items())]
    report += [f'- Unique RGB hashes: **{len(hashes)}**',
      f'- Exact duplicate pixel-content groups: **{len(dup)}**',
      f'- Unmapped BMPs: **{len(unmapped)}**','',
      '## Per-condition image counts','',
      '| Sample | wt.% | Temp C | 100x BMP | 200x BMP | 400x BMP |',
      '|---|---:|---:|---:|---:|---:|']
    for num,gnp,temp,_ in C:
        report.append(f'| S{num} | {gnp} | {temp} | {group[num][100]} | {group[num][200]} | {group[num][400]} |')
    report += ['', '## Cross-label TIFF-to-BMP identity findings','']
    pairs=Counter((m['TIFF_assigned_sample'],m['Original_BMP_label']) for m in cross_matches)
    for (assigned,original),count in sorted(pairs.items()):
        report.append(f'- TIFF folder **{assigned}** matches BMP source folder **{original}** at {count} exact decoded-pixel-identical field(s).')
    if cross_matches:
        report.append('**Critical:** This is a sample-label provenance discrepancy, NOT evidence that either historical TIFF labels or recent BMP folder labels are correct. Confirm with acquisition notebooks / original specimen log before reassigning any numerical grain results.')
        report.append('The prior grain-analysis TIFF-derived results for any affected sample are NOT validated against newly supplied BMP specimen identifiers.')
    report += ['','## Calibration and scientific interpretation',
      '',
      '- Previous grain analysis HARD-CODES **0.473 µm/pixel** for 100x images. This is an unverified calibration assumption in the absence of microscope-stage/calibration records.',
      '- BMP header DPI and TIFF image DPI are not microscopy length calibration. Never infer a valid physical µm/pixel scale solely from DPI.',
      '- The existing BMP/TIFF identity result can verify that image conversion did not alter RGB pixels, but cannot validate microscope scale, visible grain boundaries, independent fields, or dynamic recrystallization.',
      '- Confirm scale from acquisition software, certified microscope calibration, or a genuinely embedded scale bar with known provenance. Do not fabricate a scale bar.',
      '- 200x/400x micron/pixel ratios must be independently checked before micrometre scale bars are added.',
      '- Additional BMP fields from S7 and S12 must be reviewed for quality/independence before expanding prior grain measurements.',
      '','## Exceptions and cautions','']
    if unmapped:report += ['- Unmapped BMP: '+p for p in unmapped]
    if dup:report += ['- Same decoded pixels: '+', '.join(v) for v in dup]
    mism=[x for x in rows if x['Classification']=='core' and x['Status']!='RGB PIXEL IDENTICAL']
    if mism:report += ['- TIFF mismatch: '+x['BMP']+' => '+x['Status'] for x in mism]
    if not (unmapped or dup or mism):report+=['- No source file mapping/pixel-equivalence errors detected.']
    report+=['','## Next step',
      'Inspect contact sheets and representative original frames; authenticate 100x calibration before any µm-based grain-size reanalysis. Then perform manually checked segmentation overlays on anomalous fields (S2, S3, S6, S9).',
      '']
    (OUT/'TASK1_REPORT.md').write_text('\n'.join(report),encoding='utf-8')
    (OUT/'summary.json').write_text(json.dumps({'counts':dict(counts),'identical_BMP_groups':dup,'unmapped_BMP':unmapped,'core_mismatches':mism,'cross_label_matches':cross_matches},indent=2),encoding='utf-8')
    print('TASK 1 RESULT',dict(counts),'DUP_GROUPS',len(dup),'UNMAPPED',len(unmapped))
if __name__=='__main__':run()
