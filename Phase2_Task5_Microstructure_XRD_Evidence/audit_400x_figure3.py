#!/usr/bin/env python3
"""Task 5: Original 400x optical-source audit; no invented scale bars."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps
from hashlib import sha256
import json,csv
ROOT=Path(__file__).resolve().parents[1]
OUT=Path(__file__).resolve().parent/"output"
SRC=ROOT/"Optical miscrostructure_Figures_BMP file"
TIFF=ROOT/"Optical microstructure/400 x"
CONDS=[
 ("S01",0,500,"0-500 - Copy",1),("S02",0,550,"0-550 - Copy",2),("S03",0,600,"0-600 - Copy",3),
 ("S04",2,500,"2-500 - Copy",4),("S05",2,550,"2-550 - Copy",5),("S06",2,600,"2-600 - Copy",6),
 ("S07",3,500,"3.500 - Copy",7),("S08",3,550,"3-550 - Copy",8),("S09",3,600,"3-600 - Copy",9),
 ("S10",4,500,"4-500 - Copy",11),("S11",4,550,"4-550 - Copy",12),("S12",4,600,"4.600 - Copy",10),
]
W,H=1600,1200
PW,PH=980,735
MARGIN=30;GAP=16;TITLE=114;ROW_LABEL=140;BOTTOM=100
CANVAS_W=MARGIN*2+ROW_LABEL+3*PW+2*GAP
CANVAS_H=TITLE+4*PH+3*GAP+BOTTOM
FONT="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
def ft(sz):return ImageFont.truetype(FONT,sz)
def main():
    OUT.mkdir(parents=True,exist_ok=True)
    canvas=Image.new("RGB",(CANVAS_W,CANVAS_H),"white")
    d=ImageDraw.Draw(canvas)
    d.text((MARGIN,9),"Hot-extruded Al-GNP | original optical fields, nominal 400x",font=ft(32),fill="#202b39")
    d.text((MARGIN,57),"SOURCE-AUDIT DRAFT: NO VERIFIED 400x um/pixel CALIBRATION. NOT FOR SUBMISSION.",font=ft(20),fill="#aa2424")
    for col,temp in enumerate([500,550,600]):
        x=MARGIN+ROW_LABEL+col*(PW+GAP)+PW//2
        d.text((x,TITLE-13),str(temp)+" deg C",anchor="mm",font=ft(26),fill="#162e44")
    rows=[]
    for i,(sid,wt,temp,folder,old) in enumerate(CONDS):
        col=i%3; row=i//3
        y=TITLE+row*(PH+GAP)
        x=MARGIN+ROW_LABEL+col*(PW+GAP)
        if col==0:
            d.text((MARGIN+8,y+PH//2),str(wt)+" wt.% GNP",font=ft(23),
                  anchor="lm",fill="#23405a")
        for field in [1,2,3]:
            bmp=SRC/folder/("400x"+str(field)+".bmp")
            tif=TIFF/str(old)/("400x"+str(field)+".tiff")
            with Image.open(bmp) as img:
                orig=img.convert("RGB")
                if orig.size!=(W,H):raise ValueError("Image dimensions: "+str(bmp))
                pixels=orig.tobytes()
            with Image.open(tif) as img:
                archived=img.convert("RGB")
                if archived.size!=(W,H) or archived.tobytes()!=pixels:
                    raise ValueError("BMP/TIFF pixel mismatch "+sid+" F"+str(field))
            rows.append({
                "Working_Sample":sid,"GNP_wt_pct":wt,"Sinter_C":temp,
                "Field":field,"Figure3_selected":field==1,
                "Original_BMP":str(bmp.relative_to(ROOT)),
                "Historical_TIFF":str(tif.relative_to(ROOT)),
                "RGB_SHA256":sha256(pixels).hexdigest(),
                "Decoded_RGB_Identical":True,
                "Nominal_Magnification":"400x",
                "Physical_400x_um_per_pixel":"UNVERIFIED",
                "Crystallographic_Grains_Validated":False})
            if field==1:
                source=Image.frombytes("RGB",(W,H),pixels)
                resized=ImageOps.contain(source,(PW,PH),Image.Resampling.LANCZOS)
                canvas.paste(resized,(x,y))
                d.rectangle((x,y,x+PW-1,y+PH-1),outline="#354454",width=2)
                d.rectangle((x+10,y+10,x+184,y+63),fill="#111827")
                d.text((x+18,y+20),sid+" | F1",font=ft(27),fill="white")
    footer=TITLE+4*PH+3*GAP+19
    d.text((MARGIN,footer),"All 12 conditions; first archived 400x field selected uniformly; original image data unchanged",
           font=ft(20),fill="#29455c")
    d.text((MARGIN,footer+32),"NO scale bars: 100x calibration cannot be transferred to 400x without supporting instrument evidence.",
           font=ft(19),fill="#aa2424")
    canvas.save(OUT/"FIG3_400x_12condition_PROVISIONAL_NO_SCALE.jpg",quality=95,subsampling=0,optimize=True)
    with (OUT/"figure3_400x_36field_source_manifest.csv").open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    candidate=ROOT/"microstructure_scale.tif"
    meta={"file":str(candidate.relative_to(ROOT)), "exists":candidate.exists(),
          "verified_400x_ruler_image":False}
    if candidate.exists():
        with Image.open(candidate) as im:
            meta.update({"size_pixels":list(im.size),
                    "tags":{str(k):str(v)[:350] for k,v in im.tag_v2.items()}})
            ImageOps.contain(im.convert("RGB"),(1250,950)).save(
                OUT/"microstructure_scale_provenance_preview.jpg",quality=92)
    (OUT/"scale_candidate_metadata.json").write_text(json.dumps(meta,indent=2),encoding="utf8")
    (OUT/"TASK5_FIGURE3_QA.md").write_text(
        "# Original 400x optical image integrity and Figure 3\n\n"
        "All 36 original 400x BMPs reproduced the corresponding TIFF decoded-RGB pixels. "
        "Historical 4wt% TIFF folders S11/S12/S10 are crosswalked to working S10/S11/S12 respectively.\n\n"
        "Exactly field F1 for each condition was included in the candidate 4 x 3 montage; "
        "no selection by appearance, segmentation, or software agreement.\n\n"
        "Nominal magnification 400x is documented by file naming, but NO independently "
        "verified physical scale at 400x is presently archived. The preview intentionally "
        "has no micrometre scale bar and is stamped NOT FOR SUBMISSION.\n\n"
        "The standalone microstructure_scale.tif file was inventoried as an unverified reference "
        "candidate. TIFF resolution/DPI fields alone are not physical microscope calibration. "
        "User or acquisition record must establish ruler interval and relevant magnification.\n\n"
        "No change was made to any optical source, user ROI, historical metric or manuscript.\n",
        encoding="utf8")
    print("PASS: 36 of 36 original 400x optical images pixel-exactly validated; figure is uncalibrated DRAFT")
if __name__=="__main__":main()
