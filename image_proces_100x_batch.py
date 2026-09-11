import sys
import os
import pandas as pd
import matplotlib.pyplot as plt

sys.path.insert(0, r"C:\Users\HP\PycharmProjects\Microstructure\grainstat")

from grainstat import GrainAnalyzer

# -----------------------------
# PARAMETERS
# -----------------------------
BASE_DIR = r"C:\Users\HP\PycharmProjects\Microstructure\Optical microstructure\100 x"
OUTPUT_DIR = r"C:\Users\HP\PycharmProjects\Microstructure\Caluculaions\100x_report"

SCALE = 0.473
MIN_AREA = 500

os.makedirs(OUTPUT_DIR, exist_ok=True)

master_summary = []

# -----------------------------
# LOOP THROUGH SAMPLE FOLDERS 1-12
# -----------------------------
for sample_no in range(1, 13):
    sample_folder = str(sample_no)
    sample_path = os.path.join(BASE_DIR, sample_folder)

    if not os.path.isdir(sample_path):
        print(f"Sample folder missing: {sample_path}")
        continue

    print(f"\nProcessing Sample: {sample_folder}")

    analyzer = GrainAnalyzer()

    # find first supported image in that sample folder
    image_files = [
        f for f in os.listdir(sample_path)
        if f.lower().endswith((".tif", ".tiff", ".png", ".jpg", ".jpeg", ".bmp"))
    ]

    if not image_files:
        print(f"No image found in Sample {sample_folder}")
        continue

    image_path = os.path.join(sample_path, image_files[0])
    print(f"Using image: {image_path}")

    # -----------------------------
    # ANALYZE IMAGE
    # -----------------------------
    results = analyzer.analyze(
        image_path=image_path,
        scale=SCALE,
        min_area=MIN_AREA
    )

    df = pd.DataFrame.from_dict(results["metrics"], orient="index")

    # filter small noise regions
    df_clean = df[df["area_px"] >= MIN_AREA].copy()
    df_clean["Sample"] = sample_folder

    # keep only important publishable columns
    summary_df = df_clean[[
        "Sample",
        "area_px",
        "area_um2",
        "equivalent_diameter_um",
        "major_axis_um",
        "minor_axis_um",
        "aspect_ratio",
        "roundness",
        "solidity"
    ]]

    # -----------------------------
    # SAVE INDIVIDUAL CSV
    # -----------------------------
    summary_df.to_csv(
        os.path.join(OUTPUT_DIR, f"Sample_{sample_folder}_grain_data.csv"),
        index=True
    )

    # -----------------------------
    # SAVE INDIVIDUAL TXT REPORT
    # -----------------------------
    stats = summary_df["equivalent_diameter_um"].describe()

    with open(os.path.join(OUTPUT_DIR, f"Sample_{sample_folder}_report.txt"), "w") as f:
        f.write(f"Sample {sample_folder} Grain Analysis Report\n")
        f.write("====================================\n\n")
        f.write(f"Image used: {image_path}\n")
        f.write(f"Scale: {SCALE} µm/pixel\n")
        f.write(f"Minimum area filter: {MIN_AREA} pixels\n\n")
        f.write(f"Filtered grain count: {len(summary_df)}\n\n")
        f.write("Equivalent diameter statistics (µm):\n")
        f.write(str(stats))
        f.write("\n\nDetailed filtered grain table:\n")
        f.write(summary_df.to_string())

    # -----------------------------
    # HISTOGRAM
    # -----------------------------
    plt.figure(figsize=(8, 6))
    plt.hist(summary_df["equivalent_diameter_um"], bins=10, edgecolor="black")
    plt.xlabel("Equivalent Diameter (µm)")
    plt.ylabel("Frequency")
    plt.title(f"Sample {sample_folder} Grain Size Distribution")
    plt.tight_layout()
    plt.savefig(
        os.path.join(OUTPUT_DIR, f"Sample_{sample_folder}_histogram.png"),
        dpi=300
    )
    plt.close()

    # -----------------------------
    # BOXPLOT
    # -----------------------------
    plt.figure(figsize=(6, 5))
    plt.boxplot(summary_df["equivalent_diameter_um"])
    plt.ylabel("Equivalent Diameter (µm)")
    plt.title(f"Sample {sample_folder} Grain Size Box Plot")
    plt.tight_layout()
    plt.savefig(
        os.path.join(OUTPUT_DIR, f"Sample_{sample_folder}_boxplot.png"),
        dpi=300
    )
    plt.close()

    # -----------------------------
    # OVERLAY FOR VALIDATION
    # -----------------------------
    analyzer.plot_overlay(
        save_path=os.path.join(OUTPUT_DIR, f"Sample_{sample_folder}_overlay.png")
    )

    # -----------------------------
    # MASTER SUMMARY ENTRY
    # -----------------------------
    master_summary.append({
        "Sample": sample_folder,
        "Image_File": image_files[0],
        "Filtered_Grain_Count": len(summary_df),
        "Mean_Equivalent_Diameter_um": stats["mean"],
        "Std_um": stats["std"],
        "Min_um": stats["min"],
        "25%_um": stats["25%"],
        "Median_um": stats["50%"],
        "75%_um": stats["75%"],
        "Max_um": stats["max"]
    })

# -----------------------------
# SAVE MASTER EXCEL
# -----------------------------
master_df = pd.DataFrame(master_summary)

excel_path = os.path.join(OUTPUT_DIR, "Grain_Size_Master_Report.xlsx")

with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
    master_df.to_excel(writer, sheet_name="Summary", index=False)

print("\nBatch processing completed successfully.")
print(f"Master Excel saved at: {excel_path}")