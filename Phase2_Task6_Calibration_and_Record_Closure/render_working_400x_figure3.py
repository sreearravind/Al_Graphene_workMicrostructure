#!/usr/bin/env python3
"""Task 6: working Figure 3 from original, traceable 400x images.

No source photograph changes. The supplied 50um/148px 400x bar is
RESEARCHER-CONFIRMED as same acquisition field of view across
all archived 400x frames; Physical calibration is researcher-confirmed; crystallographic grains remain unverified.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps
import csv, json, math, hashlib

ROOT=Path(__file__).resolve().parents[1]
HERE=Path(__file__).resolve().parent
OUT=HERE/"output"
SOURCES=ROOT/"Optical miscrostructure_Figures_BMP file"
TIFFS=ROOT/"Optical microstructure/400 x"
META=json.loads((HERE/"400x_reference_calibration_audit.json").read_text(encoding="utf-8"))
UM_PER_PIXEL=float(META["derived_micrometre_per_pixel"])
assert abs(UM_PER_PIXEL-50/148)<1e-12
assert META.get("calibration_transfer_author_approved") is True, "Author transfer approval required"
assert META["source_image_pixels"]==[1600,1200]

CONDS=[
 ("S01",0,500,"0-500 - Copy",1),("S02",0,550,"0-550 - Copy",2),
 ("S03",0,600,"0-600 - Copy",3),("S04",2,500,"2-500 - Copy",4),
 ("S05",2,550,"2-550 - Copy",5),("S06",2,600,"2-600 - Copy",6),
 ("S07",3,500,"3.500 - Copy",7),("S08",3,550,"3-550 - Copy",8),
 ("S09",3,600,"3-600 - Copy",9),("S10",4,500,"4-500 - Copy",11),
 ("S11",4,550,"4-550 - Copy",12),("S12",4,600,"4.600 - Copy",10)]
PW,PH=900,675
MARGIN=34
LEFT=160
GAP=20
TOP=150
BOTTOM=144
TOTAL_W=MARGIN+LEFT+3*PW+2*GAP+MARGIN
TOTAL_H=TOP+4*PH+3*GAP+BOTTOM
FONT_PATH="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
def font(size):return ImageFont.truetype(FONT_PATH,size)

def add_scale(image,bar_um=100.):
    """Add geometry-based bar in pixel-accurate uniform-resize source panel."""
    assert image.size==(PW,PH)
    dr=ImageDraw.Draw(image)
    width=round((bar_um/UM_PER_PIXEL)*(PW/1600))
    if not (100<=width<=250):
        raise ValueError("Unexpected calibrated bar geometry")
    x2=PW-30
    x1=x2-width
    # black backing avoids interpretation of original bright/etched regions
    dr.rectangle([x1-25,PH-101,x2+17,PH-22],fill="#050505")
    dr.rectangle([x1,PH-85,x2,PH-78],fill="white")
    label=f"{int(bar_um)} µm"
    dr.text(((x1+x2)//2,PH-65),label,font=font(28),anchor="mt",fill="white")
    return width

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    images=[]
    manifest=[]
    for sid,wt,temp,folder,old in CONDS:
        for field in (1,2,3):
            bmp=SOURCES/folder/f"400x{field}.bmp"
            tif=TIFFS/str(old)/f"400x{field}.tiff"
            with Image.open(bmp) as b:
                rgb=b.convert("RGB")
                if rgb.size!=(1600,1200):raise ValueError("Unexpected original frame size")
                raw=rgb.tobytes()
            with Image.open(tif) as t:
                t_rgb=t.convert("RGB")
                if t_rgb.size!=(1600,1200) or t_rgb.tobytes()!=raw:
                    raise ValueError(f"Original BMP-TIFF pixel discrepancy {sid} F{field}")
            manifest.append({
                "Working_Sample":sid,
                "GNP_wt_pct":wt,"Sintering_C":temp,"Original_Field":field,
                "Original_BMP":str(bmp.relative_to(ROOT)),
                "Historical_TIFF":str(tif.relative_to(ROOT)),
                "Source_RGB_SHA256":hashlib.sha256(raw).hexdigest(),
                "Exact_BGR_TIFF_Equivalent":True,
                "Figure3_Selected":bool(field==1),
                "Nominal_400x":True,
                "Bar_Calibration_Source":"Researcher-confirmed 50um/148px reference photograph",
                "Calibration_Transfer_Author_Confirmed":True,
                "Grain_Boundaries_Physically_Validated":False
            })
            if field==1:
                ims=Image.frombytes("RGB",(1600,1200),raw)
                image=ImageOps.contain(ims,(PW,PH),Image.Resampling.LANCZOS)
                if image.size!=(PW,PH):raise ValueError("Resizing inconsistent")
                images.append((sid,wt,temp,image))
    if len(images)!=12 or len(manifest)!=36:
        raise AssertionError("Unexpected 400x image matrix")
    with (OUT/"figure3_400x_source_and_calibration_manifest.csv").open("w",newline="",encoding="utf8") as f:
        writer=csv.DictWriter(f,fieldnames=list(manifest[0]))
        writer.writeheader();writer.writerows(manifest)
    sheet=Image.new("RGB",(TOTAL_W,TOTAL_H),"white")
    draw=ImageDraw.Draw(sheet)
    draw.text((MARGIN,16),"Al-GNP | original 400× optical micrographs | 12 conditions",
              font=font(34),fill="#172b43")
    draw.text((MARGIN,65),
              "400× optical micrographs | 50 µm reference = 148 native pixels.",
              font=font(22),fill="#39495e")
    draw.text((MARGIN,97),
              "Panels are original unenhanced optical images; 100 µm scale bars are researcher-calibrated.",
              font=font(18),fill="#344b60")
    for c,t in enumerate((500,550,600)):
        x=MARGIN+LEFT+c*(PW+GAP)+PW//2
        draw.text((x,TOP-18),f"{t} °C",anchor="mm",font=font(30),fill="#173451")
    for i,(sid,wt,temp,image) in enumerate(images):
        row=i//3
        col=i%3
        x=MARGIN+LEFT+col*(PW+GAP)
        y=TOP+row*(PH+GAP)
        if col==0:
            draw.text((MARGIN+8,y+PH//2),f"{wt} wt.%",font=font(24),anchor="lm",fill="#173451")
            draw.text((MARGIN+9,y+PH//2+28),"GNP",font=font(24),anchor="lm",fill="#173451")
        img=image.copy()
        barwidth=add_scale(img,bar_um=100.)
        sheet.paste(img,(x,y))
        draw.rectangle((x,y,x+PW-1,y+PH-1),outline="#344153",width=2)
        draw.rectangle((x+12,y+12,x+190,y+63),fill="#16191d")
        draw.text((x+27,y+22),sid+" | F1",font=font(26),fill="white")
    footer=TOP+4*PH+3*GAP+26
    draw.text((MARGIN,footer),f"Author-confirmed 400× scale: 50 µm / 148 pixels = {UM_PER_PIXEL:.6f} µm/pixel.",
              font=font(23),fill="#223a50")
    draw.text((MARGIN,footer+37),"Consistent 400× acquisition settings confirmed by researcher; image contrast is not crystallographic grain identification.",
              font=font(20),fill="#344b60")
    out=OUT/"FIGURE3_400x_12conditions_100um_AUTHOR_CONFIRMED.png"
    sheet.save(out,dpi=(300,300),optimize=True)
    # Compact image for downstream visual QA without accessing the
    # multi-megabyte full-resolution scientific layout.
    ImageOps.contain(sheet,(1340,1500),Image.Resampling.LANCZOS).save(
        OUT/"FIGURE3_400x_AUTHOR_CONFIRMED_PREVIEW.jpg",
        quality=76,optimize=True)

    audit={
      "reference_sha256":META["source_sha256"],
      "source_bar_pixels":148,"source_bar_um":50,
      "computed_um_per_pixel":UM_PER_PIXEL,
      "scale_bar_um_on_draft":100,
      "bar_native_pixel_length":round(100/UM_PER_PIXEL),
      "bar_resized_pixel_length":round((100/UM_PER_PIXEL)*PW/1600),
      "original_source_pairs_verified":len(manifest),
      "conditions_shown":len(images),
      "images_selected_uniformly":"F1 for each condition",
      "original_400x_dimensions":[1600,1200],
      "researcher_approved_transfer":bool(META.get("calibration_transfer_author_approved")),
      "instrument_log_independently_verified":False,
      "calibration_statement_for_manuscript":"Microscope 400× micrographs were calibrated from an unmodified 50 µm scale reference spanning 148 pixels; 0.338 µm/pixel, researcher-confirmed common acquisition conditions.",
      "warning_100x_relation":"0.473um/px prior at 100x vs 0.337838um/px at 400x; factor ~1.40, not nominal factor 4; 100x calibration must remain separate",
      "no_physical_grain_identification":True
    }
    (OUT/"figure3_calibration_transfer_readiness.json").write_text(
        json.dumps(audit,indent=2),encoding="utf8")
    (OUT/"FIGURE3_AUTHOR_APPROVAL_GATE.md").write_text(
      "# Figure 3 | 400x scale-bar author verification\n\n"
      "- New human-supplied nominal-400x 1600x1200 JPEG contains 50µm white bar "
      "measuring exactly 148 contiguous pixels (x=1204–1351, y=1056–1063). "
      "**Digitized scale: 0.337838 µm/pixel.**\n"
      "- All original 36 standard 400x BMPs are also 1600x1200 and match the "
      "historical TIFF source pixels exactly after S10/S11/S12 crosswalk.\n"
      "- Original Figure 3 is now prepared using all twelve first fields, no "
      "segmentation preprocessing and a derived 100µm/296px native-width bar "
      "on every panel. **The author confirms calibration transfer for all 400× images.**\n"
      "- Author confirms that original 400x microscope photographs were "
      "captured with consistent objective, camera optics, software acquisition "
      "magnification and unmodified field of view as the scale-reference frame. "
      "This is author attestation, not independently certified instrument metadata.\n"
      "- Flag for investigation: prior 100x ImageJ scale 0.473µm/px is only "
      "1.4 times the new 400x pixel scale, not the nominal 4 times. This could "
      "reflect different camera interfaces/cropping, but must not be ignored.\n"
      "- The reference JPEG is not committed here; only its SHA256 and "
      "calibration geometry are preserved. Archive original unchanged reference "
      "next to these results to permit third-party replication.\n"
      "- XRD raw files are requested from the collaborator but not received. "
      "No fabricated XRD, EBSD or quantitative true-grain analysis is implied.\n",
      encoding="utf8")
    print("All 36 400x BMP/TIFF pairs verified, conditional scale montage generated")
if __name__=="__main__":main()
