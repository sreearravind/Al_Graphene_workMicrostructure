import sys
import pandas as pd
import matplotlib.pyplot as plt

sys.path.insert(0, r"C:\Users\HP\PycharmProjects\Microstructure\grainstat")

from grainstat import GrainAnalyzer

analyzer = GrainAnalyzer()

results = analyzer.analyze(
    image_path=r"C:\Users\HP\PycharmProjects\Microstructure\microstructure.tif",
    scale=0.473,
    min_area=500
)

metrics = results["metrics"]
df = pd.DataFrame.from_dict(metrics, orient="index")

# remove tiny noise regions manually
df_clean = df[df["area_px"] >= 500]

summary_df = df_clean[[
    "area_px",
    "area_um2",
    "equivalent_diameter_um",
    "major_axis_um",
    "minor_axis_um",
    "aspect_ratio",
    "roundness",
    "solidity"
]]

print(summary_df)
print("\nFiltered regions:", len(summary_df))
print("\nEquivalent diameter stats:")
print(summary_df["equivalent_diameter_um"].describe())

# -----------------------------
# Export filtered grain data
# -----------------------------
summary_df.to_csv("grain_data_filtered.csv", index=True)

# -----------------------------
# Save statistics report as text
# -----------------------------
with open("analysis_report_filtered.txt", "w") as f:
    f.write("Filtered Grain Analysis Report\n")
    f.write("==============================\n\n")
    f.write(f"Filtered regions: {len(summary_df)}\n\n")
    f.write("Equivalent diameter statistics (um):\n")
    f.write(str(summary_df["equivalent_diameter_um"].describe()))
    f.write("\n\nFull filtered table:\n")
    f.write(summary_df.to_string())

# -----------------------------
# Generate histogram from filtered data
# -----------------------------
plt.figure(figsize=(8, 6))
plt.hist(summary_df["equivalent_diameter_um"], bins=10, edgecolor="black")
plt.xlabel("Equivalent Diameter (µm)")
plt.ylabel("Frequency")
plt.title("Grain Size Distribution")
plt.tight_layout()
plt.savefig("size_distribution_filtered.png", dpi=300)
plt.close()

# -----------------------------
# Optional: box plot
# -----------------------------
plt.figure(figsize=(6, 5))
plt.boxplot(summary_df["equivalent_diameter_um"])
plt.ylabel("Equivalent Diameter (µm)")
plt.title("Grain Size Box Plot")
plt.tight_layout()
plt.savefig("grain_size_boxplot.png", dpi=300)
plt.close()

# Built-in overlay for segmentation check
analyzer.plot_overlay(save_path="grain_overlay.png")

print("\nFiltered outputs saved successfully.")
