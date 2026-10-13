#!/usr/bin/env python3
"""Phase 1 Task 4: compare REAL ImageJ manually traced polygons with GrainStat.

Requires actual human-created ROI files named S02_F1.zip etc. Absence of ROI
files returns PENDING rather than generating artificial ground truth.
"""
from __future__ import annotations

import argparse
import csv
import math
import re
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image, ImageDraw, ImageOps
from roifile import ImagejRoi, ROI_TYPE, roiread, roiwrite
from skimage.draw import polygon
from skimage.segmentation import find_boundaries
from grainstat import GrainAnalyzer

ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
OUT = HERE / "output"
ROI_DIR = HERE / "manual_rois"
PICKS = ROOT / "Phase1_Task2_Segmentation_QA" / "MANUAL_VALIDATION_TEMPLATE.csv"
TIFF = ROOT / "Optical microstructure" / "100 x"
SCALE = 0.473
MIN_AREA = 500
OLD_TO_WORK = {**{i: i for i in range(1, 10)}, 10: 12, 11: 10, 12: 11}
WORK_TO_OLD = {v: k for k, v in OLD_TO_WORK.items()}
FILE_PATTERN = re.compile(r"^S(0[1-9]|1[0-2])_F([1-6])\.zip$", re.IGNORECASE)
ALLOWED_ROIS = {ROI_TYPE.POLYGON, ROI_TYPE.FREEHAND, ROI_TYPE.TRACED}
H, W = 1200, 1600


def mask_from_points(xy, shape=(H, W)):
    """Draw a closed, manually traced ImageJ (x,y) polygon."""
    points = np.asarray(xy, dtype=float)
    if points.ndim != 2 or points.shape[1] != 2 or len(points) < 3:
        raise ValueError("ROI has fewer than 3 polygon vertices")
    if not np.all(np.isfinite(points)):
        raise ValueError("ROI contains nonfinite coordinates")
    if (points[:, 0].min() < 0 or points[:, 0].max() >= shape[1]
            or points[:, 1].min() < 0 or points[:, 1].max() >= shape[0]):
        raise ValueError("ROI exceeds original image bounds: do not clip")
    rr, cc = polygon(points[:, 1], points[:, 0], shape)
    m = np.zeros(shape, bool)
    m[rr, cc] = True
    if m.sum() < 3:
        raise ValueError("Degenerate ROI polygon")
    return m


def match_one(manual, labels, allowed):
    """One manual polygon vs best-overlap automated segmented object."""
    area = int(manual.sum())
    observed = np.bincount(labels[manual].astype("int64"))
    candidate = [int(k) for k in np.flatnonzero(observed)
                 if k != 0 and k in allowed and observed[k] > 0]
    if not candidate:
        return {"Matched_Auto_Label": "", "Intersection_px": 0,
                "Auto_Area_px": "", "IoU": 0.0, "Dice": 0.0,
                "Auto_ECD_um": float("nan")}
    best = None
    for k in candidate:
        marea = int(allowed[k])
        inter = int(observed[k])
        union = area + marea - inter
        iou = inter / union if union else 0.0
        if best is None or iou > best["IoU"]:
            best = {"Matched_Auto_Label": k, "Intersection_px": inter,
                    "Auto_Area_px": marea, "IoU": iou,
                    "Dice": (2 * inter / (area + marea)),
                    "Auto_ECD_um": SCALE * math.sqrt(4 * marea / math.pi)}
    return best


def sector(x, y):
    """Twelve non-overlapping 400 x 400 original-image review sectors."""
    col = min(int(x) // 400, 3)
    row = min(int(y) // 400, 2)
    return f"R{row+1}C{col+1}"


def substantial_overlap(px, area1, area2):
    """Conservative QA heuristic, not physical metallography acceptance."""
    return px >= 50 and px / min(area1, area2) >= 0.01


def read_manually_drawn_regions(zippath):
    rois = roiread(zippath)
    if not isinstance(rois, list):
        rois = [rois]
    if not rois:
        raise ValueError("No actual human-traced ImageJ ROIs in archive")
    result = []
    occupied = np.zeros((H, W), dtype=bool)
    for i, roi in enumerate(rois, 1):
        if roi.roitype not in ALLOWED_ROIS:
            raise ValueError(f"ROI {i} is not polygon/freehand/traced: {roi.roitype}")
        coords = np.asarray(roi.coordinates(), dtype=float)
        mask = mask_from_points(coords)
        overlap = int(np.count_nonzero(mask & occupied))
        # Preflight records overlaps. Only substantive conflicts block comparisons.
        occupied |= mask
        centroid = np.mean(np.argwhere(mask), axis=0)
        result.append((i, roi.name or f"ROI_{i:03d}", mask,
                       float(centroid[1]), float(centroid[0])))
    return result


def compare_field(pick, roi_zip):
    working = int(str(pick["Working_sample"])[1:])
    field = int(pick["Field"])
    old = WORK_TO_OLD[working]
    tif = TIFF / str(old) / f"100x{field}.tiff"
    bmp = ROOT / str(pick["BMP_path"])
    if not bmp.exists() or not tif.exists():
        raise FileNotFoundError(f"Input source unavailable for S{working} F{field}")
    from hashlib import sha256
    with Image.open(tif) as im:
        a = sha256(im.convert("RGB").tobytes()).hexdigest()
    with Image.open(bmp) as im:
        b = sha256(im.convert("RGB").tobytes()).hexdigest()
    if a != b:
        raise ValueError(f"Pixel mismatched BMP vs TIFF for S{working} F{field}")
    ga = GrainAnalyzer()
    result = ga.analyze(str(tif), scale=SCALE, min_area=MIN_AREA)
    metrics = result["metrics"]
    allowed = {int(k): int(v["area_px"]) for k, v in metrics.items()
               if int(v["area_px"]) >= MIN_AREA}
    labels = ga.labeled_image
    manual = read_manually_drawn_regions(roi_zip)
    records = []
    masks = []
    for seq, name, mask, x, y in manual:
        found = match_one(mask, labels, allowed)
        records.append(dict(
            Working_Sample=f"S{working:02d}", Field=field,
            Manual_ROI_Name=name, Manual_ROI_Sequence=seq,
            Original_BMP=str(pick["BMP_path"]),
            Historical_TIFF_Sample=f"S{old:02d}",
            Manual_Area_px=int(mask.sum()),
            Manual_ECD_um=SCALE * math.sqrt(4 * mask.sum() / math.pi),
            Sector=sector(x, y), Manual_Centroid_x=x, Manual_Centroid_y=y,
            Below_500px_Filter=int(mask.sum()) < MIN_AREA,
            **found))
        masks.append(mask)
    prepare_overlay(bmp, labels, allowed, masks, f"S{working:02d}_F{field}")
    return records


def prepare_overlay(bmp, labels, allowed, manual_masks, stem):
    """Source / computed contours / real human polygons. This last panel
    is only produced if nonempty ImageJ ROI files actually exist.
    """
    with Image.open(bmp) as im:
        rgb = np.asarray(im.convert("RGB")).copy()
    valid = np.isin(labels, list(allowed))
    compact = labels.copy()
    compact[~valid] = 0
    auto_edge = find_boundaries(compact, mode="inner")
    auto = rgb.copy()
    auto[auto_edge] = (255, 20, 20)
    human = rgb.copy()
    for mask in manual_masks:
        edge = find_boundaries(mask, mode="inner")
        human[edge] = (0, 255, 0)
    size = (500, 375)
    out = Image.new("RGB", (1500, 410), "white")
    pen = ImageDraw.Draw(out)
    for i, (arr, label) in enumerate([
        (rgb, "Original BMP"), (auto, "Automated red contours"),
        (human, "REAL ImageJ manual green outlines")]):
        im = ImageOps.contain(Image.fromarray(arr), size, Image.Resampling.LANCZOS)
        out.paste(im, (500 * i + (500 - im.width)//2, 0))
        pen.text((500*i+10, 384), label, fill="black")
    out.save(OUT / f"{stem}_manual_vs_auto.jpg", quality=84, optimize=True)



def roi_overlap_preflight(pick, roi_zip):
    """Detect independent human-ROI overlap WITHOUT editing user-drawn data.

    Visualises every submitted polygon and highlights intersections in yellow.
    Avoids reporting spurious human-automatic agreement if manual grain
    outlines cover some of the same pixels.
    """
    working=int(str(pick["Working_sample"])[1:])
    field=int(pick["Field"])
    rois=roiread(roi_zip)
    if not isinstance(rois,list):
        rois=[rois]
    if not rois:
        raise ValueError("Uploaded ImageJ ROI ZIP has no ROI entries")
    occupied=np.zeros((H,W),dtype=bool)
    masks=[]
    pairs=[]
    rows=[]
    preview_path=ROOT/str(pick["BMP_path"])
    with Image.open(preview_path) as im:
        raw=im.convert("RGB")
    overlay=raw.copy()
    mark=ImageDraw.Draw(overlay)
    total_overlap=np.zeros((H,W),dtype=bool)
    for i,roi in enumerate(rois,1):
        if roi.roitype not in ALLOWED_ROIS:
            raise ValueError(f"ROI {i} is {roi.roitype}; need closed polygon/freehand/traced")
        pts=np.asarray(roi.coordinates(),dtype=float)
        mask=mask_from_points(pts)
        overlap_unique=int(np.count_nonzero(mask & occupied))
        for j,prior in enumerate(masks,1):
            intersect=int(np.count_nonzero(mask & prior))
            if intersect:
                smaller=min(int(mask.sum()),int(prior.sum()))
                union=int(mask.sum())+int(prior.sum())-intersect
                pairs.append({
                    "Working_Sample":f"S{working:02d}",
                    "Field":field,
                    "Manual_ROI_A":j,"Manual_ROI_B":i,
                    "Intersection_px":intersect,
                    "Overlap_as_pct_smaller_ROI":100*intersect/smaller,
                    "Pair_IoU":intersect/union,
                    "Substantial_for_comparison_gate":substantial_overlap(intersect,int(mask.sum()),int(prior.sum())),
                    "Needs_expert_review":True})
        total_overlap |= mask & occupied
        occupied |= mask
        masks.append(mask)
        cx=float(pts[:,0].mean());cy=float(pts[:,1].mean())
        coordinates=[(float(x),float(y)) for x,y in pts]
        mark.line(coordinates+[coordinates[0]],fill=(0,255,170),width=3)
        mark.text((max(0,cx),max(0,cy)),str(i),fill=(255,255,255),
                  stroke_width=2,stroke_fill=(0,0,0))
        rows.append({"Working_Sample":f"S{working:02d}","Field":field,
            "ROI_Number":i,"ROI_Name":roi.name or f"ROI_{i}",
            "Manual_Area_px":int(mask.sum()),
            "Manual_ECD_um":SCALE*math.sqrt(4*mask.sum()/math.pi),
            "Overlap_with_prior_unique_px":overlap_unique,
            "Overlaps_prior":bool(overlap_unique),
            "Centroid_of_vertices_x":cx,
            "Centroid_of_vertices_y":cy})
    if int(total_overlap.sum()):
        pix=np.asarray(overlay).copy()
        pix[total_overlap]=(255,245,0)
        overlay=Image.fromarray(pix)
    sheet=Image.new("RGB",(1920,765),"white")
    original=ImageOps.contain(raw,(960,720),Image.Resampling.LANCZOS)
    markup=ImageOps.contain(overlay,(960,720),Image.Resampling.LANCZOS)
    sheet.paste(original,((960-original.width)//2,0))
    sheet.paste(markup,(960+(960-markup.width)//2,0))
    d=ImageDraw.Draw(sheet)
    d.text((12,730),f"S{working:02d} F{field}: original BMP",fill=(20,20,20))
    d.text((970,730),"Human ImageJ ROI polygons: cyan; overlaps: yellow (pixels)",fill=(20,20,20))
    d.text((970,747),f"{len(masks)} expert ROI entries; {len(pairs)} overlapping pairs",fill=(20,20,20))
    sheetname=f"S{working:02d}_F{field}_manual_ROI_overlap_diagnostic.jpg"
    sheet.save(OUT/sheetname,quality=88,optimize=True)
    with (OUT/f"S{working:02d}_F{field}_roi_inventory.csv").open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    overlap_file = OUT / f"S{working:02d}_F{field}_overlap_pairs.csv"
    if pairs:
        with overlap_file.open("w", newline="", encoding="utf-8") as f:
            writer=csv.DictWriter(f,fieldnames=list(pairs[0]))
            writer.writeheader()
            writer.writerows(pairs)
    else:
        # The old ROI submission may leave outdated overlap data.
        # Remove derived stale output ONLY; keep source and backups untouched.
        overlap_file.unlink(missing_ok=True)
    return {
        "Working_Sample":f"S{working:02d}",
        "Field":field,
        "ROI_Count":len(rois),
        "Overlapping_Pairs":len(pairs),
        "Substantial_Overlapping_Pairs":sum(bool(p["Substantial_for_comparison_gate"]) for p in pairs),
        "Total_Unique_Overlap_Pixels":int(total_overlap.sum()),
        "Pairs":pairs,
        "Diagnostic_Image":sheetname,
        "Scientific_Comparison_Allowed":not any(p["Substantial_for_comparison_gate"] for p in pairs)
    }

def self_test():
    """Synthetic in-memory software test; never a scientific manual ROI."""
    labels = np.zeros((100, 100), dtype=np.int32)
    labels[20:60, 30:70] = 7
    roi_mask = np.zeros((100, 100), dtype=bool)
    roi_mask[20:60, 30:70] = True
    result = match_one(roi_mask, labels, {7: 1600})
    assert result["Matched_Auto_Label"] == 7 and result["IoU"] == 1.0
    assert abs(result["Dice"] - 1) < 1e-10
    # Ensure ImageJ ROI ZIP parser round-trips true coordinate archives.
    roi = ImagejRoi.frompoints([[30, 20], [70, 20], [70, 60], [30, 60]])
    roi.roitype = ROI_TYPE.POLYGON
    roi.name = "SOFTWARE_TEST_ONLY"
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "synthetic_software_unit_test.zip"
        roiwrite(p, [roi])
        actual = roiread(p)
        assert len(actual) == 1
        assert len(actual[0].coordinates()) == 4
    assert substantial_overlap(649,24338,25247)
    assert substantial_overlap(459,4235,5515)
    assert substantial_overlap(88,27071,4960)
    assert not substantial_overlap(31,24338,10766)
    assert not substantial_overlap(1,27071,6822)
    print("SOFTWARE TEST PASS: ROI geometry, ZIP reader, substantive overlap QA")
    print("IMPORTANT: artificial software fixture created only in a temporary directory; no scientific human tracing performed")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    OUT.mkdir(parents=True, exist_ok=True)
    ROI_DIR.mkdir(parents=True, exist_ok=True)
    manifest = pd.read_csv(PICKS)
    known = {(int(str(x.Working_sample)[1:]), int(x.Field)): x.to_dict()
             for _, x in manifest.iterrows()}
    # Match active ImageJ archives case-insensitively. Keep explicitly
    # named _backup.zip originals for provenance, NEVER as active ground truth.
    discovered = sorted(p for p in ROI_DIR.iterdir() if p.is_file()
                        and p.suffix.lower() == ".zip")
    backups = [p for p in discovered if p.name.lower().endswith("_backup.zip")]
    all_files = [p for p in discovered if not p.name.lower().endswith("_backup.zip")]
    # Never silently pick two differently cased files for the same specimen.
    active_keys = [p.name.lower() for p in all_files]
    if len(active_keys) != len(set(active_keys)):
        raise ValueError("Two active archives differ only by filename case; resolve duplicates")
    print(f"ROI discovery: {len(all_files)} active and {len(backups)} preserved backup(s)",
          flush=True)
    reports = []
    diagnostics = []
    if not all_files:
        (OUT / "MANUAL_VALIDATION_STATUS.md").write_text(
            "# Task 4: expert manual ROI comparison\n\n"
            "**Status: PENDING HUMAN ROI SUBMISSION.**\n\n"
            "No active ImageJ ROI ZIP archives are present (preserved backups are not evidence of a revised validation). No human-vs-automated "
            "agreement, false-boundary rate or validated grain-size distribution "
            "can honestly be computed. Use the original 100x BMP images and "
            "the ImageJ collection macro to trace a documented expert ROI sample.\n",
            encoding="utf-8")
        print("PENDING: no expert ROI archives; wrote status only")
        return
    for p in all_files:
        match = FILE_PATTERN.match(p.name)
        if not match:
            raise ValueError(f"Unrecognized ROI ZIP: {p.name}. Use S02_F1.zip")
        key = int(match.group(1)), int(match.group(2))
        if key not in known:
            raise ValueError(f"ROI file {p.name} not in preselected 19-field register")
        check = roi_overlap_preflight(known[key], p)
        diagnostics.append(check)
        if check["Substantial_Overlapping_Pairs"]:
            continue  # Human ROIs must be clarified: don't report invalid agreement
        reports += compare_field(known[key], p)
    if diagnostics:
        import json
        (OUT / "expert_roi_preflight.json").write_text(
            json.dumps(diagnostics, indent=2), encoding="utf-8")
        # A successful workflow can still contain unsatisfied scientific data
        # gates. Record every submitted field, INCLUDING any held-back fields.
        status_rows = []
        for item in diagnostics:
            blocked = item["Substantial_Overlapping_Pairs"] > 0
            status_rows.append({
                "Working_Sample": item["Working_Sample"],
                "Field": item["Field"],
                "Active_Manual_ROIs": item["ROI_Count"],
                "Overlapping_Pairs_All": item["Overlapping_Pairs"],
                "Substantive_Overlapping_Pairs": item["Substantial_Overlapping_Pairs"],
                "Overlapping_Pixels_Unique": item["Total_Unique_Overlap_Pixels"],
                "Comparison_Status": "HOLD_REVIEW_BOUNDARIES" if blocked else "SCORED_EXPERT_SIGNOFF_PENDING",
                "Expert_Grain_Identity_Signed_Off": False
            })
        pd.DataFrame(status_rows).to_csv(
            OUT / "roi_field_validation_gate.csv", index=False)
    if not reports:
        details = []
        for item in diagnostics:
            details.append(
                f"- {item['Working_Sample']} field {item['Field']}: "
                f"{item['ROI_Count']} actual ROI entries, "
                f"{item['Overlapping_Pairs']} overlapping ROI pair(s), "
                f"{item['Substantial_Overlapping_Pairs']} substantive, "
                f"{item['Total_Unique_Overlap_Pixels']} overlap pixel(s).")
            for pair in item["Pairs"]:
                details.append(
                    f"  - ROI #{pair['Manual_ROI_A']} versus "
                    f"#{pair['Manual_ROI_B']}: {pair['Intersection_px']} pixels; "
                    f"{pair['Overlap_as_pct_smaller_ROI']:.2f}% of smaller ROI.")
        (OUT / "MANUAL_VALIDATION_STATUS.md").write_text(
            "# Task 4 — expert ROI preflight review\n\n"
            "**Status: MANUAL ROI OVERLAP REVIEW REQUIRED.**\n\n"
            "Original human ROI ZIP archives were found. Their source files "
            "are unchanged. The script has deliberately withheld "
            "human-vs-automatic IoU/Dice scoring until the overlapping "
            "expert polygon selections are reviewed.\n\n"
            + "\n".join(details) + "\n\n"
            "Refer to the individual Sxx_Fy_manual_ROI_overlap_diagnostic.jpg "
            "and overlapping-pairs CSVs, then edit the ROI Manager entries "
            "in Fiji/ImageJ, verify boundaries and re-export the authentic "
            "human ROI ZIP. Do not automatically delete overlapping ROIs.\n",
            encoding="utf-8")
        print("ROI REVIEW REQUIRED: overlap diagnostics saved; no scientific agreement scores generated")
        return
    df = pd.DataFrame(reports)
    df.to_csv(OUT / "manual_vs_auto_per_roi.csv", index=False)
    per_field = []
    for (s, f), sub in df.groupby(["Working_Sample", "Field"]):
        sectors = sub.Sector.nunique()
        per_field.append({
            "Working_Sample": s, "Field": f,
            "Manual_ROI_Count": len(sub),
            "Image_Sectors_Covered_of_12": sectors,
            "Median_IoU": sub.IoU.median(),
            "Mean_Dice": sub.Dice.mean(),
            "Fraction_IoU_gte_050": (sub.IoU >= .5).mean(),
            "Fraction_IoU_gte_070": (sub.IoU >= .7).mean(),
            "Manual_Mean_ECD_um": sub.Manual_ECD_um.mean(),
            "Auto_Matched_Mean_ECD_um": sub.Auto_ECD_um.mean(),
            "Field_Review_Status": "EXPERT_SIGNOFF_PENDING"
        })
    pd.DataFrame(per_field).to_csv(OUT / "manual_vs_auto_per_field.csv", index=False)
    field_lines = [
        "", "## Measured agreement on SELECTED expert polygon ROIs", "",
        "| Field | ROI count | Sectors covered (of 12) | Median IoU | Mean Dice | IoU >= 0.5 | Manual mean ECD (um) | Matched automatic mean ECD (um) |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in per_field:
        field_lines.append(
            f"| {row['Working_Sample']} F{int(row['Field'])} | "
            f"{row['Manual_ROI_Count']} | {row['Image_Sectors_Covered_of_12']} | "
            f"{row['Median_IoU']:.3f} | {row['Mean_Dice']:.3f} | "
            f"{row['Fraction_IoU_gte_050']:.1%} | "
            f"{row['Manual_Mean_ECD_um']:.2f} | "
            f"{row['Auto_Matched_Mean_ECD_um']:.2f} |")
    field_lines += [
        "",
        "**Scope limitation:** Researchers drew only a selected number of shapes,"
        " not a randomly sampled, complete or certified set of metallurgical grain"
        " boundaries. Scores apply ONLY to the selected traced ROIs and do not"
        " validate the remaining automated segmented regions.",
        "",
    ]
    # The three submitted ZIP files need not all be eligible for scoring.
    # Do not label an unscored field as validated merely because CI passed.
    gate_lines = [
        "", "## Field-level provenance and scientific validation gates",
        "", "| Submitted field | Human ROIs | Substantive overlapping pairs | Scientific scoring status |",
        "|---|---:|---:|---|"
    ]
    for item in diagnostics:
        hold = item["Substantial_Overlapping_Pairs"] > 0
        gate_lines.append(
            f"| {item['Working_Sample']} F{int(item['Field'])} | "
            f"{item['ROI_Count']} | {item['Substantial_Overlapping_Pairs']} | "
            f"{'HOLD — inspect and revise polygon overlap' if hold else 'PROVISIONAL SCORED — expert grain identity signoff pending'} |"
        )
    blocked = [d for d in diagnostics if d["Substantial_Overlapping_Pairs"] > 0]
    if blocked:
        gate_lines += [
            "",
            "**IMPORTANT:** The workflow can complete successfully while some "
            "uploaded fields remain scientifically BLOCKED. The agreement "
            "tables include only eligible fields; do not interpret all "
            "submitted human ROIs as scored.",
            "",
            "### Conflicting manual polygons requiring original-image review",
        ]
        for item in blocked:
            gate_lines.append(
                f"- **{item['Working_Sample']} F{int(item['Field'])}:** "
                f"{item['Substantial_Overlapping_Pairs']} substantive intersection(s)."
            )
            for p in item["Pairs"]:
                if p["Substantial_for_comparison_gate"]:
                    gate_lines.append(
                        f"  - ROI #{p['Manual_ROI_A']} versus #{p['Manual_ROI_B']}: "
                        f"{p['Intersection_px']} overlapping native pixels; "
                        f"{p['Overlap_as_pct_smaller_ROI']:.2f}% of smaller traced region."
                    )
        gate_lines += [
            "",
            "Inspect original ImageJ ROI Manager objects against physical "
            "etched boundaries. Do NOT automatically delete or merge "
            "polygons to improve an agreement statistic.",
        ]
    text = [
        "# Phase 1 Task 4 — Independent manual versus automated optical segmentation",
        "", f"Active manual ROI archives submitted: **{len(all_files)}**.",
        f"Preserved historical backup ROI archives ignored: **{len(backups)}**.",
        f"Total independently drawn ROI polygons: **{len(df)}**.",
        "", "These are agreement metrics for the explicitly traced objects only.",
        "No assertion of representative metallographic grain-size distribution "
        "or mechanism is made until expert field selection and boundary identity are signed off.",
        "", "The sources of human ROI data are the uploaded ROI ZIP archives, not programmatic simulations.",
        "Human contours were compared to rerun historical GrainStat objects on matching TIFFs, "
        "with exact BMP pixel identities and the fixed S10–S12 label crosswalk.",
        "", "Expert signoff remains pending. Numerical agreement alone does not determine physical grain identity.",
        "", "See manual_vs_auto_per_roi.csv, manual_vs_auto_per_field.csv and generated three-panel images."
    ]
    (OUT / "MANUAL_VALIDATION_STATUS.md").write_text(
        "\n".join(text + gate_lines + field_lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
