from pathlib import Path
import warnings

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image

from grainstat import GrainAnalyzer

ROOT = Path(__file__).resolve().parents[1]
BASE_100 = ROOT / "Optical microstructure" / "100 x"
BASE_400 = ROOT / "Optical microstructure" / "400 x"
OUT = ROOT / "Revision_Comments_3_4_5" / "output"
OUT.mkdir(parents=True, exist_ok=True)

# Same calibration/filter used in the original analysis code.
SCALE_UM_PER_PIXEL = 0.473
MIN_AREA_PX = 500

# Factor mapping used throughout the manuscript.
CONDITIONS = {
    1: (0, 500), 2: (0, 550), 3: (0, 600),
    4: (2, 500), 5: (2, 550), 6: (2, 600),
    7: (3, 500), 8: (3, 550), 9: (3, 600),
    10: (4, 500), 11: (4, 550), 12: (4, 600),
}

# Condition-level responses already reported in the manuscript.
HARDNESS = {1:18.50,2:18.00,3:18.50,4:20.33,5:21.20,6:22.40,7:20.60,8:21.76,9:22.37,10:20.75,11:23.40,12:24.50}
UTS = {1:79,2:76,3:128,4:80,5:95,6:105,7:88,8:78,9:90,10:120,11:129,12:98}
ELONGATION = {1:4.7,2:4.5,3:21.5,4:2.5,5:5.5,6:7.6,7:3.5,8:3.0,9:8.5,10:12.5,11:30.0,12:6.0}

warnings.filterwarnings("ignore", category=FutureWarning)


def _metrics_to_df(results):
    metrics = results.get("metrics")
    if metrics is None:
        metrics = results.get("properties")
    if metrics is None:
        raise KeyError("GrainStat result contained neither 'metrics' nor 'properties'.")
    df = pd.DataFrame.from_dict(metrics, orient="index")
    if "area_px" in df.columns:
        df = df[df["area_px"] >= MIN_AREA_PX].copy()
    return df


def analyse_100x_fields():
    grain_tables = []
    field_rows = []

    for sample in range(1, 13):
        gnp, temp = CONDITIONS[sample]
        sample_dir = BASE_100 / str(sample)
        image_files = sorted(sample_dir.glob("*.tif*"))
        if not image_files:
            raise FileNotFoundError(f"No 100x TIFF images found for sample {sample}: {sample_dir}")

        for field_index, image_path in enumerate(image_files, start=1):
            analyzer = GrainAnalyzer()
            results = analyzer.analyze(
                image_path=str(image_path),
                scale=SCALE_UM_PER_PIXEL,
                min_area=MIN_AREA_PX,
            )
            df = _metrics_to_df(results)
            if "equivalent_diameter_um" not in df.columns:
                raise KeyError(f"equivalent_diameter_um missing for {image_path}")

            with Image.open(image_path) as im:
                width_px, height_px = im.size
            field_area_um2 = width_px * height_px * SCALE_UM_PER_PIXEL**2

            df = df.copy()
            df.insert(0, "Sample", f"S{sample}")
            df.insert(1, "Sample_Number", sample)
            df.insert(2, "GNP_wt_pct", gnp)
            df.insert(3, "Sintering_Temperature_C", temp)
            df.insert(4, "Field", field_index)
            df.insert(5, "Image_File", image_path.name)
            df.insert(6, "Image_Width_px", width_px)
            df.insert(7, "Image_Height_px", height_px)
            df.insert(8, "Field_Area_um2", field_area_um2)
            grain_tables.append(df)

            d = df["equivalent_diameter_um"].astype(float)
            field_rows.append({
                "Sample": f"S{sample}",
                "Sample_Number": sample,
                "GNP_wt_pct": gnp,
                "Sintering_Temperature_C": temp,
                "Field": field_index,
                "Image_File": image_path.name,
                "Image_Width_px": width_px,
                "Image_Height_px": height_px,
                "Field_Area_um2": field_area_um2,
                "Grain_Count": int(d.size),
                "Mean_ECD_um": d.mean(),
                "SD_ECD_um": d.std(ddof=1) if d.size > 1 else np.nan,
                "Median_ECD_um": d.median(),
                "Q1_ECD_um": d.quantile(0.25),
                "Q3_ECD_um": d.quantile(0.75),
                "Min_ECD_um": d.min(),
                "Max_ECD_um": d.max(),
            })

    grains = pd.concat(grain_tables, ignore_index=True)
    fields = pd.DataFrame(field_rows)

    condition_rows = []
    for sample in range(1, 13):
        s = f"S{sample}"
        g = grains.loc[grains["Sample"] == s, "equivalent_diameter_um"].astype(float)
        fs = fields.loc[fields["Sample"] == s]
        gnp, temp = CONDITIONS[sample]
        field_means = fs["Mean_ECD_um"].astype(float)
        condition_rows.append({
            "Sample": s,
            "Sample_Number": sample,
            "GNP_wt_pct": gnp,
            "Sintering_Temperature_C": temp,
            "Number_of_Fields": int(fs.shape[0]),
            "Total_Sampled_Area_um2": fs["Field_Area_um2"].sum(),
            "Total_Grain_Count": int(g.size),
            "Pooled_Mean_ECD_um": g.mean(),
            "Pooled_SD_ECD_um": g.std(ddof=1) if g.size > 1 else np.nan,
            "Pooled_Median_ECD_um": g.median(),
            "Pooled_Q1_ECD_um": g.quantile(0.25),
            "Pooled_Q3_ECD_um": g.quantile(0.75),
            "Pooled_IQR_ECD_um": g.quantile(0.75) - g.quantile(0.25),
            "Field_Mean_ECD_um": field_means.mean(),
            "Field_to_Field_SD_um": field_means.std(ddof=1) if len(field_means) > 1 else np.nan,
            "Field_to_Field_CV_pct": 100 * field_means.std(ddof=1) / field_means.mean() if len(field_means) > 1 else np.nan,
            "Hardness_HRB": HARDNESS[sample],
            "UTS_MPa": UTS[sample],
            "Elongation_pct": ELONGATION[sample],
        })

    conditions = pd.DataFrame(condition_rows)
    return grains, fields, conditions


def save_tables(grains, fields, conditions):
    grains.to_csv(OUT / "grain_level_multifield_100x.csv", index=False)
    fields.to_csv(OUT / "field_level_summary_100x.csv", index=False)
    conditions.to_csv(OUT / "condition_level_grain_summary_100x.csv", index=False)
    with pd.ExcelWriter(OUT / "Grain_Size_Multifield_Report.xlsx", engine="openpyxl") as writer:
        conditions.to_excel(writer, sheet_name="Condition_Summary", index=False)
        fields.to_excel(writer, sheet_name="Field_Summary", index=False)
        grains.to_excel(writer, sheet_name="Grain_Level", index=False)


def plot_high_res_microstructure_matrix():
    fig, axes = plt.subplots(4, 3, figsize=(12, 13))
    row_gnp = [0, 2, 3, 4]
    col_temp = [500, 550, 600]

    for r, gnp in enumerate(row_gnp):
        for c, temp in enumerate(col_temp):
            sample = next(k for k, v in CONDITIONS.items() if v == (gnp, temp))
            sample_dir = BASE_400 / str(sample)
            candidates = sorted(sample_dir.glob("*.tif*"))
            if not candidates:
                raise FileNotFoundError(f"No 400x image for sample {sample}")
            image_path = candidates[0]
            with Image.open(image_path) as im:
                image = np.asarray(im.convert("RGB"))
            ax = axes[r, c]
            ax.imshow(image)
            ax.set_xticks([])
            ax.set_yticks([])
            ax.text(
                0.02, 0.96, f"S{sample}", transform=ax.transAxes,
                va="top", ha="left", fontsize=11, fontweight="bold",
                bbox=dict(facecolor="white", alpha=0.78, edgecolor="none", pad=2.5),
            )
            if r == 0:
                ax.set_title(f"{temp} °C", fontsize=13, fontweight="bold")
            if c == 0:
                ax.set_ylabel(f"{gnp} wt.% GNP", fontsize=12, fontweight="bold")

    fig.subplots_adjust(wspace=0.02, hspace=0.08, left=0.08, right=0.995, top=0.96, bottom=0.02)
    fig.savefig(OUT / "Figure_3_HighResolution_Optical_Microstructure_400x.png", dpi=300, bbox_inches="tight")
    fig.savefig(OUT / "Figure_3_HighResolution_Optical_Microstructure_400x.tiff", dpi=300, bbox_inches="tight", pil_kwargs={"compression":"tiff_lzw"})
    plt.close(fig)


def plot_distributions(grains, conditions):
    samples = [f"S{i}" for i in range(1, 13)]
    data = [grains.loc[grains["Sample"] == s, "equivalent_diameter_um"].astype(float).to_numpy() for s in samples]

    fig, ax = plt.subplots(figsize=(12, 6.6))
    ax.boxplot(data, labels=samples, showfliers=True, medianprops={"linewidth": 1.8})
    ax.set_xlabel("Processing condition", fontsize=13, fontweight="bold")
    ax.set_ylabel("Equivalent grain diameter (µm)", fontsize=13, fontweight="bold")
    ax.grid(axis="y", alpha=0.22)
    fig.tight_layout()
    fig.savefig(OUT / "Figure_Grain_Size_Distribution_Boxplots.png", dpi=600, bbox_inches="tight")
    fig.savefig(OUT / "Figure_Grain_Size_Distribution_Boxplots.tiff", dpi=600, bbox_inches="tight", pil_kwargs={"compression":"tiff_lzw"})
    plt.close(fig)

    # Supplementary 12-panel histograms, common global bins for direct comparison.
    all_values = grains["equivalent_diameter_um"].astype(float).to_numpy()
    bins = np.linspace(np.nanmin(all_values), np.nanpercentile(all_values, 99.5), 13)
    fig, axes = plt.subplots(4, 3, figsize=(12, 12))
    for ax, s in zip(axes.ravel(), samples):
        vals = grains.loc[grains["Sample"] == s, "equivalent_diameter_um"].astype(float)
        ax.hist(vals, bins=bins, edgecolor="black")
        row = conditions.loc[conditions["Sample"] == s].iloc[0]
        ax.set_title(f"{s}: {int(row['GNP_wt_pct'])} wt.% GNP, {int(row['Sintering_Temperature_C'])} °C")
        ax.set_xlabel("ECD (µm)")
        ax.set_ylabel("Frequency")
    fig.tight_layout()
    fig.savefig(OUT / "Supplementary_Grain_Size_Histograms_12_Conditions.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def _scatter_with_fit(ax, x, y, ylabel, panel):
    ax.scatter(x, y, s=70, edgecolors="black", linewidths=0.7)
    fit = np.polyfit(x, y, 1)
    xx = np.linspace(np.min(x), np.max(x), 200)
    ax.plot(xx, np.polyval(fit, xx), linestyle="--", linewidth=1.8)
    r = np.corrcoef(x, y)[0, 1]
    ax.set_xlabel("Mean equivalent grain diameter (µm)", fontweight="bold")
    ax.set_ylabel(ylabel, fontweight="bold")
    ax.set_title(f"{panel} r = {r:.3f}", loc="left", fontweight="bold")
    ax.grid(alpha=0.22)
    return r


def plot_correlations(conditions):
    x = conditions["Pooled_Mean_ECD_um"].to_numpy(float)
    y_h = conditions["Hardness_HRB"].to_numpy(float)
    y_u = conditions["UTS_MPa"].to_numpy(float)
    y_e = conditions["Elongation_pct"].to_numpy(float)

    fig, axes = plt.subplots(1, 3, figsize=(15, 4.8))
    r_h = _scatter_with_fit(axes[0], x, y_h, "Rockwell hardness (HRB)", "(a)")
    r_u = _scatter_with_fit(axes[1], x, y_u, "Ultimate tensile strength (MPa)", "(b)")
    r_e = _scatter_with_fit(axes[2], x, y_e, "Elongation (%)", "(c)")
    fig.tight_layout()
    fig.savefig(OUT / "Figure_Grain_Size_vs_Mechanical_Responses.png", dpi=600, bbox_inches="tight")
    fig.savefig(OUT / "Figure_Grain_Size_vs_Mechanical_Responses.tiff", dpi=600, bbox_inches="tight", pil_kwargs={"compression":"tiff_lzw"})
    plt.close(fig)
    return r_h, r_u, r_e


def write_report(fields, conditions, correlations):
    r_h, r_u, r_e = correlations
    lines = []
    lines.append("# Multi-field grain analysis for Reviewer 2 Comments 3, 4 and 5\n")
    lines.append(f"- Magnification used for quantitative analysis: **100×**\n")
    lines.append(f"- Calibration: **{SCALE_UM_PER_PIXEL} µm/pixel**\n")
    lines.append(f"- Minimum segmented region area: **{MIN_AREA_PX} pixels**\n")
    lines.append("- Fields analysed per processing condition: **3** (all available 100× TIFF fields)\n")
    lines.append("- Grain-size descriptor: **equivalent circular diameter (ECD)** from calibrated digital segmentation\n")
    lines.append("- Uncertainty reported at two levels: pooled grain distribution and SD of the three field means.\n")
    lines.append("- The analysis is a calibrated image-analysis workflow; it should **not** be described as EBSD or as independent confirmation of dynamic recrystallization.\n\n")

    lines.append("## Condition-level summary\n\n")
    display_cols = [
        "Sample", "GNP_wt_pct", "Sintering_Temperature_C", "Number_of_Fields",
        "Total_Sampled_Area_um2", "Total_Grain_Count", "Pooled_Mean_ECD_um",
        "Pooled_SD_ECD_um", "Pooled_Median_ECD_um", "Pooled_IQR_ECD_um",
        "Field_to_Field_SD_um", "Field_to_Field_CV_pct",
    ]
    lines.append(conditions[display_cols].round(3).to_markdown(index=False))
    lines.append("\n\n## Grain-size / mechanical-response correlations (condition level, n = 12)\n\n")
    lines.append(f"- Grain size vs hardness: **r = {r_h:.3f}**\n")
    lines.append(f"- Grain size vs UTS: **r = {r_u:.3f}**\n")
    lines.append(f"- Grain size vs elongation: **r = {r_e:.3f}**\n")
    lines.append("\nThese correlations are exploratory because the mechanical responses are available at condition level and the experimental design contains only twelve conditions.\n")
    lines.append("\n## Important interpretation boundary\n\n")
    lines.append("Optical morphology and ECD distributions quantify condition-dependent grain-structure differences, but they do not provide crystallographic orientation, boundary misorientation, recrystallized fraction or grain-boundary character. Therefore, EBSD-dependent DRX claims must remain withdrawn/qualified.\n")

    (OUT / "analysis_report_comments_3_4_5.md").write_text("".join(lines), encoding="utf-8")


def main():
    plt.rcParams.update({
        "font.family": "serif",
        "font.size": 11,
        "axes.labelsize": 12,
        "axes.titlesize": 11,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
    })

    grains, fields, conditions = analyse_100x_fields()
    save_tables(grains, fields, conditions)
    plot_high_res_microstructure_matrix()
    plot_distributions(grains, conditions)
    correlations = plot_correlations(conditions)
    write_report(fields, conditions, correlations)

    print("Multi-field grain analysis completed.")
    print(conditions[["Sample", "Total_Grain_Count", "Pooled_Mean_ECD_um", "Pooled_SD_ECD_um", "Field_to_Field_SD_um"]].round(3).to_string(index=False))


if __name__ == "__main__":
    main()
